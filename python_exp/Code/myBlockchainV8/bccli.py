# -*- encoding: utf-8 -*-
'''
------------------------------------------------------------
-文件        : bccli.py
-说明        : 区块链命令行接口实现
-时间        : 2020/11/18 11:40:37
-作者        : newdao
------------------------------------------------------------
-版本号      ：myBlockchainV8
------------------------------------------------------------
'''
'''
python3 bccli.py printchain -n NODE_ID
python3 bccli.py createblockchain -a ADDRESS -n NODE_ID
python3 bccli.py getblance -a ADDRESSS -n NODE_ID
python3 bccli.py send -f FROM_ADDRESS -t TO_ADDRESS -m AMOUNT -n NODE_ID [-mine]
python3 bccli.py createwallet -n NODE_ID
python3 bccli.py printwallets -n NODE_ID
python3 bccli.py startnode -n NODE_ID [-a MINER_ADDRESS]
'''
import argparse
from blockchain import BlockChain
from transaction import *
import wallets
from address import Address
from utxo_set import UTXOSet
from server import Server
from message import BcMsg


def print_chain(args):
    args_dict = vars(args)
    node_id = int(args_dict['node'])

    bc = BlockChain(node_id)
    bc.print_chain()

def createblockchain(args):
    args_dict = vars(args)
    addr_str = args_dict['address']
    node_id = int(args_dict['node'])

    bc = BlockChain(node_id, Address(address_str=addr_str))
    utxo_set = UTXOSet(bc)
    utxo_set.rebuild()

    print('Done!')

def getblance(args):
    args_dict = vars(args)
    addr_str = args_dict['address']
    node_id = int(args_dict['node'])

    bc = BlockChain(node_id)
    utxo_set = UTXOSet(bc)
    utxos = utxo_set.find_utxo(Address(address_str=addr_str))
    blance = 0

    for out in utxos:
        blance += out.amount

    print('Blance of "{}": {}'.format(addr_str, blance))

def send(args):
    args_dict = vars(args)
    from_address_str = args_dict['from']
    to_address_str = args_dict['to']
    amount = int(args_dict['amount'])
    node_id = int(args_dict['node'])

    bc = BlockChain(node_id)
    utxo_set = UTXOSet(bc)
    from_address = Address(address_str=from_address_str)
    to_address = Address(address_str=to_address_str)
    ws = wallets.Wallets(node_id)
    w = ws.get_wallet(from_address_str)
    tx = UTXOTransaction(w, to_address, amount, utxo_set)
    bc.sign_transaction(tx, w.sign_key)
    if args.mine:
        print('miner now')
        cb_tx = CoinbaseTx(from_address)
        bc.sign_transaction(cb_tx, w.sign_key)
        tx_list = [cb_tx, tx]
        new_block = bc.mine_block(tx_list)
        utxo_set.update(new_block)
    else :
        BcMsg('tx', 'localhost:{}'.format(node_id), tx).send_msg(Server.CENTRAL_NODE)
    print('Success!')

def createwallet(args):
    args_dict = vars(args)
    node_id = int(args_dict['node'])

    ws = wallets.Wallets(node_id)
    w = ws.create_wallet()
    ws.save_to_file()
    print('Your new address: {}'.format(w.address.get_address_str()))

def printwallets(args):
    args_dict = vars(args)
    node_id = int(args_dict['node'])

    ws = wallets.Wallets(node_id)
    print('Walltes List:')
    print('=====================================\n')
    for addr in ws.get_addresses():
        print(addr)
    print('\n=====================================')

def startnode(args):
    args_dict = vars(args)
    node_id = int(args_dict['node'])
    print('startnode', node_id, flush=True)
    addr_str = ''
    try:
        addr_str = args_dict['address']
    except KeyError:
        addr_str = ''
    if addr_str and not Address.is_valid_address_str(addr_str):
        print('Error: wrong miner address!')
        return
    server = Server(node_id, addr_str)
    server.run()


class BcCli(object):
    def __init__(self):
        self._parser = argparse.ArgumentParser()
        sub_parser = self._parser.add_subparsers(help='commands')

        # printchain command
        print_parser = sub_parser.add_parser(
                       'printchain', help='Print all the blocks of the blockchain.')
        print_parser.add_argument('-n','--node', required=True, help='node id')
        print_parser.set_defaults(func=print_chain)

        # createblockchain command
        createchain_parser = sub_parser.add_parser('createblockchain', help='Create a blockchain and send genesis block reward to ADDRESS')
        createchain_parser.add_argument('-n','--node', required=True, help='node id')
        createchain_parser.add_argument('-a','--address', required=True, help='address')
        createchain_parser.set_defaults(func=createblockchain)

        # getblance command
        blance_parser = sub_parser.add_parser('getblance', help='Get balance of address')
        blance_parser.add_argument('-a','--address', required=True, help='address')
        blance_parser.add_argument('-n','--node', required=True, help='node id')
        blance_parser.set_defaults(func=getblance)

        # send command
        send_parser = sub_parser.add_parser('send', help='Send AMOUNT of coins from FROM address to TO')
        send_parser.add_argument('-f','--from', required=True, help='from address')
        send_parser.add_argument('-t','--to', required=True, help='to address')
        send_parser.add_argument('-m','--amount', required=True, help='amount')
        send_parser.add_argument('-n','--node', required=True, help='node id')
        send_parser.add_argument('-mine', action='store_true', help='Mine immediately on the same node')
        send_parser.set_defaults(func=send)

        # createwallet command
        wallet_parser = sub_parser.add_parser('createwallet', help='Create a wallet')
        wallet_parser.add_argument('-n','--node', required=True, help='node id')
        wallet_parser.set_defaults(func=createwallet)

        # printwallets command
        wallets_parser = sub_parser.add_parser('printwallets', help='Print wallet list')
        wallets_parser.add_argument('-n','--node', required=True, help='node id')
        wallets_parser.set_defaults(func=printwallets)

        # startnode command 
        node_parser = sub_parser.add_parser('startnode', help='Start a blockchain node')
        node_parser.add_argument('-n','--node', required=True, help='node id')
        node_parser.add_argument('-a','--address', help='miner address')
        node_parser.set_defaults(func=startnode)


    def run(self):
        args = self._parser.parse_args()
        if hasattr(args, 'func'):
            args.func(args)


if __name__ == '__main__':
    bccli = BcCli()
    bccli.run()
