"""CreditAccount domain class for the Personal Finance Dashboard.

withdraw() now raises ValidationError/AccountError instead of
returning False, matching the Account update in this lesson.
"""

from dashboard.account import Account
from dashboard.exceptions import ValidationError, AccountError


class CreditAccount(Account):
    """An Account that permits a negative balance up to a credit limit.

    Attributes inherited from Account: name, account_type, balance.
    """

    def __init__(self, name: str, balance: float = 0.0, credit_limit: float = 1000.0) -> None:
        """Initialize a new CreditAccount.

        Args:
            name: The display name for this account.
            balance: The starting balance. Defaults to 0.0. May be
                negative if reconstructing from stored data.
            credit_limit: The maximum amount the balance may go
                negative by. Must be a positive number. Defaults to
                1000.0.

        Raises:
            ValueError: If credit_limit is not a positive number.
        """
        if not isinstance(credit_limit, (int, float)) or isinstance(credit_limit, bool) or credit_limit <= 0:
            raise ValueError(f"credit_limit must be a positive number, got {credit_limit!r}")
        self._credit_limit = float(credit_limit)
        super().__init__(name=name, account_type="credit", balance=balance)

    @property
    def credit_limit(self) -> float:
        """float: The maximum amount the balance may go negative by (read-only)."""
        return self._credit_limit

    @property
    def available_credit(self) -> float:
        """float: How much more can be charged before hitting the credit limit."""
        return self.credit_limit + self.balance

    def withdraw(self, amount: float) -> bool:
        """Charge the credit account, allowed to go negative up to credit_limit.

        This is a full override of Account.withdraw — the base
        class's "sufficient funds" rule does not apply to credit
        accounts.

        Args:
            amount: The amount to charge. Must be positive.

        Returns:
            True if the charge succeeded.

        Raises:
            ValidationError: If amount is not a positive number.
            AccountError: If the charge would push the balance below
                -credit_limit.
        """
        if not isinstance(amount, (int, float)) or isinstance(amount, bool) or amount <= 0:
            raise ValidationError(f"charge amount must be a positive number, got {amount!r}")
        if self.balance - amount < -self.credit_limit:
            raise AccountError(
                f"charge of {amount} would exceed credit limit of {self.credit_limit}"
            )
        self.balance = self.balance - amount
        return True

    def to_dict(self) -> dict:
        """Serialize this credit account to a plain dictionary.

        Returns:
            A dictionary including all Account fields (with "class"
            correctly set to "CreditAccount" by the base
            implementation) plus "credit_limit".
        """
        data = super().to_dict()
        data["credit_limit"] = self.credit_limit
        return data

    @classmethod
    def from_dict(cls, data: dict) -> "CreditAccount":
        """Construct a CreditAccount from a dictionary.

        Args:
            data: A dictionary with keys "name", "balance", and
                "credit_limit".

        Returns:
            A new CreditAccount instance built from the dictionary.
        """
        return cls(
            name=data["name"],
            balance=float(data.get("balance", 0.0)),
            credit_limit=float(data.get("credit_limit", 1000.0)),
        )

    def get_summary(self) -> str:
        """Return a formatted multi-line summary including credit details.

        Returns:
            The base Account summary with credit limit and available
            credit lines appended.
        """
        base_summary = super().get_summary()
        return (
            f"{base_summary}\n"
            f"  Credit Limit:     {Account.format_balance(self.credit_limit)}\n"
            f"  Available Credit: {Account.format_balance(self.available_credit)}"
        )

    def __str__(self) -> str:
        """Return a human-readable string representation of this account."""
        return f"{self.name} (credit): {Account.format_balance(self.balance)} | Limit: {Account.format_balance(self.credit_limit)}"

    def __repr__(self) -> str:
        """Return an unambiguous developer-facing representation of this account."""
        return (
            f"CreditAccount(name={self.name!r}, balance={self.balance!r}, "
            f"credit_limit={self.credit_limit!r})"
        )