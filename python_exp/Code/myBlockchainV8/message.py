# -*- encoding: utf-8 -*-
'''
------------------------------------------------------------
-文件        : message.py
-说明        : 消息协议实现
-时间        : 2021/01/25 09:34:10
-作者        : newdao
------------------------------------------------------------
-版本号      ：myBlockchainV8
------------------------------------------------------------
'''
import socket
import pickle
import struct
from address import Address
from utxo_set import UTXOSet
from transaction import CoinbaseTx
from errors import UnknownMsg

class CmdVersionBody(object):
    def __init__(self, source_addr, best_height):
        self.source_addr = source_addr
        self.best_height = best_height

    def handler(self, server):
        print('>> Handle version msg({})'.format(self))
        print('==================')
        bc = server.blockchain
        local_best_height = bc.get_best_height()
        peer_best_height = self.best_height

        if local_best_height < peer_best_height:
            BcMsg('getblocks', server.node_address).send_msg(self.source_addr)
        elif local_best_height > peer_best_height:
            BcMsg('version', server.node_address, bc.get_best_height()).send_msg(self.source_addr)
        else:
            print('Same best_height do nothing.')

        if self.source_addr not in server.known_nodes:
            server.known_nodes.append(self.source_addr)
        print('')

    def __repr__(self):
        return 'CmdVersion(source_addr:{}, best_height:{})'.format(self.source_addr, self.best_height)

class CmdBlockBody(object):
    def __init__(self, source_addr, block):
        self.source_addr = source_addr
        self.block = block

    def handler(self, server):
        print('>> Handle block msg({})'.format(self))
        print('==================')
        print('Recevied a new block!')
        bc = server.blockchain
        bc.add_block(self.block)
        print('Added block {}'.format(self.block.hash()))

        if len(server.blocks_in_transit) > 0 :
            block_hash = server.blocks_in_transit[0]
            BcMsg('getdata', server.node_address, 'block', block_hash).send_msg(self.source_addr)
            del(server.blocks_in_transit[0])
        else :
            utxo_set = UTXOSet(bc)
            utxo_set.rebuild()
        print('')

    def __repr__(self):
        return 'CmdBlock(source_addr:{}, block:{})'.format(self.source_addr, self.block.hash())

class CmdGetBLocksBody(object):
    def __init__(self, source_addr):
        self.source_addr = source_addr

    def handler(self, server):
        print('>> Handle getblocks msg({})'.format(self))
        print('==================')
        bc = server.blockchain
        blocks_hash = bc.get_blockhashes()
        BcMsg('inv', server.node_address, 'block', blocks_hash).send_msg(self.source_addr)
        print('')

    def __repr__(self):
        return 'CmdGetBlocks(source_addr:{})'.format(self.source_addr)

class CmdGetDataBody(object):
    def __init__(self, source_addr, data_type, data_id):
        self.source_addr = source_addr
        self.data_type = data_type
        self.data_id = data_id

    def handler(self, server):
        print('>> Handle getdata msg({})'.format(self))
        print('==================')
        bc = server.blockchain
        if self.data_type == 'block':
            block = bc.get_block(self.data_id)
            if block!=None:
                BcMsg('block', server.node_address, block).send_msg(self.source_addr)
            else:
                print('Error: Block not found!')
        elif self.data_type == 'tx':
            try:
                tx = server.mempool[self.data_id] 
                BcMsg('tx', server.node_address, tx).send_msg(self.source_addr)
            except KeyError:
                print('Error: Tx not found!')
        print('')

    def __repr__(self):
        return 'CmdGetData(source_addr:{}, type:{}, id:{})'.format(self.source_addr, self.data_type, self.data_id)

class CmdInvBody(object):
    def __init__(self, source_addr, data_type, items):
        self.source_addr = source_addr
        self.data_type = data_type
        self.items = items

    def handler(self, server):
        print('>> Handle inv msg({})'.format(self))
        print('==================')
        if self.data_type == 'block':
            server.blocks_in_transit = self.items
            block_hash = self.items[0]
            BcMsg('getdata', server.node_address, 'block', block_hash).send_msg(self.source_addr)
            server.blocks_in_transit.remove(block_hash)
        elif self.data_type == 'tx':
            tx_id = self.items[0]
            if tx_id not in server.mempool.keys() :
                BcMsg('getdata', server.node_address, 'tx', tx_id).send_msg(self.source_addr)
        print('')

    def __repr__(self):
        return 'CmdInv(source_addr:{}, type:{}, items:{})'.format(self.source_addr, self.data_type, self.items)

