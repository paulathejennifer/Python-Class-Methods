class Account:
    def __init__(self,account_number, owner_name, initial_balance = 0):
            if not isinstance (account_number, str)or not account_number:
                raise ValueError("Account number must be a non-empty string.")
            if not isinstance (owner_name, str) or not owner_name:
                raise ValueError("Owner name must be a non-empty string.")
            if not isinstance (initial_balance, (int, float)) or initial_balance < 0:
                raise ValueError("Initial balance must be a non-negative number.")

            self.account_number = account_number
            self.owner_name = owner_name
            self.transactions =[]
            self.loans=[]
            self.is_frozen = False
            self.minimum_balance = 0

            if initial_balance > 0:
                self.transactions.append(("Deposit", initial_balance, initial_balance))
    def _get_current_balance(self):
        balance = 0
        for transaction_type, amount, _ in self.transactions:
            if transaction_type in ["Deposit", "Interest", "Transfer In", "Loan"]:
                balance += amount
            elif transaction_type in ["Withdrawal", "Loan Repayment", "Transfer Out"]:
                balance -= amount
        return balance

    def  deposit(self, amount):
        if self.is_frozen:
            return "Account is frozen. Deposit not allowed."
        if not isinstance(amount, (int,float)) or amount <= 0:
            return "Deposit amount must be a positive number."
        # current_balance = self._get_current_balance()
        new_balance = self._get_current_balance() + amount
        self.transactions.append(("Deposit", amount, new_balance))
        return f"Deposit successful. New balance: ${new_balance:.2f}"


    def withdraw(self, amount):
        if self.is_frozen:
            return "Account is frozen. Withdrawal not allowed."
        if not isinstance(amount, (int,float)) or amount <= 0:
            return "Withdrawal amount must be a positive number."
        
        current_balance = self._get_current_balance()
        if current_balance - amount < self.minimum_balance:
            return f"Insufficient funds or withdrawal would go below the minimum balance of ${new_balance:.2f}. Current balance: ${current_balance:.2f}"

        new_balance = current_balance - amount
        self.transactions.append(("Withdrawal", amount, new_balance))
        return f"Withdrawal successful. New balance: ${new_balance:.2f}"
    
        

    def transfer_funds(self, target_account, amount):
        if self.is_frozen:
            return "Your account is frozen. Transfer not allowed."
        if target_account.is_frozen:
            return "Target account is frozen. Transfer not allowed."
        if not isinstance(amount, (int, float)) or amount <= 0:
            return "Transfer amount must be a positive number."
        if not isinstance(target_account, Account):
            return "Target must be an instance of the Account class"
        
        current_balance = self._get_current_balance()
        if current_balance - amount < self.minimum_balance:
            return f"Insufficient funds or withdrawal would go below the  minimum balance of ${self.minimum_balance:.2f}. Current balance: ${current_balance:.2f}"

        new_balance = current_balance - amount
        self.transactions.append(("Transfer Out", amount, new_balance))
        target_new_balance = target_account._get_current_balance() + amount

        target_account.transactions.append(("Transfer In", amount, target_new_balance))
        return f"Transfer of ${amount:.2f} to {target_account.owner_name} successful"

    def get_balance(self):
        return self._get_current_balance()

    def request_loan(self, amount):
        if self.is_frozen:
            return "Account is frozen.  Loan request not allowed."
        if not isinstance(amount, (int, float)) or amount <= 0:
            return "Loan amount must be a positive number."

        self.loans.append((amount, amount))
        new_balance = self._get_current_balance() + amount
        self.transactions.append(("Loan", amount, new_balance))
        return f"Loan  of ${amount:.2f} registered and approved. New balance: ${new_balance:.2f}"

    def repay_loan(self, amount):
        if self.is_frozen:
            return "Account is froxen. Loan repayment not allowed."
        if not isinstance (amount, (int, float)) or amount <= 0:
            return "Repayment amount must be a positive number."

        if not self.loans:
            return "No active loan to repay."

        current_balance = self._get_current_balance()
        if amount > current_balance:
            return f"Insufficient balance to repay loann. Current balance: ${current_balance:.2f}"
    

        remaining_debt = sum(loan[1] for loan in self.loans)
        repaid_amount = min(amount, remaining_debt)
        self.transactions.append(("Loan Repayment", repaid_amount, current_balance - repaid_amount))
        # if amount > remaining_debt:
        #     return f"Insufficient funds to repay loan. Current balance: ${current_balance:.2f}"

        new_loans = []
        for original, remaining in self.loans:
            if repaid_amount == 0:
                new_loans.append((original, remaining))
            elif repaid_amount >= remaining:
                repaid_amount -= remaining
            else:
                new_loans.append((original, remaining - repaid_amount))
                repaid_amount = 0
            self.loans = new_loans

            return f"Loan repayment of ${amount:.2f} successful. Remaining debt: ${sum(l[1] for l in self.loans):.2f}"
       

    def view_account_details(self):
        return(
            f"Account Number: {self.account_number}\n"
            f"Account Owner: {self.owner_name}\n"
            f"Current Balance: {self._get_current_balance():.2f}\n"
            f"Account Status: {'Frozen' if self.is_frozen else 'Active'}\n"
            f"Minimum Balance Required: ${self.minimum_balance:.2f}\n"
        
        )

        

    def change_account_owner(self, new_owner_name):
        if not isinstance(new_owner_name, str) or not new_owner_name:
            return "New owner name must be a non-empty string."
        self.owner_name = new_owner_name
        return f"Account owner changed to : {self.owner_name}"
            
    def account_statement(self):
        statement = f"___Account Statement for Account___ {self.account_number}___\n"
        statement += f"Owner: {self.owner_name}\n"
        statement += f"{'Type':<15} {'Amount':<10} {'Balance After':<15}\n".format("Type", "Amount", "Balance After")
        statement += "-"*45 +"\n"
        for trans_type, amount, balance in self.transactions:
             statement += "-"*45 +"\n"
        statement +=  f"Current Balance: ${self._get_current_balance():.2f}\n"
        statement += "___End of statement__"
        return statement

    def  interest_calculation(self, rate = 0.05):
        if self.is_frozen:
            return "Account is frozen. Interest cannot be applied."
        if not isinstance(rate, (int,float)) or not (0 <=rate <= 1):
            return "Interest rate must be between 0 and 1 (e.g., 0.05 for 5%)."

        current_balance = self._get_current_balance()
        if current_balance <= 0:
            return "No positive balance to apply interest"

        interest_amount = current_balance * rate
        new_balance = current_balance + interest_amount
        self.transactions.append(("Interest", interest_amount, new_balance))
        return f"{interest_amount:.2f} applied. New balance: ${new_balance:.2f}"
        return ""

    def freeze_account(self):
        if self.is_frozen:
            return "Account is already frozen."
        self.is_frozen = True
        return "Account has been frozen"

    def unfreeze_account(self):
        if not self.is_frozen:
            return "Account is not frozen."
        self.is_frozen = False
        return "Account has been unfrozen."

    def set_minimum_balance(self, amount):
        if not isinstance(amount, (int,float)) or amount < 0:
            return "Mimimum balance must be a non-negative number."
            
        self.minimum_balance = amount
        return f"Minimum balance set to: ${self.minimum_balance:.2f}"

    def close_account(self):
        if self.is_frozen:
            return "Account is frozen. Cannot close a frozen account. Pls unfreeze"

        self.transactions = []
        self.loans = []
        self.owner_name = "None"
        self.is_frozen = True
        self.minimum_balance = 0
        return f"Account {self.account_number} has been closed."




        #SCRIPT TO TEST ACCOUNT CLASS AND METHODS
