# Finance Manager Technical Documentation

## Overview

Finance Manager is an object-oriented CLI utility for tracking personal finances. It provides interactive menus to manage transactions, monitor category budgets, and calculate balances, persisting state between sessions using a local JSON file.

## Architecture & Data Model

The application revolves around the `FinanceManager` class, which manages in-memory state and handles serialization.

### State Attributes

- `self.transactions`: List of transaction records.
- `self.budgets`: Dictionary mapping category names to numeric budget caps (`{category: amount}`).
- `self.categories`: Set of valid category strings.

### Transaction Schema

Each transaction dictionary contains:

| Field | Type | Description |
| :--- | :--- | :--- |
| `Type` | `str` | Must be `"Income"` or `"Expense"` |
| `Amount` | `float` / `int` | Strictly positive number |
| `Category` | `str` | Name of an existing registered category |
| `Date` | `datetime.date` | In-memory `date` object (serialized to ISO string) |
| `Description` | `str` | Free-text note or memo |

### JSON Storage Format

State is persisted to `Finance_data.json` in the current working directory:

```json
{
  "transactions": [
    {
      "Type": "Expense",
      "Amount": 42.50,
      "Category": "Groceries",
      "Date": "2026-10-10",
      "Description": "Supermarket"
    }
  ],
  "budgets": {
    "Groceries": 500.0
  },
  "categories": [
    "Groceries",
    "Salary",
    "Utilities"
  ]
}
```

Categories are serialized as an array and loaded into a Python `set` for O(1) lookups.

## Class Methods & Functional Components

### 1. Transaction Operations
- `add_transaction(trans_type, amount, category, date, description)`: Validates inputs, creates the transaction, appends it to `self.transactions`, and commits to disk.
- `add_transaction_input()`: Interactive CLI prompt that gathers transaction fields and catches invalid numeric inputs.
- `view_all_transactions()`: Prints all logged transactions with 1-based index numbers.
- `delete_transaction(transaction_number)`: Deletes an entry by its 1-based index and saves changes.
- `find_transactions_by_category(category)`: Case-insensitive substring search across transaction categories.

### 2. Categories & Budgets
- `add_category(category)`: Strips whitespace, rejects duplicates or empty strings, adds to `self.categories`, and saves.
- `add_category_input()`: Interactive prompt for creating a new category.
- `add_budget(budget_category, budget_amount)`: Confirms the category exists, verifies the amount is positive, sets the limit in `self.budgets`, and saves.
- `add_budget_input()`: Interactive prompt for setting a budget limit.
- `budget_status_report(budget_category)`: Compares total expenses in a category against its assigned budget, printing total spend, remaining headroom, and over-budget warnings.

### 3. Reporting & Calculations
- `calculate_total_income()`: Returns the sum of all `"Income"` transactions.
- `calculate_total_expenses()`: Returns the sum of all `"Expense"` transactions.
- `calculate_balance()`: Computes net balance (`income - expenses`).
- `calculate_category_wise_expense_total(category)`: Sums expenses matching a specific category.
- `financial_summary()`: Prints overall income, expenses, and net balance.
- `monthly_financial_summary(year, month)`: Filters transactions for a given month and year, printing monthly income, expenses, and net cash flow.
- `category_expense_report()`: Prints total expenses for all categories with non-zero spending.

### 4. Standalone Query Helpers (Unlinked in Menu)
The class includes three helper methods implemented for direct querying that are not wired to the current interactive menu:
- `filtering_category_wise_transactions(category)`: Displays transactions strictly matching a specific category.
- `filtering_date_wise_transactions(year, month, day)`: Displays transactions matching an exact calendar date.
- `calculate_date_wise_expense_total(year, month, day)`: Sums total expenses incurred on a specific calendar date.

### 5. Date Validation
Custom date parsing and Gregorian validation utilities:
- `leapyear(year)`: Returns boolean indicating leap year status.
- `days_in_month(year, month)`: Returns maximum days in a given month (accounting for February leap days).
- `validate_date(year, month, day)`: Validates month (1–12) and day ranges before constructing date objects.

### 6. Persistence & Lifecycle
- `save_data()`: Converts `Date` objects to ISO strings (`YYYY-MM-DD`) and writes `transactions`, `budgets`, and `categories` to `Finance_data.json`.
- `load_state()`: Reads `Finance_data.json`, converts date strings back to `datetime.date`, and populates in-memory collections. If the file is missing or contains invalid JSON, initializes empty collections without crashing.
- `display_menu()` & `run()`: Core CLI event loop prompting the user until option 11 (Exit) is selected.

## Validation & Error Handling

- **User Input**: Terminal numeric prompts wrap conversions in `try...except ValueError` blocks to catch non-numeric entries gracefully.
- **Data Integrity**: Transactions require pre-registered categories and positive values. Categories reject empty strings and duplicates.
- **Corrupted State**: If `Finance_data.json` is missing or invalid JSON, `load_state()` falls back to empty defaults (`[]`, `{}`, `set()`).

## Future Considerations

- **Currency Precision**: Migrate amounts from floats to `decimal.Decimal` to avoid floating-point rounding artifacts.
- **Database Backend**: Replace single-file JSON persistence with SQLite for atomic transactions and concurrent read safety.
- **CLI Exposure**: Wire up date-wise queries and category filtering methods to the interactive menu.
- **Testing**: Add a `pytest` suite covering date validation edge cases and state persistence.
