"""Unit tests for the Account class."""

import unittest

from dashboard.account import Account
from dashboard.exceptions import ValidationError, AccountError


class TestAccount(unittest.TestCase):
    """Tests for dashboard.account.Account."""

    def test_initial_balance(self) -> None:
        """A new Account stores the balance it was constructed with."""
        account = Account("Checking", "checking", 500.0)
        self.assertEqual(account.balance, 500.0)

    def test_deposit_happy_path(self) -> None:
        """Depositing a positive amount increases the balance."""
        account = Account("Checking", "checking", 500.0)
        account.deposit(100.0)
        self.assertEqual(account.balance, 600.0)

    def test_withdraw_happy_path(self) -> None:
        """Withdrawing a valid amount decreases the balance."""
        account = Account("Checking", "checking", 500.0)
        account.withdraw(200.0)
        self.assertEqual(account.balance, 300.0)

    def test_withdraw_exact_balance(self) -> None:
        """Withdrawing exactly the full balance succeeds and leaves 0.0."""
        account = Account("Checking", "checking", 500.0)
        account.withdraw(500.0)
        self.assertEqual(account.balance, 0.0)

    def test_withdraw_overdraft_raises_account_error(self) -> None:
        """Withdrawing more than the balance raises AccountError."""
        account = Account("Checking", "checking", 100.0)
        with self.assertRaises(AccountError):
            account.withdraw(200.0)

    def test_deposit_non_positive_raises_validation_error(self) -> None:
        """Depositing a non-positive amount raises ValidationError."""
        account = Account("Checking", "checking", 100.0)
        with self.assertRaises(ValidationError):
            account.deposit(-50.0)

    def test_get_summary_returns_string(self) -> None:
        """get_summary() returns a string, not None or a printed side effect."""
        account = Account("Checking", "checking", 500.0)
        summary = account.get_summary()
        self.assertIsInstance(summary, str)
        self.assertIn("Checking", summary)

    def test_to_dict_from_dict_round_trip(self) -> None:
        """to_dict() followed by from_dict() reconstructs an equivalent Account."""
        original = Account("Checking", "checking", 500.0)
        data = original.to_dict()
        reconstructed = Account.from_dict(data)
        self.assertEqual(reconstructed.name, original.name)
        self.assertEqual(reconstructed.account_type, original.account_type)
        self.assertEqual(reconstructed.balance, original.balance)


if __name__ == "__main__":
    unittest.main()