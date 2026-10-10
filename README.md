# Finance Manager

A lightweight CLI personal finance tracker written in Python. It logs income and expenses, tracks category budgets, generates summaries, and saves data locally to JSON.

## Features

- **Transaction Tracking**: Record income and expense entries with amounts, categories, dates, and optional notes.
- **Budgeting**: Set spending caps for individual categories and check budget status.
- **Reporting**: View overall cash balance, monthly summaries, and category expense breakdowns.
- **Local Persistence**: Automatically saves and loads state from `Finance_data.json`.
- **Search & Filtering**: Search transactions by category keyword and view numbered lists for easy deletion.

## Requirements

Python 3.8+ (standard library only; no external dependencies). Uses built-in `datetime` and `json` modules.

## Getting Started

Run the script from your terminal:

```bash
python finance_manager_commented.py
```

> **First step**: Add at least one category (Option 2) before recording transactions or setting budgets.

## Menu Options

1. Add Transaction
2. Add Category
3. Add Budget
4. View All Transactions
5. Delete Transaction
6. Find Transaction By Category
7. Budget Status Report
8. Financial Summary
9. Monthly Financial Summary
10. Category Expense Report
11. Exit

## Data Storage

Data is stored in `Finance_data.json` inside the working directory. Transaction dates are serialized as `YYYY-MM-DD` strings and parsed into Python `date` objects at runtime. If the file is missing or invalid on launch, the program initializes with empty records.

## Limitations

- Amounts are handled as floats rather than `decimal.Decimal`.
- Data is stored in unencrypted local JSON without automated backup.
- A few helper query methods (`filtering_date_wise_transactions`, `filtering_category_wise_transactions`, and `calculate_date_wise_expense_total`) are implemented on the class but not currently exposed in the CLI menu.

## Project Structure

- `finance_manager_commented.py`: Core logic and CLI interface.
- `README.md`: Quick-start overview and usage guide.
- `DOCUMENTATION.md`: Architecture details, data schema, and method breakdown.
