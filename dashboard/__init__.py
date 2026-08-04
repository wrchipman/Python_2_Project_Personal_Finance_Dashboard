"""Personal Finance Dashboard package.

Public interface for the dashboard application. Classes are added to
this module's exports lesson by lesson as they are built:
    - Account -> Lesson 9
    - Transaction -> Lesson 11
    - CreditAccount, SavingsAccount -> Lesson 12
    - BaseAccount, Category -> Lesson 13
    - Dashboard -> Lesson 14
    - validators -> Lesson 19 (this lesson)
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
from dashboard.base_account import BaseAccount
from dashboard.transaction import Transaction
from dashboard.category import Category
from dashboard.dashboard import Dashboard
from dashboard.validators import (
    validate_amount,
    validate_date,
    validate_account_type,
    validate_category_name,
)

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
    "validate_amount",
    "validate_date",
    "validate_account_type",
    "validate_category_name",
]