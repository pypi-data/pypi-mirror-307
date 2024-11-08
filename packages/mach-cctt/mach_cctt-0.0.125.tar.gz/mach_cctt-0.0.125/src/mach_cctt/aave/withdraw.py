from typing import Optional

from eth_account.signers.local import LocalAccount
from mach_client import Token, transactions, utility

from .. import config
from ..log import LogContextAdapter, Logger
from .atoken import get_atoken_balance


async def withdraw(
    token: Token, account: LocalAccount, logger: Logger
) -> tuple[int, Optional[Exception]]:
    logger = LogContextAdapter(logger, f"Aave {token} => account")
    w3 = await utility.make_w3(token.chain.id)

    if (balance := await get_atoken_balance(w3, token, account.address)) <= 0:
        logger.debug("Balance was empty, not withdrawing")
        return 0, None

    try:
        aave_pool_address = config.aave_pool_addresses[token.chain.id]
        pool_contract = w3.eth.contract(
            address=aave_pool_address,  # type: ignore
            abi=config.aave_pool_abi(token.chain.id),
        )
        withdraw_function = pool_contract.functions.withdraw(
            token.contract_address,
            config.solidity_uint_max,  # Means withdraw everything
            account.address,
        )

        logger.info(f"Withdrawing {balance} units")

        await transactions.send_contract_function_transaction(withdraw_function, account, logger)
    except Exception as e:
        return balance, e

    logger.info("Withdraw successful")

    return balance, None
