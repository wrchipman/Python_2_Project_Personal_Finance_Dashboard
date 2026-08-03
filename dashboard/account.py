"""Account domain class for the Personal Finance Dashboard.

Now includes the full instance/class/static method pattern. Gains
full encapsulation with properties in Lesson 11, and becomes the
base for CreditAccount/SavingsAccount subclasses in Lesson 12.
"""


class Account:
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
            ValueError: If account_type is not in VALID_TYPES.
        """
        if not Account.is_valid_type(account_type):
            raise ValueError(
                f"account_type must be one of {sorted(Account.VALID_TYPES)}, "
                f"got {account_type!r}"
            )
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
            f"  Balance: {Account.format_balance(self.balance)}"
        )

    def to_dict(self) -> dict:
        """Serialize this account to a plain dictionary.

        Returns:
            A dictionary with keys "name", "account_type", "balance".
        """
        return {
            "name": self.name,
            "account_type": self.account_type,
            "balance": self.balance,
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
        return f"{self.name} ({self.account_type}): {Account.format_balance(self.balance)}"

    def __repr__(self) -> str:
        """Return an unambiguous developer-facing representation of this account."""
        return f"Account(name={self.name!r}, account_type={self.account_type!r}, balance={self.balance!r})"