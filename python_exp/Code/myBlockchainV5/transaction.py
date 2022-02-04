import pickle
import hashlib
import random
import string

from transaction_input import TXInput
from transaction_output import TXOutput


class Transaction(object):
    @staticmethod
    def hash_tx(vins, vouts):
        m = hashlib.sha256(pickle.dumps(vins+vouts))
        return m.hexdigest()

    def __init__(self, vins, vouts):
        self.vins = vins
        self.vouts = vouts
        self.id = Transaction.hash_tx(vins, vouts)

    def hash(self):
        self.id = Transaction.hash_tx(self.vins, self.vouts)
        return self.id

    def __repr__(self):
        return 'Transaction(id={}, vins={}, vouts={})'.format(
            self.id, self.vins, self.vouts
        )


class CoinbaseTx(Transaction):
    subsidy = 50

    def __init__(self, to_account, data=None):
        if data is None:
            data = ''.join(random.sample(string.ascii_letters +
                                         string.digits, 20))

        vins = [TXInput(None, -1, data)]
        vouts = [TXOutput(to_account, CoinbaseTx.subsidy)]
        super(CoinbaseTx, self).__init__(vins, vouts)

    def __repr__(self):
        return "CoinbaseTx(id={}, vins={}, vouts={})".format(
            self.id, self.vins, self.vouts)


class NotEnoughFundsError(Exception):
    pass


class UTXOTransaction(Transaction):
    def __init__(self, from_account, to_account, amount,
                 blockchain):
        inputs = []
        outputs = []

        acc, valid_outputs = blockchain.find_spendable_outputs(from_account, amount)
        if acc < amount:
            raise NotEnoughFundsError()

        # 构建交易输入列表
        for tx_id, outs in valid_outputs.items():
            for idx, out in enumerate(outs):
                input1 = TXInput(tx_id, idx, from_account)
                inputs.append(input1)

        # 构建交易输出列表
        outputs.append(TXOutput(to_account, amount))

        # 找零
        if acc >= amount:
            outputs.append(TXOutput(from_account, acc-amount))

            super(UTXOTransaction, self).__init__(inputs, outputs)

    def __repr__(self):
        return 'UTXOTransaction(id={}, vins={}, vouts={})'.format(
                self.id, self.vins, self.vouts)
