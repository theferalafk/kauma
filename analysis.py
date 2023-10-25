from test import test, create_random_setup, random_byte_string
from bytenigma import encrypt
import matplotlib.pyplot as plt

def count_occuring_bytes(byte_string):
    res = [0]*256
    for i in byte_string:
        res[i] += 1
    return res

def count_occuring_bits(byte_string):
    res = [0,0]
    for i in byte_string:
        ones = "{0:b}".format(i).count('1')
        res[0] += 8 - ones
        res[1] += ones
    return res

zero_mbi = encrypt(b'\x00'*(2**20), create_random_setup(5))
occuring_bytes = count_occuring_bytes(zero_mbi)
bits = count_occuring_bits(zero_mbi)
print(occuring_bytes)
print(len(occuring_bytes))
'''
print(bits)
print(bits[0]/(bits[1]+bits[0]))
bstr=random_byte_string(2**20)
rng = encrypt(bstr, create_random_setup(10))
bits = count_occuring_bits(bstr)
print(bits)
print(bits[0]/(bits[1]+bits[0]))
print(count_occuring_bits([i for i in range(256)]))
'''

plt.bar([i for i in range(256)], occuring_bytes, width=1)
plt.ylabel('occurance')
plt.xlabel('byte value')
plt.savefig('nullbytes_histogram.png')