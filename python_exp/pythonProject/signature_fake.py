import rsa

# 创建签名公钥对
(verifykey, signkey) = rsa.newkeys(512)
# 创建伪装者的密钥对
(fake_verifykey, fake_signkey) = rsa.newkeys(512)

# 计算消息的散列值
message = b"I like blockchain."
message_hash = rsa.compute_hash(message, 'SHA-1')

# 使用伪装者的签名密钥，生成数字签名
fake_signature = rsa.sign_hash(message_hash, fake_signkey, 'SHA-1')

# 使用正确的密钥，验证伪装者的签名
rsa.verify(message, fake_signature, verifykey)
