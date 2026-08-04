"""Abstract base class for all account types in the Personal Finance Dashboard."""

from abc import ABC, abstractmethod


class BaseAccount(ABC):
    """Defines the required interface every account type must implement.

    Any class representing an account — Account, CreditAccount,
    SavingsAccount, or any future account type — must implement all
    five methods below to be instantiable.
    """

    @abstractmethod
    def deposit(self, amount: float) -> bool:
        """Add funds to the account balance.

        Args:
            amount: The amount to deposit.

        Returns:
            True if the deposit succeeded, False otherwise.
        """
        raise NotImplementedError

    @abstractmethod
    def withdraw(self, amount: float) -> bool:
        """Remove funds from the account balance.

        Args:
            amount: The amount to withdraw.

        Returns:
            True if the withdrawal succeeded, False otherwise.
        """
        raise NotImplementedError

    @abstractmethod
    def get_summary(self) -> str:
        """Return a formatted multi-line summary of this account.

        Returns:
            A multi-line string describing the account.
        """
        raise NotImplementedError

    @abstractmethod
    def to_dict(self) -> dict:
        """Serialize this account to a plain dictionary.

        Returns:
            A dictionary representation of this account.
        """
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def from_dict(cls, data: dict) -> "BaseAccount":
        """Construct an account instance from a dictionary.

        Args:
            data: A dictionary of account field values.

        Returns:
            A new instance of the implementing account class.
        """
        raise NotImplementedError