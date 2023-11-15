from gf import GF, GFElement
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms

class AES_128_GCM:

    def aes_ecb(pt):
        pass

    def __init__(self, key):
        self.key = key
        self.auth_key = self.aes_ecb("Nullstream")    

    def ghash(ad, ct):
        pass

    def encrypt(pt, ad, nonce):
        pass