# -*- encoding: utf-8 -*-
'''
------------------------------------------------------------
-文件        : utxo_set.py
-说明        : UTXO集实现
-时间        : 2021/01/08 08:40:49
-作者        : newdao
------------------------------------------------------------
-版本号      ：myBlockchainV8
------------------------------------------------------------
'''
from collections import defaultdict
from db import DB
from transaction import *
from errors import TransactionNotFound

class UTXOSet(object):
    DB_FILE_PATTERN = './bc_utxoset_{}.db'

    def __init__(self, blockchain):
        self._db = DB(UTXOSet.DB_FILE_PATTERN.format(blockchain.node_id))
        self.blockchain = blockchain

    def rebuild(self):
        # 清空重置数据库
        self._db.reset()

        # 从区块链中获取所有未花费交易
        utxos = self.blockchain.find_utxo()

        # 将未花费交易放入UTXO集数据库中
        for tx_id, outs_list in utxos.items():
            self._db.put(tx_id, outs_list)

        # 提交数据库操作
        self._db.commit()


    def find_spendable_outputs(self, address, amount):
        accumulated = 0
        unspent_outputs = defaultdict(list)        

        for tx_id, outs in self._db.kv.items():
            for idx, out in enumerate(outs):
                if out.is_locked_with(address) and accumulated<amount:
                    accumulated += out.amount
                    unspent_outputs[tx_id].append(idx)
        return accumulated, unspent_outputs


    def find_utxo(self, address):
        utxos = []

        for outs in self._db.kv.values():
            for out in outs:
                if out.is_locked_with(address):
                    utxos.append(out)
        return utxos

    def find_transaction_utxo(self, tx_id):
        try :
            return self._db.kv[tx_id]
        except KeyError:
            raise TransactionNotFound()
    
    def update(self, new_block):
        for tx in new_block.data:
            if not isinstance(tx, CoinbaseTx):
                for vin in tx.vins:
                    update_outs = []
                    outs = self._db.get(vin.tx_id)

                    for out_idx, out in enumerate(outs):
                        if out_idx != vin.vout_idx:
                            update_outs.append(out)
                    
                    if len(update_outs) == 0:
                        self._db.delete(vin.tx_id)
                    else :
                        self._db.put(vin.tx_id, update_outs)
            new_outputs = [o for o in tx.vouts]
            self._db.put(tx.id, new_outputs)

        self._db.commit()

    
    def print_utxo_set(self):
        print('UTXO SET:    ')
        for tx_id, outs in self._db.kv.items():
            print("{}:{}".format(tx_id, outs))
        print('')
        