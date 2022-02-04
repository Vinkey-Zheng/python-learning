import pickle
import dill
import hashlib
import random
import string
from transaction_input import TXInput
from transaction_output import TXOutput
from errors import NotEnoughFundsError
import wallets
import wallet
import address


class Transaction(object):
    @staticmethod
    def hash_tx(vins, vouts):
        print(vins)
        print(vouts)
        m = hashlib.sha256(pickle.dumps(vins+vouts))
        return m.hexdigest()

    def __init__(self, vins, vouts):
        self.vins = vins
        self.vouts = vouts
        self.id = Transaction.hash_tx(vins, vouts)

    def hash(self):
        self.id = Transaction.hash_tx(self.vins, self.vouts)
        return self.id

    def _trimmed_copy(self):
        inputs = []
        outputs = []

        for vin in self.vins:
            inputs.append(TXInput(vin.tx_id, vin.vout_idx, None, vin.verify_key))

        for vout in self.vouts:
            outputs.append(TXOutput(vout.address, vout.amount))

        return Transaction(inputs, outputs)

    def sign(self, sign_key):

        tx_copy = self._trimmed_copy()

        for vin_idx, vin in enumerate(tx_copy.vins):
            self.vins[vin_idx].signature = sign_key.sign(tx_copy.hash().encode('ascii'))


    def verify(self, utxos):
        tx_copy = self._trimmed_copy()
        for vin_idx, vin in enumerate(tx_copy.vins):
            outs = utxos[vin.tx_id]
            if not outs[vin.vout_idx].is_locked_with(address.Address(vin.verify_key)):
                print("verify error: address", outs[vin.vout_idx], address.Address(vin.verify_key))
                return False
            sig = self.vins[vin_idx].signature
            if not vin.verify_key.verify(sig, tx_copy.hash().encode('ascii')):
                print('vefiry error: verify error')
                return False
        return True

    def __repr__(self):
        return 'Transatcion(id={}, vins={}, vouts={})'.format(self.id, self.vins, self.vouts)

class CoinbaseTx(Transaction):
    subsidy = 50
    def __init__(self, to_address, data=None):
        if data==None:
            data = ''.join(random.choice(string.
                                         ascii_uppercase + string.digits) for _ in range(20))
        vins = [TXInput(None, -1, None, data)]
        print(to_address)
        vouts = [TXOutput(to_address, CoinbaseTx.subsidy)]
        super(CoinbaseTx, self).__init__(vins, vouts)

    def sign(self, sign_key, prev_txs):
        pass

    def verify(self, prev_txs):
        return True

    def __repr__(self):
        return "CoinbaseTx(id={}, vins={}, vouts={})".\
            format(self.id, self.vins, self.vouts)


class UTXOTransaction(Transaction):
    def __init__(self, from_address, to_address, amount, utxo_set):
        inputs = []
        outputs = []

        acc, valid_outputs = utxo_set.\
            find_spendable_outputs(from_address, amount)
        if acc < amount:
            raise NotEnoughFundsError()

        # 构建交易输入列表
        ws = wallets.Wallets()
        w = ws.get_wallet(from_address.get_address_str())
        for tx_id, out_idx_s in valid_outputs.items():
            for idx in out_idx_s:
                input = TXInput(tx_id, idx, None, w.verify_key)
                inputs.append(input)

        # 构建交易输出列表
        outputs.append(TXOutput(to_address, amount))

        # 找零
        if acc > amount:
            outputs.append(TXOutput(from_address, acc-amount))

        super(UTXOTransaction, self).__init__(inputs, outputs)

    def __repr__(self):
        return "UTXOTransaction(id={}, " \
               "vins={}, vouts={})".\
            format(self.id, self.vins, self.vouts)
