import uuid
from datetime import datetime

class Account:
    def __init__(self, name, balance):
        self.name = name
        self.balance = balance
        self.transactions = []
        self.overdraft_limit = 500  # New: Allow negative balance up to 500
        self.interest_rate = 0.02  # 2% annual interest

    def _record_transaction(self, transaction_type, amount, item=None):
        transaction = {
            'id': str(uuid.uuid4()),
            'type': transaction_type,
            'amount': amount,
            'item': item,
            'timestamp': datetime.now(),
            'balance_after': self.balance
        }
        self.transactions.append(transaction)

    def deposit(self, amount):
        try:
            amount = float(amount)
            if amount > 0:
                self.balance += amount
                print(f"Deposited {amount:.2f}, New balance: {self.balance:.2f}")
                self._record_transaction('deposit', amount)
            else:
                print("Deposit amount must be positive")
        except ValueError:
            print("Invalid input - please enter a valid number")

    def withdraw(self, amount):
        try:
            amount = float(amount)
            if amount > 0:
                if self.balance - amount >= -self.overdraft_limit:
                    self.balance -= amount
                    print(f"Withdrew {amount:.2f}, New balance: {self.balance:.2f}")
                    self._record_transaction('withdrawal', amount)
                else:
                    print("Exceeds overdraft limit")
            else:
                print("Withdrawal amount must be positive")
        except ValueError:
            print("Invalid input - please enter a valid number")

    def purchase(self, item_name, price):
        try:
            price = float(price)
            if price > 0:
                if self.balance - price >= -self.overdraft_limit:
                    self.balance -= price
                    print(f"Purchased {item_name} for {price:.2f}, Remaining balance: {self.balance:.2f}")
                    self._record_transaction('purchase', price, item_name)
                else:
                    print("Insufficient funds (including overdraft)")
            else:
                print("Price must be positive")
        except ValueError:
            print("Invalid input - please enter valid numbers")

    def show_balance(self):
        print(f"Current balance: {self.balance:.2f}")

    def show_transactions(self, num_transactions=5):
        if not self.transactions:
            print("No transactions yet")
            return

        print("\nTransaction History:")
        print(f"{'Date':20} {'Type':10} {'Amount':10} {'Item':15} {'Balance After':12}")
        for t in self.transactions[-num_transactions:]:
            print(f"{t['timestamp'].strftime('%Y-%m-%d %H:%M:%S'):20} "
                  f"{t['type']:10} "
                  f"{t['amount']:10.2f} "
                  f"{t['item'] or 'N/A':15} "
                  f"{t['balance_after']:12.2f}")

    def remove_transaction(self, transaction_id):
        for i, t in enumerate(self.transactions):
            if t['id'] == transaction_id:
                if t['type'] == 'purchase':
                    self.balance += t['amount']
                elif t['type'] == 'deposit':
                    self.balance -= t['amount']
                elif t['type'] == 'withdrawal':
                    self.balance += t['amount']
                del self.transactions[i]
                print(f"Transaction {transaction_id} removed")
                return
        print("Transaction ID not found")

    def calculate_interest(self):
        interest = self.balance * self.interest_rate / 12  # Monthly interest
        if interest > 0:
            self.balance += interest
            self._record_transaction('interest', interest)
            print(f"Interest added: {interest:.2f}")

    def export_statement(self, filename):
        with open(filename, 'w') as f:
            f.write(f"Account Statement for {self.name}\n")
            f.write(f"Date,Type,Amount,Item,Balance After\n")
            for t in self.transactions:
                f.write(f"{t['timestamp'].isoformat()},"
                        f"{t['type']},"
                        f"{t['amount']:.2f},"
                        f"{t['item'] or ''},"
                        f"{t['balance_after']:.2f}\n")
            print(f"Statement exported to {filename}")

    def __str__(self):
        return (f"Account Holder: {self.name}\n"
                f"Current Balance: {self.balance:.2f}\n"
                f"Available Credit: {self.balance + self.overdraft_limit:.2f}")


if __name__ == "__main__":
    acc = Account("Kasa", 4000)
    
    # Test new features
    acc.deposit(500)
    acc.purchase("Milk", 2.99)
    acc.purchase("Bread", 3.49)
    acc.withdraw(200)
    acc.show_transactions()
    

    if acc.transactions:
        transaction_id = acc.transactions[0]['id']
        acc.remove_transaction(transaction_id)

    acc.calculate_interest()

    acc.export_statement("account_statement.csv")
    
    print("\nAccount Summary:")
    print(acc)