from importlib import resources
from importlib.abc import Traversable
import json
import os
from typing import Any

from .constants import ChainId


def load_abi(path: Traversable) -> Any:
    with path.open("r") as abi:
        return json.load(abi)


# A layer-n chain's unique identifier is "<layer n-1 identifier>_<layer n identifier>"
# ie. "ETHEREUM_OP" for the Optimism chain on Ethereum
# We use "ENDPOINT_URI_<chain identifier>" to specify the endpoint URI for each chain
def get_endpoint_uris() -> dict[ChainId, str]:
    result = {}

    for chain in ChainId:
        if endpoint_uri := os.environ.get(f"ENDPOINT_URI_ETHEREUM_{str(chain).upper()}"):
            result[chain] = endpoint_uri

    return result


endpoint_uris = get_endpoint_uris()

backend_url = os.environ.get(
    "MACH_BACKEND_URL", "https://cache-half-full-production.fly.dev"
)

endpoints = {
    "orders": "/v1/orders",
    "gas": "/v1/orders/gas",
    "quotes": "/v1/quotes",
    "points": "/v1/points",
    "token_balances": "/tokenBalances",
    "get_config": "/get_config",
}


# Relative to the root of the repository
abi_path = resources.files("abi")

order_book_abi = load_abi(abi_path / "mach" / "order_book.json")

erc20_abi = load_abi(abi_path / "ethereum" / "erc20.json")
