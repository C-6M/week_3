class BankAccount:

    def __init__(self, name, balance=0):
        self.name = name
        self._balance = balance
        self._transactions = []
        self._withdraw_limit = 5000

    def deposit(self, amount):
        if amount <= 0:
            return "存款失败：金额必须大于 0"
        self._balance = self._balance + amount
        self._transactions.append(("存款", amount))
        return "存入" + str(amount) + "元，余额" + str(self._balance) + "元"

    def withdraw(self, amount):
        if amount <= 0:
            return "取款失败：金额必须大于 0"
        if amount > self._withdraw_limit:
            return "取款失败：单次最多取" + str(self._withdraw_limit) + "元"
        if amount > self._balance:
            return "取款失败：余额不足（余额" + str(self._balance) + "元，想取" + str(amount) + "元）"
        self._balance = self._balance - amount
        self._transactions.append(("取款", amount))
        return "取出" + str(amount) + "元，余额" + str(self._balance) + "元"

    def get_balance(self):
        return "【" + self.name + "】当前余额：" + str(self._balance) + "元"

    def get_transactions(self):
        if len(self._transactions) == 0:
            return "暂无交易记录"
        result = "【" + self.name + "】交易记录："
        for i in range(len(self._transactions)):
            action = self._transactions[i][0]
            money = self._transactions[i][1]
            result = result + "\n  " + str(i + 1) + ". " + action + " " + str(money) + "元"
        return result


if __name__ == "__main__":
    acc1 = BankAccount("Alice")
    print(acc1.deposit(700))
    print(acc1.deposit(300))
    print(acc1.withdraw(200))
    print(acc1.withdraw(900))
    print(acc1.withdraw(-50))
    print(acc1.withdraw(6000))
    print(acc1.get_balance())
    print(acc1.get_transactions())
