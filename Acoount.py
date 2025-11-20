class BankAccount:
    def __init__(self,accountHolder):
        self._balance=10000
        self._name=accountHolder
        with open(self._name+'Ledger.txt', 'w') as ledgerFile :
            ledgerFile.write('Blance is 0\n')
    
    @property
    def balance(self):
        return self._balance

    @balance.setter
    def balance(self,value):

        if value > 1:
            self._balance=value
        else:
            raise ValueError("Invalid amount " +str(value))
    

    def deposit(self,amount):
        if amount<=0:
            return #don't allow negtive deposit
        self.balance+=amount
        with open(self._name+'Ledger.txt', 'a') as ledgerFile :
            ledgerFile.write('Deposit '+str(amount) +'\n')
            ledgerFile.write('Blance is '+ str(self.balance)+'\n')
    
    def withdrawal(self,amount):
        if self._balance <amount or amount < 0:
            return
        self.balance-=amount
        with open(self._name+'Ledger.txt', 'a') as ledgerFile :
            ledgerFile.write('Withdraw '+str(amount) +'\n')
            ledgerFile.write('Blance is '+ str(self.balance)+'\n')

    def  get_balance(self):
         return self.balance
    def __str__(self):
        return f'{self._name} : {self.balance}'

        
acct =BankAccount('Alice')
acct.deposit(25000)
acct.withdrawal(10000)

print(acct)



acct2 =BankAccount('Alice')
acct2.deposit(1000)
acct2.withdrawal(100)
print(acct2)
print(acct==acct2)