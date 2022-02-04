# -*- encoding: utf-8 -*-
'''
------------------------------------------------------------
-文件        : wallet.py
-说明        : 钱包类的实现
-时间        : 2020/12/22 14:21:07
-作者        : newdao
------------------------------------------------------------
-版本号      ：myBlockchainV8
------------------------------------------------------------
'''
import ecdsa
import address

class Wallet(object):
    def __init__(self, comments=''):
        self.comments = comments
        self.sign_key = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
        self.verify_key = self.sign_key.get_verifying_key()

        self.address = address.Address(self.verify_key)

    def __repr__(self):
        return 'Wallet(address={}, comments="{}")'.format(self.address, self.comments)

if __name__ == '__main__':
    w = Wallet('Newdao\'s wallet')
    print(w)