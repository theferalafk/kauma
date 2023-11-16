from gf import GF, GFElement
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

class AES_128_GCM:

    def _aes_ecb_encrypt(self, pt):
        encryptor = self.cipher.encryptor()
        return encryptor.update(pt) + encryptor.finalize()
    
    def _aes_ecb_decrypt(self, ct):
        decryptor = self.cipher.decryptor()
        return decryptor.update(ct) + decryptor.finalze()

    def __init__(self, key):
        self.key = key
        self.auth_key = self._aes_ecb_encrypt(b'\x00'*16)
        self.cipher = Cipher(algorithms.AES(key), modes.ECB())

    def ghash(ad, ct):
        pass

    def encrypt(pt, ad, nonce):
        pass