from datetime import date, datetime 
import json 

class FinanceManager:
    
    def __init__(self):
        self.transactions = []
        self.budgets = {}
        self.categories = set()

    def add_transaction(
        self, transaction_type, 
        amount, 
        category, 
        year,
        month,
        day, 
        description=""):
        category = category.strip(" ")
        if transaction_type not in ["Income", "Expense"]:
            print("Error! Transaction type must be either Income or Expense.")
            return

        if category not in self.categories:
            print("Category Does not Exist")
            return

        if amount <= 0:
            print("Error! Amount must be more than 0.")
            return

        if not self.validate_date(year, month, day):
            print("Error: Invalid date.")
            return

        transaction_date = date(year, month, day)

        transaction_fields = {
            "Type": transaction_type,
            "Amount": amount,
            "Category": category,
            "Date": transaction_date,
            "Description": description
        }

        self.transactions.append(transaction_fields)
        self.save_data()
        print(f"Success: Added {transaction_type} of ₹{amount} under '{category}'.")

    def add_category(self,category):
        category = category.strip(" ")
        if category == "":
            print("Please Enter a category in it.")
            return

        if category in self.categories:
            print("Category Already Exists!, Please Enter a New One.")
            return

        else:
            self.categories.add(category)
            self.save_data()
            print("Category Added Successfully.")
            return
    
    def add_budget(self, budget_category,budget_amount):
        
        if budget_category not in self.categories:
            print("category does not exist")
            return
        
        if budget_amount <= 0:
            print(" Amount Should be more than 0!.")
            return 
        
        self.budgets[budget_category] = budget_amount
        self.save_data()
        

    def validate_date(self,year, month, day):
        if not 1 <= month <= 12:
            return False
        max_days = self.days_in_month(year, month)
        return 1 <= day <= max_days

    
    def leapyear(self,year):
        return year % 400 == 0 or (
            year % 4 == 0 and year % 100 != 0)

    def days_in_month(self, year, month):
            if month in [1,3,5,7,8,10,12]:
                return 31
            elif month in [4,6,9,11]:
                return 30
            elif month == 2:
                if self.leapyear(year):
                    return 29
                else:
                    return 28
            else:
                return 0
                
    def calculate_total_income(self):
        total_income = 0
        for transaction in self.transactions:
            if transaction["Type"] == "Income":
                total_income += transaction["Amount"]
        return total_income
        
    def calculate_total_expenses(self):
        total_expenses = 0
        for expense_transaction in self.transactions:
            if expense_transaction["Type"] == "Expense":
                total_expenses += expense_transaction["Amount"]
        return total_expenses

    def budget_status_report(self, budget_category):
        if budget_category not in self.budgets:
            print(f"No budget found for {budget_category}")
            return

        budget_amount = self.budgets[budget_category]   

        expense_total = self.calculate_category_wise_expense_total(budget_category)

        remaining_budget = budget_amount - expense_total
        
        print(f"Category: {budget_category}")
        print(f"Budget: ₹{budget_amount}")
        print(f"Spent: ₹{expense_total}")
        print(f"Remaining Budget: ₹{remaining_budget}")

        if remaining_budget > 0:
            print("Budget not exceeded")
        elif remaining_budget == 0:
            print("Budget is fully consumed")
        else:
            overspending = expense_total - budget_amount
            print(f"Budget Exceeded by {overspending}")
    
    def calculate_balance(self):
        balance = self.calculate_total_income() - self.calculate_total_expenses()
        return balance

    def filtering_category_wise_transactions(self, name_category):
        
        for category_transactions in self.transactions:
            if category_transactions["Category"] == name_category:
                print(f"Your Transaction of {name_category} are {category_transactions['Amount']}")
        return
    
    def calculate_category_wise_expense_total(self, category_total_name):
        category_total = 0

        for calculating_category_expense_total in self.transactions:
            if calculating_category_expense_total["Category"] == category_total_name and calculating_category_expense_total["Type"] == "Expense":
                    category_total += calculating_category_expense_total["Amount"]
        return category_total
    
    def filtering_date_wise_transactions(self, year,month, day):
        requested_date = date(year, month, day)
        found = False
        for transaction in self.transactions:
            if transaction["Date"] == requested_date:
                print(f"{transaction['Date']}\n{transaction['Type']} {transaction['Amount']} {transaction['Category']}")
                found = True
        if not found:
            print(f"No Transactions Found for {requested_date}")
        
    def calculate_date_wise_expense_total(self, year, month, day):

        requested_date = date(year, month, day)
        date_expense_total = 0
        found = False

        for transaction in self.transactions:
            if transaction["Date"] == requested_date and transaction["Type"] == "Expense":
                date_expense_total += transaction["Amount"]
                found = True    
                

        if not found:
            print(f"No Expenses Found for {requested_date}")
        print(date_expense_total)
        return
    
    def financial_summary(self):
        print("============ Financial Summary =======")

        print(f"Total Income: {self.calculate_total_income()}")
        print(f"Total Expenses: {self.calculate_total_expenses()}")
        print(f"Balance: {self.calculate_balance()}")
        print("======================================")
        return 
    
    def monthly_financial_summary(self, year, month):
        monthly_income = 0
        monthly_expenses = 0
        found = False
        for transaction in self.transactions:
            if transaction["Date"].year == year and transaction["Date"].month == month:
                found = True
                if transaction["Type"] == "Income":
                    monthly_income += transaction["Amount"]
                elif transaction["Type"] == "Expense":
                    monthly_expenses += transaction["Amount"]
        if not found:
            print(f"No transactions found for {month}/{year}")
            return
        
        monthly_balance = monthly_income - monthly_expenses
        print(f"Monthly Financial Summary for {month}/{year}:")
        print(f"Total Income: ₹{monthly_income}")
        print(f"Total Expenses: ₹{monthly_expenses}")
        print(f"Balance: ₹{monthly_balance}")
        
    def category_expense_report(self):
        found = False
        print("--- Category Expense Report ---")
        for category in self.categories:

            category_expense = self.calculate_category_wise_expense_total(category)

            if category_expense > 0:
                found = True 
                print(f"{category}: {category_expense}")
        
        if not found:
            print("No expenses found for any category.")

    def view_all_transactions(self):
        found = False
        print("=========Transactions===========")
        
        for number, transaction in enumerate(self.transactions, start = 1):
            found = True
            print(f"{number}. Date: {transaction['Date']} \nType: {transaction['Type']} \nAmount: {transaction['Amount']} \nCategory: {transaction['Category']} \nDescription: {transaction['Description']} \n--------------------------")
        
        if not found:
            print("No transactions found")

    def delete_transaction(self, transaction_number):
        if not self.transactions:
            print("No transactions to delete.")
            return
        if not (1 <= transaction_number <= len(self.transactions)):
            print("Invalid transaction number.")
            return
        index = transaction_number - 1
        self.transactions.pop(index)
        self.save_data()
        print(f"Transaction Number: {transaction_number} deleted successfully.")

    def find_transactions_by_category(self, category):
        found = False
        for number,category_transactions in enumerate(self.transactions, start = 1):
            
            if category in category_transactions['Category']:
                found = True
                print(f"{number}.{category_transactions['Type']} {category_transactions['Amount']} - {category_transactions['Category']} - {category_transactions['Date']}")

        if not found:
            print("No Such Transactions Found For The Given Category")
        return

    def add_transaction_input(self):
        try:
            transaction_type = input("Enter your Transaction Type: ")
            amount = float(input("Enter your transactions Amount: "))
            category = input("Enter the transaction category: ")
            year = int(input("Enter the transaction Year: "))
            month = int(input("Enter the transaction Month: "))
            day = int(input("Enter the transaction Day: "))
            description = input("Enter your transaction Description (Optional): ")

        except ValueError:
            print("You have entered wrong value in the input Box!")
            return

        self.add_transaction(transaction_type, amount, category, year, month,day, description)

    def add_category_input(self):
        category = input("Enter The Category name: ")
        self.add_category(category)
    
    def add_budget_input(self):
        try:
            budget_category = input("Enter The Category Name: ")
            budget_amount = int(input("Set The Category Budget: "))
        except ValueError:
            print("Make Sure the Detials you enter are Correct!.")
            return
        self.add_budget(budget_category,budget_amount)

    def display_menu(self):
        print("     ========== Finance Manager ==========")
        print("1. Add Transaction ")
        print("2. Add Category")
        print("3. Add Budget")
        print("4. View All Transactions ")
        print("5. Delete Transaction")
        print("6. Find Transaction By Category")
        print("7. Budget Status Report")
        print("8. Financial Summary")
        print("9. Monthly Financial Summary ")
        print("10. Category Expense Report ")
        print("11. Exit\n")

    def run(self):
        while True:
            self.display_menu()

            choice = input("Enter Your Option Here: ").strip()

            if choice == "1":
                self.add_transaction_input()
                
            elif choice == "2":
                self.add_category_input()
            
            elif choice == "3":
                self.add_budget_input()

            elif choice == "4":
                self.view_all_transactions()
            
            elif choice == "5":
                try:
                    transaction_number = int(input("Enter the Transaction Number Here: "))
                except ValueError:
                    print("Transaction Number must be an Integar.")
                    continue

                self.delete_transaction(transaction_number)

            elif choice == "6":   
                category = input("Enter the Category Name: ")
                self.find_transactions_by_category(category)

            elif choice == "7":
                budget_category = input("Enter The Budget Category Name Here: ")
                self.budget_status_report(budget_category)

            elif choice == "8":
                self.financial_summary()
            elif choice == "9":
                try:   
                    year = int(input("Enter The Year: "))
                    month = int(input("Enter The Month: "))
                except ValueError:
                    print("Year/Month must be an Integars.")
                    continue
                self.monthly_financial_summary(year, month)
            elif choice == "10":
                self.category_expense_report()
                
            elif choice == "11":
                break

            else:
                print("Invalid Option .Please Select from the Given Options 1 to 11.")
    
    def save_data(self):
        data_copy = []
        
        for transaction in self.transactions:
            transaction_copy = transaction.copy()
            transaction_copy["Date"] = transaction_copy["Date"].strftime("%Y-%m-%d")
            data_copy.append(transaction_copy)

        data_to_save = {
            "transactions": data_copy,
            "budgets": self.budgets,
            "categories": list(self.categories)
        }

        with open("Finance_data.json", "w") as file:
            json.dump(data_to_save, file, indent=4)

    def load_state(self):
        try:        
            with open("Finance_data.json", "r") as file:
                loaded_data = json.load(file)

            valid_transactions = []
            required_fields = {"Type", "Amount", "Category", "Date", "Description"}

            for transaction in loaded_data["transactions"]:
                if not isinstance(transaction, dict) or not required_fields.issubset(transaction):
                    print("Warning: Skipping an invalid transaction record.")
                    continue

                transaction_date = transaction["Date"]
                parse_date = datetime.strptime(transaction_date,"%Y-%m-%d")
                transaction["Date"] = parse_date.date()
                valid_transactions.append(transaction)

            self.transactions = valid_transactions
            self.budgets = loaded_data["budgets"]
            self.categories = set(loaded_data["categories"])
        except FileNotFoundError:
            print("No Finance_data.json file found. Starting with empty data.")
            self.transactions = []
            self.budgets = {}
            self.categories = set()

        except json.JSONDecodeError:
            print("Finance_data.json is empty or contains invalid JSON. Starting with empty data.")
            self.transactions = []
            self.budgets = {}
            self.categories = set()

        
    
                 
if __name__ == "__main__":
    fin = FinanceManager()
    fin.load_state()
    fin.run()