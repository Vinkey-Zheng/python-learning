# -*- encoding: utf-8 -*-
'''
------------------------------------------------------------
-文件        : wallets.py
-说明        : 钱包管理类的实现
-时间        : 2020/12/22 11:39:37
-作者        : newdao
------------------------------------------------------------
-版本号      ：myBlockchainV8
------------------------------------------------------------
'''
import pickle
import wallet

class Wallets(object):
    WALLETS_FILE_PATTERN= 'wallets_{}.db'

    def __init__(self, node_id):
        self.db_file = Wallets.WALLETS_FILE_PATTERN.format(node_id)
        try:
            with open(self.db_file, 'rb') as f:
                self._wallets = pickle.load(f)
        except FileNotFoundError:
            self._wallets = {}
    
    def create_wallet(self, comments=''):
        w = wallet.Wallet(comments)
        addr_str = w.address.get_address_str()
        self._wallets[addr_str] = w 
        return w

    def get_wallet(self, addr_str):
        return self._wallets[addr_str]

    def get_addresses(self):
        return [addr for addr in self._wallets.keys()]
    
    def save_to_file(self):
        with open(self.db_file, 'wb') as f:
            pickle.dump(self._wallets, f)