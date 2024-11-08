from __future__ import annotations
from enum import Enum
from typing import Any

from hexbytes import HexBytes


class ChainKind(Enum):
    BITCOIN = "bitcoin"
    ETHEREUM = "ethereum"
    SOLANA = "solana"
    TRON = "tron"


# CAIP-2 Chain IDs
class Chain(Enum):
    # BITCOIN = "bip122:000000000019d6689c085ae165831e93"

    ETHEREUM = "eip155:1"
    OP = "eip155:10"
    BNB = "eip155:56"
    POLYGON = "eip155:137"
    OPBNB = "eip155:204"
    MANTLE = "eip155:5000"
    BASE = "eip155:8453"
    MODE = "eip155:34443"
    ARBITRUM = "eip155:42161"
    CELO = "eip155:42220"
    AVALANCHE_C_CHAIN = "eip155:43114"
    BLAST = "eip155:81457"
    SCROLL = "eip155:54352"

    # SOLANA = "solana:5eykt4UsFv8P8NJdTREpY1vzqKqZKvdp"

    TRON = "tron:27Lqcw"

    @property
    def id(self) -> str:
        return self.value

    @property
    def namespace(self) -> str:
        return self.value.split(":")[0]

    @property
    def reference(self) -> str:
        return self.value.split(":")[1]

    @property
    def kind(self) -> ChainKind:
        match self.namespace:
            case "bip122":
                return ChainKind.BITCOIN
            case "eip155":
                return ChainKind.ETHEREUM
            case "solana":
                return ChainKind.SOLANA
            case "tron":
                return ChainKind.TRON
            case _:
                raise NotImplementedError()

    @property
    def layerzero_id(self) -> int:
        return LAYERZERO_IDS[self]

    @property
    def native_id(self) -> Any:
        match self.kind:
            case ChainKind.ETHEREUM:
                return int(self.reference)
            case _:
                return self.reference

    def __str__(self) -> str:
        return CHAIN_NAMES[self]

    def __repr__(self) -> str:
        return self.id


# https://github.com/tristeroresearch/cache-half-full/blob/staging/config/deployments.json
CHAIN_NAMES = {
    # Chain.BITCOIN: "Bitcoin",
    Chain.ETHEREUM: "Ethereum",
    Chain.OP: "Optimism",
    Chain.BNB: "BNB",
    Chain.POLYGON: "Polygon",
    Chain.OPBNB: "opBNB",
    Chain.MANTLE: "Mantle",
    Chain.BASE: "Base",
    Chain.MODE: "Mode",
    Chain.ARBITRUM: "Arbitrum",
    Chain.CELO: "Celo",
    Chain.AVALANCHE_C_CHAIN: "Avalanche",
    Chain.BLAST: "Blast",
    Chain.SCROLL: "Scroll",
    # Chain.SOLANA: "Solana",
    Chain.TRON: "Tron",
}

CHAIN_IDS = {name: id for id, name in CHAIN_NAMES.items()}

LAYERZERO_IDS = {
    # Chain.BITCOIN: ,
    Chain.ETHEREUM: 101,
    Chain.OP: 111,
    Chain.BNB: 102,
    Chain.POLYGON: 109,
    Chain.OPBNB: 202,
    Chain.MANTLE: 181,
    Chain.BASE: 184,
    Chain.MODE: 260,
    Chain.ARBITRUM: 111,
    Chain.CELO: 125,
    Chain.AVALANCHE_C_CHAIN: 106,
    Chain.BLAST: 243,
    Chain.SCROLL: 214,
    # Chain.SOLANA: 168,
    Chain.TRON: 30420,
}

ETHEREUM_SCANNERS = {
    Chain.ETHEREUM: "https://etherscan.io",
    Chain.OP: "https://optimistic.etherscan.io",
    Chain.BNB: "https://bscscan.com",
    Chain.POLYGON: "https://polygonscan.com",
    Chain.OPBNB: "https://opbnbscan.com",
    Chain.MANTLE: "https://explorer.mantle.xyz",
    Chain.BASE: "https://basescan.org",
    Chain.MODE: "https://modescan.io",
    Chain.ARBITRUM: "https://arbiscan.io",
    Chain.CELO: "https://explorer.celo.org/mainnet",
    Chain.AVALANCHE_C_CHAIN: "https://snowscan.xyz",
    Chain.BLAST: "https://blastscan.io",
    Chain.SCROLL: "https://scrollscan.com",
    Chain.TRON: "https://tronscan.io/#",
}


class Scanner:
    @staticmethod
    def address(chain: Chain, wallet) -> str:
        match chain.kind:
            case ChainKind.ETHEREUM:
                return f"{ETHEREUM_SCANNERS[chain]}/address/{wallet}"
            case ChainKind.TRON:
                raise NotImplementedError()
                return f"https://tronscan.io/#/address/{wallet}"
            case _:
                raise NotImplementedError()

    @staticmethod
    def transaction(chain: Chain, transaction_hash) -> str:
        match chain.kind:
            case ChainKind.ETHEREUM:
                assert isinstance(transaction_hash, HexBytes)
                return f"{ETHEREUM_SCANNERS[chain]}/tx/{transaction_hash.to_0x_hex()}"
            case ChainKind.TRON:
                raise NotImplementedError()
                return f"https://tronscan.io/#/transaction/{transaction_hash}"
            case _:
                raise NotImplementedError()

    @staticmethod
    def token(token: Token) -> str:
        match token.chain.kind:
            case ChainKind.ETHEREUM:
                return (
                    f"{ETHEREUM_SCANNERS[token.chain]}/token/{token.contract_address}"
                )
            case ChainKind.TRON:
                raise NotImplementedError()
                return f"https://tronscan.io/#/token20/{token.contract_address}"
            case _:
                raise NotImplementedError()
