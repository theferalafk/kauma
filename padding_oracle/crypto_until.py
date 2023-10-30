from cryptography.hazmat.primitives.padding import PKCS7
BLOCK_SIZE = 16
SECRET_KEY = b'zuttomayonakadeiinoni'

def _encrypt_block(data):
    return int.from_bytes(SECRET_KEY, byteorder='little')&(2**BLOCK_SIZE-1) ^ data

def encrypt(iv, pt):
    res = []
    last_block = iv
    for i in range(int(len(pt)/BLOCK_SIZE)):
        starting_byte = BLOCK_SIZE * i
        current_block = pt[starting_byte:starting_byte+BLOCK_SIZE]
        ct = _encrypt_block(int.from_bytes(current_block, byteorder='little') ^ int.from_bytes(last_block, byteorder='little')).to_bytes(BLOCK_SIZE, byteorder='little')
        res.append(ct)
    return b''.join(res)

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