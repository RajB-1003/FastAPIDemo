import os
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from datetime import datetime

class BankAccount:
    def __init__(self,
                 balance_file="balance.txt",
                 deposit_file="deposits.txt",
                 withdraw_file="withdrawals.txt"):
        self.balance_file = balance_file
        self.deposit_file = deposit_file
        self.withdraw_file = withdraw_file

        # ensure files exist; initialize balance to 0.00 if missing or invalid
        if not os.path.exists(self.balance_file):
            self._write_balance(Decimal("0.00"))
        else:
            # if balance file is corrupted, reset to 0.00
            try:
                self.get_balance()
            except Exception:
                self._write_balance(Decimal("0.00"))

    def _read_balance(self) -> Decimal:
        with open(self.balance_file, "r") as f:
            raw = f.read().strip()
            if raw == "":
                return Decimal("0.00")
            # use Decimal for money
            return Decimal(raw)

    def _write_balance(self, amount: Decimal):
        # normalize to 2 decimal places
        amt = amount.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        with open(self.balance_file, "w") as f:
            f.write(str(amt))

    def get_balance(self) -> Decimal:
        return self._read_balance()

    def valid_amount(self, amount: Decimal) -> bool:
        # requires amount strictly greater than 1.00 (matches your message)
        return amount > Decimal("1.00")

    def _log(self, filename: str, entry: str):
        with open(filename, "a") as f:
            f.write(entry + "\n")

    def deposit(self, amount: Decimal) -> str:
        if not self.valid_amount(amount):
            return "Invalid amount! Enter more than 1."

        balance = self.get_balance() + amount
        self._write_balance(balance)

        timestamp = datetime.now().isoformat(sep=" ", timespec="seconds")
        self._log(self.deposit_file, f"{timestamp} | Deposited: {amount}")
        return f"Deposit successful. New balance: {balance.quantize(Decimal('0.01'))}"

    def withdraw(self, amount: Decimal) -> str:
        if not self.valid_amount(amount):
            return "Invalid amount! Enter more than 1."

        balance = self.get_balance()
        if amount > balance:
            return "Insufficient balance."

        balance -= amount
        self._write_balance(balance)

        timestamp = datetime.now().isoformat(sep=" ", timespec="seconds")
        self._log(self.withdraw_file, f"{timestamp} | Withdrawn: {amount}")
        return f"Withdrawal successful. New balance: {balance.quantize(Decimal('0.01'))}"


# ------------------------------
# MAIN MENU
# ------------------------------
def parse_amount(user_input: str):
    try:
        # Normalize input and use Decimal for precision
        amt = Decimal(user_input.strip())
        # force two decimal places for internal representation
        return amt.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    except (InvalidOperation, ValueError):
        return None

def main():
    acc = BankAccount()

    while True:
        print("\n--- Bank Menu ---")
        print("1. Check Balance")
        print("2. Deposit Money")
        print("3. Withdraw Money")
        print("4. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            bal = acc.get_balance().quantize(Decimal("0.01"))
            print("Current Balance:", bal)

        elif choice == "2":
            raw = input("Enter deposit amount (e.g. 100.00): ")
            amt = parse_amount(raw)
            if amt is None:
                print("Invalid input. Enter a numeric amount like 100 or 100.50")
                continue
            print(acc.deposit(amt))

        elif choice == "3":
            raw = input("Enter withdrawal amount (e.g. 50.00): ")
            amt = parse_amount(raw)
            if amt is None:
                print("Invalid input. Enter a numeric amount like 50 or 50.00")
                continue
            print(acc.withdraw(amt))

        elif choice == "4":
            print("Goodbye!")
            break

        else:
            print("Invalid option.")

if __name__ == "__main__":
    main()