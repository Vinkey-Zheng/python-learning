from block import Block
from datetime import datetime
from proofofwork import ProofOfWork
from db import DB


class BlockChain(object):
    LAST_BLOCK_HASH_KEY = 'Last'
    DB_FILE = './bc_block.db'

    def __init__(self):
        print('Created a new blockchain.\n')
        self.pow = ProofOfWork()
        self._db = DB(BlockChain.DB_FILE)
        try:
            self._tail = self._db.get(BlockChain.LAST_BLOCK_HASH_KEY)
        except KeyError:
            genesis_block = self.pow.mine_block('This is a genesis block')
            self._put_block(genesis_block)

    def _put_block(self, block):
        self._db.put(block.hash(), block)
        self._db.put(BlockChain.LAST_BLOCK_HASH_KEY, block.hash())
        self._db.commit()
        self._tail = block.hash()

    def mine_block(self, data):
        new_block = self.pow.mine_block(data, self._tail)
        self._put_block(new_block)

    @property
    def blocks(self):
        current = self._tail
        while True:
            if not current:
                return
            block = self._db.get(current)
            yield block
            current = block.prev_block_hash

    def print_chain(self):
        for block in self.blocks:
            print('Block hash: {}'.format(block.hash()))
            print('Prey Block Hash: {}'.format(block.prev_block_hash))
            print('TimeStamp: {}'.format(datetime.fromtimestamp(block.timestamp)))
            print('Nonce: {}'.format(block.nonce))
            print('Data: {}'.format(block.data))
            print('POW: {}'.format(self.pow.validate_block(block)))
            print('')
