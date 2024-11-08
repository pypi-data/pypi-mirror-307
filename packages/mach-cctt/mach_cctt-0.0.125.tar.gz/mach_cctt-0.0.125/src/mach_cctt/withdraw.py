import asyncio
import logging
from pprint import pformat

from eth_account.signers.local import LocalAccount
from eth_typing import ChecksumAddress
from mach_client import Chain, ChainId, Token, client, transactions, utility
from web3 import AsyncWeb3

from .log import LogContextAdapter, Logger


async def drain_gas(
    w3: AsyncWeb3, account: LocalAccount, wallet: ChecksumAddress, logger: Logger
) -> None:
    chain = ChainId(await w3.eth.chain_id)

    logger = LogContextAdapter(logger, f"Withdraw {chain} gas")
    logger.info(f"Withdrawing {chain} gas")

    params = await transactions.fill_transaction_defaults(w3, account.address)
    params["to"] = wallet

    gas_estimate = await client.estimate_gas(ChainId(await w3.eth.chain_id))
    logger.debug(f"Gas estimate: {gas_estimate}")

    params["maxFeePerGas"] = w3.to_wei(gas_estimate["gas_estimate"], "wei")

    total_gas_cost = w3.to_wei(
        gas_estimate["gas_estimate"] * gas_estimate["gas_price"], "wei"
    )
    balance = await w3.eth.get_balance(account.address)
    value = w3.to_wei(max(0, balance - total_gas_cost), "wei")

    logger.debug(f"Gas balance of {balance}")
    logger.debug(f"Total gas cost of {total_gas_cost}")
    logger.debug(f"Transfer amount would be {value}")

    if value <= 0:
        logger.info("Skipping, balance of 0")
        return

    params["value"] = value

    await transactions.send_transaction(w3, account, params, logger)


# Drains balances of all tokens and gas asset on the chain into the destination wallet
async def drain_chain(
    chain: Chain,
    balances: dict[str, int],
    account: LocalAccount,
    wallet: ChecksumAddress,
    logger: Logger,
) -> None:
    logger = LogContextAdapter(logger, f"Drain {chain}")
    logger.info("Draining")

    w3 = await utility.make_w3(chain.id)

    gas_token = client.gas_tokens[chain.id]

    # First drain everything but the gas token
    await asyncio.gather(
        *(
            transactions.transfer_token(
                w3, Token(chain.id, symbol), balance, account, wallet, logger
            )
            for symbol, balance in filter(
                lambda item: item[0] != gas_token, balances.items()
            )
        )
    )

    # Then drain the gas token
    try:
        await drain_gas(w3, account, wallet, logger)
    except Exception as e:
        logging.warning(f"Failed to withdraw gas ok {chain}: {e}")


async def drain_all(
    account: LocalAccount, wallet: ChecksumAddress, logger: Logger
) -> None:
    all_balances = await client.get_token_balances(account.address)

    logger.info("Balances:")
    logger.info(pformat(all_balances))

    await asyncio.gather(
        *(
            drain_chain(Chain(chain_id), balances, account, wallet, logger)
            for chain_id, balances in all_balances.items()
        )
    )
