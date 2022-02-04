# -*- encoding: utf-8 -*-
'''
------------------------------------------------------------
-文件        : address.py
-说明        : 比特币地址实现类
-时间        : 2020/12/30 15:22:35
-作者        : newdao
------------------------------------------------------------
-版本号      ：myBlockchainV8
------------------------------------------------------------
'''
from binascii import hexlify, unhexlify
import base58
import hashlib
from errors import InvalidAddressString, AddressParamError

class Address(object):
    ADDRESS_VERSION = 0
    def __init__(self, verify_key=None, address_str=None):
        if verify_key != None:
            # 生成验证密钥的散列值
            ripemd160 = hashlib.new('ripemd160')
            ripemd160.update(hashlib.sha256(verify_key.to_string()).digest())
            verify_key_hash = ripemd160.hexdigest()

            # 加上版本号
            version = Address.ADDRESS_VERSION
            payload = ('{:0>2x}'.format(version)) + verify_key_hash

            # 生成验证码
            checksum = hashlib.sha256(hashlib.sha256(unhexlify(payload)).digest()).digest()[:4]
            self.address_str = base58.base58_encode(payload+hexlify(checksum).decode('ascii'))
        elif address_str != None:
            if Address.is_valid_address_str(address_str):
                self.address_str = address_str
            else:
                raise InvalidAddressString()
        else:
            raise AddressParamError()

    def __eq__(self, other):
        return type(self)==type(other) and self.address_str==other.address_str

    def __repr__(self):
        return self.address_str

    def get_address_str(self):
        return self.address_str

    @staticmethod
    def is_valid_address_str(address_str):
        base58_decode_str = base58.base58_decode(address_str)
        base58_decode_bytes = unhexlify(base58_decode_str)
        if len(base58_decode_bytes) < 4:
            print('len < 4')
            return False
        version = base58_decode_bytes[0]
        if version!=Address.ADDRESS_VERSION:
            print('version error', version)
            return False
        checksum1 = hashlib.sha256(hashlib.sha256(base58_decode_bytes[:-4]).digest()).digest()[:4]
        checksum2 = base58_decode_bytes[-4:]
        if checksum1!=checksum2:
            print('checksum compare error', checksum1, checksum2)
            return False
        return True
        
# 单元测试代码
if __name__ == '__main__':
    import ecdsa
    sk1 = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
    vk1 = sk1.get_verifying_key()
    a1 = Address(vk1)
    a2 = Address(vk1)
    print('a1:',a1)
    assert(Address.is_valid_address_str(a1.get_address_str()))
    sk2 = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
    vk2 = sk2.get_verifying_key()
    a3 = Address(vk2)
    a4 = Address(address_str='1GR3u7Lnq8NnHR8aW62h6shXishMTd6FCs')
    try:
        a5 = Address(address_str='12323') #非法的地址
    except InvalidAddressString:
        print('InvalidAddressString')
    print('a3:',a3)
    assert(a1==a2)
    assert(a1!=a3)
    assert(not Address.is_valid_address_str('123234243')) #非法的地址
    assert(not Address.is_valid_address_str('2BU3EyZpAPethrchnNwZp86uZdQ6kzRHjN')) #非法的地址
    assert(not Address.is_valid_address_str('1BU3EyZpAPethrchnNwZp86uZdQ6kzRHjx')) #非法的地址
    assert(not Address.is_valid_address_str('1BU3EyZpAPe1hrchnNwZp86uZdQ6kzRHjN')) #非法的地址