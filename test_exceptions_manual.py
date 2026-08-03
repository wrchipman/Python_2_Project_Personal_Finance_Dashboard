"""Manual verification script for the dashboard exception hierarchy.

Run this from the project root: python test_exceptions_manual.py
"""

from dashboard import (
    DashboardError,
    ValidationError,
    AccountError,
    FileLoadError,
    FileSaveError,
)


def check_raise_and_catch(exception_class, label: str) -> None:
    """Raise the given exception class and confirm it can be caught
    both as itself and as DashboardError.

    Args:
        exception_class: The exception class to test.
        label: A human-readable label for the test output.
    """
    try:
        raise exception_class(f"test error for {label}")
    except exception_class as e:
        print(f"[OK] Caught {label} as {exception_class.__name__}: {e}")

    try:
        raise exception_class(f"test error for {label}")
    except DashboardError as e:
        print(f"[OK] Caught {label} as DashboardError (base class): {e}")


def main() -> None:
    """Run all exception hierarchy verification checks."""
    check_raise_and_catch(ValidationError, "ValidationError")
    check_raise_and_catch(AccountError, "AccountError")
    check_raise_and_catch(FileLoadError, "FileLoadError")
    check_raise_and_catch(FileSaveError, "FileSaveError")

    # Confirm DashboardError itself can be raised and caught directly.
    try:
        raise DashboardError("base error")
    except DashboardError as e:
        print(f"[OK] Caught DashboardError directly: {e}")

    # Confirm a plain Exception does NOT get caught by DashboardError.
    try:
        try:
            raise ValueError("unrelated error")
        except DashboardError:
            print("[FAIL] ValueError should not be caught by DashboardError")
    except ValueError:
        print("[OK] Plain ValueError correctly NOT caught by DashboardError")


if __name__ == "__main__":
    main()