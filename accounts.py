class Account:
    def __init__(self,account_number, owner_name, initial_balance = 0):
        if not isinstance (account_number, str)or not account_number:
            raise ValueError("Account number must be a non-empty string.")
        if not isinstance (owner_name, str) or not owner_name:
            raise ValueError("Owner name must be a non-empty string.")
        if not isinstance (initial_balance, int, float) or initial_balance < 0:
            raise ValueError("Initial balance must be a non-negative number.")

        self.account_number = account_number
        self.owner_name = owner_name
        self.transactions =[]
        self.loans=[]
        self.is_frozen = False
        self.minimum_balance = 0

        if initial_balance > 0:
            self.transactions.append(("Dposit", initial_balance, initial_balance))
            def _get_ current balance(self):
                balance = 0
                for transaction_type, amount, _ in self.transactions:
                    if transaction_type == "Deposit" or transaction_type == "Interest":
                        balance += amount
                    elif transaction_type == "Withdrawal" or transaction_type == "Loan Repayment" or transaction == "Transfer Out":
                        balance -= amount
                    return balance
            def  deposit(self, amount):
                if self.is_frozen:
                    return "Account is frozen. Deposit not allowed."
                if not isinstance(amount, (int,float)) or amount <= 0:
                    return "Deposit amount must be a positive number."
                current_balance = self._get_current_balance()
                new_balance = current_balance + amount
                self.transactions.append("Deposit", amount, new_balance)
                return f"Deposit successful. New balance: ${new_balance:.2f}"


            def Withdrawal(self, amount):
                if self.is_frozen:
                    erturn "Account is frozen. Withdrawal not allowed."
                if not isinstance(amount, (int,float)) or amount <= 0:
                    return "Withdrawal amount must be a positive number."
                
                current_balance = self._get_current_balance()
                if current_balance - amount < self.minimum_balance:
                    return f"Insufficient funds or withdrawal would go below the minimum balance of ${new_balance:.2f}. Current balance: ${current_balance:.2f}"

                    new_balance = current_balance - amount
                      self.transactions.append(("Withdrawal", amount, new_balance))
                return f"Withdrawal successful. New balance: ${New:.2f}"
            
             

            def transfer_funds(self, target_account, amount):
                if self.is_frozen:
                    return "Your account is frozen. Transafer not allowed."
                if target_account.is_frozen:
                    return "Target account is frozen. Transfer not allowed."
                if not isinstance(amount, (int, float)) or amount <= 0:
                    return "Transfer amount must be a positive number."
                if not isinstance(target_account, Account):
                    return "Target must be an instance of the Account class"
               
                current_balance = self._get_current_balance()
                if current_balance - amount < self.minimum_balance:
                    return f"Insufficient funds or withdrawal would go below the  minimum balance of ${self.minimum_balance:.2f}. Current balance: ${current_balance:.2f}"

                self.transactions.append(("Transfer Out", amount, current_balance - amount))

                target_account.transactions.append(("Transfer In", amount, target_account_balance + amount))

            def get_balance(self):
                return self._get_current_balance()

            def request_loan(self, amount):
                if self.is_frozen:
                    return "Account is frozen.  Loan request not allowed."
                if not isinstance(amount, (int, float)) or amount <= 0:
                    return "Loan amount must be a positive number."

                    current_balance = self._get_current_balance()
                    self.transactions.append((amount, amount))
                    return f"Loan  of ${amount:.2f} registered and approved. New balance: ${self._get_current_balance():.2f}"

            def repay_loan(self, amount):
                if self.is_frozen:
                    return "Account is froxen. Loan repayment not allowed."
                if not isinstance (amount, (int, float)) or amount <= 0:
                    return "Repayment amount must be a positive number."

                if not self.loans:
                    return "No active loan to repay."

                remaining_debt = sum(loan[1] for loan in self.loans)
                if amount > remaining_debt:
                    return f"Insufficient funds to repay loan. Current balance: ${current_balance:.2f}"

                repaid_amount = 0
                for i in range(len(self.loans)):
                    if amount == 0:
                        break
                    loan_original, loan_remaining = self.loans[i]
                    if amount >= loan_remaining:
                        repaid_amount += loan_remaining
                        amount -= loan_remaining
                        self.loans[i] = (loan_original, 0)
                    else:
                        self.loans[i] = (loan_original, loan_remaining)
                        repaid_amount += amount
                        amount = 0

                self.transactions.append(("Loan Repayment", repaid_amount, current_balance - repaid_amount))
                return f"Loan repayment of ${repaid_amount:.2f} successful. New balance: ${self._get_current_balance():.2f}. Remaining loan debt: ${sum(loan[1] for loan in self.loans):.2f}"

            def view_account_details(self):
                details = f"Account Number: {self.account_number}\n"
                details += f"Account Owner: {self.owner_name}\n"
                details += f"Current Balance: {self._get_current_balance():.2f}\n"
                details += f"Account Status: {'Frozen' if self.is_frozen else 'Active'}\n"
                details += f"Minimum Balance Required: ${self.minimum_balance:.2f}\n"
                return details

            def change_account_owner(self, new_owner_name):
                if not isinstance(new_owner_name, str) or not new_owner_name:
                    return "New owner name must be a non-empty string."
                    self.owner_name new_owner_name
                    return f"Account owner changed to : {self.owner_name}"
                    
            def account_statement(self:
                statement = f"___Account Statement for Account___ {self.account_number}___\n")
                statement += f"Owner: {self.owner_name}\n"
                statement +="___\n"
                statement += "{:<15} {:<10} {:<15}\n".format("Type", "Amount", "Balance After")
                statement += "___\n"
                if not self.transactions:
                    statement += "No transactions yet.\n"
                else:
                    for trans_type, trans_amount, balance_after in self.transactions:
                        statement+= "{:<15} ${:<9.2f} ${:<14.2f}\n".format(trans_type, trans_amount, balance_after)
                        statement +="___\n"
                        statement +=f"Current Balance: ${self._get_current_balance():.2f}\n"
                        statement += "___End of Statement___\n"
                        return statement

            def  interest_calculation(self, rate = 0.05):
                if self.is_frozen:
                    return "Account is frozen. Interest cannot be applied."
                if not isinstance(rate, (int,float)) or not (0 <=rate <= 1):
                    return "Interest rate must be between 0 and 1 (e.g., 0.05 for 5%)."

                current_balance = self._get_current_balance()
                interest_amount = current_balance * rate
                if interest_amount > 0:
                    new_balance = current_balance + interest_amount
                    self.transactions.append(("Interest", interest_amount, new_balance))
                    return "No positive balance tto apply interest."

            def freeze_account(self):
                if self.is_frozen:
                    return "Account is already frozen."
                self.is_frozen = True
                return "Account has been frozen"

            def unfreeze_account(self):
                if not self.is_frozen:
                    return "Account is not frozen."
                self.is_frozen = Falsereturn "Account has been unfrozen."

            def set_minimum_balance(self, amount):
                if not isinstance(amount, (int,float)) or amount < 0:
                    return "Mimimum balance must be a non-negative number."
                    self.minimum_balance = amount
                    return f"Minimum balance set to: ${self.minimum_balance:.2f}"

            def close_account(self):
                if self.is_frozen:
                    return "Account is frozen. Cannotclose a frozen account. Pls unfreeze"

                self.transactions = []
                self.loans = []
                self.owner_name = "None"
                self.is_frozen = Trueself.minimum_balance = 0
                return f"Account {self.account_number} has been closed. All balances are zero and transactions cleared."
