from typing import Optional

from eth_account.signers.local import LocalAccount
from mach_client import Token, transactions, utility

from .. import config
from ..log import LogContextAdapter, Logger


async def supply(
    token: Token, account: LocalAccount, logger: Logger
) -> tuple[int, Optional[Exception]]:
    logger = LogContextAdapter(logger, f"{token} => Aave")

    w3 = await utility.make_w3(token.chain.id)
    token_contract = utility.make_token_contract(w3, token)

    if (
        balance := await token_contract.functions.balanceOf(account.address).call()
    ) <= 0:
        logger.warning("Balance was empty, not supplying")
        return 0, None

    try:
        aave_pool_address = config.aave_pool_addresses[token.chain.id]
        pool_contract = w3.eth.contract(
            address=aave_pool_address,  # type: ignore
            abi=config.aave_pool_abi(token.chain.id),
        )
        supply_function = pool_contract.functions.supply(
            token.contract_address,
            balance,
            account.address,
            0,  # Referral code
        )

        logger.info(f"Supplying {balance} units")

        await transactions.approve_send_contract_function_transaction(
            supply_function,
            account,
            token_contract,
            # TODO: This should be `balance`, but that causes occasional errors like this:
            # web3.exceptions.ContractLogicError: ('execution reverted: ERC20: transfer amount exceeds allowance', '0x08c379a00000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000000000000000002845524332303a207472616e7366657220616d6f756e74206578636565647320616c6c6f77616e6365000000000000000000000000000000000000000000000000')
            # Maybe you can't withdraw any additional interest accrued within the current block even if it is counted in balanceOf?
            config.solidity_uint_max,
            logger,
        )
    except Exception as e:
        return balance, e

    logger.info("Supply successful")

    return balance, None
