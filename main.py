# ---------------------------------------------------------------------------
# IMPORT MAP
#
# main.py
#   -> full import: dashboard (absolute import of the package)
#
# dashboard/__init__.py
#   -> selective import: from dashboard.exceptions import DashboardError,
#      ValidationError, AccountError, FileLoadError, FileSaveError
#   -> selective import: from dashboard.account import Account
#
# dashboard/exceptions.py
#   -> no imports (Exception is a builtin)
#
# dashboard/account.py
#   -> no imports yet
#
# dashboard/transaction.py, dashboard/category.py, dashboard/dashboard.py
#   -> currently empty; populated starting Lesson 11
#
# utils.py, transaction_utils.py, dashboard_functions.py
#   -> standalone practice files at project root, not part of the
#      dashboard package, never imported by it
# ---------------------------------------------------------------------------

"""Entry point for the Personal Finance Dashboard application."""

from dashboard import Account


def main() -> None:
    """Run the Personal Finance Dashboard application."""
    print("Personal Finance Dashboard — starting up...")

    # --- Lesson 9 smoke test: create one Account of each type ---
    checking = Account("Everyday Checking", "checking", 1500.00)
    savings = Account("Emergency Fund", "savings", 8000.00)
    credit = Account("Rewards Card", "credit", 0.00)

    for account in (checking, savings, credit):
        print(account.get_summary())
        print()


if __name__ == "__main__":
    main()