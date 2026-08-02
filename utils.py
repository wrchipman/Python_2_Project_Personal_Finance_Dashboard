"""General-purpose utility functions for the Personal Finance Dashboard.

This module holds formatting, logging, validation, and filtering
helpers that are not tied to any single domain class. Functions here
are pure where possible and are safe to import from any other module
in the project.

Note: the validators and formatters below (make_range_validator,
make_string_validator, and the six named validators; make_currency_formatter
and the three named currency formatters) are practice implementations
of the factory/closure pattern. The Dashboard's actual production
validators live in dashboard/validators.py starting in Lesson 19 and
use a different contract (they raise ValidationError rather than
returning a tuple).
"""

from typing import Callable


def format_currency(amount: float, symbol: str = "$") -> str:
    """Format a numeric amount as a currency string.

    Args:
        amount: The numeric value to format.
        symbol: The currency symbol to prepend. Defaults to "$".

    Returns:
        A string with the symbol prepended, thousands separators,
        and exactly two decimal places.

    Raises:
        TypeError: If amount is not a number.
    """
    if not isinstance(amount, (int, float)) or isinstance(amount, bool):
        raise TypeError(f"amount must be a number, got {type(amount).__name__}")
    return f"{symbol}{amount:,.2f}"


def log_event(event_type: str, *args: str, **kwargs: float) -> None:
    """Print a structured event log entry.

    Args:
        event_type: A short label describing the kind of event.
        *args: Any number of positional detail strings to include.
        **kwargs: Any number of named numeric values to include.

    Returns:
        None. This function only prints; it does not return a value.
    """
    arg_part = ", ".join(str(a) for a in args)
    kwarg_part = ", ".join(f"{key}={value}" for key, value in kwargs.items())

    pieces = [f"[{event_type}]"]
    if arg_part:
        pieces.append(arg_part)
    if kwarg_part:
        pieces.append(f"| {kwarg_part}")

    print(" ".join(pieces))


def filter_by_field(
    records: list[dict],
    field: str,
    value: str | float | None = None,
) -> list[dict]:
    """Filter a list of record dictionaries by a field's value.

    Args:
        records: A list of dictionaries to filter.
        field: The dictionary key to check on each record.
        value: The value the field must match. If None, all records
            are returned unfiltered.

    Returns:
        A new list containing only the records where record[field]
        equals value, or all records if value is None.
    """
    if value is None:
        return list(records)
    return [record for record in records if record.get(field) == value]


# ---------------------------------------------------------------------------
# Validation factory layer (practice pattern — see module docstring)
# ---------------------------------------------------------------------------


def make_range_validator(
    min_val: float,
    max_val: float,
    field_name: str,
) -> Callable[[object], tuple[bool, str]]:
    """Create a validator function that checks a numeric value falls in a range.

    Args:
        min_val: The minimum acceptable value, inclusive.
        max_val: The maximum acceptable value, inclusive.
        field_name: A human-readable name used in error messages.

    Returns:
        A function that accepts a single value and returns a
        (bool, str) tuple: (True, "") on success, or
        (False, error_message) on failure.
    """
    def validator(value: object) -> tuple[bool, str]:
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            return False, f"{field_name} must be a number, got {type(value).__name__}"
        if not (min_val <= value <= max_val):
            return False, f"{field_name} must be between {min_val} and {max_val}"
        return True, ""

    return validator


def make_string_validator(
    field_name: str,
    max_length: int,
) -> Callable[[object], tuple[bool, str]]:
    """Create a validator function that checks a value is a valid string.

    Args:
        field_name: A human-readable name used in error messages.
        max_length: The maximum allowed length after stripping.

    Returns:
        A function that accepts a single value and returns a
        (bool, str) tuple: (True, "") on success, or
        (False, error_message) on failure.
    """
    def validator(value: object) -> tuple[bool, str]:
        if not isinstance(value, str):
            return False, f"{field_name} must be a string, got {type(value).__name__}"
        stripped = value.strip()
        if not stripped:
            return False, f"{field_name} cannot be empty or whitespace-only"
        if len(stripped) > max_length:
            return False, f"{field_name} cannot exceed {max_length} characters"
        return True, ""

    return validator


