import time
import hashlib


class Block(object):
    def __init__(self, data, prev_block_hash=''):
        self.timestamp = int(time.time())  # 初始化时间戳
        self.prev_block_hash = prev_block_hash  # 初始化前一个区块的哈希值，默认为''
        self.data = data  # 初始化数据
        self.nonce = 0  # 添加 nonce 成员，初始值为 0
        self.data_hash = hashlib.sha256(data.encode('utf-8')).hexdigest()  # 初始化当前区块的哈希值

    def hash(self):  # 计算散列值时，同样加入 nonce值
        data_list = [str(self.nonce), str(self.timestamp),
                     self.prev_block_hash, self.data_hash]
        return hashlib.sha256(''.join(data_list).encode('utf-8')).hexdigest()

    def __repr__(self):  # 打印输出，同样加入 nonce值
        return 'Block(Hash={}, TimeStamp={}, PrevBlockHash={}, Nonce={}, \
        Data={}, DataHash={})'.format(self.hash(), self.timestamp,
                                      self.prev_block_hash, self.nonce, self.data, self.data_hash)

