"""Category domain class for the Personal Finance Dashboard.

Category is implemented as a frozen (immutable, hashable) dataclass
rather than a BaseAccount subclass — it is a data-centric class, not
an account type, and does not participate in the account hierarchy.
"""

from dataclasses import dataclass, field, FrozenInstanceError
from typing import ClassVar


@dataclass(frozen=True)
class Category:
    """Represents a transaction category, such as "Groceries" or "Salary".

    Attributes:
        name: The category's display name, normalized to title case.
        category_type: Either "income" or "expense".

    Class Attributes:
        VALID_TYPES: The list of valid category_type values.
    """

    name: str
    category_type: str
    VALID_TYPES: ClassVar[list] = ["income", "expense"]

    def __post_init__(self) -> None:
        """Validate category_type and normalize name after initialization.

        Raises:
            ValueError: If category_type is not in VALID_TYPES.
        """
        if self.category_type not in Category.VALID_TYPES:
            raise ValueError(
                f"category_type must be one of {Category.VALID_TYPES}, "
                f"got {self.category_type!r}"
            )
        object.__setattr__(self, "name", self.name.strip().title())

    def to_dict(self) -> dict:
        """Serialize this category to a plain dictionary.

        Returns:
            A dictionary with keys "name" and "type".
        """
        return {"name": self.name, "type": self.category_type}

    @classmethod
    def from_dict(cls, data: dict) -> "Category":
        """Construct a Category from a dictionary.

        Args:
            data: A dictionary with keys "name" and "type".

        Returns:
            A new Category instance built from the dictionary.
        """
        return cls(name=data["name"], category_type=data["type"])

    def is_income(self) -> bool:
        """Check whether this category represents income.

        Returns:
            True if category_type is "income", False otherwise.
        """
        return self.category_type == "income"

    def is_expense(self) -> bool:
        """Check whether this category represents an expense.

        Returns:
            True if category_type is "expense", False otherwise.
        """
        return self.category_type == "expense"


if __name__ == "__main__":
    c1 = Category("groceries", "expense")
    c2 = Category("Groceries", "expense")
    print(c1 == c2)  # True — same normalized name and type

    try:
        c1.name = "Rent"
    except FrozenInstanceError as e:
        print(f"Caught expected error: {e}")

    category_totals = {c1: 0.0}
    category_totals[c1] += 42.50
    print(category_totals)