validate_amount = make_range_validator(0.01, 1_000_000, "amount")
validate_year = make_range_validator(2000, 2100, "year")
validate_month = make_range_validator(1, 12, "month")
validate_day = make_range_validator(1, 31, "day")
validate_account_name = make_string_validator("account_name", 50)
validate_description = make_string_validator("description", 200)


# ---------------------------------------------------------------------------
# Formatting factory layer
# ---------------------------------------------------------------------------


def make_currency_formatter(symbol: str, decimal_places: int) -> Callable[[float], str]:
    """Create a currency formatting function with a fixed symbol and precision.

    Args:
        symbol: The currency symbol to prepend.
        decimal_places: The number of decimal places to display.

    Returns:
        A function that accepts a numeric amount and returns it
        formatted with the given symbol and decimal places.
    """
    def formatter(amount: float) -> str:
        return f"{symbol}{amount:,.{decimal_places}f}"

    return formatter


format_usd = make_currency_formatter("$", 2)
format_eur = make_currency_formatter("€", 2)
format_jpy = make_currency_formatter("¥", 0)


def make_column_formatter(width: int, align: str) -> Callable[[str], str]:
    """Create a function that pads or truncates a string to a fixed column width.

    Args:
        width: The target column width in characters.
        align: One of "left", "right", or "center".

    Returns:
        A function that accepts a string and returns it truncated to
        width if too long, or padded to width using the given
        alignment if too short.

    Raises:
        ValueError: If align is not one of "left", "right", "center".
    """
    if align not in ("left", "right", "center"):
        raise ValueError(f"align must be 'left', 'right', or 'center', got {align!r}")

    def formatter(text: str) -> str:
        text = str(text)
        if len(text) > width:
            return text[:width]
        if align == "left":
            return text.ljust(width)
        if align == "right":
            return text.rjust(width)
        return text.center(width)

    return formatter


format_category_col = make_column_formatter(20, "left")
format_amount_col = make_column_formatter(12, "right")
format_date_col = make_column_formatter(12, "left")


if __name__ == "__main__":
    print(format_currency(1250.5))
    print(format_currency(42.1, symbol="€"))

    log_event("deposit", "Checking", amount=250.00)
    log_event("startup")

    sample_records = [
        {"category": "Groceries", "amount": 42.50},
        {"category": "Rent", "amount": 1200.00},
    ]
    print(filter_by_field(sample_records, "category", "Groceries"))
    print(filter_by_field(sample_records, "category", None))

    # --- Validation factory tests ---
    print(validate_amount(500.00))
    print(validate_amount(-5))
    print(validate_amount(True))

    print(validate_year(2026))
    print(validate_year(1999))

    print(validate_month(6))
    print(validate_month(13))

    print(validate_day(15))
    print(validate_day(32))

    print(validate_account_name("Checking"))
    print(validate_account_name("   "))

    print(validate_description("Weekly groceries"))
    print(validate_description("x" * 250))

    # --- Formatting factory tests ---
    print(format_usd(1250.5))
    print(format_eur(1250.5))
    print(format_jpy(1250.5))

    sample_transactions = [
        {"category": "Groceries", "amount": 42.50, "date": "2026-01-03"},
        {"category": "Rent", "amount": 1200.00, "date": "2026-01-01"},
        {"category": "Utilities", "amount": 95.00, "date": "2026-01-10"},
    ]
    for t in sample_transactions:
        row = (
            format_category_col(t["category"])
            + format_amount_col(format_usd(t["amount"]))
            + format_date_col(t["date"])
        )
        print(row)