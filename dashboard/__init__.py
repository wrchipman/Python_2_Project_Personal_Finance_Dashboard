"""Personal Finance Dashboard package.

Public interface for the dashboard application. Classes are added to
this module's exports lesson by lesson as they are built:
    - Account -> Lesson 9
    - Transaction -> Lesson 11
    - CreditAccount, SavingsAccount -> Lesson 12 (this lesson)
    - BaseAccount -> Lesson 13
    - Category -> Lesson 13
    - Dashboard -> Lesson 14
    - validators -> Lesson 19
"""

from dashboard.exceptions import (
    DashboardError,
    ValidationError,
    AccountError,
    FileLoadError,
    FileSaveError,
)
# Account is the base class for all account types. CreditAccount and
# SavingsAccount are specialized subclasses, each defined in its own
# file (credit_account.py, savings_account.py), that inherit from it.
from dashboard.account import Account
from dashboard.credit_account import CreditAccount
from dashboard.savings_account import SavingsAccount
from dashboard.transaction import Transaction

__all__ = [
    "DashboardError",
    "ValidationError",
    "AccountError",
    "FileLoadError",
    "FileSaveError",
    "Account",
    "CreditAccount",
    "SavingsAccount",
    "Transaction",
]