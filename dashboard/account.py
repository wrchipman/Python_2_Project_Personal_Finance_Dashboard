"""Account domain class for the Personal Finance Dashboard.

This is the initial, unencapsulated version of Account. It gains
class/static methods in Lesson 10, full encapsulation with properties
in Lesson 11, and becomes the base for CreditAccount/SavingsAccount
subclasses in Lesson 12.
"""


class Account:
    """Represents a single financial account (checking, savings, or credit).

    Class Attributes:
        account_count: The total number of Account instances created
            during the program's lifetime.
    """

    account_count = 0

    def __init__(self, name: str, account_type: str, balance: float = 0.0) -> None:
        """Initialize a new Account.

        Args:
            name: The display name for this account.
            account_type: The kind of account (e.g., "checking",
                "savings", "credit").
            balance: The starting balance. Defaults to 0.0.
        """
        self.name = name
        self.account_type = account_type
        self.balance = balance
        Account.account_count += 1

    def deposit(self, amount: float) -> bool:
        """Add funds to the account balance.

        Args:
            amount: The amount to deposit. Must be positive.

        Returns:
            True if the deposit succeeded, False if amount was not
            a positive number.
        """
        if not isinstance(amount, (int, float)) or isinstance(amount, bool) or amount <= 0:
            return False
        self.balance += amount
        return True

    def withdraw(self, amount: float) -> bool:
        """Remove funds from the account balance.

        Args:
            amount: The amount to withdraw. Must be positive and no
                greater than the current balance.

        Returns:
            True if the withdrawal succeeded, False if amount was
            invalid or exceeded the current balance.
        """
        if not isinstance(amount, (int, float)) or isinstance(amount, bool) or amount <= 0:
            return False
        if amount > self.balance:
            return False
        self.balance -= amount
        return True

    def get_balance(self) -> float:
        """Return the current account balance.

        Returns:
            The current balance as a float.
        """
        return self.balance

    def get_summary(self) -> str:
        """Return a formatted multi-line summary of this account.

        Returns:
            A multi-line string describing the account's name, type,
            and current balance. Does not print anything.
        """
        return (
            f"Account Summary\n"
            f"  Name:    {self.name}\n"
            f"  Type:    {self.account_type}\n"
            f"  Balance: ${self.balance:,.2f}"
        )

    def __str__(self) -> str:
        """Return a human-readable string representation of this account."""
        return f"{self.name} ({self.account_type}): ${self.balance:,.2f}"

    def __repr__(self) -> str:
        """Return an unambiguous developer-facing representation of this account."""
        return f"Account(name={self.name!r}, account_type={self.account_type!r}, balance={self.balance!r})"