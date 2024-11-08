import async_lru

from ..chain import Chain, ChainKind
from .chain_client import ChainClient
from .ethereum import EthereumClient
from .tron import TronClient


__all__ = []


@async_lru.alru_cache()
async def create(chain: Chain, *args, **kwargs) -> ChainClient:
    match chain.kind:
        case ChainKind.ETHEREUM:
            return await EthereumClient.create(chain, *args, **kwargs)
        case ChainKind.TRON:
            return await TronClient.create(chain, *args, **kwargs)
        case _:
            raise NotImplementedError(f"Unsupported chain kind: {chain.kind}")
