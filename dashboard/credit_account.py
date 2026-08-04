"""CreditAccount domain class for the Personal Finance Dashboard.

A CreditAccount is an Account whose balance may go negative up to a
configured credit limit. This requires overriding the balance
property itself (not just withdraw()) — Account's inherited balance
setter forbids any negative value, which is correct for checking and
savings accounts but wrong for credit accounts, where a negative
balance is the normal representation of amount owed.
"""

from dashboard.account import Account


class CreditAccount(Account):
    """An Account that permits a negative balance up to a credit limit.

    Attributes inherited from Account: name, account_type, balance
    (with a permissive lower bound overridden below).
    """

    def __init__(self, name: str, balance: float = 0.0, credit_limit: float = 1000.0) -> None:
        """Initialize a new CreditAccount.

        Args:
            name: The display name for this account.
            balance: The starting balance. Defaults to 0.0. May be
                negative (down to -credit_limit) if reconstructing
                from stored data.
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

    @property
    def balance(self) -> float:
        """float: The account's current balance.

        Overrides Account.balance to permit a negative value down to
        -credit_limit, since a credit account's balance represents
        amount owed and is expected to go negative under normal use.
        Both the getter and setter must be redefined together — you
        cannot override just one half of an inherited property.
        """
        return self._balance

    @balance.setter
    def balance(self, value: float) -> None:
        """Set the balance, permitting negative values down to -credit_limit.

        Args:
            value: The new balance. Must be a number no less than
                -credit_limit.

        Raises:
            ValueError: If value is not a number, or is less than
                -credit_limit.
        """
        if not isinstance(value, (int, float)) or isinstance(value, bool):
            raise ValueError(f"balance must be a number, got {type(value).__name__}")
        if value < -self._credit_limit:
            raise ValueError(
                f"balance cannot go below -{self._credit_limit} (credit_limit), got {value}"
            )
        self._balance = float(value)

    def withdraw(self, amount: float) -> bool:
        """Charge the credit account, allowed to go negative up to credit_limit.

        This is a full override of Account.withdraw — the base
        class's "sufficient funds" rule does not apply to credit
        accounts.

        Args:
            amount: The amount to charge. Must be positive.

        Returns:
            True if the charge succeeded, False if amount was invalid
            or would push the balance below -credit_limit.
        """
        if not isinstance(amount, (int, float)) or isinstance(amount, bool) or amount <= 0:
            return False
        if self.balance - amount < -self.credit_limit:
            return False
        self.balance = self.balance - amount
        return True

    def to_dict(self) -> dict:
        """Serialize this credit account to a plain dictionary.

        Returns:
            A dictionary including all Account fields plus
            "credit_limit" and "class".
        """
        data = super().to_dict()
        data["credit_limit"] = self.credit_limit
        data["class"] = "CreditAccount"
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