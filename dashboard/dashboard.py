"""Dashboard controller class for the Personal Finance Dashboard.

get_net_worth() was added via the red-green-refactor TDD cycle in
Lesson 20. Its first green implementation duplicated
get_total_balance()'s generator-expression-and-sum() logic; the
refactor step consolidated it to delegate instead, since for this
Dashboard's account model the two calculations are identical (a
credit account's negative balance already represents a liability, so
summing all balances IS the net worth).
"""

from datetime import date, datetime

from dashboard.transaction import Transaction
from dashboard.account import Account
from dashboard.credit_account import CreditAccount
from dashboard.savings_account import SavingsAccount
from dashboard.category import Category
from dashboard.exceptions import DashboardError, FileLoadError, FileSaveError, AccountError
from dashboard.persistence import (
    load_accounts,
    save_accounts,
    load_categories,
    save_categories,
    load_transactions,
    save_transactions,
)
from dashboard.validators import (
    validate_amount,
    validate_date,
    validate_account_type,
    validate_category_name,
)
from dashboard.logging_config import get_logger

logger = get_logger(__name__)

ACCOUNTS_FILE = "data/accounts.json"
CATEGORIES_FILE = "data/categories.json"
TRANSACTIONS_FILE = "data/transactions.csv"


class Dashboard:
    """Owns and coordinates the accounts, transactions, and categories
    that make up a Personal Finance Dashboard session, and drives the
    interactive CLI loop.
    """

    def __init__(self) -> None:
        """Initialize a new Dashboard with empty in-memory collections."""
        self._accounts: list = []
        self._transactions: list = []
        self._categories: list = []

    def add_account(self, account) -> None:
        """Add an account to the dashboard's in-memory collection.

        Args:
            account: An Account (or subclass) instance to add.
        """
        self._accounts.append(account)

    def add_transaction(self, transaction: Transaction) -> None:
        """Add a transaction to the dashboard's in-memory collection.

        Args:
            transaction: A Transaction instance to add.
        """
        self._transactions.append(transaction)

    def add_category(self, category: Category) -> None:
        """Add a category to the dashboard's in-memory collection.

        Args:
            category: A Category instance to add.
        """
        self._categories.append(category)

    def load(self) -> None:
        """Load all three collections from their JSON/CSV files.

        Raises:
            FileLoadError: If any file exists but cannot be read or
                is corrupted.
        """
        self._accounts = load_accounts(ACCOUNTS_FILE)
        self._categories = load_categories(CATEGORIES_FILE)
        self._transactions = load_transactions(TRANSACTIONS_FILE)

    def save(self) -> None:
        """Save all three collections to their JSON/CSV files.

        Raises:
            FileSaveError: If any file cannot be written.
        """
        save_accounts(self._accounts, ACCOUNTS_FILE)
        save_categories(self._categories, CATEGORIES_FILE)
        save_transactions(self._transactions, TRANSACTIONS_FILE)

    def _find_account(self, name: str) -> Account:
        """Find an account by name.

        Args:
            name: The account name to search for.

        Returns:
            The matching Account instance.

        Raises:
            AccountError: If no account with that name exists.
        """
        for account in self._accounts:
            if account.name == name:
                return account
        raise AccountError(f"No account named {name!r} found.")

    def _get_valid_amount(self, prompt: str) -> float:
        """Prompt the user until they enter a valid positive amount.

        Used by _prompt_deposit()/_prompt_withdraw(), which don't
        touch file-loaded data — the simple retry-loop pattern from
        Lesson 15 is still the right fit there. Transaction entry
        uses validate_amount() instead (see _prompt_add_transaction).

        Args:
            prompt: The text to display when asking for input.

        Returns:
            A positive float parsed from user input.
        """
        while True:
            raw = input(prompt).strip()
            try:
                amount = float(raw)
            except ValueError:
                print("Please enter a valid number.")
                continue
            else:
                if amount <= 0:
                    print("Amount must be positive.")
                    continue
                return amount

    def _get_valid_date(self, prompt: str) -> datetime:
        """Prompt the user until they enter a valid YYYY-MM-DD date.

        Retained for potential future use with retry-style prompts.
        Not currently called — _prompt_add_transaction() uses
        validate_date() with single-shot validation instead.

        Args:
            prompt: The text to display when asking for input.

        Returns:
            A datetime object parsed from user input.
        """
        while True:
            raw = input(prompt).strip()
            try:
                parsed = datetime.strptime(raw, Transaction.DATE_FORMAT)
            except ValueError:
                print(f"Please enter a date in {Transaction.DATE_FORMAT} format.")
                continue
            else:
                return parsed

    def _prompt_add_account(self) -> None:
        """Interactively prompt for and create a new account.

        account_type is validated at the boundary with
        validate_account_type() before any Account subclass is
        constructed, so bad input surfaces as ValidationError here
        rather than reaching Account._validate_type()'s internal
        ValueError.
        """
        name = input("Account name: ").strip()
        raw_type = input("Account type (checking/savings/credit): ")
        account_type = validate_account_type(raw_type)
        has_balance = input("Start with a balance? (y/n): ").strip().lower() == "y"
        balance = self._get_valid_amount("Starting balance: ") if has_balance else 0.0

        if account_type == "credit":
            account = CreditAccount(name, balance)
        elif account_type == "savings":
            account = SavingsAccount(name, balance)
        else:
            account = Account(name, account_type, balance)

        self.add_account(account)
        print(f"Added: {account}")

    def _prompt_add_category(self) -> None:
        """Interactively prompt for and create a new category.

        name is validated at the boundary with validate_category_name().
        category_type is validated by Category.__post_init__ itself,
        which raises ValidationError (as of Lesson 19).
        """
        raw_name = input("Category name: ")
        name = validate_category_name(raw_name)
        category_type = input("Category type (income/expense): ").strip().lower()

        category = Category(name, category_type)
        self.add_category(category)
        print(f"Added: {category.name} ({category.category_type})")

    def _prompt_deposit(self) -> None:
        """Interactively prompt for and perform a deposit."""
        name = input("Account name: ").strip()
        account = self._find_account(name)
        amount = self._get_valid_amount("Deposit amount: ")
        account.deposit(amount)
        print(f"New balance: {Account.format_balance(account.balance)}")

    def _prompt_withdraw(self) -> None:
        """Interactively prompt for and perform a withdrawal."""
        name = input("Account name: ").strip()
        account = self._find_account(name)
        amount = self._get_valid_amount("Withdraw amount: ")
        account.withdraw(amount)
        print(f"New balance: {Account.format_balance(account.balance)}")

    def _prompt_add_transaction(self) -> None:
        """Interactively prompt for and record a new transaction.

        Uses the boundary validator pattern: one input() per field,
        one validator call per field, no retry loop. Any
        ValidationError/AccountError raised here propagates up to
        run()'s single except DashboardError block. An empty date
        input defaults to today's date without calling validate_date().
        """
        account_name = input("Account name: ").strip()
        self._find_account(account_name)  # raises AccountError if not found

        raw_amount = input("Transaction amount: ")
        amount = validate_amount(raw_amount)

        raw_date = input("Date (YYYY-MM-DD, press Enter for today): ")
        if raw_date.strip() == "":
            transaction_date = date.today()
        else:
            transaction_date = validate_date(raw_date)

        category = input("Category: ").strip()
        description = input("Description (optional): ").strip()

        transaction = Transaction(
            amount=amount,
            date=transaction_date.strftime(Transaction.DATE_FORMAT),
            category=category,
            account_name=account_name,
            description=description,
        )
        self.add_transaction(transaction)
        print(f"Added: {transaction}")

    def _display_summary(self) -> None:
        """Print a summary of all accounts and recent transactions.

        Uses explicit for loops rather than comprehensions: these are
        side effects (printing), and the decision cascade calls for
        an explicit loop whenever the result is a side effect rather
        than a reused value.
        """
        print(self)
        print("--- Accounts ---")
        for account in self._accounts:
            print(f"  {account}")
        print("--- Transactions ---")
        for transaction in self._transactions:
            print(f"  {transaction}")

    def get_total_balance(self) -> float:
        """Return the sum of all account balances.

        Uses a generator expression inside sum() since the result
        feeds a single aggregator and is not reused elsewhere.

        Returns:
            The sum of every account's balance as a float.
        """
        return sum(account.balance for account in self._accounts)

    def get_net_worth(self) -> float:
        """Return the dashboard's total net worth.

        Delegates to get_total_balance(). For this Dashboard's
        account model, a credit account's negative balance already
        represents a liability, so summing all account balances
        (assets and liabilities alike) IS the net worth calculation —
        there is no separate math to perform. This method exists
        under its own domain-facing name for callers that want to
        express "net worth" rather than "total balance," and was
        built independently via the Lesson 20 TDD cycle before this
        equivalence was noticed and the duplicate logic was
        refactored away.

        Returns:
            The sum of every account's balance as a float.
        """
        return self.get_total_balance()

    def get_account_names(self) -> list:
        """Return a list of every account's name.

        Uses a list comprehension since the result is reused for
        display purposes (e.g., populating a menu of account names).

        Returns:
            A list of account name strings.
        """
        return [account.name for account in self._accounts]

    def get_unique_categories(self) -> set:
        """Return the set of distinct transaction category names.

        Uses a set comprehension since duplicate category names must
        collapse to a single entry.

        Returns:
            A set of unique category name strings.
        """
        return {t.category for t in self._transactions}

    def _is_income_category(self, category_name: str) -> bool:
        """Determine whether a category name represents income.

        Normalizes category_name the same way Category.__post_init__
        does, then looks it up against self._categories. If no
        matching Category is found, defaults to treating it as an
        expense — the safer assumption for a budgeting tool, since
        undercounting income is less harmful than overcounting it.

        Args:
            category_name: The category name to classify.

        Returns:
            True if a matching Category with type "income" is found,
            False otherwise (including when no match is found).
        """
        normalized = category_name.strip().title()
        for cat in self._categories:
            if cat.name == normalized:
                return cat.is_income()
        return False

    def iter_monthly_summaries(self):
        """Yield one summary dictionary per calendar month present in transactions.

        Uses a set comprehension to derive the unique (year, month)
        pairs, and a generator expression inside sum() for the
        income/expense aggregation within each month.

        Yields:
            dict: Keys are "year", "month", "month_label" (formatted
            "YYYY-MM"), "income", "expenses", "net", and
            "transaction_count". Yielded in chronological order.
        """
        year_months = {
            (
                datetime.strptime(t.date, Transaction.DATE_FORMAT).year,
                datetime.strptime(t.date, Transaction.DATE_FORMAT).month,
            )
            for t in self._transactions
        }

        for year, month in sorted(year_months):
            month_transactions = [
                t
                for t in self._transactions
                if datetime.strptime(t.date, Transaction.DATE_FORMAT).year == year
                and datetime.strptime(t.date, Transaction.DATE_FORMAT).month == month
            ]

            income = sum(
                t.amount for t in month_transactions if self._is_income_category(t.category)
            )
            expenses = sum(
                t.amount for t in month_transactions if not self._is_income_category(t.category)
            )

            yield {
                "year": year,
                "month": month,
                "month_label": f"{year:04d}-{month:02d}",
                "income": income,
                "expenses": expenses,
                "net": income - expenses,
                "transaction_count": len(month_transactions),
            }

    def display_monthly_report(self) -> None:
        """Print a formatted table of monthly summaries via iter_monthly_summaries()."""
        print("--- Monthly Report ---")
        for summary in self.iter_monthly_summaries():
            print(
                f"{summary['month_label']} | "
                f"Income: {Account.format_balance(summary['income']):>12} | "
                f"Expenses: {Account.format_balance(summary['expenses']):>12} | "
                f"Net: {Account.format_balance(summary['net']):>12} | "
                f"Transactions: {summary['transaction_count']}"
            )

    def run(self) -> None:
        """Run the interactive CLI menu loop.

        Loads existing data on startup (warning, not crashing, on
        failure), loops through menu actions catching DashboardError
        around each one, and saves on exit (warning, not crashing,
        on failure). Logs session start and end.
        """
        logger.info("Dashboard session starting")
        try:
            self.load()
        except FileLoadError as e:
            print(f"Warning: could not load saved data ({e}). Starting with an empty dashboard.")

        while True:
            print()
            print(self)
            print("1. Add Account")
            print("2. Deposit")
            print("3. Withdraw")
            print("4. Add Transaction")
            print("5. Add Category")
            print("6. View Summary")
            print("7. Monthly Report")
            print("8. Exit")
            choice = input("Choose an option: ").strip()

            try:
                if choice == "1":
                    self._prompt_add_account()
                elif choice == "2":
                    self._prompt_deposit()
                elif choice == "3":
                    self._prompt_withdraw()
                elif choice == "4":
                    self._prompt_add_transaction()
                elif choice == "5":
                    self._prompt_add_category()
                elif choice == "6":
                    self._display_summary()
                elif choice == "7":
                    self.display_monthly_report()
                elif choice == "8":
                    break
                else:
                    print("Invalid option, please try again.")
            except DashboardError as e:
                print(f"Error: {e}")

        try:
            self.save()
        except FileSaveError as e:
            print(f"Warning: could not save data ({e}). Changes may be lost.")
        logger.info("Dashboard session ending")

    def __repr__(self) -> str:
        """Return an unambiguous developer-facing representation of this dashboard."""
        return (
            f"Dashboard(accounts={len(self._accounts)}, "
            f"transactions={len(self._transactions)}, "
            f"categories={len(self._categories)})"
        )

    def __str__(self) -> str:
        """Return a formatted header string suitable for report output."""
        return (
            f"Personal Finance Dashboard — "
            f"{len(self._accounts)} account(s), "
            f"{len(self._transactions)} transaction(s), "
            f"{len(self._categories)} categor(y/ies)"
        )

    def __len__(self) -> int:
        """Return the number of transactions currently loaded."""
        return len(self._transactions)

    def __contains__(self, transaction: Transaction) -> bool:
        """Check whether a transaction is present in this dashboard.

        Args:
            transaction: The Transaction to check for.

        Returns:
            True if an equal Transaction (per Transaction.__eq__) is
            present in self._transactions, False otherwise.
        """
        return transaction in self._transactions

    def __iter__(self):
        """Return an iterator over this dashboard's transactions."""
        return iter(self._transactions)

    def __enter__(self) -> "Dashboard":
        """Load data on entering a `with` block.

        Returns:
            self, with load() already called.
        """
        self.load()
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> bool:
        """Save data on clean exit; warn (without saving) on exception exit.

        Args:
            exc_type: The exception class raised inside the with
                block, or None if no exception occurred.
            exc_value: The exception instance, or None.
            traceback: The exception traceback, or None.

        Returns:
            False in all cases, so any exception raised inside the
            with block continues to propagate normally.
        """
        if exc_type is None:
            self.save()
        else:
            print(f"WARNING: Dashboard session ended with an exception ({exc_type.__name__}): {exc_value}")
        return False