import rsa

# 创建签名公钥对
(verifykey, signkey) = rsa.newkeys(512)

# 计算消息的散列值
message = b"I like blockchain."
message_hash = rsa.compute_hash(message, 'SHA-1')

# 生成数字签名
signature = rsa.sign_hash(message_hash, signkey, 'SHA-1')

# 验证正确的签名
rsa.verify(message, signature, verifykey)
