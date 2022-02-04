from blockchain import BlockChain


if __name__ == '__main__':
    # 创建区块链
    block_chain = BlockChain()

    # 添加第一个区块到区块链中
    block_chain.add_block('Send 1 BTC to Ivan')
    # 添加第二个区块到区块链中
    block_chain.add_block('Send 2 more BTC to Ivan')

    # 打印整个区块链的信息
    block_chain.print_chain()
