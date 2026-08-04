"""Personal Finance Dashboard package.

Public interface for the dashboard application. Classes are added to
this module's exports lesson by lesson as they are built:
    - Account -> Lesson 9
    - Transaction -> Lesson 11
    - CreditAccount, SavingsAccount -> Lesson 12
    - BaseAccount, Category -> Lesson 13
    - Dashboard -> Lesson 14 (this lesson)
    - validators -> Lesson 19
"""

from dashboard.exceptions import (
    DashboardError,
    ValidationError,
    AccountError,
    FileLoadError,
    FileSaveError,
)
from dashboard.base_account import BaseAccount
# Account is the base class for all account types. CreditAccount and
# SavingsAccount are specialized subclasses, each defined in its own
# file (credit_account.py, savings_account.py), that inherit from it.
from dashboard.account import Account
from dashboard.credit_account import CreditAccount
from dashboard.savings_account import SavingsAccount
from dashboard.transaction import Transaction
from dashboard.category import Category
from dashboard.dashboard import Dashboard

__all__ = [
    "DashboardError",
    "ValidationError",
    "AccountError",
    "FileLoadError",
    "FileSaveError",
    "BaseAccount",
    "Account",
    "CreditAccount",
    "SavingsAccount",
    "Transaction",
    "Category",
    "Dashboard",
]