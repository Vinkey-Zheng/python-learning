# -*- encoding: utf-8 -*-
'''
------------------------------------------------------------
-文件        : blockchain.py
-说明        : 区块链类的实现
-时间        : 2020/10/20 11:37:16
-作者        : newdao
------------------------------------------------------------
-版本号      : myBlockchainV8
------------------------------------------------------------
'''
from collections import defaultdict
from block import Block
from datetime import datetime
from proofofwork import ProofOfWork
from db import DB
from transaction import *
from utxo_set import UTXOSet
from errors import BlockchainAlreadyExists, NeedInitAccount, TransactionNotFound

class BlockChain(object):
    # 数据库中存储最后一个区块的散列值的key
    LAST_BLOCK_HASH_KEY = 'Last'
    # 数据库文件
    DB_FILE_PATTERN = './bc_blocks_{}.db'

    def __init__(self, node_id, init_address=None):
        self.node_id = node_id
        self.pow = ProofOfWork()  # 创建工作量证明类
        self._db = DB(BlockChain.DB_FILE_PATTERN.format(node_id)) # 创建区块链数据库
        try:
            self._tail = self._db.get(BlockChain.LAST_BLOCK_HASH_KEY)
            if init_address != None:
                raise BlockchainAlreadyExists()
        except KeyError:
            if init_address == None:
                raise NeedInitAccount()
            coinbase_tx = CoinbaseTx(init_address)
            genesis_block = self.pow.mine_block([coinbase_tx], '', 1) # 通过工作量证明类来挖出创世区块
            self._put_block(genesis_block)
            print('Created a new blockchain.\n')

    # 将区块存放到数据库中，并更新_tail成员
    def _put_block(self, block):
        self._db.put(block.hash(), block)
        self._db.put(BlockChain.LAST_BLOCK_HASH_KEY, block.hash())
        self._db.commit()
        self._tail = block.hash()

    # 挖出一个数据为data的区块
    def mine_block(self, data): 
        height = 1 
        try:
            last_block = self._db.get(self._tail)
            height = last_block.height + 1
        except KeyError:
            height = 1

        new_block = self.pow.mine_block(data, self._tail, height)
        for tx in new_block.data:
            if not self.verify_transaction(tx):
                print('Error: Invalid transaction!')
                return
        self._put_block(new_block)
        return new_block

    @property
    def blocks(self):
        current = self._tail
        while True:
            if not current: # 为空，表明已遍历到区块链的创世块
                return
            block = self._db.get(current)
            yield block
            current = block.prev_block_hash
            
    def print_chain(self):
        for block in self.blocks:
            print('Block Hash: {}'.format(block.hash()))
            print('Prev Block Hash: {}'.format(block.prev_block_hash))
            print('TimeStamp: {}'.format(datetime.fromtimestamp(block.timestamp)))
            print('Nonce: {}'.format(block.nonce)) # 增加打印 nonce值
            print('Data: {}'.format(block.data))
            print('POW: {}'.format(self.pow.validate_block(block)))
            print('')

    def find_unspent_transactions(self, address):
        unspent_transactions = []
        spent_outputs = defaultdict(list)

        for block in self.blocks:
            for tx in block.data:
                if not isinstance(tx, CoinbaseTx):
                    for vin in tx.vins:
                       if vin.ref_address(address):
                           spent_outputs[vin.tx_id].append(vin.vout_idx)

                for idx, out in enumerate(tx.vouts):
                    if out.is_locked_with(address) == False:
                        continue
                    _spent_flag = False 
                    if len(spent_outputs[tx.id]) != 0:
                        for spent_idx in spent_outputs[tx.id]:
                            if spent_idx == idx:
                                _spent_flag = True
                                break
                    if _spent_flag==False:
                        unspent_transactions.append(tx) 
                
        return unspent_transactions

    def find_spendable_outputs(self, address, amount):
        accumulated = 0
        unspent_outputs = defaultdict(list)        

        unspent_txs = self.find_unspent_transactions(address)

        for tx in unspent_txs:
            for idx, out in enumerate(tx.vouts):
                if out.is_locked_with(address) and accumulated<amount:
                    accumulated += out.amount
                    unspent_outputs[tx.id].append(idx)
        
        return accumulated, unspent_outputs

    def find_utxo(self):
        utxos = defaultdict(list)
        spent_outputs = defaultdict(list)

        for block in self.blocks:
            for tx in block.data:
                if not isinstance(tx, CoinbaseTx):
                    for vin in tx.vins:
                        spent_outputs[vin.tx_id].append(vin.vout_idx)

                for idx, out in enumerate(tx.vouts):
                    _spent_flag = False 
                    if len(spent_outputs[tx.id]) != 0:
                        for spent_idx in spent_outputs[tx.id]:
                            if spent_idx == idx:
                                _spent_flag = True
                                break
                    if _spent_flag==False:
                        utxos[tx.id].append(out) 

        return utxos

    def find_transaction(self, tx_id):
        for block in self.blocks:
            for tx in block.data:
                if tx.id == tx_id:
                    return tx
        raise TransactionNotFound
    
    def sign_transaction(self, tx, sign_key):
        if isinstance(tx, CoinbaseTx):
            return
        tx.sign(sign_key)

    def verify_transaction(self, tx):
        if isinstance(tx, CoinbaseTx):
            return True
        utxo_set = UTXOSet(self)
        prev_utxos = {}

        for vin in tx.vins:
            prev_utxo = utxo_set.find_transaction_utxo(vin.tx_id)
            prev_utxos[vin.tx_id] = prev_utxo
        return tx.verify(prev_utxos)

    def get_best_height(self):
        height = 0
        try:
            last_block = self._db.get(self._tail)
            height = last_block.height
        except KeyError:
            height = 0

        return height 

    def add_block(self, block):
        if not self.pow.validate_block(block):
            print('Error: invalid block')
            return
        try:
            block_in_db = self._db.get(block.hash())
        except KeyError:
            self._db.put(block.hash(), block)

            last_block = self._db.get(self._tail)
            if block.height > last_block.height:
                self._db.put(BlockChain.LAST_BLOCK_HASH_KEY, block.hash())
                self._tail = block.hash()
            self._db.commit()

    def get_blockhashes(self):
        blocks_hash = list(self._db.kv.keys())
        blocks_hash.remove(BlockChain.LAST_BLOCK_HASH_KEY)
        return blocks_hash
    
    def get_block(self, block_hash):
        try:
            block = self._db.get(block_hash)
            return block
        except KeyError:
            return None
        

if __name__ == '__main__':
    bc = BlockChain('Newdao')
    print(bc.find_unspent_transactions('Newdao'))
    print(bc.find_spendable_outputs('Newdao', 30))