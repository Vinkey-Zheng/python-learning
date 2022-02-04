from datetime import datetime
from block import Block


class BlockChain(object):
    def __init__(self):
        print('Created a new blockchain.\n')
        self.chain = []
        genesis_block = Block('This is a genesis block')
        self.chain.append(genesis_block)

    def add_block(self, data):
        new_block = Block(data, self.chain[-1].hash())
        self.chain.append(new_block)

    def print_chain(self):
        for block in self.chain:
            print('Block Hash: {}'.format(block.hash()))
            print('Prev Block Hash: {}'.format(block.prev_block_hash))
            print('TimeStamp: {}'.format(datetime.fromtimestamp(block.timestamp)))
            print('Data: {}'.format(block.data))
            print('')
