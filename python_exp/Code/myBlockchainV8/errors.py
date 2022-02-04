# -*- encoding: utf-8 -*-
'''
------------------------------------------------------------
-文件        : errors.py
-说明        : 定义各种异常
-时间        : 2021/01/11 19:26:00
-作者        : newdao
------------------------------------------------------------
-版本号      ：myBlockchainV8
------------------------------------------------------------
'''

# 区块链已经存在
class BlockchainAlreadyExists(Exception):
    pass

# 创建区块链需要指定初始账号地址
class NeedInitAccount(Exception):
    pass

# 未找到指定的交易
class TransactionNotFound(Exception):
    pass

# 无效的地址格式
class InvalidAddressString(Exception):
    pass

# 地址参数错误
class AddressParamError(Exception):
    pass

# 余额不足
class NotEnoughFundsError(Exception):
    pass

# 无效消息类型
class UnknownMsg(Exception):
    pass