from __future__ import annotations
import abc
from abc import ABC
from typing import Any

from ..chain import Chain


# Connect to a chain
# Replaces web3.AsyncWeb3/solana.rpc.async_api.AsyncClient/etc.
class ChainClient(ABC):
    @classmethod
    @abc.abstractmethod
    async def create(cls, chain: Chain, *args, **kwargs) -> ChainClient:
        pass

    def __init__(self, chain: Chain, client: Any) -> None:
        self._chain = chain
        self.client = client

    @property
    async def chain(self) -> Chain:
        return self._chain

    @property
    async def native_client(self) -> Any:
        return self.client

    @abc.abstractmethod
    async def is_connected(self) -> bool:
        pass

    @abc.abstractmethod
    async def 
