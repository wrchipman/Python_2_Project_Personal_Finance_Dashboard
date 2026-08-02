"""General-purpose utility functions for the Personal Finance Dashboard.

This module holds formatting, logging, and filtering helpers that are
not tied to any single domain class. Functions here are pure where
possible and are safe to import from any other module in the project.
"""


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


if __name__ == "__main__":
    print(format_currency(1250.5))
    print(format_currency(42.1, symbol="€"))

    log_event("deposit", "Checking", amount=250.00)
    log_event("startup")

    sample_records = [
        {"category": "Groceries", "amount": 42.50},
        {"category": "Rent", "amount": 1200.00},
        {"category": "Groceries", "amount": 18.75},
        {"category": "Utilities", "amount": 85.00},
    ]
    print(filter_by_field(sample_records, "category", "Groceries"))
    print(filter_by_field(sample_records, "category", None))