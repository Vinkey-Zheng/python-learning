from blockchain import BlockChain


if __name__ == '__main__':
    # 创建区块链
    block_chain = BlockChain()

    # 挖出第一个区块
    block_chain.mine_block('Send 1 BTC to Ivan')
    # 挖出第二个区块
    block_chain.mine_block('Send 2 more BTC to Ivan')

    # 打印整个区块链的信息
    block_chain.print_chain()
