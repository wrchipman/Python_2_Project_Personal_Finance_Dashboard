# ---------------------------------------------------------------------------
# IMPORT MAP
#
# main.py
#   -> (no imports yet; models/ files are currently empty stubs)
#
# utils.py
#   -> full import: time
#   -> selective import: from functools import wraps
#   -> selective import: from typing import Callable
#
# transaction_utils.py
#   -> selective import: from functools import reduce
#   -> selective import: from typing import Callable
#
# dashboard_functions.py
#   -> selective import: from utils import log_to_list, timed,
#      require_positive, retry, rate_limit, call_log
#
# models/account.py, models/transaction.py, models/category.py,
# models/dashboard.py
#   -> currently empty; no imports yet. These files become
#      dashboard/account.py, dashboard/transaction.py,
#      dashboard/category.py, dashboard/dashboard.py after the
#      package refactor in Lesson 7.
# ---------------------------------------------------------------------------

"""Entry point for the Personal Finance Dashboard application."""


def main() -> None:
    """Run the Personal Finance Dashboard application."""
    print("Personal Finance Dashboard — starting up...")


if __name__ == "__main__":
    main()