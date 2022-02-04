import hashlib

s256 = hashlib.new('sha256', b'I like blockchain!')
s256.hexdigest()

s256 = hashlib.new('sha256')
s256.update(b'I like ')
s256.update(b'blockchain!')
s256.hexdigest()

