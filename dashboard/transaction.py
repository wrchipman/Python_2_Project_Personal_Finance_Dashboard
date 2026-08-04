"""Transaction domain class for the Personal Finance Dashboard.

from_dict() now pre-validates amount/date with the boundary
validators from dashboard/validators.py and re-raises failures as
FileLoadError, since from_dict() is the path used when reconstructing
Transactions from a (potentially corrupted) loaded file. Direct
construction via Transaction(...) is unaffected — it still goes
through _validate_amount/_validate_date, which still raise ValueError.
"""

from datetime import datetime
from functools import total_ordering

from dashboard.exceptions import ValidationError, FileLoadError


@total_ordering
class Transaction:
    """Represents a single financial transaction.

    A transaction records a monetary movement — an amount, the date
    it occurred, a category, the account it belongs to, and an
    optional description. All fields are read-only after creation.

    Class Attributes:
        DATE_FORMAT: The expected string format for the date field.
    """

    DATE_FORMAT = "%Y-%m-%d"

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
            date: The transaction date as a "%Y-%m-%d" string.
            category: The transaction's category (e.g., "Groceries").
            account_name: The name of the Account this transaction
                belongs to.
            description: An optional free-text description. Defaults
                to an empty string.

        Raises:
            ValueError: If amount is not a positive int or float, or
                if date does not match DATE_FORMAT.
        """
        self._validate_amount(amount)
        self._validate_date(date)
        self._amount = amount
        self._date = date
        self._category = category
        self._account_name = account_name
        self._description = description

    def _validate_amount(self, amount: object) -> None:
        """Raise ValueError if amount is not a positive number.

        Args:
            amount: The value to validate.

        Raises:
            ValueError: If amount is not a positive int or float.
        """
        if not Transaction.is_valid_amount(amount):
            raise ValueError(f"amount must be a positive number, got {amount!r}")

    def _validate_date(self, date: str) -> None:
        """Raise ValueError if date does not match DATE_FORMAT.

        Args:
            date: The date string to validate.

        Raises:
            ValueError: If date cannot be parsed with DATE_FORMAT.
        """
        try:
            datetime.strptime(date, Transaction.DATE_FORMAT)
        except (ValueError, TypeError) as exc:
            raise ValueError(
                f"date must match format {Transaction.DATE_FORMAT}, got {date!r}"
            ) from exc

    @property
    def amount(self) -> float:
        """float: The transaction amount (read-only)."""
        return self._amount

    @property
    def date(self) -> str:
        """str: The transaction date as a "%Y-%m-%d" string (read-only)."""
        return self._date

    @property
    def category(self) -> str:
        """str: The transaction's category (read-only)."""
        return self._category

    @property
    def account_name(self) -> str:
        """str: The name of the Account this transaction belongs to (read-only)."""
        return self._account_name

    @property
    def description(self) -> str:
        """str: An optional free-text description (read-only)."""
        return self._description

    def to_dict(self) -> dict:
        """Serialize this transaction to a plain dictionary.

        Returns:
            A dictionary with keys "amount", "date", "category",
            "account_name", "description". date is already stored as
            a "%Y-%m-%d" string, so no additional formatting is
            needed here.
        """
        return {
            "amount": self.amount,
            "date": self.date,
            "category": self.category,
            "account_name": self.account_name,
            "description": self.description,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Transaction":
        """Construct a Transaction from a dictionary, validating at the boundary.

        This is the reconstruction path used when loading from a
        (potentially corrupted or tampered) file. amount and date are
        pre-validated with the boundary validators from
        dashboard/validators.py; a validation failure here means the
        stored data itself is bad, so it is surfaced as FileLoadError
        rather than the plain ValueError direct construction would
        raise.

        Args:
            data: A dictionary with keys "amount", "date", "category",
                "account_name", and optionally "description".

        Returns:
            A new Transaction instance built from the dictionary.

        Raises:
            FileLoadError: If amount or date fail boundary validation.
        """
        # Imported here (not at module level) to avoid a circular
        # import: validators.py imports from dashboard.account, and
        # transaction.py is imported before account.py finishes
        # loading in some import orders.
        from dashboard.validators import validate_amount, validate_date

        try:
            clean_amount = validate_amount(str(data["amount"]))
            clean_date = validate_date(data["date"])
        except ValidationError as exc:
            raise FileLoadError(f"Transaction record failed validation: {exc}") from exc

        return cls(
            amount=clean_amount,
            date=clean_date.strftime(Transaction.DATE_FORMAT),
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

    def __str__(self) -> str:
        """Return a human-readable string: date | category | $amount | (account)."""
        return (
            f"{self.date} | {self.category} | "
            f"{Transaction.format_amount(self.amount)} | ({self.account_name})"
        )

    def __repr__(self) -> str:
        """Return an unambiguous developer-facing representation of this transaction."""
        return (
            f"Transaction(amount={self.amount!r}, date={self.date!r}, "
            f"category={self.category!r}, account_name={self.account_name!r}, "
            f"description={self.description!r})"
        )

    def __eq__(self, other: object) -> bool:
        """Compare two transactions for equality by amount, date, category, account.

        Args:
            other: The object to compare against.

        Returns:
            True if other is a Transaction with the same amount, date,
            category, and account_name. Returns NotImplemented if
            other is not a Transaction.
        """
        if not isinstance(other, Transaction):
            return NotImplemented
        return (
            self.amount == other.amount
            and self.date == other.date
            and self.category == other.category
            and self.account_name == other.account_name
        )

    def __hash__(self) -> int:
        """Return a hash consistent with __eq__ (based on amount, date, category, account_name)."""
        return hash((self.amount, self.date, self.category, self.account_name))

    def __lt__(self, other: object) -> bool:
        """Compare two transactions by date, for use with sorted()/total_ordering.

        Args:
            other: The object to compare against.

        Returns:
            True if this transaction's date is earlier than other's.
            Returns NotImplemented if other is not a Transaction.
        """
        if not isinstance(other, Transaction):
            return NotImplemented
        return self.date < other.date