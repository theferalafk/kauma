from gcm_util import GF, GFElement, gcm_nonce, byte_xor
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

class AES_128_GCM:

    def _aes_ecb_encrypt(self, pt):
        encryptor = self.cipher.encryptor()
        return encryptor.update(pt) + encryptor.finalize()
    
    def _aes_ecb_decrypt(self, ct):
        decryptor = self.cipher.decryptor()
        return decryptor.update(ct) + decryptor.finalize()

    def __init__(self, key, nonce):
        self.key = key
        self.cipher = Cipher(algorithms.AES(key), modes.ECB())
        self.auth_key = self._aes_ecb_encrypt(b'\x00'*16)
        print("auth key:", self.auth_key)
        self.y = iter(gcm_nonce(nonce))
        print("y0:", self.y.y0)

    def ghash(self, ad, ct):
        pass

    def encrypt(self, pt):
        padding_bytes = 16-len(pt)%16
        if padding_bytes:
            pt+=b'\x00'*padding_bytes
        res = bytearray()
        for i in range(len(pt)//16):
            current = next(self.y)
            current = GF.block_to_poly(current)
            crypt = 0
            for j in current:
                crypt += 2**j
            xor_bytes = self._aes_ecb_encrypt(crypt.to_bytes(16, byteorder='little'))
            print(f"round: {i}, {xor_bytes}")
            res += byte_xor(pt[i*16:16+i*16], xor_bytes)#self._aes_ecb_encrypt(next(self.y)))
        return bytes(res)
            



if __name__ == "__main__":
    iv = gcm_nonce(123)
    a = iter(iv)
    print(next(a))
    key = b'\xfe\xff\xe9\x92\x86es\x1cmj\x8f\x94g0\x83\x08'
    nonce = b'\xca\xfe\xba\xbe\xfa\xce\xdb\xad\xde\xca\xf8\x88'
    pt = b'\xd912%\xf8\x84\x06\xe5\xa5Y\t\xc5\xaf\xf5&\x9a\x86\xa7\xa9S\x154\xf7\xda.L0=\x8a1\x8ar\x1c<\x0c\x95\x95h\tS/\xcf\x0e$I\xa6\xb5%'
    h = b'\xb8;S7\x08\xbfS]\n\xa6\xe5)\x80\xd5;x'
    y0 = b'\xca\xfe\xba\xbe\xfa\xce\xdb\xad\xde\xca\xf8\x88\x00\x00\x00\x01'
    auth_tag = b'Qh\xa0S\xa2FQ\x85\xf6\xb1\x9e\xc2e\xa4\xe8\x8b'
    ct = b'B\x83\x1e\xc2!wt$Kr!\xb7\x84\xd0\xd4\x9c\xe3\xaa!/,\x02\xa4\xe05\xc1~#)\xac\xa1.!\xd5\x14\xb2Tf\x93\x1c}\x8fjZ\xac\x84\xaa\x05'
    print("Expected keystream =", byte_xor(pt[:16],ct[:16]))
    ciphero = AES_128_GCM(key, int.from_bytes(nonce, byteorder='big'))
    print(ciphero.encrypt(pt))
