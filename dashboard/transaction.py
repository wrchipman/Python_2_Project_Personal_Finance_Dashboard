"""Transaction domain class for the Personal Finance Dashboard.

This is the initial scaffold version. It gains full encapsulation
with read-only properties in Lesson 11 — including the account_name
field established here, which must NOT be dropped in that pass.
"""


class Transaction:
    """Represents a single financial transaction.

    A transaction records a monetary movement — an amount, the date
    it occurred, a category, the account it belongs to, and an
    optional description.
    """

    def __init__(
        self,
        amount: float,
        date: str,
        category: str,
        account_name: str,
        description: str = "",
    ) -> None:
        """Initialize a new Transaction.

        Args:
            amount: The transaction amount. Must be a positive
                number.
            date: The transaction date as a string.
            category: The transaction's category (e.g., "Groceries").
            account_name: The name of the Account this transaction
                belongs to.
            description: An optional free-text description. Defaults
                to an empty string.

        Raises:
            ValueError: If amount is not a positive int or float.
        """
        if not Transaction.is_valid_amount(amount):
            raise ValueError(f"amount must be a positive number, got {amount!r}")
        self.amount = amount
        self.date = date
        self.category = category
        self.account_name = account_name
        self.description = description

    def to_dict(self) -> dict:
        """Serialize this transaction to a plain dictionary.

        Returns:
            A dictionary with keys "amount", "date", "category",
            "account_name", "description".
        """
        return {
            "amount": self.amount,
            "date": self.date,
            "category": self.category,
            "account_name": self.account_name,
            "description": self.description,
        }

    def get_summary(self) -> dict:
        """Return a dictionary summary of this transaction.

        Returns:
            A dictionary with all transaction fields plus a
            "formatted_amount" key.
        """
        summary = self.to_dict()
        summary["formatted_amount"] = Transaction.format_amount(self.amount)
        return summary

    @classmethod
    def from_dict(cls, data: dict) -> "Transaction":
        """Construct a Transaction from a dictionary.

        Args:
            data: A dictionary with keys "amount", "date", "category",
                "account_name", and optionally "description".

        Returns:
            A new Transaction instance built from the dictionary.
        """
        return cls(
            amount=float(data["amount"]),
            date=data["date"],
            category=data["category"],
            account_name=data["account_name"],
            description=data.get("description", ""),
        )

    @staticmethod
    def is_valid_amount(amount: object) -> bool:
        """Check whether a value is a valid transaction amount.

        Args:
            amount: The value to check.

        Returns:
            True if amount is a float or int greater than zero,
            False otherwise.
        """
        if isinstance(amount, bool):
            return False
        return isinstance(amount, (int, float)) and amount > 0

    @staticmethod
    def format_amount(amount: float) -> str:
        """Format a numeric amount as a currency string.

        Args:
            amount: The numeric value to format.

        Returns:
            A string formatted as "$1,234.56".
        """
        return f"${amount:,.2f}"


if __name__ == "__main__":
    t = Transaction(150.00, "2026-04-20", "Groceries", "Everyday Checking", "Weekly shop")
    print(t.to_dict())
    round_tripped = Transaction.from_dict(t.to_dict())
    print(round_tripped.to_dict())
    assert round_tripped.to_dict() == t.to_dict()
    print("Round trip OK")