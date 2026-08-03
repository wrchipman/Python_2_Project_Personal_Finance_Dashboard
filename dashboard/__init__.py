"""Personal Finance Dashboard package.

Public interface for the dashboard application. Classes are added to
this module's exports lesson by lesson as they are built:
    - Account, CreditAccount, SavingsAccount, BaseAccount -> Lessons 9-13
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

__all__ = [
    "DashboardError",
    "ValidationError",
    "AccountError",
    "FileLoadError",
    "FileSaveError",
]