

class TXOutput(object):
    def __init__(self, account, amount):
        self.amount = amount
        self.account = account

    def can_be_spent_by_account(self, account):
        return self.account == account

    def __repr__(self):
        return "TXOutput(account={}, amount={}".format(self.account, self.amount)
