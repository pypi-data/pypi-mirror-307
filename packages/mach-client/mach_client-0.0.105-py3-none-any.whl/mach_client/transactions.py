from pprint import pformat
from typing import Optional

from eth_account.signers.local import LocalAccount
from eth_typing import ChecksumAddress
from hexbytes import HexBytes
from web3 import AsyncWeb3
from web3.contract.async_contract import AsyncContract, AsyncContractFunction
from web3.types import TxParams

from . import utility
from .data_types import Token
from .log import LogContextAdapter, Logger


async def fill_transaction_defaults(
    w3: AsyncWeb3, address: ChecksumAddress
) -> TxParams:
    params: TxParams = {
        "from": address,
        "nonce": await w3.eth.get_transaction_count(address, "latest"),
    }
    return params


async def send_transaction(
    w3: AsyncWeb3,
    account: LocalAccount,
    params: TxParams,
    logger: Logger,
) -> HexBytes:
    logger.debug("Sending transaction with params:")
    logger.debug(pformat(params))

    signed_transaction = account.sign_transaction(params)  # type: ignore

    logger.debug(f"Sending raw transaction: {pformat(signed_transaction)}")

    transaction_hash = await w3.eth.send_raw_transaction(
        signed_transaction.raw_transaction
    )

    logger.debug(f"Transaction hash: {transaction_hash.to_0x_hex()}")

    transaction_receipt = await w3.eth.wait_for_transaction_receipt(transaction_hash)

    logger.debug("Received receipt:")
    logger.debug(pformat(dict(transaction_receipt)))

    assert transaction_receipt["status"] == 0x1, "Transaction failed"

    logger.debug("Transaction success")

    return transaction_hash


async def approve(
    account: LocalAccount,
    spender: ChecksumAddress,
    token_contract: AsyncContract,
    amount: int,
    logger: Logger,
) -> HexBytes:
    logger = LogContextAdapter(logger, "Approve")

    approve_function = token_contract.functions.approve(
        spender, amount
    )

    params = await fill_transaction_defaults(token_contract.w3, account.address)
    params = await approve_function.build_transaction(params)

    logger.debug("Sending approve transaction")

    return await send_transaction(token_contract.w3, account, params, logger)


async def send_contract_function_transaction(
    contract_function: AsyncContractFunction,
    account: LocalAccount,
    logger: Logger,
) -> HexBytes:
    logger.debug(f"{contract_function=}")
    params = await fill_transaction_defaults(contract_function.w3, account.address)
    params = await contract_function.build_transaction(params)
    params["gas"] = int(1.5 * params["gas"])  # type: ignore

    return await send_transaction(contract_function.w3, account, params, logger)


async def approve_send_contract_function_transaction(
    contract_function: AsyncContractFunction,
    account: LocalAccount,
    token_contract: AsyncContract,
    amount: int,
    logger: Logger,
) -> HexBytes:
    await approve(account, contract_function.address, token_contract, amount, logger)
    return await send_contract_function_transaction(contract_function, account, logger)


async def transfer_token(
    w3: AsyncWeb3,
    token: Token,
    amount: int,
    account: LocalAccount,
    wallet: ChecksumAddress,
    logger: Logger,
) -> Optional[HexBytes]:
    logger = LogContextAdapter(logger, f"Transfer {token}")

    if amount <= 0:
        logger.info(f"Skipping {token} - balance empty")
        return

    logger.info(f"Transferring {amount} units of {token}")

    contract = utility.make_token_contract(w3, token)

    params = await fill_transaction_defaults(w3, account.address)
    params["chainId"] = token.chain.id

    params = await contract.functions.transfer(wallet, amount).build_transaction(params)

    return await send_transaction(w3, account, params, logger)
