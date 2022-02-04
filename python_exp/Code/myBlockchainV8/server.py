# -*- encoding: utf-8 -*-
'''
------------------------------------------------------------
-文件        : server.py
-说明        : TCP 服务端实现
-时间        : 2021/01/18 16:43:56
-作者        : newdao
------------------------------------------------------------
-版本号      ：myBlockchainV8
------------------------------------------------------------
'''
from socketserver import ThreadingTCPServer, StreamRequestHandler
from blockchain import BlockChain
from message import BcMsg


class BlockchainHanlder(StreamRequestHandler):
    def handle(self):
        msg = BcMsg('').recv_msg(self.request)
        msg.handler(self.server)

class Server(ThreadingTCPServer):
    CENTRAL_NODE = 'localhost:3000'
    def __init__(self, node_id, miner_address_str):
        # open the blockchain
        self.blockchain = BlockChain(node_id)
        self.node_address = 'localhost:{}'.format(node_id)
        self.known_nodes = [Server.CENTRAL_NODE]
        self.miner_address_str = miner_address_str
        self.blocks_in_transit = []
        self.mempool = {}

        # running a blockchain node
        host, port = self.node_address.split(':') 
        port = int(port)
        super().__init__((host, port), BlockchainHanlder)

        if self.node_address != Server.CENTRAL_NODE:
            BcMsg('version', self.node_address, self.blockchain.get_best_height()).send_msg(Server.CENTRAL_NODE)

    def run(self):
        print('Node({}) is running...'.format(self.node_address))
        self.serve_forever()



if __name__ == '__main__':
    server = Server(3001, '1y246yaVqborJQgsiKKaJ9mmCB7Rziodj')
    server.run()