class CmdTXBody(object):
    def __init__(self, source_addr, transaction):
        self.source_addr = source_addr
        self.transaction = transaction

    def handler(self, server):
        print('>> Handle tx msg({})'.format(self))
        print('==================')
        tx = self.transaction
        bc = server.blockchain
        server.mempool[tx.id] = tx
        print('Added tx(id:{}) to mempool(len:{})'.format(tx.id, len(server.mempool.values())))

        if server.node_address == server.known_nodes[0]:
            for node in server.known_nodes:
                if node != server.node_address and node != self.source_addr:
                    BcMsg('inv', server.node_address, 'tx', [tx.id]).send_msg(node)
        elif len(server.mempool.values()) > 1 and len(server.miner_address_str) > 0:
            while len(server.mempool.values()) > 0:
                txs = []
                tx_ids = []
                for tx_id, tx in server.mempool.items():
                    if bc.verify_transaction(tx):
                        txs.append(tx)
                        tx_ids.append(tx_id)
                
                if len(txs) == 0:
                    print('All transactions are invalid! Waiting for new ones...')
                    return
                cb_tx = CoinbaseTx(Address(address_str=server.miner_address_str))
                txs.append(cb_tx)

                new_block = bc.mine_block(txs)
                utxo_set = UTXOSet(bc)
                utxo_set.update(new_block)
                print('Mined a newblock(hash:{})'.format(new_block.hash()))

                for tx_id in tx_ids:
                    del(server.mempool[tx_id])

                for node in server.known_nodes:
                    if node != server.node_address:
                        BcMsg('inv', server.node_address, 'block', [new_block.hash()]).send_msg(node)
        print('')

    def __repr__(self):
        return 'CmdTX(source_addr:{}, transaction:{})'.format(self.source_addr, self.transaction.id)

cmd_body_constructor = {
    'version':CmdVersionBody,
    'block':CmdBlockBody,
    'inv':CmdInvBody,
    'getblocks':CmdGetBLocksBody,
    'getdata':CmdGetDataBody,
    'tx':CmdTXBody,
}

class BcMsg(object):
    MSG_PACKER = struct.Struct('12p H')
    MSG_HEAD_SIZE = MSG_PACKER.size
    def __init__(self, cmd, *args):
        self.cmd = cmd
        if cmd:
            try:
                constructor = cmd_body_constructor[self.cmd]
            except KeyError:
                print('Unknown msg {}'.format(self.cmd))
                raise UnknownMsg()
            self.body = constructor(*args)
        else:
            self.body = None

    def handler(self, server):
        if hasattr(self.body,'handler'):
            self.body.handler(server)
        else:
            print('Can\'t handle msg({})'.format(self.cmd))

    def _pack_msg(self): 
        body_bytes = pickle.dumps(self.body)
        return BcMsg.MSG_PACKER.pack(self.cmd.encode('ascii'), len(body_bytes)) + body_bytes

    def send_msg(self, target):
        print('Send msg({}) to {}'.format(self.body, target))
        BcMsg._send_data(BcMsg._unpack_address(target), self._pack_msg())

    def recv_msg(self, the_socket):
        msg_head_bytes = the_socket.recv(BcMsg.MSG_HEAD_SIZE)
        cmd, data_len = BcMsg.unpack_msg_head(msg_head_bytes)
        cmd_body_bytes = the_socket.recv(data_len)
        self.cmd = cmd
        self.body = pickle.loads(cmd_body_bytes)
        return self
    
    @staticmethod
    def unpack_msg_head(msg_head_bytes):
        cmd, data_len = BcMsg.MSG_PACKER.unpack(msg_head_bytes)
        cmd = cmd.decode('ascii')
        return cmd, data_len

    @staticmethod
    def _send_data(target, data):    
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect(target)
            sock.sendall(data)
    
    @staticmethod
    def _unpack_address(address_str):
        host, port = address_str.split(':') 
        port = int(port)
        return (host, port)     
 