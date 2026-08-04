"""Account domain class for the Personal Finance Dashboard.

deposit() and withdraw() now raise ValidationError/AccountError on
failure instead of returning False, matching the exception hierarchy
finalized in Lesson 7. This supersedes the return-bool behavior from
Lessons 9-12.
"""

from dashboard.base_account import BaseAccount
from dashboard.exceptions import ValidationError, AccountError


class Account(BaseAccount):
    """Represents a single financial account (checking, savings, or credit).

    Class Attributes:
        VALID_TYPES: The set of account type strings accepted by
            is_valid_type.
        account_count: The total number of Account instances created
            during the program's lifetime.
    """

    VALID_TYPES = {"checking", "savings", "credit"}
    account_count = 0

    def __init__(self, name: str, account_type: str, balance: float = 0.0) -> None:
        """Initialize a new Account.

        Args:
            name: The display name for this account.
            account_type: The kind of account. Must be one of
                VALID_TYPES.
            balance: The starting balance. Defaults to 0.0.

        Raises:
            ValueError: If account_type is not in VALID_TYPES, or if
                balance is negative.
        """
        self._validate_type(account_type)
        self._name = name
        self._account_type = account_type
        self.balance = balance  # goes through the setter for validation
        Account.account_count += 1

    def _validate_type(self, account_type: str) -> None:
        """Raise ValueError if account_type is not a valid type.

        Args:
            account_type: The string to validate.

        Raises:
            ValueError: If account_type is not in VALID_TYPES.
        """
        if not Account.is_valid_type(account_type):
            raise ValueError(
                f"account_type must be one of {sorted(Account.VALID_TYPES)}, "
                f"got {account_type!r}"
            )

    @property
    def name(self) -> str:
        """str: The account's display name (read-only)."""
        return self._name

    @property
    def account_type(self) -> str:
        """str: The account's type (read-only)."""
        return self._account_type

    @property
    def balance(self) -> float:
        """float: The account's current balance."""
        return self._balance

    @balance.setter
    def balance(self, value: float) -> None:
        """Set the account's balance with validation.

        Args:
            value: The new balance. Must be a non-negative number.

        Raises:
            ValueError: If value is not a non-negative number.
        """
        if not isinstance(value, (int, float)) or isinstance(value, bool):
            raise ValueError(f"balance must be a number, got {type(value).__name__}")
        if value < 0:
            raise ValueError(f"balance cannot be negative, got {value}")
        self._balance = float(value)

    def deposit(self, amount: float) -> bool:
        """Add funds to the account balance.

        Args:
            amount: The amount to deposit. Must be positive.

        Returns:
            True if the deposit succeeded.

        Raises:
            ValidationError: If amount is not a positive number.
        """
        if not isinstance(amount, (int, float)) or isinstance(amount, bool) or amount <= 0:
            raise ValidationError(f"deposit amount must be a positive number, got {amount!r}")
        self.balance = self.balance + amount
        return True

    def withdraw(self, amount: float) -> bool:
        """Remove funds from the account balance.

        Args:
            amount: The amount to withdraw. Must be positive and no
                greater than the current balance.

        Returns:
            True if the withdrawal succeeded.

        Raises:
            ValidationError: If amount is not a positive number.
            AccountError: If amount exceeds the current balance.
        """
        if not isinstance(amount, (int, float)) or isinstance(amount, bool) or amount <= 0:
            raise ValidationError(f"withdraw amount must be a positive number, got {amount!r}")
        if amount > self.balance:
            raise AccountError(
                f"insufficient funds: balance is {self.balance}, cannot withdraw {amount}"
            )
        self.balance = self.balance - amount
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
            f"  Balance: {Account.format_balance(self.balance)}"
        )

    def to_dict(self) -> dict:
        """Serialize this account to a plain dictionary.

        Returns:
            A dictionary with keys "name", "account_type", "balance",
            and "class" (the actual runtime class name, so subclasses
            get the correct value automatically via super().to_dict()).
        """
        return {
            "name": self.name,
            "account_type": self.account_type,
            "balance": self.balance,
            "class": type(self).__name__,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Account":
        """Construct an Account from a dictionary.

        Args:
            data: A dictionary with keys "name", "account_type", and
                "balance". "balance" may be a string or number.

        Returns:
            A new Account instance built from the dictionary.
        """
        return cls(
            name=data["name"],
            account_type=data["account_type"],
            balance=float(data.get("balance", 0.0)),
        )

    @classmethod
    def from_csv_row(cls, row: list) -> "Account":
        """Construct an Account from a positional list of values.

        Args:
            row: A list in the order [name, account_type, balance].

        Returns:
            A new Account instance built from the row.
        """
        name, account_type, balance = row
        return cls(name=name, account_type=account_type, balance=float(balance))

    @classmethod
    def get_account_count(cls) -> int:
        """Return the total number of Account instances created.

        Returns:
            The current value of account_count.
        """
        return cls.account_count

    @staticmethod
    def is_valid_type(account_type: str) -> bool:
        """Check whether a given string is a valid account type.

        Args:
            account_type: The string to check.

        Returns:
            True if account_type is in VALID_TYPES, False otherwise.
        """
        return account_type in Account.VALID_TYPES

    @staticmethod
    def format_balance(amount: float) -> str:
        """Format a numeric amount as a currency string.

        Args:
            amount: The numeric value to format.

        Returns:
            A string formatted as "$1,234.56".
        """
        return f"${amount:,.2f}"

    def __str__(self) -> str:
        """Return a human-readable string representation of this account."""
        return f"{self.name} ({self.account_type}) | Balance: {Account.format_balance(self.balance)}"

    def __repr__(self) -> str:
        """Return an unambiguous developer-facing representation of this account."""
        return (
            f"Account(name={self.name!r}, account_type={self.account_type!r}, "
            f"balance={self.balance!r})"
        )

    def __eq__(self, other: object) -> bool:
        """Compare two accounts for equality by name and account_type.

        Args:
            other: The object to compare against.

        Returns:
            True if other is an Account with the same name and
            account_type. Returns NotImplemented if other is not an
            Account, letting Python fall back appropriately.
        """
        if not isinstance(other, Account):
            return NotImplemented
        return self.name == other.name and self.account_type == other.account_type

    def __hash__(self) -> int:
        """Return a hash consistent with __eq__ (based on name and account_type)."""
        return hash((self.name, self.account_type))

    def __lt__(self, other: object) -> bool:
        """Compare two accounts by balance, for use with sorted().

        Args:
            other: The object to compare against.

        Returns:
            True if this account's balance is less than other's.
            Returns NotImplemented if other is not an Account.
        """
        if not isinstance(other, Account):
            return NotImplemented
        return self.balance < other.balance

    def __add__(self, other: object) -> float:
        """Combine the balances of two accounts.

        Args:
            other: The other Account to combine with.

        Returns:
            The sum of both accounts' balances as a float. Returns
            NotImplemented if other is not an Account.
        """
        if not isinstance(other, Account):
            return NotImplemented
        return self.balance + other.balance

    def __radd__(self, other: object) -> float:
        """Support sum() by handling the initial 0 + account case.

        Args:
            other: The left-hand operand, expected to be 0 (as
                supplied by sum()'s default start value).

        Returns:
            This account's balance if other == 0. Returns
            NotImplemented otherwise.
        """
        if other == 0:
            return self.balance
        return NotImplemented

    def __iadd__(self, amount: float) -> "Account":
        """Increase the balance in place using += .

        Args:
            amount: The amount to add to the balance.

        Returns:
            self, with balance updated.

        Raises:
            ValidationError: If amount is not a positive number.
        """
        if not isinstance(amount, (int, float)) or isinstance(amount, bool) or amount <= 0:
            raise ValidationError(f"amount must be a positive number, got {amount!r}")
        self.balance = self.balance + amount
        return self

    def __isub__(self, amount: float) -> "Account":
        """Decrease the balance in place using -= , via withdraw().

        Args:
            amount: The amount to withdraw from the balance.

        Returns:
            self, with balance updated on success.

        Raises:
            ValidationError: If amount is not a positive number
                (propagated from withdraw()).
            AccountError: If amount exceeds the current balance
                (propagated from withdraw()).
        """
        self.withdraw(amount)
        return self