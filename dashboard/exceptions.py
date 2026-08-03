"""Exception hierarchy for the Personal Finance Dashboard.

This is the complete and final exception hierarchy for the project.
All custom exceptions raised anywhere in the dashboard package
inherit from DashboardError, so callers can catch broadly with
DashboardError or narrowly with a specific subclass.

Hierarchy:
    DashboardError
        ValidationError  - invalid user or file data
        AccountError     - account-level business rule violations
        FileLoadError     - a data file could not be read or parsed
        FileSaveError     - a data file could not be written
"""


class DashboardError(Exception):
    """Base class for all Personal Finance Dashboard application errors."""


class ValidationError(DashboardError):
    """Raised when user-supplied or file-loaded data fails validation."""


class AccountError(DashboardError):
    """Raised for account-level business rule violations, such as
    insufficient funds on withdrawal or an invalid account type."""


class FileLoadError(DashboardError):
    """Raised when a data file cannot be read or parsed."""


class FileSaveError(DashboardError):
    """Raised when a data file cannot be written."""