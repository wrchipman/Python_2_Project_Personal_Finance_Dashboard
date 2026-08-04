"""Dashboard controller class for the Personal Finance Dashboard.

Dashboard now has a real (if temporary) persistence layer via
dashboard/persistence.py, plus the interactive CLI entry point,
run(), with full exception handling around load/save and each menu
action. The pipe-delimited persistence.py backing this is replaced
wholesale in Lesson 18 with real CSV/JSON handling.
"""

from datetime import datetime

from dashboard.transaction import Transaction
from dashboard.account import Account
from dashboard.credit_account import CreditAccount
from dashboard.savings_account import SavingsAccount
from dashboard.exceptions import DashboardError, FileLoadError, FileSaveError, AccountError
from dashboard.persistence import (
    load_accounts,
    save_accounts,
    load_categories,
    save_categories,
    load_transactions,
    save_transactions,
)

ACCOUNTS_FILE = "data/accounts.txt"
CATEGORIES_FILE = "data/categories.txt"
TRANSACTIONS_FILE = "data/transactions.txt"


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

    def add_category(self, category) -> None:
        """Add a category to the dashboard's in-memory collection.

        Args:
            category: A Category instance to add.
        """
        self._categories.append(category)

    def load(self) -> None:
        """Load all three collections from their pipe-delimited text files.

        Raises:
            FileLoadError: If any file exists but cannot be read or
                is corrupted.
        """
        self._accounts = load_accounts(ACCOUNTS_FILE)
        self._categories = load_categories(CATEGORIES_FILE)
        self._transactions = load_transactions(TRANSACTIONS_FILE)

    def save(self) -> None:
        """Save all three collections to their pipe-delimited text files.

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
        """Interactively prompt for and create a new account."""
        name = input("Account name: ").strip()
        account_type = input("Account type (checking/savings/credit): ").strip().lower()
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

        Note: this method is hardened further in Lesson 19, which
        replaces the retry-loop helpers used here with the dedicated
        validate_amount()/validate_date() functions from
        dashboard/validators.py.
        """
        account_name = input("Account name: ").strip()
        self._find_account(account_name)  # raises AccountError if not found
        amount = self._get_valid_amount("Transaction amount: ")
        date_obj = self._get_valid_date("Date (YYYY-MM-DD): ")
        category = input("Category: ").strip()
        description = input("Description (optional): ").strip()

        transaction = Transaction(
            amount=amount,
            date=date_obj.strftime(Transaction.DATE_FORMAT),
            category=category,
            account_name=account_name,
            description=description,
        )
        self.add_transaction(transaction)
        print(f"Added: {transaction}")

    def _display_summary(self) -> None:
        """Print a summary of all accounts and recent transactions."""
        print(self)
        print("--- Accounts ---")
        for account in self._accounts:
            print(f"  {account}")
        print("--- Transactions ---")
        for transaction in self._transactions:
            print(f"  {transaction}")

    def run(self) -> None:
        """Run the interactive CLI menu loop.

        Loads existing data on startup (warning, not crashing, on
        failure), loops through menu actions catching DashboardError
        around each one, and saves on exit (warning, not crashing,
        on failure).
        """
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
            print("5. View Summary")
            print("6. Exit")
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
                    self._display_summary()
                elif choice == "6":
                    break
                else:
                    print("Invalid option, please try again.")
            except DashboardError as e:
                print(f"Error: {e}")

        try:
            self.save()
        except FileSaveError as e:
            print(f"Warning: could not save data ({e}). Changes may be lost.")

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