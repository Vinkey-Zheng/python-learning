

class TXOutput(object):
    def __init__(self, address, amount):
        self.address = address
        self.amount = amount

    def is_locked_with(self, address):
        return self.address == address

    def __repr__(self):
        return "TXOutput(address={}, amount={})".format(self.address, self.amount)

