class User:

    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.user_accounts = []
        self.user_accounts.append(BankAccount(int_rate=0.02, balance = 0, name = input(f"{self.name}, what would you like your first account's name to be?\n")))
        print()

    def create_account(self):
        account_name = input(f"{self.name}, what would you like your account's name to be?\n")
        self.user_accounts.append(BankAccount(int_rate = 0.02, balance = 0, name = account_name))
        print()
        return self

    def make_deposit(self,amount):
        for i, account in enumerate(self.user_accounts):
            print(f"Account {i+1}: {account.name}")
        print()
        account_choice = input("Which account would you like to make a deposit to? Please select a number.\n")
        self.user_accounts[int(account_choice)-1].deposit(amount)
        print()
        return self
    
    def make_withdrawal(self,amount):
        for i, account in enumerate(self.user_accounts):
            print(f"Account {i+1}: {account.name}")
        print()
        account_choice = input("Which account would you like to withdraw from? Please select a number.\n")
        self.user_accounts[int(account_choice)-1].withdraw(amount)
        print()
        return self
    
    def display_user_balances(self):
        for account in self.user_accounts:
            print(f"User: {self.name}, {account.name} Balance: {account.balance}\n")
        return self
    
    def transfer_money(self,amount,other_user):
        for i, account in enumerate(self.user_accounts):
            print(f"Account {i+1}: {account.name}")
        print()
        account_choice = input(f"{self.name}, which account would you like to transfer from? Please select a number.\n")
        
        for i, account in enumerate(other_user.user_accounts):
            print(f"Account {i+1}: {account.name}")
        print()
        account_choice = input("Which account would you like to transfer into? Please select a number.\n")

        self.user_accounts[int(account_choice)-1].withdraw(amount)
        other_user.user_accounts[int(account_choice)-1].deposit(amount)

class BankAccount:

    accounts = []

    def __init__(self, int_rate = 0.00, balance = 0, name = ""): 
        self.int_rate = int_rate
        self.balance = balance
        self.name = name
        BankAccount.accounts.append(self)

    def deposit(self, amount):
        self.balance += amount
        return self

    def withdraw(self, amount):
        if amount <= self.balance:
            self.balance -= amount
        else:
            print("Insufficient funds: Charging a $5 fee\n")
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

user_1 = User("Kyle", "kcr@gmail.com")
user_1.create_account()

user_1.make_deposit(50)
user_1.make_withdrawal(25).make_withdrawal(25)

user_1.display_user_balances()

user_2 = User("Katie","ker@gmail.com")
user_1.transfer_money(25,user_2)

user_1.display_user_balances()
user_2.display_user_balances()