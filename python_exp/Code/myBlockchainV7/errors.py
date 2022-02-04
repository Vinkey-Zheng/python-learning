
# 区块链已经存在
class BlockchainAlreadyExists(Exception):
    pass


class NeedInitAccount(Exception):
    pass


# 未找到指定交易
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
