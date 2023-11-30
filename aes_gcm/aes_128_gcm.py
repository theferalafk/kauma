from aes_gcm.gcm_util import GF, GFElement, gcm_nonce
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

class AES_128_GCM:

    def __init__(self, key, nonce):
        self.key = key
        self.cipher = Cipher(algorithms.AES(key), modes.ECB())
        self.auth_key = self._aes_ecb_encrypt(b'\x00'*16)

        #check if nonce is 96 bit long and initialize y accordingly, otherwise transform before nonce
        if len(nonce)==12:
            tmp = nonce+b'\x00\x00\x00\x01'            
            self.y = iter(gcm_nonce(tmp))
            self.y0 = tmp
        else:
            tmp = self._ghash_wrapper(nonce+b'\x00'*(8+16-len(nonce)%16)+(len(nonce)*8).to_bytes(8, byteorder='big'),b'', True)
            self.y = iter(gcm_nonce(tmp))
            self.y0 = tmp

    def _aes_ecb_encrypt(self, pt):
        encryptor = self.cipher.encryptor()
        return encryptor.update(pt) + encryptor.finalize()
    
    def _byte_xor(a, b):
            return bytes(a ^ b for (a, b) in zip(a, b))

    def _slice_bytestring(a : bytes, slice_size):
        #slices a bytestring in slices of slice_size, if len(a) is not a multiple of the block size, the last block will be smaller
        #returns an array of bytestrings -> [a_slice1, a_slice2, ...]
        res = []
        for i in range(0, len(a), slice_size):
            block = a[i: slice_size + i]
            if len(block) < slice_size:
                block = block + b'\x00'*(slice_size-len(block))
            res.append(block)
        return res

    def _slice_and_combine(ad, ct, nonce=False):
        #slices two bytstrings into 16 byte blocks with b'\x00' appended if needed and appends length field for aes_gcm
        if nonce:
            return AES_128_GCM._slice_bytestring(ct,16)
        return AES_128_GCM._slice_bytestring(ad, 16) + AES_128_GCM._slice_bytestring(ct, 16) + [(len(ad)*8).to_bytes(8, byteorder='big')+(len(ct)*8).to_bytes(8, byteorder='big')]
    
    def _ghash(byte_blocks, hash_subkey):
        y = b'\x00'*16
        for block in byte_blocks:
            y_xor_block = AES_128_GCM._byte_xor(y, block)
            poly_block = GF.block_to_poly(y_xor_block)
            tmp = hash_subkey * GFElement(poly_block)
            y = GF.poly_to_block(tmp)
        return y

    def _ghash_wrapper(self, ct, ad, nonce=False):
        h_poly = GF.block_to_poly(self.auth_key)
        hash_subkey = GFElement(h_poly)
        mul_blocks = AES_128_GCM._slice_and_combine(ad, ct, nonce)
        return AES_128_GCM._ghash(mul_blocks, hash_subkey)

    def _auth_tag(self, ct, ad=b''):
        return AES_128_GCM._byte_xor(self._ghash_wrapper(ct, ad), self._aes_ecb_encrypt(self.y0))

    def _encrypt(self, pt):
        res = bytearray()
        block_size = 16
        for i in range(0, len(pt), block_size):
            tmp = next(self.y)
            xor_bytes = self._aes_ecb_encrypt(tmp)
            res += AES_128_GCM._byte_xor(pt[i:block_size+i], xor_bytes)
        self.ct = bytes(res)
        return self.ct
    
    def encrypt_and_tag(self, pt, ad):
        ct = self._encrypt(pt)
        return ct, self._auth_tag(ct, ad) 