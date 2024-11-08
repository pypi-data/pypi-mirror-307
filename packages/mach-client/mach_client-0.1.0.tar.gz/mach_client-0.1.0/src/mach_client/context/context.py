import abc
from abc import ABC


class Context(ABC):
    """
    A chain-specific context. This serves the purpose of web3.py's Web3 class, or solana's Connection class.
    """

    def __init__(self, chain: Chain) -> None:
        self._chain = chain

    @abc.abstractmethod
    def chain() -> Chain:
        """
        The chain this Context is associated with.
        """
    
    @abc.abstractmethod
    def native_client() -> Any:
        """
        The native client for this chain.
        """
    
    @abc.abstractmethod
    async def estimate_gas(transaction: Transaction) -> int:
        """
        Estimate the gas for a transaction.
        """
    
    @abc.abstractmethod
    async def get_balance(token: Token, address: str) -> int:
        """
        Get the balance of a token.
        """
    
    @abc.abstractmethod
    async def get_gas_balance(address: str) -> int:
        """
        Get the gas balance.
        """