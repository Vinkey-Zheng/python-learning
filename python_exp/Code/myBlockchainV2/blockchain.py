from block import Block
from datetime import datetime
from proofofwork import ProofOfWork


class BlockChain(object):
    def __init__(self):
        print('Created a new blockchain.\n')
        self.chain = []
        self.pow = ProofOfWork()  # 创建工作量证明类
        genesis_block = self.pow.mine_block('This is a genesis block') # 通过工作量证明类来挖出创世区块
        self.chain.append(genesis_block)

    # 挖出一个数据为data的区块
    def mine_block(self, data):
        new_block = self.pow.mine_block(data, self.chain[-1].hash())
        self.chain.append(new_block)

    def print_chain(self):
        for block in self.chain:
            print('Block Hash: {}'.format(block.hash()))
            print('Prev Block Hash: {}'.format(block.prev_block_hash))
            print('TimeStamp: {}'.format(datetime.fromtimestamp(block.timestamp)))
            print('Nonce: {}'.format(block.nonce)) # 增加打印 nonce值
            print('Data: {}'.format(block.data))
            print('POW: {}'.format(self.pow.validate_block(block))) # 校验区块
            print('')
