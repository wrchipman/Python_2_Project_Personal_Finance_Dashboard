"""Temporary plain-text persistence scaffold.

This module intentionally avoids csv/json — those aren't taught until
Lesson 18. It uses plain open()/read()/write() and a pipe-delimited
line format, giving the exception-handling patterns from Lesson 15
real files to wrap. Now also logs each operation.

This entire module is REPLACED (not extended) in Lesson 18 with a
real CSV/JSON implementation backed by csv.DictReader/DictWriter and
json.dump/json.load. Nothing in this file survives past Lesson 18.
"""

from dashboard.exceptions import FileLoadError, FileSaveError
from dashboard.account import Account
from dashboard.transaction import Transaction
from dashboard.category import Category
from dashboard.logging_config import get_logger

logger = get_logger(__name__)


def load_accounts(filepath: str) -> list:
    """Load accounts from a pipe-delimited text file.

    Args:
        filepath: Path to the accounts file.

    Returns:
        A list of Account instances, or an empty list if the file
        does not exist.

    Raises:
        FileLoadError: If the file exists but cannot be read, or if
            its contents are malformed.
    """
    logger.debug(f"Attempting to load accounts from {filepath}")
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except FileNotFoundError:
        logger.warning(f"Accounts file {filepath} not found; returning empty list")
        return []
    except OSError as exc:
        logger.error(f"Failed to read accounts from {filepath}: {exc}")
        raise FileLoadError(f"Could not read accounts from {filepath}") from exc
    else:
        accounts = []
        try:
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                name, account_type, balance = line.split("|")
                accounts.append(Account(name, account_type, float(balance)))
        except (ValueError, IndexError) as exc:
            logger.error(f"Accounts file {filepath} is corrupted: {exc}")
            raise FileLoadError(f"Accounts file {filepath} is corrupted") from exc
        logger.info(f"Loaded {len(accounts)} accounts from {filepath}")
        return accounts


def save_accounts(accounts: list, filepath: str) -> None:
    """Save accounts to a pipe-delimited text file.

    Args:
        accounts: A list of Account instances to save.
        filepath: Path to write to.

    Raises:
        FileSaveError: If the file cannot be written.
    """
    logger.debug(f"Attempting to save {len(accounts)} accounts to {filepath}")
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            for account in accounts:
                f.write(f"{account.name}|{account.account_type}|{account.balance}\n")
    except OSError as exc:
        logger.error(f"Failed to save accounts to {filepath}: {exc}")
        raise FileSaveError(f"Could not save accounts to {filepath}") from exc
    logger.info(f"Saved {len(accounts)} accounts to {filepath}")


def load_categories(filepath: str) -> list:
    """Load categories from a pipe-delimited text file.

    Args:
        filepath: Path to the categories file.

    Returns:
        A list of Category instances, or an empty list if the file
        does not exist.

    Raises:
        FileLoadError: If the file exists but cannot be read, or if
            its contents are malformed.
    """
    logger.debug(f"Attempting to load categories from {filepath}")
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except FileNotFoundError:
        logger.warning(f"Categories file {filepath} not found; returning empty list")
        return []
    except OSError as exc:
        logger.error(f"Failed to read categories from {filepath}: {exc}")
        raise FileLoadError(f"Could not read categories from {filepath}") from exc
    else:
        categories = []
        try:
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                name, category_type = line.split("|")
                categories.append(Category(name, category_type))
        except (ValueError, IndexError) as exc:
            logger.error(f"Categories file {filepath} is corrupted: {exc}")
            raise FileLoadError(f"Categories file {filepath} is corrupted") from exc
        logger.info(f"Loaded {len(categories)} categories from {filepath}")
        return categories


def save_categories(categories: list, filepath: str) -> None:
    """Save categories to a pipe-delimited text file.

    Args:
        categories: A list of Category instances to save.
        filepath: Path to write to.

    Raises:
        FileSaveError: If the file cannot be written.
    """
    logger.debug(f"Attempting to save {len(categories)} categories to {filepath}")
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            for category in categories:
                f.write(f"{category.name}|{category.category_type}\n")
    except OSError as exc:
        logger.error(f"Failed to save categories to {filepath}: {exc}")
        raise FileSaveError(f"Could not save categories to {filepath}") from exc
    logger.info(f"Saved {len(categories)} categories to {filepath}")


def load_transactions(filepath: str) -> list:
    """Load transactions from a pipe-delimited text file.

    Args:
        filepath: Path to the transactions file.

    Returns:
        A list of Transaction instances, or an empty list if the
        file does not exist.

    Raises:
        FileLoadError: If the file exists but cannot be read, or if
            its contents are malformed.
    """
    logger.debug(f"Attempting to load transactions from {filepath}")
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except FileNotFoundError:
        logger.warning(f"Transactions file {filepath} not found; returning empty list")
        return []
    except OSError as exc:
        logger.error(f"Failed to read transactions from {filepath}: {exc}")
        raise FileLoadError(f"Could not read transactions from {filepath}") from exc
    else:
        transactions = []
        try:
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                amount, date, category, account_name, description = line.split("|")
                transactions.append(
                    Transaction(float(amount), date, category, account_name, description)
                )
        except (ValueError, IndexError) as exc:
            logger.error(f"Transactions file {filepath} is corrupted: {exc}")
            raise FileLoadError(f"Transactions file {filepath} is corrupted") from exc
        logger.info(f"Loaded {len(transactions)} transactions from {filepath}")
        return transactions


def save_transactions(transactions: list, filepath: str) -> None:
    """Save transactions to a pipe-delimited text file.

    Args:
        transactions: A list of Transaction instances to save.
        filepath: Path to write to.

    Raises:
        FileSaveError: If the file cannot be written.
    """
    logger.debug(f"Attempting to save {len(transactions)} transactions to {filepath}")
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            for t in transactions:
                f.write(
                    f"{t.amount}|{t.date}|{t.category}|{t.account_name}|{t.description}\n"
                )
    except OSError as exc:
        logger.error(f"Failed to save transactions to {filepath}: {exc}")
        raise FileSaveError(f"Could not save transactions to {filepath}") from exc
    logger.info(f"Saved {len(transactions)} transactions to {filepath}")