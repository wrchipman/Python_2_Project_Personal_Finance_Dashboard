"""Boundary validation functions for the Personal Finance Dashboard.

These functions validate untrusted string data at the points where it
enters the application — CLI input and file loading. All four share
the same contract: raise ValidationError on bad input, return clean,
type-coerced data on success.

These are distinct from the internal _validate_type/_validate_amount/
_validate_date helpers inside Account and Transaction, which remain
in place as a defensive backstop against direct, non-CLI misuse and
still raise plain ValueError.
"""

from datetime import date, datetime

from dashboard.exceptions import ValidationError
from dashboard.account import Account


def validate_amount(raw: str) -> float:
    """Validate and coerce a raw amount string.

    Args:
        raw: The raw amount string to validate.

    Returns:
        The clean, positive float amount.

    Raises:
        ValidationError: If raw cannot be converted to a float, is
            not positive, or exceeds 1,000,000.
    """
    stripped = raw.strip()
    try:
        amount = float(stripped)
    except ValueError as exc:
        raise ValidationError(f"amount must be a number, got {raw!r}") from exc

    if amount <= 0:
        raise ValidationError(f"amount must be positive, got {amount}")
    if amount > 1_000_000:
        raise ValidationError(f"amount cannot exceed 1,000,000, got {amount}")
    return amount


def validate_date(raw: str) -> date:
    """Validate and parse a raw date string.

    Args:
        raw: The raw date string, expected in "%Y-%m-%d" format.

    Returns:
        The clean date object.

    Raises:
        ValidationError: If raw cannot be parsed as a "%Y-%m-%d"
            date, or if the parsed date is in the future.
    """
    stripped = raw.strip()
    try:
        parsed = datetime.strptime(stripped, "%Y-%m-%d")
    except ValueError as exc:
        raise ValidationError(f"date must match format %Y-%m-%d, got {raw!r}") from exc

    parsed_date = parsed.date()
    if parsed_date > date.today():
        raise ValidationError(f"date cannot be in the future, got {parsed_date}")
    return parsed_date


def validate_account_type(raw: str) -> str:
    """Validate and normalize a raw account type string.

    Args:
        raw: The raw account type string.

    Returns:
        The normalized (stripped, lowercased) account type string.

    Raises:
        ValidationError: If the normalized string is not one of
            Account.VALID_TYPES.
    """
    normalized = raw.strip().lower()
    if normalized not in Account.VALID_TYPES:
        raise ValidationError(
            f"account_type must be one of {sorted(Account.VALID_TYPES)}, got {raw!r}"
        )
    return normalized


def validate_category_name(raw: str) -> str:
    """Validate and clean a raw category name string.

    Args:
        raw: The raw category name string.

    Returns:
        The stripped category name string.

    Raises:
        ValidationError: If the stripped name is empty or exceeds 50
            characters.
    """
    stripped = raw.strip()
    if not stripped:
        raise ValidationError("category name cannot be empty")
    if len(stripped) > 50:
        raise ValidationError(f"category name cannot exceed 50 characters, got {len(stripped)}")
    return stripped