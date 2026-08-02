"""Higher order function utilities for working with transaction data.

Functions in this module operate on the transaction dictionary shape:
    {
        "category": str,
        "amount": float,
        "type": "Income" | "Expense",
        "description": str,
        "date": str,
    }
This is the same shape the Transaction class will formalize starting
in Lesson 10.
"""

from functools import reduce
from typing import Callable


def make_category_filter(category: str) -> Callable[[dict], bool]:
    """Create a predicate function that matches a transaction category.

    Args:
        category: The category name to match against, case-insensitive.

    Returns:
        A function that accepts a transaction dictionary and returns
        True if its "category" matches, case-insensitively.
    """
    target = category.strip().lower()

    def predicate(transaction: dict) -> bool:
        return transaction.get("category", "").strip().lower() == target

    return predicate


def total_amounts(transactions: list[dict]) -> float:
    """Sum the amount of all Income transactions.

    Args:
        transactions: A list of transaction dictionaries.

    Returns:
        The sum of "amount" for every transaction where "type" is
        "Income". Returns 0.0 if there are no Income transactions.
    """
    income_only = filter(lambda t: t.get("type") == "Income", transactions)
    return reduce(lambda total, t: total + t["amount"], income_only, 0.0)


def normalize_descriptions(transactions: list[dict]) -> list[dict]:
    """Return a new list with each transaction's description cleaned up.

    Args:
        transactions: A list of transaction dictionaries.

    Returns:
        A new list of new dictionaries where "description" has been
        stripped of surrounding whitespace and title-cased. The
        original list and its dictionaries are not modified.
    """
    def clean(transaction: dict) -> dict:
        updated = dict(transaction)
        updated["description"] = updated.get("description", "").strip().title()
        return updated

    return list(map(clean, transactions))


def make_threshold_alert(limit: float) -> Callable[[dict], str | None]:
    """Create a function that flags transactions exceeding a limit.

    Args:
        limit: The amount threshold that triggers an alert.

    Returns:
        A function that accepts a transaction dictionary and returns
        an alert string if transaction["amount"] exceeds limit, or
        None otherwise.
    """
    def check(transaction: dict) -> str | None:
        if transaction["amount"] > limit:
            return (
                f"ALERT: {transaction.get('category', 'Unknown')} "
                f"transaction of {transaction['amount']} exceeds "
                f"threshold of {limit}"
            )
        return None

    return check


def make_formatter(symbol: str, decimal_places: int) -> Callable[[float], str]:
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


def main() -> None:
    """Run all transaction_utils.py demonstration calls (audited __main__ guard)."""
    sample_transactions = [
        {"category": "Salary", "amount": 3000.00, "type": "Income", "description": "  monthly salary  ", "date": "2026-01-01"},
        {"category": "Groceries", "amount": 85.40, "type": "Expense", "description": "weekly groceries", "date": "2026-01-03"},
        {"category": "Freelance", "amount": 450.00, "type": "Income", "description": "  side project payment", "date": "2026-01-05"},
        {"category": "Rent", "amount": 1200.00, "type": "Expense", "description": "monthly rent", "date": "2026-01-01"},
        {"category": "groceries", "amount": 32.10, "type": "Expense", "description": "snacks and drinks  ", "date": "2026-01-08"},
        {"category": "Utilities", "amount": 95.00, "type": "Expense", "description": "electric bill", "date": "2026-01-10"},
    ]

    grocery_filter = make_category_filter("Groceries")
    print([t for t in sample_transactions if grocery_filter(t)])

    print(total_amounts(sample_transactions))

    normalized = normalize_descriptions(sample_transactions)
    print(normalized[0]["description"])
    print(sample_transactions[0]["description"])

    alert_500 = make_threshold_alert(500)
    alert_1000 = make_threshold_alert(1000)
    print(alert_500(sample_transactions[0]))
    print(alert_500(sample_transactions[1]))
    print(alert_1000(sample_transactions[3]))

    format_usd = make_formatter("$", 2)
    format_jpy = make_formatter("¥", 0)
    print(format_usd(1250.5))
    print(format_jpy(1250.5))


if __name__ == "__main__":
    main()