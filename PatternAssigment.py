class AccountStatus:
    Active = "Active"
    Closed = "Closed"
    Suspended = "Suspended"
    Overdue = "Overdue"


class Account:
    def __init__(self, opening_balance: int):
        self.current_balance = opening_balance
        self.current_overdue_amount = 500
        self.min_balance = 500
        self.current_account_status = AccountStatus.Active

    def withdraw(self, amount: int):
        if self.current_account_status == AccountStatus.Closed:
            raise Exception("Cannot Withdraw the amount requested...Account is CLOSED state")

        if amount > self.current_balance + self.current_overdue_amount:
            raise Exception("Cannot Withdraw the amount requested...")

        if self.current_balance > amount:
            self.current_balance -= amount
        else:
            # Take the remaining amount from OD
            self.current_overdue_amount += (self.current_balance - amount)
            self.current_balance = 0

        self._set_account_status()

    def deposit(self, amount: int):
        if self.current_account_status == AccountStatus.Closed:
            raise Exception("Cannot Deposit the amount requested...Account is CLOSED state")

        if self.current_overdue_amount < 500:
            self.current_overdue_amount += amount
            self.current_balance = self.current_overdue_amount - 500
            self.current_overdue_amount = 500
        else:
            self.current_balance += amount

        self._set_account_status()

    def get_balance(self) -> int:
        return self.current_balance

    def get_status(self) -> str:
        return self.current_account_status

    def _set_account_status(self):
        if self.current_account_status == AccountStatus.Active:
            # ACTIVE → CLOSED, SUSPENDED, OVERDUE
            if self.current_balance < self.min_balance + self.current_overdue_amount:
                self.current_account_status = AccountStatus.Closed
            elif self._is_overdue():
                self.current_account_status = AccountStatus.Overdue
            elif self._is_suspended():
                self.current_account_status = AccountStatus.Suspended

        elif self.current_account_status == AccountStatus.Suspended:
            # SUSPENDED → ACTIVE, OVERDUE
            if self._is_active():
                self.current_account_status = AccountStatus.Active
            elif self._is_overdue():
                self.current_account_status = AccountStatus.Overdue

        elif self.current_account_status == AccountStatus.Overdue:
            # OVERDUE → SUSPENDED, ACTIVE
            if self._is_active():
                self.current_account_status = AccountStatus.Active
            elif self._is_suspended():
                self.current_account_status = AccountStatus.Suspended

    def _is_active(self) -> bool:
        return self.current_balance > self.min_balance

    def _is_suspended(self) -> bool:
        return self.current_overdue_amount == 0

    def _is_overdue(self) -> bool:
        return self.current_overdue_amount < 500


# --- Demo usage (like Program.Main in C#) ---
if __name__ == "__main__":
    input("Press Enter to continue...")  # simulates Console.ReadLine()
    acc = Account(1000)
    acc.withdraw(1100)
    print(
        f"Account Balance is: {acc.get_balance()} "
        f"AND Account Status is : {acc.get_status()} "
        f"AND Account OD balance now is : {acc.current_overdue_amount}"
    )
    input("Press Enter to exit...")
