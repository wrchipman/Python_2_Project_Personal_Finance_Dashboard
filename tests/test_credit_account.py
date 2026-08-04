"""Unit tests for CreditAccount's overridden balance property (Lesson 12)."""

import unittest

from dashboard.credit_account import CreditAccount
from dashboard.exceptions import AccountError


class TestCreditAccount(unittest.TestCase):
    """Tests for dashboard.credit_account.CreditAccount."""

    def test_charge_within_credit_limit_goes_negative(self) -> None:
        """A charge that pushes the balance negative but within credit_limit succeeds."""
        account = CreditAccount("Rewards Card", balance=0.0, credit_limit=500.0)
        account.withdraw(200.0)
        self.assertEqual(account.balance, -200.0)

    def test_charge_exceeding_credit_limit_raises_account_error(self) -> None:
        """A charge that would exceed credit_limit raises AccountError and leaves balance unchanged."""
        account = CreditAccount("Rewards Card", balance=0.0, credit_limit=500.0)
        with self.assertRaises(AccountError):
            account.withdraw(600.0)
        self.assertEqual(account.balance, 0.0)

    def test_available_credit_reflects_negative_balance(self) -> None:
        """available_credit correctly reflects a negative balance."""
        account = CreditAccount("Rewards Card", balance=0.0, credit_limit=500.0)
        account.withdraw(150.0)
        self.assertEqual(account.available_credit, 350.0)


if __name__ == "__main__":
    unittest.main()