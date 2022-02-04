# -*- encoding: utf-8 -*-
'''
------------------------------------------------------------
-文件        : transaction_input.py
-说明        : 
-时间        : 2020/12/04 10:35:12
-作者        : newdao
------------------------------------------------------------
-版本号      ：myBlockchainV8
------------------------------------------------------------
'''
import address

class TXInput(object):
    def __init__(self, tx_id, vout_idx, signature, verify_key):
        self.tx_id = tx_id
        self.vout_idx = vout_idx
        self.signature = signature
        self.verify_key = verify_key

    def ref_address(self, addr):
        return address.Address(self.verify_key) == addr

    def __repr__(self):
        return 'TXInput(tx_id={}, vout_idx={}, signature={})'.format(self.tx_id, self.vout_idx, self.signature)