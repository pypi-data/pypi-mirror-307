import asyncio
from pprint import pformat
import time
from typing import AsyncGenerator, Optional

from eth_account.signers.local import LocalAccount
from eth_typing import ChecksumAddress
from mach_client import (
    ChainId,
    Token,
    balances,
    client,
    transactions,
    utility as client_utility,
)

from .. import config, utility
from .amount_policy import AmountPolicy, max_amount_policy
from .destination_policy import DestinationPolicy
from ..log import LogContextAdapter, Logger
from .event import (
    CannotFill,
    DestinationNotReceived,
    EmptySourceBalance,
    GasEstimateFailed,
    InsufficientDestinationGas,
    MachEvent,
    NoViableDestination,
    PlaceOrderFailed,
    QuoteFailed,
    QuoteInvalidAmount,
    QuoteLiquidityUnavailable,
    RiskManagerRejection,
    SubmitOrderFailed,
    SourceNotWithdrawn,
    Trade,
)
from .risk_manager import RiskManager, SimilarTokenRiskManager


async def run(
    *,
    src_token: Token,
    destination_policy: DestinationPolicy,
    amount_policy: AmountPolicy = max_amount_policy,
    check_destination_gas: bool = True,
    account: LocalAccount,
    destination_wallet: Optional[ChecksumAddress] = None,
    logger: Logger,
) -> AsyncGenerator[MachEvent, None]:
    # TODO: custom destination address
    if not destination_wallet:
        destination_wallet = account.address

    src_context = await client_utility.make_context(src_token.chain)

    risk_manager: RiskManager = SimilarTokenRiskManager(
        account.address, config.slippage_tolerance, logger
    )

    # Permanently exclude chains on which we have no gas
    permanently_excluded_chains: set[ChainId] = set()

    # Temporarily exclude the source chain since we don't support single chain swaps
    destination_policy.exclude_chain(src_token.chain)

    while True:
        base_logger = LogContextAdapter(logger, f"{src_token} => (UNSELECTED)")

        initial_src_balance = await src_context.get_balance(
            src_token, account.address
        )
        base_logger.debug(f"{initial_src_balance=}")

        # TODO: some pairs have trouble filling 1 tick, so treat it as 0
        if initial_src_balance <= 1:
            base_logger.critical("Source balance empty. Cannot continue trading.")
            yield EmptySourceBalance(src_token, account.address)
            break

        if not (dest_token := destination_policy()):
            base_logger.critical("No viable destination token")
            yield NoViableDestination(destination_policy)
            break

        base_logger = LogContextAdapter(logger, f"{src_token} => {dest_token}")

        destination_policy.exclude_token(dest_token)
        dest_context = await client_utility.make_context(dest_token.chain)

        if check_destination_gas:
            try:
                gas_estimate = await client.estimate_gas(dest_token.chain.id)
            except Exception as e:
                base_logger.error("Gas estimate failed:", exc_info=e)
                yield GasEstimateFailed(dest_token.chain, e)
                continue

            base_logger.debug(f"Gas estimate: {gas_estimate}")
            estimated_gas = gas_estimate["gas_estimate"] * gas_estimate["gas_price"]
            base_logger.debug(f"Estimated gas cost: {estimated_gas}")

            gas_available = await balances.get_gas_balance(dest_context, account.address)
            base_logger.debug(f"Available gas: {gas_available}")

            if gas_available < estimated_gas:
                base_logger.info(
                    f"Insufficient gas on chain {
                        dest_token.chain.name}, will be excluded from future selection"
                )
                destination_policy.permanently_exclude_chain(dest_token.chain.id)
                permanently_excluded_chains.add(dest_token.chain.id)
                yield InsufficientDestinationGas(
                    dest_token, gas_estimate, gas_available
                )
                continue

        desired_src_amount = amount_policy(src_token, dest_token, initial_src_balance)

        try:
            quote = await client.request_quote(
                src_token,
                dest_token,
                desired_src_amount,
                account.address,
            )
        except Exception as e:
            base_logger.error("Quote request failed:", exc_info=e)
            yield QuoteFailed(
                (src_token, dest_token), desired_src_amount, account.address, e
            )
            continue

        base_logger.debug("Quote:")
        base_logger.debug(pformat(quote))

        if quote["invalid_amount"]:
            base_logger.warning("Quote had invalid amount")
            yield QuoteInvalidAmount(
                (src_token, dest_token), desired_src_amount, account.address, quote
            )
            continue

        if quote["liquidity_source"] == "unavailable":
            base_logger.warning("No liquidity source")
            yield QuoteLiquidityUnavailable(
                (src_token, dest_token), desired_src_amount, account.address, quote
            )
            continue

        if (risk_analyis := risk_manager(src_token, dest_token, quote)).reject:
            base_logger.warning("Order rejected by risk manager")
            yield RiskManagerRejection(
                (src_token, dest_token), desired_src_amount, quote, risk_analyis
            )
            continue

        src_amount, dest_amount = quote["src_amount"], quote["dst_amount"]

        base_logger.debug(
            f"Can fill {src_amount=}/{desired_src_amount=} "
            f"({100 * src_amount / desired_src_amount}%) "
            f"through liquidity source {quote['liquidity_source']}"
        )

        assert src_amount <= desired_src_amount

        if src_amount < desired_src_amount:
            base_logger.warning("Not enough liquidity to trade entire source balance")

            if src_amount <= 0:
                base_logger.warning(
                    "Cannot fill any amount, trying a different destination"
                )
                yield CannotFill((src_token, dest_token), desired_src_amount, quote)
                continue

        order_direction = (
            quote["src_asset_address"],  # srcAsset: address
            quote["dst_asset_address"],  # dstAsset: address
            dest_token.chain.lz_cid,  # dstLzc: uint32
        )

        order_funding = (
            src_amount,  # srcQuantity: uint96
            dest_amount,  # dstQuantity: uint96
            quote["bond_fee"],  # bondFee: uint16
            quote["bond_asset_address"],  # bondAsset: address
            quote["bond_amount"],  # bondAmount: uint96
        )

        # Note on why we aren't using quote["challenge_offset"] and quote["challenge_window"]:
        # https://tristeroworkspace.slack.com/archives/C07RJC68VD0/p1728678088837679
        order_expiration = (
            int(time.time()) + 3600,  # timestamp: uint32
            1,  # challengeOffset: uint16
            1,  # challengeWindow: uint16
        )

        is_maker = False

        src_order_book_contract = client_utility.make_order_book_contract(src_w3, src_token)
        place_order = src_order_book_contract.functions.placeOrder(
            order_direction,
            order_funding,
            order_expiration,
            is_maker,
        )

        src_token_contract = client_utility.make_token_contract(src_w3, src_token)

        try:
            tx_hash = await transactions.approve_send_contract_function_transaction(
                place_order, account, src_token_contract, src_amount, base_logger
            )

            base_logger.info(f"Placed order with hash: {tx_hash.to_0x_hex()}")

        except Exception as e:
            base_logger.error("Failed to place order:", exc_info=e)
            yield PlaceOrderFailed(
                (src_token, dest_token),
                account.address,
                place_order,
                e,
            )
            continue

        # These need to be computed before the order has been submitted
        start_dest_balance = await balances.get_balance(
            dest_context, dest_token, account.address
        )
        expected_src_balance = desired_src_amount - src_amount
        expected_dest_balance = start_dest_balance + dest_amount

        try:
            order_response = await client.submit_order(src_token.chain.id, tx_hash)

        except Exception as e:
            base_logger.error("There was an error submitting this order:", exc_info=e)
            yield SubmitOrderFailed((src_token, dest_token), tx_hash, e)
            continue

        base_logger.info("Submitted order")
        base_logger.debug("Response:")
        base_logger.debug(pformat(order_response))

        src_balance = await balances.get_balance(src_w3, src_token, account.address)
        base_logger.info(
            "Waiting for source balance to be withdrawn "
            f"({src_balance=}, {expected_src_balance=})..."
        )
        prev_src_balance = src_balance

        count = 0

        while (
            src_balance := await balances.get_balance(
                src_w3, src_token, account.address
            )
        ) > expected_src_balance and count < config.max_polls:
            count += 1

            if (filled_amount := prev_src_balance - src_balance) > 0:
                base_logger.warning(
                    f"Expected to fill {src_amount} ticks, actually filled {
                        filled_amount} ticks"
                )
                break

            prev_src_balance = src_balance

            await asyncio.sleep(config.poll_timeout)

        if count >= config.max_polls:
            base_logger.warning("Source balance not withdrawn after max waiting time")
            yield SourceNotWithdrawn(
                (src_token, dest_token),
                order_response,
                config.max_polls * config.poll_timeout,
            )
            continue

        dest_balance = await balances.get_balance(dest_context, dest_token, account.address)
        base_logger.info(
            "Source balance withdrawn, waiting to receive destination token "
            f"({dest_balance=}, {expected_dest_balance=})..."
        )
        prev_dest_balance = dest_balance

        count = 0

        while (
            dest_balance := await balances.get_balance(
                dest_context, dest_token, account.address
            )
        ) < expected_dest_balance and count < config.max_polls:
            count += 1

            if (received_amount := dest_balance - prev_dest_balance) > 0:
                base_logger.warning(
                    f"Expected to receive {dest_amount} ticks, actually received {
                        received_amount} ticks"
                )
                break

            prev_dest_balance = dest_balance

            await asyncio.sleep(config.poll_timeout)

        if count >= config.max_polls:
            base_logger.warning(
                "Exceeded max number of polls. Transaction possibly stuck."
            )
            yield DestinationNotReceived(
                (src_token, dest_token),
                order_response,
                config.max_polls * config.poll_timeout,
            )

            src_token = await utility.choose_source_token(
                permanently_excluded_chains, account.address
            )
            src_w3 = await client_utility.make_w3(src_token.chain.id)
            src_order_book_contract = client_utility.make_order_book_contract(
                src_w3, src_token
            )

        else:
            base_logger.info("Destination balance received - order complete")

            yield Trade((src_token, dest_token), quote, order_response)

            src_token, src_w3, src_order_book_contract = (
                dest_token,
                dest_context,
                client_utility.make_order_book_contract(dest_context, dest_token),
            )

        destination_policy.reset()
        destination_policy.exclude_chain(src_token.chain.id)

