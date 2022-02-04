import argparse
from Blockchain import BlockChain
from utxo_set import UTXOSet
from transaction import *
import wallets
import address


def print_chain(args):
    bc = BlockChain()
    bc.print_chain()


def createblockchain(args):
    args_dict = vars(args)
    addr_str = args_dict['address']

    bc = BlockChain(address.Address(address_str=addr_str))
    # 构建UTXOSet类， 并从去区块中同步数据
    utxo_set = UTXOSet(bc)
    utxo_set.rebuild()
    print('Done!')


def getbalance(args):
    args_dict = vars(args)
    addr_str = args_dict['address']
    bc = BlockChain()
    utxo_set = UTXOSet(bc)
    utxos = utxo_set.find_utxo(address.Address(address_str=addr_str))
    balance = 0
    for out in utxos:
        balance += out.amount

    print('Balance of "{}": {}'.format(addr_str, balance))


def send(args):
    args_dict = vars(args)
    from_address_str = args_dict['from']
    to_address_str = args_dict['to']
    amount = int(args_dict['amount'])

    bc = BlockChain()
    utxo_set =UTXOSet(bc)
    from_address = address.Address(address_str=from_address_str)
    to_address = address.Address(address_str=to_address_str)
    ws = wallets.Wallets()
    w = ws.get_wallet(from_address_str)
    tx = UTXOTransaction(from_address, to_address, amount, utxo_set)
    bc.sign_transaction(tx, w.sign_key)
    cb_tx = CoinbaseTx(from_address)
    bc.sign_transaction(cb_tx, w.sign_key)
    tx_list = [cb_tx, tx]
    new_block =bc.mine_block(tx_list)
    bc.mine_block(tx_list)
    # 更新UTXO集
    utxo_set.update(new_block)
    print('Success!')


def createwallet(args):
    ws = wallets.Wallets()
    w = ws.create_wallet()
    ws.save_to_file()
    print('Your new address:{}'.format(w.address.get_address_str()))


def printwallets(args):
    ws = wallets.Wallets()
    print('Wallets List:')
    print('=====================================\n')
    for addr in ws.get_addresses():
        print(addr)
    print('\n=====================================')


class BcCli(object):
    def __init__(self):
        self._parser = argparse.ArgumentParser()
        sub_parser = self._parser.add_subparsers(help='commands')

        # printchain command
        print_parser = sub_parser.add_parser(
                       'printchain', help='Print all '
                                          'the blocks '
                                          'of the blockchain.')
        print_parser.set_defaults(func=print_chain)

        # createblockchain command
        createchain_parser = sub_parser.add_parser('createblockchain',
                                                   help='Create a blockchain and send '
                                                        'genesis block reward to ADDRESS')
        createchain_parser.add_argument('-a', '--address', help='address')
        createchain_parser.set_defaults(func=createblockchain)

        # getbalance command
        balance_parser = sub_parser.add_parser('getbalance', help='Get balance of address')
        balance_parser.add_argument('-a', '--address', required=True, help='address')
        balance_parser.set_defaults(func=getbalance)

        # send command
        send_parser = sub_parser.add_parser('send', help='Send AMOUNT of coins from '
                                                         'FROM address to TO')
        send_parser.add_argument('-f', '--from', required=True, help='from address')
        send_parser.add_argument('-t', '--to', required=True, help='to address')
        send_parser.add_argument('-m', '--amount', required=True, help='amount')
        send_parser.set_defaults(func=send)

        # ceatewallet command
        wallet_parser = sub_parser.add_parser('createwallet',
                                              help='Create a wallet')
        wallet_parser.set_defaults(func=createwallet)

        # printwallets command
        wallet_parser = sub_parser.add_parser('printwallets',
                                              help='Print wallet list')
        wallet_parser.set_defaults(func=printwallets)

    def run(self):
        args = self._parser.parse_args()
        if hasattr(args, 'func'):
            args.func(args)


if __name__ == '__main__':
    bccli = BcCli()
    bccli.run()
# python bccli.py printchain
# python bccli.py createblockchain -a ADDRESS
# python bccli.py getbalance -a ADDRESSS
# python bccli.py send -f FROM_ADDRESS -t TO_ADDRESS -m AMOUNT
# python bccli.py createwallet
# python bccli.py printwallets
