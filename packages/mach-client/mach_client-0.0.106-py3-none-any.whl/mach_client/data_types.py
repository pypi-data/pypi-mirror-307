from eth_typing import ChecksumAddress
from typing import Any

from .client import client
from .constants import ChainId


class Token:
    __slots__ = ("chain", "symbol", "chain_id", "contract_address", "decimals")

    def __init__(self, chain_id: ChainId, symbol: str):
        self.symbol = symbol
        self.chain = Chain(chain_id)
        asset_data = self.chain.data["assets"][self.symbol]
        self.contract_address: ChecksumAddress = asset_data["address"]
        self.decimals: int = asset_data["decimals"]

    @classmethod
    def from_str(cls, identifier: str):
        chain_name, symbol = identifier.split("-")
        chain_id = ChainId.from_name(chain_name)
        return cls(chain_id, symbol)

    @classmethod
    def from_contract_address(cls, chain: ChainId, contract_address: ChecksumAddress):
        symbol = client.symbol_by_contract[(chain, contract_address)]
        return cls(chain, symbol)

    def __eq__(self, other: Any) -> bool:
        return (
            isinstance(other, Token)
            and self.chain == other.chain
            and self.symbol == other.symbol
        )

    def __hash__(self) -> int:
        return hash((self.chain, self.symbol))

    def __repr__(self) -> str:
        return f"{self.chain}-{self.symbol}"

    def is_gas_token(self) -> bool:
        return self.symbol == client.gas_tokens.get(self.chain.id, None)

    def is_stablecoin(self) -> bool:
        return self.symbol in ("FRAX", "DAI", "MIM") or any(
            map(
                lambda symbol: symbol in self.symbol,
                ("USD", "EUR", "JPY", "GPB", "CHF"),
            )
        )

    def is_chf_stablecoin(self) -> bool:
        return "CHF" in self.symbol

    def is_eur_stablecoin(self) -> bool:
        return "EUR" in self.symbol

    def is_gbp_stablecoin(self) -> bool:
        return "GBP" in self.symbol

    def is_jpy_stablecoin(self) -> bool:
        return "JPY" in self.symbol

    def is_usd_stablecoin(self) -> bool:
        return "USD" in self.symbol or self.symbol in ("FRAX", "DAI", "MIM")

    def is_btc(self) -> bool:
        return "BTC" in self.symbol

    def is_eth(self) -> bool:
        return "ETH" in self.symbol


class Chain:
    __slots__ = ("id", "data", "lz_cid")

    def __init__(self, id: ChainId):
        self.id = id
        self.data = client.deployments[self.id]
        self.lz_cid: int = self.data["lz_cid"]  # type: ignore

    @classmethod
    def from_id(cls, id: int):
        return cls(ChainId(id))

    @classmethod
    def from_name(cls, name: str):
        return cls(ChainId.from_name(name))

    @property
    def name(self) -> str:
        return str(self.id)

    def __eq__(self, other) -> bool:
        return isinstance(other, Chain) and self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)

    def __repr__(self) -> str:
        return self.name
