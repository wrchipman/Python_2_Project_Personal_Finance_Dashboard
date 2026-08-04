"""Unit tests for the Dashboard class, built via the red-green-refactor TDD cycle
for get_net_worth (Lesson 20).
"""

import unittest

from dashboard.dashboard import Dashboard
from dashboard.account import Account


class TestDashboard(unittest.TestCase):
    """Tests for dashboard.dashboard.Dashboard."""

    def setUp(self) -> None:
        """Create a Dashboard with two accounts of known balances."""
        self.dashboard = Dashboard()
        self.checking = Account("Checking", "checking", 500.0)
        self.savings = Account("Savings", "savings", 300.0)
        self.dashboard.add_account(self.checking)
        self.dashboard.add_account(self.savings)

    def test_get_net_worth_sums_all_balances(self) -> None:
        """get_net_worth() returns the sum of all account balances."""
        self.assertEqual(self.dashboard.get_net_worth(), 800.0)

    def test_get_net_worth_with_no_accounts(self) -> None:
        """get_net_worth() returns 0.0 for a Dashboard with no accounts."""
        empty_dashboard = Dashboard()
        self.assertEqual(empty_dashboard.get_net_worth(), 0.0)

    def test_get_net_worth_updates_after_deposit(self) -> None:
        """get_net_worth() reflects a deposit made after setUp."""
        self.checking.deposit(200.0)
        self.assertEqual(self.dashboard.get_net_worth(), 1000.0)


if __name__ == "__main__":
    unittest.main()