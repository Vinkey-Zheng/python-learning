import rsa
# 1. 生成密钥对
(pubkey, privkey) = rsa.newkeys(512)

# 2. 明文信息
message1 = 'I like blockchain!'.encode('utf8')
print(message1)

# 3. 加密过程，由明文生成密文
crypto = rsa.encrypt(message1, pubkey)
print(crypto)

# 4. 解密过程，由密文得到明文
message2 = rsa.decrypt(crypto, privkey)
print(message2.decode('utf8'))
