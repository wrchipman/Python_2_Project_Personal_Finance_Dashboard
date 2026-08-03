# ---------------------------------------------------------------------------
# IMPORT MAP
#
# main.py
#   -> full import: dashboard (absolute import of the package)
#
# dashboard/__init__.py
#   -> selective import: from dashboard.exceptions import DashboardError,
#      ValidationError, AccountError, FileLoadError, FileSaveError
#
# dashboard/exceptions.py
#   -> no imports (Exception is a builtin)
#
# dashboard/account.py, dashboard/transaction.py, dashboard/category.py,
# dashboard/dashboard.py
#   -> currently empty; populated starting Lesson 9
#
# utils.py, transaction_utils.py, dashboard_functions.py
#   -> standalone practice files at project root, not part of the
#      dashboard package, never imported by it
# ---------------------------------------------------------------------------

"""Entry point for the Personal Finance Dashboard application."""

import dashboard


def main() -> None:
    """Run the Personal Finance Dashboard application."""
    print("Personal Finance Dashboard — starting up...")


if __name__ == "__main__":
    main()