import time
import hashlib


class Block(object):
    def __init__(self, transaction_list, prev_block_hash=''):
        self.timestamp = int(time.time())
        self.prev_block_hash = prev_block_hash
        self.data = transaction_list
        self.nonce = 0
        self.data_hash = hashlib.sha256(''.join([tx.hash()
                                                 for tx in transaction_list]
                                                ).encode('utf-8')).hexdigest()

    def hash(self):
        data_list = [str(self.nonce), str(self.timestamp), self.prev_block_hash, self.data_hash]
        return hashlib.sha256(''.join(data_list).encode('utf-8')).hexdigest()

    def __repr__(self):
        s = 'Block(Hash={}, TimeStamp={}, PrevBlockHash={}, Nonce={}, \
        Data={}, DataHash={})'
        return s.format(self.hash(), self.timestamp, self.prev_block_hash, self.nonce, self.data, self.data_hash)
