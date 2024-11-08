# Note: this module should really be merged with the data_types module, but is kept separate to avoid circular imports in the client module

from __future__ import annotations
from enum import IntEnum

from eth_typing import ChecksumAddress
from hexbytes import HexBytes


class ChainId(IntEnum):
    ETHEREUM = 1
    OP = 10
    BSC = 56
    POLYGON = 137
    OPBNB = 204
    MANTLE = 5000
    BASE = 8453
    MODE = 34443
    ARBITRUM = 42161
    CELO = 42220
    AVALANCHE_C_CHAIN = 43114
    BLAST = 81457
    SCROLL = 54352

    @staticmethod
    def from_name(name: str) -> ChainId:
        return CHAIN_IDS[name]

    def __str__(self):
        return CHAIN_NAMES[self]


CHAIN_NAMES = {
    ChainId.ETHEREUM: "ethereum",
    ChainId.OP: "optimism",
    ChainId.BSC: "bsc",
    ChainId.POLYGON: "polygon",
    ChainId.OPBNB: "opbnb",
    ChainId.MANTLE: "mantle",
    ChainId.BASE: "base",
    ChainId.MODE: "mode",
    ChainId.ARBITRUM: "arbitrum",
    ChainId.CELO: "celo",
    ChainId.AVALANCHE_C_CHAIN: "avalanche",
    ChainId.BLAST: "blast",
    ChainId.SCROLL: "scroll",
}

CHAIN_IDS = {name: id for id, name in CHAIN_NAMES.items()}

SCANNERS = {
    ChainId.ETHEREUM: "https://etherscan.io",
    ChainId.OP: "https://optimistic.etherscan.io",
    ChainId.BSC: "https://bscscan.com",
    ChainId.POLYGON: "https://polygonscan.com",
    ChainId.OPBNB: "https://opbnbscan.com",
    ChainId.MANTLE: "https://explorer.mantle.xyz",
    ChainId.BASE: "https://basescan.org",
    ChainId.MODE: "https://modescan.io",
    ChainId.ARBITRUM: "https://arbiscan.io",
    ChainId.CELO: "https://explorer.celo.org/mainnet",
    ChainId.AVALANCHE_C_CHAIN: "https://snowscan.xyz",
    ChainId.BLAST: "https://blastscan.io",
    ChainId.SCROLL: "https://scrollscan.com",
}


class Scanner:
    @staticmethod
    def address(chain_id: ChainId, wallet: ChecksumAddress) -> str:
        return f"{SCANNERS[chain_id]}/address/{wallet}"

    @staticmethod
    def transaction(chain_id: ChainId, transaction_hash: HexBytes) -> str:
        return f"{SCANNERS[chain_id]}/tx/{transaction_hash.to_0x_hex()}"

    @staticmethod
    def token(token: Token) -> str:  # type: ignore
        return f"{SCANNERS[token.chain.id]}/token/{token.contract_address}"
