from gcm_util import GF, GFElement, gcm_nonce, byte_xor
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

class AES_128_GCM:

    def _aes_ecb_encrypt(self, pt):
        encryptor = self.cipher.encryptor()
        return encryptor.update(pt) + encryptor.finalize()

    def __init__(self, key, nonce):
        self.key = key
        self.cipher = Cipher(algorithms.AES(key), modes.ECB())
        self.auth_key = self._aes_ecb_encrypt(b'\x00'*16)
        self.y = iter(gcm_nonce(nonce))

    def ghash(self, ct, ad=b'\x00'*16):
        #ad needs padding if < 16 bytes
        ad_int = 0
        for i in GF.block_to_poly(ad):
            ad_int += 2**i
        diff = 16-len(ct)%16
        ad_len = 0#len(ad)
        if diff:
            ct += b'\x00'*diff
        ct_len = len(ct)
        h_poly = GF.block_to_poly(self.auth_key)
        hash_subkey = GFElement(h_poly)
        y = GF.poly_to_block(GFElement([0]) * hash_subkey)
        print(y)
        for i in range(len(ct)//16):
            y_xor_block = byte_xor(y,ct[i*16:16+i*16])
            print("Index ", i, "T+B",y_xor_block)
            block_poly = GF.block_to_poly(y_xor_block)
            y = hash_subkey * GFElement(block_poly)
            y = GF.poly_to_block(y)
            print("H * B ", y)
        length_field = ad_len.to_bytes(8, byteorder='big') + ct_len.to_bytes(8, byteorder='big')
        y_xor_l = byte_xor(y, length_field)
        res = GFElement(GF.block_to_poly(y_xor_l)) * hash_subkey
        return GF.poly_to_block(res)


    def encrypt(self, pt):
        res = bytearray()
        for i in range(len(pt)//16):
            tmp = next(self.y)
            xor_bytes = self._aes_ecb_encrypt(tmp)
            res += byte_xor(pt[i*16:16+i*16], xor_bytes)
        self.ct = bytes(res)
        return self.ct
            



if __name__ == "__main__":

    #known answer test 1
    key = b'\xfe\xff\xe9\x92\x86es\x1cmj\x8f\x94g0\x83\x08'
    nonce = b'\xca\xfe\xba\xbe\xfa\xce\xdb\xad\xde\xca\xf8\x88'
    pt = b'\xd912%\xf8\x84\x06\xe5\xa5Y\t\xc5\xaf\xf5&\x9a\x86\xa7\xa9S\x154\xf7\xda.L0=\x8a1\x8ar\x1c<\x0c\x95\x95h\tS/\xcf\x0e$I\xa6\xb5%'
    h = b'\xb8;S7\x08\xbfS]\n\xa6\xe5)\x80\xd5;x'
    y0 = b'\xca\xfe\xba\xbe\xfa\xce\xdb\xad\xde\xca\xf8\x88\x00\x00\x00\x01'
    auth_tag = b'Qh\xa0S\xa2FQ\x85\xf6\xb1\x9e\xc2e\xa4\xe8\x8b'
    ct = b'B\x83\x1e\xc2!wt$Kr!\xb7\x84\xd0\xd4\x9c\xe3\xaa!/,\x02\xa4\xe05\xc1~#)\xac\xa1.!\xd5\x14\xb2Tf\x93\x1c}\x8fjZ\xac\x84\xaa\x05'
    ciphero = AES_128_GCM(key, int.from_bytes(nonce, byteorder='big'))
    assert ciphero.auth_key == h
    assert ciphero.y.y0 == y0
    assert ciphero.encrypt(pt) == ct
    cipherino = AES_128_GCM(key, int.from_bytes(nonce, byteorder='big'))
    assert cipherino.encrypt(ct) == pt
    print(cipherino.ghash(ct))