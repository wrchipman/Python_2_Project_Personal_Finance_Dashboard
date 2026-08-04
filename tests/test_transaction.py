"""Unit tests for the Transaction class."""

import unittest

from dashboard.transaction import Transaction


class TestTransaction(unittest.TestCase):
    """Tests for dashboard.transaction.Transaction."""

    def test_amount_stored_correctly(self) -> None:
        """The amount passed to the constructor is stored unchanged."""
        t = Transaction(42.50, "2026-01-03", "Groceries", "Checking")
        self.assertEqual(t.amount, 42.50)

    def test_date_stored_as_string(self) -> None:
        """The date is stored as a validated '%Y-%m-%d' string, not a date object.

        Transaction.date has been a string since Lesson 10/11 and is
        never converted to a datetime.date instance — validation
        happens at construction time, but the stored representation
        stays a string throughout the class's lifetime.
        """
        t = Transaction(42.50, "2026-01-03", "Groceries", "Checking")
        self.assertIsInstance(t.date, str)
        self.assertEqual(t.date, "2026-01-03")

    def test_to_dict_contains_all_required_keys(self) -> None:
        """to_dict() returns a dictionary with all five expected keys."""
        t = Transaction(42.50, "2026-01-03", "Groceries", "Checking", "Snacks")
        data = t.to_dict()
        expected_keys = {"amount", "date", "category", "account_name", "description"}
        self.assertEqual(set(data.keys()), expected_keys)

    def test_from_dict_round_trip(self) -> None:
        """to_dict() followed by from_dict() reconstructs an equal Transaction."""
        original = Transaction(42.50, "2026-01-03", "Groceries", "Checking", "Snacks")
        reconstructed = Transaction.from_dict(original.to_dict())
        self.assertEqual(reconstructed, original)

    def test_zero_amount_raises_value_error(self) -> None:
        """Direct construction with a zero amount raises ValueError."""
        with self.assertRaises(ValueError):
            Transaction(0.0, "2026-01-03", "Groceries", "Checking")

    def test_negative_amount_raises_value_error(self) -> None:
        """Direct construction with a negative amount raises ValueError."""
        with self.assertRaises(ValueError):
            Transaction(-10.0, "2026-01-03", "Groceries", "Checking")

    def test_invalid_date_string_raises_value_error(self) -> None:
        """Direct construction with a malformed date string raises ValueError."""
        with self.assertRaises(ValueError):
            Transaction(42.50, "03-01-2026", "Groceries", "Checking")


if __name__ == "__main__":
    unittest.main()