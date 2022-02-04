# -*- encoding: utf-8 -*-
'''
------------------------------------------------------------
-文件        : transaction_output.py
-说明        : 
-时间        : 2020/12/04 10:09:32
-作者        : newdao
------------------------------------------------------------
-版本号      ：myBlockchainV8
------------------------------------------------------------
'''
class TXOutput(object):
    def __init__(self, address, amount):
        self.address = address
        self.amount = amount

    def is_locked_with(self, address):
        return self.address == address

    def __repr__(self):
        return "TXOutput(address={}, amount={})".format(self.address, self.amount)