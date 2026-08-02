"""General-purpose utility functions for the Personal Finance Dashboard.

This module holds formatting, logging, validation, filtering, and
decorator helpers that are not tied to any single domain class.
Functions here are pure where possible and are safe to import from
any other module in the project.

Note: the validators and formatters in this module (make_range_validator,
make_string_validator, and the six named validators; make_currency_formatter
and the three named currency formatters) are practice implementations
of the factory/closure pattern. The Dashboard's actual production
validators live in dashboard/validators.py starting in Lesson 19 and
use a different contract (they raise ValidationError rather than
returning a tuple).
"""

import time
from functools import wraps
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


# ---------------------------------------------------------------------------
# Decorator library
# ---------------------------------------------------------------------------

call_log: list[str] = []


def log_to_list(func: Callable) -> Callable:
    """Decorator that appends a call record to the module-level call_log.

    Args:
        func: The function being decorated.

    Returns:
        A wrapped version of func that logs its name and arguments to
        call_log before executing, then returns func's normal result.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        call_log.append(f"{func.__name__} called with args={args}, kwargs={kwargs}")
        return func(*args, **kwargs)

    return wrapper


def timed(func: Callable) -> Callable:
    """Decorator that prints how long the wrapped function took to run.

    Args:
        func: The function being decorated.

    Returns:
        A wrapped version of func that prints its elapsed execution
        time in seconds, then returns func's normal result.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"{func.__name__} took {elapsed:.6f}s")
        return result

    return wrapper


def require_positive(func: Callable) -> Callable:
    """Decorator that requires the first positional argument to be positive.

    Args:
        func: The function being decorated. Its first positional
            argument (after self, if any) is treated as an amount
            that must be greater than zero.

    Returns:
        A wrapped version of func that raises ValueError if the
        checked argument is not a positive number, otherwise calls
        func normally.

    Raises:
        ValueError: If the checked argument is not a positive number.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        amount = args[0] if args else kwargs.get("amount")
        if not isinstance(amount, (int, float)) or isinstance(amount, bool) or amount <= 0:
            raise ValueError(f"{func.__name__} requires a positive amount, got {amount!r}")
        return func(*args, **kwargs)

    return wrapper


def retry(max_attempts: int) -> Callable:
    """Decorator factory that retries a function on exception.

    Args:
        max_attempts: The maximum number of times to attempt the call
            before letting the final exception propagate.

    Returns:
        A decorator that wraps a function to retry it up to
        max_attempts times if it raises an exception.
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as exc:
                    last_exception = exc
                    print(f"{func.__name__} attempt {attempt} failed: {exc}")
            raise last_exception

        return wrapper

    return decorator


def rate_limit(max_per_session: int) -> Callable:
    """Decorator factory that limits how many times a function may be called.

    Args:
        max_per_session: The maximum number of calls allowed during
            the current program run.

    Returns:
        A decorator that wraps a function to raise RuntimeError once
        it has been called more than max_per_session times.

    Raises:
        RuntimeError: If the wrapped function is called more than
            max_per_session times.
    """
    def decorator(func: Callable) -> Callable:
        list_counter = [0]

        @wraps(func)
        def wrapper(*args, **kwargs):
            list_counter[0] += 1
            if list_counter[0] > max_per_session:
                raise RuntimeError(
                    f"{func.__name__} exceeded rate limit of "
                    f"{max_per_session} calls per session"
                )
            return func(*args, **kwargs)

        return wrapper

    return decorator


def main() -> None:
    """Run all utils.py demonstration calls (audited __main__ guard)."""
    print(format_currency(1250.5))
    log_event("deposit", "Checking", amount=250.00)

    print(validate_amount(500.00))
    print(format_usd(1250.5))

    sample_transactions = [
        {"category": "Groceries", "amount": 42.50, "date": "2026-01-03"},
        {"category": "Rent", "amount": 1200.00, "date": "2026-01-01"},
    ]
    for t in sample_transactions:
        row = (
            format_category_col(t["category"])
            + format_amount_col(format_usd(t["amount"]))
            + format_date_col(t["date"])
        )
        print(row)


if __name__ == "__main__":
    main()