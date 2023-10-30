from cryptography.hazmat.primitives.padding import PKCS7
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
BLOCK_SIZE = 16
SECRET_KEY = b'mayonakadeiinoni'

def _encrypt_block(data):
    tmp = int.from_bytes(SECRET_KEY, byteorder='little')&(2**(8*BLOCK_SIZE)-1) ^ data
    return tmp

def encrypt(iv, pt):
    res = []
    last_block = iv
    for i in range(int(len(pt)/BLOCK_SIZE)):
        starting_byte = BLOCK_SIZE * i
        current_block = pt[starting_byte:starting_byte+BLOCK_SIZE]
        ct = _encrypt_block(int.from_bytes(current_block, byteorder='little') ^ int.from_bytes(last_block, byteorder='little')).to_bytes(BLOCK_SIZE, byteorder='little')
        res.append(ct)
    return b''.join(res)

def two_crypt(iv, pt):
    algo = algorithms.AES(key=SECRET_KEY)
    cipher = Cipher(algo, mode='CBC')
    encryptor = cipher.encryptor()
    ct = encryptor.update(pt)
    return ct

def three_crypt(iv, ct):
    algo = algorithms.AES(key=SECRET_KEY)
    cipher = Cipher(algo, mode='CBC')
    decryptor = cipher.decryptor()
    pt = decryptor.update(ct)
    return pt

def pad(data):
    padder = PKCS7(BLOCK_SIZE*8).padder()
    padded_data = padder.update(data)
    return padded_data + padder.finalize()

def unpad(data):
    try:
        unpadder = PKCS7(BLOCK_SIZE*8).unpadder()
        unpadded_data = unpadder.update(data)
        return unpadded_data + unpadder.finalize()
    except ValueError:
        return False

if __name__ == '__main__':
    c2 = encrypt(b'\x12\x34'*8, pad(b'djbernstein'))
    p2 = encrypt(b'\x12\x34'*8, c2)
    p1 = encrypt(b'\x00'*15+b'\x04', c2)
    print(c2)
    print(p2)
    print(p1)
    print(_encrypt_block(_encrypt_block(int.from_bytes(pad(b'djbernstein'), byteorder='little')^0x12341234123412341234123412341234)).to_bytes(16, byteorder='little'))
    print(_encrypt_block((_encrypt_block(int.from_bytes(pad(b'djbernstein'), byteorder='little')))^0x12341234123412341234123412341234).to_bytes(16, byteorder='little'))