#>>> from accounts import Account
#>>> acc1 = Account("12345", "Jane Gitau", initial_balance = 900)
#>>> acc2 = Account("6789", "Peter Njau", initial_balance=100)
#>>> print(acc1.deposit(100))
#Deposit successful. New balance: $1000.00
#>>> print(acc1.withdraw(300))
#Withdrawal successful. New balance: $700.00
#>>> print(acc1.transfer_funds(acc2, 250))
#Transfer of $250.00 to Peter Njau successful
#>>> print(acc1.request_loan(300))
#Loan  of $300.00 registered and approved. New balance: $750.00
#>>> print(acc1.repay_loan(90))
#Loan repayment of $90.00 successful. Remaining debt: $210.00
#>>> print(acc1.interest_calculation())
#33.00 applied. New balance: $693.00
#>>> print(acc1.freeze_account())
#Account has been frozen
#>>> print(acc1.deposit(500))
#Account is frozen. Deposit not allowed.
#>>> print(acc1.unfreeze_account())
#Account has been unfrozen.
#>>> print(acc1.unfreeze_account())
#Account is not frozen.
#>>> print(acc1.deposit(50))
#Deposit successful. New balance: $743.00
#>>> print(acc1.change_account_owner("Jennifer Chinyere"))
#Account owner changed to : Jennifer Chinyere
#>>> acc1.owner_name
#'Jennifer Chinyere'
#>>> print(acc1.set_minimum_balance(100))
#Minimum balance set to: $100.00
#>>> print(acc1.account_statement())
#___Account Statement for Account___ 12345___
#Owner: Jennifer Chinyere
#Type            Amount     Balance After  
#---------------------------------------------
#---------------------------------------------
#---------------------------------------------
#---------------------------------------------
#---------------------------------------------
#---------------------------------------------
#---------------------------------------------
#---------------------------------------------
#---------------------------------------------
#Current Balance: $743.00
#___End of statement__
#>>> print(acc1.close_account())
#Account 12345 has been closed.
#>>> print(acc1.deposit(50))
#Account is frozen. Deposit not allowed.
#>>> print(acc1.unfreeze_account())
#Account has been unfrozen.
#>>> print(acc1.unfreeze_account())
#Account is not frozen.
#>>> print(acc1.deposit(50))
#Deposit successful. New balance: $50.00
#>>> print("\n" + acc1.view_account_details())

#Account Number: 12345
#Account Owner: None
#Current Balance: 50.00
#Account Status: Active
#Minimum Balance Required: $0.00

#>>> print("\n" + acc2.view_account_details())

#Account Number: 6789
#Account Owner: Peter Njau
#Current Balance: 350.00
#Account Status: Active
#Minimum Balance Required: $0.00

