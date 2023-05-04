class BankAccount:

    accounts = []

    def __init__(self, int_rate = 0.00, balance = 0): 
        self.int_rate = int_rate
        self.balance = balance
        BankAccount.accounts.append(self)

    def deposit(self, amount):
        self.balance += amount
        return self

    def withdraw(self, amount):
        if amount <= self.balance:
            self.balance -= amount
        else:
            print("Insufficient funds: Charging a $5 fee")
            self.balance -= 5
        return self

    def display_account_info(self):
        print(f"Balance: ${self.balance}")
        return self

    def yield_interest(self):
        if self.balance > 0:
            self.balance += self.balance * self.int_rate
        return self
    
    @classmethod
    def print_all_info(cls):
        for account in cls.accounts:
            print(f"Balance: ${account.balance}")

account_1 = BankAccount(0.02,500)
account_2 = BankAccount(0.10)

account_1.deposit(50).deposit(100).deposit(150).withdraw(100).yield_interest().display_account_info()
account_2.deposit(100).deposit(50).withdraw(20).withdraw(200).withdraw(15).withdraw(50).yield_interest().display_account_info()

BankAccount.print_all_info()