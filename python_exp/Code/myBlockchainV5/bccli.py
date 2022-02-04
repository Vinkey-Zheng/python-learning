import argparse
from Blockchain import BlockChain
from transaction import *


def print_chain(args):
    bc = BlockChain()
    bc.print_chain()


def createblockchain(args):
    args_dict = vars(args)
    account = args_dict['account']
    bc = BlockChain(account)
    print('Done!')


def getbalance(args):
    args_dict = vars(args)
    account = args_dict['account']

    bc = BlockChain()
    utxos = bc.find_utxo(account)
    balance = 0

    for out in utxos:
        balance += out.amount

    print('Balance of "{}": {}'.format(account, balance))


def send(args):
    args_dict = vars(args)
    from_account = args_dict['from']
    to_account = args_dict['to']
    amount = int(args_dict['amount'])

    bc = BlockChain()
    tx = UTXOTransaction(from_account, to_account, amount, bc)
    cb_tx = CoinbaseTx(from_account)
    tx_list = [cb_tx, tx]
    bc.mine_block(tx_list)
    print('Success!')


class BcCli(object):
    def __init__(self):
        self._parser = argparse.ArgumentParser()
        sub_parser = self._parser.add_subparsers(help='commands')

        # printchain command
        print_parser = sub_parser.add_parser(
                       'printchain', help='Print all the blocks of the blockchain.')
        print_parser.set_defaults(func=print_chain)

        # createblockchain command
        createchain_parser = sub_parser.add_parser('createblockchain',
                                                   help='Create a blockchain and send '
                                                        'genesis block reward to ACCOUNT')
        createchain_parser.add_argument('-a', '--account', required=True, help='account')
        createchain_parser.set_defaults(func=createblockchain)

        # getbalance command
        balance_parser = sub_parser.add_parser('getbalance', help='Get balance of account')
        balance_parser.add_argument('-a', '--account', required=True, help='account')
        balance_parser.set_defaults(func=getbalance)

        # send command
        send_parser = sub_parser.add_parser('send', help='Send AMOUNT of coins from '
                                                         'FROM account to TO')
        send_parser.add_argument('-f', '--from', required=True, help='from account')
        send_parser.add_argument('-t', '--to', required=True, help='to account')
        send_parser.add_argument('-m', '--amount', required=True, help='amount')
        send_parser.set_defaults(func=send)

    def run(self):
        args = self._parser.parse_args()
        if hasattr(args, 'func'):
            args.func(args)


if __name__ == '__main__':
    bccli = BcCli()
    bccli.run()
# createblockchain
# 功能：创建或打开一个新的区块链，新创建区块链时，可通过参数指定创世块的铸币交易的输出账户。
# 使用方法：python bccli.py createblockchain -a INIT_ACCOUNT
# getblance
# 功能：获取某个账户的余额信息
# 使用方法：python bccli.py getbalance -a INIT_ACCOUNT
# send
# 功能：让一个指定账户向另一个指定账户支付一定数目的比特币
# 使用方法：python bccli.py send -f INIT_ACCOUNT -t TO_ACCOUNT -m 50
