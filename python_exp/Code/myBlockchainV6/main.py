from block import Block
from Blockchain import BlockChain


if __name__ == '__main__':
    block_chain = BlockChain()
    block_chain.mine_block('Send 1 BTC to Ivan')
    block_chain.mine_block('Send 2 more BTC to Ivan')
    block_chain.print_chain()
