"""Personal Finance Dashboard package.

Public interface for the dashboard application. Classes are added to
this module's exports lesson by lesson as they are built:
    - Account -> Lesson 9 (this lesson)
    - CreditAccount, SavingsAccount, BaseAccount -> Lessons 12-13
    - Transaction -> Lesson 11
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
from dashboard.account import Account

__all__ = [
    "DashboardError",
    "ValidationError",
    "AccountError",
    "FileLoadError",
    "FileSaveError",
    "Account",
]