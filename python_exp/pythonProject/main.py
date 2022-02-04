import hashlib

md5 = hashlib.new('md5')
s256 = hashlib.new('sha256')
r160 = hashlib.new('ripemd160')

print('The length of md5 hash value is {}'.format(md5.digest_size))
print('The length of sha256 hash value is {}'.format(s256.digest_size))
print('The length of ripemd160 hash value is {}'.format(r160.digest_size))
