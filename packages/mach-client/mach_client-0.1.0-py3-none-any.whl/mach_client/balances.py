from decimal import Decimal

from eth_typing import ChecksumAddress
from web3 import AsyncWeb3
from web3.types import Wei

from . import utility
from .client import client
from .constants import ChainId
from .data_types import Token


def decimal_balance(chain: ChainId, symbol: str, balance: int) -> Decimal:
    decimals = client.deployments[chain]["assets"][symbol]["decimals"]
    return Decimal(balance) / (10**decimals)


def _helper(chain: ChainId, raw_balances: dict[str, int]) -> dict[str, Decimal]:
    return {
        symbol: decimal_balance(chain, symbol, balance)
        for symbol, balance in raw_balances.items()
    }


async def get_balance(w3: AsyncWeb3, token: Token, wallet: ChecksumAddress) -> int:
    src_token_contract = utility.make_token_contract(w3, token)
    return await src_token_contract.functions.balanceOf(wallet).call()


# Balances of a wallet denominated in coins instead of ticks
async def get_balances(wallet: ChecksumAddress) -> dict[ChainId, dict[str, Decimal]]:
    raw_balances = await client.get_token_balances(wallet)
    return {
        chain: _helper(chain, raw_chain_balances)
        for chain, raw_chain_balances in raw_balances.items()
    }


async def get_gas_balance(w3: AsyncWeb3, wallet: ChecksumAddress) -> Wei:
    return await w3.eth.get_balance(wallet)
