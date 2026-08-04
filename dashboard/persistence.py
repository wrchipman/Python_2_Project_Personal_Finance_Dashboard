"""Real CSV/JSON persistence layer for the Personal Finance Dashboard.

Replaces the temporary plain-text scaffold from Lessons 15-16. Same
function names and exception contract as before (FileNotFoundError ->
empty list, other read failures -> FileLoadError, write failures ->
FileSaveError), now backed by json.dump/json.load for accounts and
categories and csv.DictReader/DictWriter for transactions.

Account reconstruction dispatches on the "class" key each account
dict carries (Account.to_dict(), Lesson 13) so CreditAccount and
SavingsAccount reload with their subclass-specific fields intact.
"""

import csv
import json
import os

from dashboard.exceptions import FileLoadError, FileSaveError
from dashboard.account import Account
from dashboard.credit_account import CreditAccount
from dashboard.savings_account import SavingsAccount
from dashboard.transaction import Transaction
from dashboard.category import Category
from dashboard.logging_config import get_logger

logger = get_logger(__name__)

_ACCOUNT_CLASS_MAP = {
    "Account": Account,
    "CreditAccount": CreditAccount,
    "SavingsAccount": SavingsAccount,
}

TRANSACTION_FIELDS = ["amount", "date", "category", "account_name", "description"]


def _account_from_dict(data: dict):
    """Reconstruct the correct Account subclass based on its "class" key.

    Args:
        data: A dictionary produced by one of Account/CreditAccount/
            SavingsAccount.to_dict(), including a "class" key.

    Returns:
        A new instance of the class named by data["class"]. Falls
        back to plain Account if "class" is missing or unrecognized.
    """
    account_class = _ACCOUNT_CLASS_MAP.get(data.get("class"), Account)
    return account_class.from_dict(data)


def load_accounts(filepath: str) -> list:
    """Load accounts from a JSON file, dispatching on each record's class.

    Args:
        filepath: Path to the accounts JSON file.

    Returns:
        A list of Account/CreditAccount/SavingsAccount instances, or
        an empty list if the file does not exist.

    Raises:
        FileLoadError: If the file exists but cannot be read/parsed,
            or if a record cannot be reconstructed.
    """
    logger.debug(f"Attempting to load accounts from {filepath}")
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            raw_data = json.load(f)
    except FileNotFoundError:
        logger.warning(f"Accounts file {filepath} not found; returning empty list")
        return []
    except (OSError, json.JSONDecodeError) as exc:
        logger.error(f"Failed to read accounts from {filepath}: {exc}")
        raise FileLoadError(f"Could not read accounts from {filepath}") from exc
    else:
        try:
            accounts = [_account_from_dict(record) for record in raw_data]
        except (ValueError, KeyError, TypeError) as exc:
            logger.error(f"Accounts file {filepath} is corrupted: {exc}")
            raise FileLoadError(f"Accounts file {filepath} is corrupted") from exc
        logger.info(f"Loaded {len(accounts)} accounts from {filepath}")
        return accounts


def save_accounts(accounts: list, filepath: str) -> None:
    """Save accounts to a JSON file.

    Args:
        accounts: A list of Account (or subclass) instances to save.
        filepath: Path to write to.

    Raises:
        FileSaveError: If the file cannot be written.
    """
    logger.debug(f"Attempting to save {len(accounts)} accounts to {filepath}")
    try:
        os.makedirs(os.path.dirname(filepath) or ".", exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump([account.to_dict() for account in accounts], f, indent=2)
    except OSError as exc:
        logger.error(f"Failed to save accounts to {filepath}: {exc}")
        raise FileSaveError(f"Could not save accounts to {filepath}") from exc
    logger.info(f"Saved {len(accounts)} accounts to {filepath}")


def load_categories(filepath: str) -> list:
    """Load categories from a JSON file.

    Args:
        filepath: Path to the categories JSON file.

    Returns:
        A list of Category instances, or an empty list if the file
        does not exist.

    Raises:
        FileLoadError: If the file exists but cannot be read/parsed,
            or if a record cannot be reconstructed.
    """
    logger.debug(f"Attempting to load categories from {filepath}")
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            raw_data = json.load(f)
    except FileNotFoundError:
        logger.warning(f"Categories file {filepath} not found; returning empty list")
        return []
    except (OSError, json.JSONDecodeError) as exc:
        logger.error(f"Failed to read categories from {filepath}: {exc}")
        raise FileLoadError(f"Could not read categories from {filepath}") from exc
    else:
        try:
            categories = [Category.from_dict(record) for record in raw_data]
        except (ValueError, KeyError, TypeError) as exc:
            logger.error(f"Categories file {filepath} is corrupted: {exc}")
            raise FileLoadError(f"Categories file {filepath} is corrupted") from exc
        logger.info(f"Loaded {len(categories)} categories from {filepath}")
        return categories


def save_categories(categories: list, filepath: str) -> None:
    """Save categories to a JSON file.

    Args:
        categories: A list of Category instances to save.
        filepath: Path to write to.

    Raises:
        FileSaveError: If the file cannot be written.
    """
    logger.debug(f"Attempting to save {len(categories)} categories to {filepath}")
    try:
        os.makedirs(os.path.dirname(filepath) or ".", exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump([category.to_dict() for category in categories], f, indent=2)
    except OSError as exc:
        logger.error(f"Failed to save categories to {filepath}: {exc}")
        raise FileSaveError(f"Could not save categories to {filepath}") from exc
    logger.info(f"Saved {len(categories)} categories to {filepath}")


def load_transactions(filepath: str) -> list:
    """Load transactions from a CSV file.

    Args:
        filepath: Path to the transactions CSV file.

    Returns:
        A list of Transaction instances, or an empty list if the
        file does not exist.

    Raises:
        FileLoadError: If the file exists but cannot be read, or if
            a row cannot be reconstructed into a Transaction.
    """
    logger.debug(f"Attempting to load transactions from {filepath}")
    try:
        with open(filepath, "r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
    except FileNotFoundError:
        logger.warning(f"Transactions file {filepath} not found; returning empty list")
        return []
    except OSError as exc:
        logger.error(f"Failed to read transactions from {filepath}: {exc}")
        raise FileLoadError(f"Could not read transactions from {filepath}") from exc
    else:
        try:
            transactions = [Transaction.from_dict(row) for row in rows]
        except (ValueError, KeyError, TypeError) as exc:
            logger.error(f"Transactions file {filepath} is corrupted: {exc}")
            raise FileLoadError(f"Transactions file {filepath} is corrupted") from exc
        logger.info(f"Loaded {len(transactions)} transactions from {filepath}")
        return transactions


def save_transactions(transactions: list, filepath: str) -> None:
    """Save transactions to a CSV file.

    Args:
        transactions: A list of Transaction instances to save.
        filepath: Path to write to.

    Raises:
        FileSaveError: If the file cannot be written.
    """
    logger.debug(f"Attempting to save {len(transactions)} transactions to {filepath}")
    try:
        os.makedirs(os.path.dirname(filepath) or ".", exist_ok=True)
        with open(filepath, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=TRANSACTION_FIELDS)
            writer.writeheader()
            for t in transactions:
                writer.writerow(t.to_dict())
    except OSError as exc:
        logger.error(f"Failed to save transactions to {filepath}: {exc}")
        raise FileSaveError(f"Could not save transactions to {filepath}") from exc
    logger.info(f"Saved {len(transactions)} transactions to {filepath}")