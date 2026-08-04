"""Entry point for the Personal Finance Dashboard application."""

from dashboard import Dashboard


def main() -> None:
    """Run the Personal Finance Dashboard application."""
    dashboard = Dashboard()
    dashboard.run()


if __name__ == "__main__":
    main()