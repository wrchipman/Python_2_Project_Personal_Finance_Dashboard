"""Dashboard controller class for the Personal Finance Dashboard.

Dashboard owns the in-memory collections of accounts, transactions,
and categories, and provides the collection-style and context-manager
dunder interface the CLI loop will use starting in Lesson 15.

load() and save() are placeholders at this stage — they hold no file
I/O yet. Lesson 15 adds exception-handling patterns around a simple
version of persistence, and Lesson 18 replaces that with the real
CSV/JSON read/write implementation backed by dashboard/persistence.py.
"""

from dashboard.transaction import Transaction


class Dashboard:
    """Owns and coordinates the accounts, transactions, and categories
    that make up a Personal Finance Dashboard session.
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
        """Load data from disk into the in-memory collections.

        This is currently a placeholder. It performs no file I/O.
        The real implementation is added in Lesson 18, backed by
        dashboard/persistence.py.
        """
        pass

    def save(self) -> None:
        """Save the in-memory collections to disk.

        This is currently a placeholder. It performs no file I/O.
        The real implementation is added in Lesson 18, backed by
        dashboard/persistence.py.
        """
        pass

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