"""Unit tests for the Category class."""

import unittest

from dashboard.category import Category
from dashboard.exceptions import ValidationError


class TestCategory(unittest.TestCase):
    """Tests for dashboard.category.Category."""

    def test_name_and_type_stored_correctly(self) -> None:
        """name is normalized (stripped, title-cased) and category_type is stored as given."""
        c = Category("  groceries  ", "expense")
        self.assertEqual(c.name, "Groceries")
        self.assertEqual(c.category_type, "expense")

    def test_invalid_type_raises_validation_error(self) -> None:
        """An invalid category_type raises ValidationError, not ValueError.

        This changed in Lesson 19 when Category first became reachable
        from the CLI and needed to be catchable by run()'s
        `except DashboardError` handling.
        """
        with self.assertRaises(ValidationError):
            Category("Misc", "not_a_real_type")

    def test_equality_between_identical_categories(self) -> None:
        """Two Category instances with the same normalized name and type are equal."""
        c1 = Category("Groceries", "expense")
        c2 = Category("groceries", "expense")
        self.assertEqual(c1, c2)

    def test_inequality_between_different_categories(self) -> None:
        """Categories with different names or types are not equal."""
        c1 = Category("Groceries", "expense")
        c2 = Category("Salary", "income")
        self.assertNotEqual(c1, c2)

    def test_hashability_via_set_insertion(self) -> None:
        """Category instances can be inserted into a set (frozen dataclass is hashable)."""
        c1 = Category("Groceries", "expense")
        c2 = Category("groceries", "expense")  # equal to c1
        category_set = {c1, c2}
        self.assertEqual(len(category_set), 1)


if __name__ == "__main__":
    unittest.main()