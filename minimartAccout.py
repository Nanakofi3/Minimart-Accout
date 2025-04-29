#Creating a simple minimart account class for transaction


class Account:
# Creating a contractor with parameters name and balance   
    def __init__(self, name, balance):
        self.name = name
        self.balance = balance
        self.transactions = {}

# Creating a deposit with parameter amount  
    def deposit(self, amount):
        try:
          if amount > 0:
            self.balance += amount
            print(f"Deposited {amount}, New balance: {self.balance}")
          else:
            print("Deposit amount must be positive")
        except:
            print("Invalid input")

 # Creating a withdraw with parameter amount
    def withdraw(self, amount):
        try:
            if amount > 0:
               if amount <= self.balance:
                    self.balance -= amount
                    print(f"Withdrew {amount}, New balance: {self.balance}")
               else:
                    print("Insufficient funds")
            else:
                print("Withdrawal amount must be positive")
        except:
                print("Invalid input")

# Creating a  purchase with parameter item name and price
    def purchase(self, item_name, price):
     try:
        if price > 0:
            if price <= self.balance:
                self.balance -= price
                self.transactions[item_name] = price
                print(f"Purchased {item_name} for {price}, Remaining balance: {self.balance}")
            else:
                print("Insufficient funds for this purchase")
        else:
            print("Price must be positive")
     except:
         print("Invalid input")

# Creating a method to show balance
    def show_balance(self):
        print(f"Current balance: {self.balance}")

# Method to show all purchases made 
    def show_transactions(self):
        if not self.transactions:
            print("No purchases have been made.")
        else:
            print("Purchase history: ")
            for item, price in self.transactions.items():
                print(f"{item}: {price}")


# Find and remove the first matching transaction
    def remove_purchase(self, item):
        if item in self.transactions:
           
            self.balance += self.transactions.pop(item)
            print(f"Removed {item} purchase from transactions.")
        else:
            print(f"No purchase found for {item} to remove.")



if __name__ == "__main__":
    account = Account("Kasa", 4000) 

    account.show_balance()
    
    account.purchase("Apple", 90)  
    account.purchase("Banana", 80) 
    account.purchase("Orange", 10) 
    account.withdraw(30)  
    account.deposit(60) 
    account.show_balance()
    account.remove_purchase("Apple")
    
    account.show_transactions() 
 