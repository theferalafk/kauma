from test import test, create_random_setup, random_byte_string
from bytenigma import encrypt
from collections import Counter
zero_mbi = encrypt(b'\x00'*(2**20), test["rotors"])
print(Counter(zero_mbi))
bstr=random_byte_string(2**20)
rng = encrypt(bstr, create_random_setup(10))
print(Counter(rng))