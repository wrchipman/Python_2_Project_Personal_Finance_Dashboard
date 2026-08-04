"""SavingsAccount domain class for the Personal Finance Dashboard.

A SavingsAccount is an Account that accrues interest at a fixed rate
and can apply that interest to its own balance on demand.
SavingsAccount inherits BaseAccount conformance through Account.
"""

from dashboard.account import Account


class SavingsAccount(Account):
    """An Account that accrues interest at a fixed rate.

    Attributes inherited from Account: name, account_type, balance.
    """

    def __init__(self, name: str, balance: float = 0.0, interest_rate: float = 0.05) -> None:
        """Initialize a new SavingsAccount.

        Args:
            name: The display name for this account.
            balance: The starting balance. Defaults to 0.0.
            interest_rate: The interest rate applied by
                apply_interest(), as a decimal between 0.0 and 1.0.
                Defaults to 0.05 (5%).

        Raises:
            ValueError: If interest_rate is not between 0.0 and 1.0.
        """
        if not isinstance(interest_rate, (int, float)) or isinstance(interest_rate, bool):
            raise ValueError(f"interest_rate must be a number, got {interest_rate!r}")
        if not (0.0 <= interest_rate <= 1.0):
            raise ValueError(f"interest_rate must be between 0.0 and 1.0, got {interest_rate!r}")
        self._interest_rate = float(interest_rate)
        super().__init__(name=name, account_type="savings", balance=balance)

    @property
    def interest_rate(self) -> float:
        """float: The interest rate applied by apply_interest (read-only)."""
        return self._interest_rate

    def apply_interest(self) -> float:
        """Calculate and deposit interest based on the current balance.

        Returns:
            The interest amount that was deposited, rounded to two
            decimal places.
        """
        interest_amount = round(self.balance * self.interest_rate, 2)
        self.deposit(interest_amount)
        return interest_amount

    def to_dict(self) -> dict:
        """Serialize this savings account to a plain dictionary.

        Returns:
            A dictionary including all Account fields (with "class"
            correctly set to "SavingsAccount" by the base
            implementation) plus "interest_rate".
        """
        data = super().to_dict()
        data["interest_rate"] = self.interest_rate
        return data

    @classmethod
    def from_dict(cls, data: dict) -> "SavingsAccount":
        """Construct a SavingsAccount from a dictionary.

        Args:
            data: A dictionary with keys "name", "balance", and
                "interest_rate".

        Returns:
            A new SavingsAccount instance built from the dictionary.
        """
        return cls(
            name=data["name"],
            balance=float(data.get("balance", 0.0)),
            interest_rate=float(data.get("interest_rate", 0.05)),
        )

    def get_summary(self) -> str:
        """Return a formatted multi-line summary including interest details.

        Returns:
            The base Account summary with interest rate and projected
            monthly gain lines appended.
        """
        base_summary = super().get_summary()
        projected_monthly_gain = round(self.balance * self.interest_rate, 2)
        return (
            f"{base_summary}\n"
            f"  Interest Rate:          {self.interest_rate:.2%}\n"
            f"  Projected Monthly Gain: {Account.format_balance(projected_monthly_gain)}"
        )

    def __str__(self) -> str:
        """Return a human-readable string representation of this account."""
        return f"{self.name} (savings): {Account.format_balance(self.balance)} | Rate: {self.interest_rate:.2%}"

    def __repr__(self) -> str:
        """Return an unambiguous developer-facing representation of this account."""
        return (
            f"SavingsAccount(name={self.name!r}, balance={self.balance!r}, "
            f"interest_rate={self.interest_rate!r})"
        )