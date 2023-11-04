from cryptography.hazmat.primitives.padding import PKCS7
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
BLOCK_SIZE = 16
SECRET_KEY = b'mayonakadeiinoni'

def encrypt(iv, pt):
    cipher = Cipher(algorithms.AES(SECRET_KEY), modes.CBC(iv))
    encryptor = cipher.encryptor()
    return encryptor.update(pt) + encryptor.finalize()

def decrypt(iv, ct):
    cipher = Cipher(algorithms.AES(SECRET_KEY), modes.CBC(iv))
    decryptor = cipher.decryptor()
    return decryptor.update(ct) + decryptor.finalize()


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
    
def byte_xor(a,b):
    return (int.from_bytes(a, byteorder='little') ^ int.from_bytes(b, byteorder='little')).to_bytes(16, byteorder='little')
