"""Standalone decorator-stacking practice file.

These four stub functions exist only to practice applying decorator
stacks from utils.py. They are NOT wired into the real application.
The real, permanent homes for this logic are:
    - add_transaction   -> Account.deposit() / Account.withdraw() (Lesson 9)
    - load_transactions  -> dashboard/persistence.py (Lesson 18)
    - save_transactions  -> dashboard/persistence.py (Lesson 18)
    - apply_interest     -> SavingsAccount.apply_interest() (Lesson 12)
This file is never imported by main.py or the dashboard package.
"""

from utils import log_to_list, timed, require_positive, retry, rate_limit, call_log


@log_to_list
@timed
@require_positive
def add_transaction(amount: float, category: str) -> str:
    """Stub: simulate adding a transaction.

    Args:
        amount: The transaction amount. Must be positive.
        category: The transaction category.

    Returns:
        A confirmation string describing the simulated transaction.
    """
    return f"Added {category} transaction of {amount}"


@log_to_list
@timed
def load_transactions(filepath: str) -> list:
    """Stub: simulate loading transactions from a file.

    Args:
        filepath: The path to load from.

    Returns:
        An empty list. This is a stub — real loading is implemented
        in dashboard/persistence.py in Lesson 18.
    """
    print(f"(stub) loading from {filepath}")
    return []


@log_to_list
@timed
@retry(max_attempts=3)
def save_transactions(transactions: list, filepath: str) -> bool:
    """Stub: simulate saving transactions to a file.

    Args:
        transactions: The list of transactions to save.
        filepath: The path to save to.

    Returns:
        True on simulated success.
    """
    print(f"(stub) saving {len(transactions)} transactions to {filepath}")
    return True


@log_to_list
@timed
@require_positive
def apply_interest(balance: float, rate: float = 0.02) -> float:
    """Stub: simulate applying interest to a balance.

    Args:
        balance: The current balance. Must be positive.
        rate: The interest rate to apply. Defaults to 0.02.

    Returns:
        The interest amount calculated.
    """
    return round(balance * rate, 2)


@rate_limit(max_per_session=3)
def export_report(report_name: str) -> str:
    """Stub: simulate exporting a report, limited to 3 calls per session.

    Args:
        report_name: The name of the report being exported.

    Returns:
        A confirmation string describing the simulated export.
    """
    return f"Exported report: {report_name}"


if __name__ == "__main__":
    print(add_transaction(150.00, "Groceries"))
    print(load_transactions("data/transactions.csv"))
    print(save_transactions([{"amount": 150.00}], "data/transactions.csv"))
    print(apply_interest(1000.00))

    print("--- call_log contents ---")
    for entry in call_log:
        print(entry)

    print("--- require_positive on negative amount ---")
    try:
        add_transaction(-50.00, "Groceries")
    except ValueError as e:
        print(f"Caught expected error: {e}")

    print("--- rate_limit test ---")
    for i in range(1, 5):
        try:
            print(export_report(f"report_{i}"))
        except RuntimeError as e:
            print(f"Call {i} failed: {e}")