import sys
from block import Block


class ProofOfWork(object):
    MAX_NONCE = sys.maxsize

    def __init__(self, difficulty_bits=12):
        self.target = 1 << (256-difficulty_bits)

    def mine_block(self, data, prev_hash=''):
        print('Mining the block containing"{}"'.format(data))
        tmp_block = Block(data, prev_hash)
        while tmp_block.nonce < ProofOfWork.MAX_NONCE:
            hash_int = int(tmp_block.hash(), 16)
            if hash_int < self.target:
                break
            else:
                tmp_block.nonce += 1
        return tmp_block

    def validate_block(self, block):
        hash_int = int(block.hash(), 16)
        return True if hash_int < self.target else False
