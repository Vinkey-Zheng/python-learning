# -*- encoding: utf-8 -*-
'''
------------------------------------------------------------
-文件        : base58.py
-说明        : base58编解码算法实现
-时间        : 2020/12/23 08:57:13
-作者        : newdao
------------------------------------------------------------
-版本号      ：myBlockchainV8
------------------------------------------------------------
'''
import sys
from binascii import hexlify, unhexlify

BASE58_ALPHABET = b"123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
BASE58 = 58
BASE256 = 256

def base58_encode(data):
    """
    * data : 编码前十六进制形式的字符串
    * 返回值： base58编码的字符串
    """
    bytes_str = unhexlify(data)

    n = 0
    for c in bytes_str:
        n = n * BASE256 + c

    result = []
    while n>=BASE58:
        n, mod = divmod(n, BASE58)
        result.append(BASE58_ALPHABET[mod])
    else:
        result.append(BASE58_ALPHABET[n])

    for c in bytes_str:
        if c==0:
            result.append(BASE58_ALPHABET[0])
        else:
            break

    result.reverse()

    return bytes(result).decode('ascii')

def base58_decode(base58_str):
    """
    * base58_str: base58编码的字符串
    * 返回值: 解码后十六进制形式的字符串
    """
    bytes_str = base58_str.encode('ascii')
    n = 0

    for c in bytes_str:
        index = BASE58_ALPHABET.find(c)
        n = n*BASE58 + index
    
    result = []
    while n>=BASE256:
        n, mod = divmod(n, BASE256)
        result.append(mod)
    else:
        result.append(n)

    for c in bytes_str:
        if c == ord('1'):
            result.append(0)
        else :
            break

    result.reverse()
    return hexlify(bytes(result)).decode('ascii')

# 单元测试代码
if __name__ == '__main__':
    import ecdsa
    sk = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
    vk = sk.get_verifying_key()

    hex_str = hexlify(vk.to_string()).decode('ascii')
    print('hex_str: ', hex_str)

    base58_str = base58_encode(hex_str)
    print('base58_str: '+base58_str) 
    assert(hex_str==base58_decode(base58_str))

    zero_leading_str = '0000123456'    
    print('zero_leading_str: ', zero_leading_str)
    base58_str2 = base58_encode(zero_leading_str)
    print('base58_str2: ', base58_str2)
    assert(zero_leading_str==base58_decode(base58_str2))