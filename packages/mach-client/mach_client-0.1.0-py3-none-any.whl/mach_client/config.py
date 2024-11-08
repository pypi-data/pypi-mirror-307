from importlib import resources
from importlib.abc import Traversable
import json
import os
from typing import Any

import yaml

from .chain import Chain


config: dict = yaml.safe_load(os.environ.get("CONFIG_PATH", "config.yaml"))[
    "mach_client"
]


def load_abi(path: Traversable) -> Any:
    with path.open("r") as abi:
        return json.load(abi)


endpoint_uris: dict[Chain, str] = {
    Chain(chain): endpoint_uri
    for chain, endpoint_uri in config["chain_endpoint_uris"].items()
    if chain in Chain
}

backend_url = config["backend"]["url"]

endpoints: dict[str, str] = config["backend"]["endpoints"]


# Relative to the root of the repository
abi_path = resources.files("abi")

ethereum_order_book_abi = load_abi(abi_path / "mach" / "order_book.json")

erc20_abi = load_abi(abi_path / "ethereum" / "erc20.json")
