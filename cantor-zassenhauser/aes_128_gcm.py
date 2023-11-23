from gcm_util import GF, GFElement, gcm_nonce, byte_xor, slice_bytestring
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
        ct_len = len(ct)*8
        #if diff:
        #    ct += b'\x00'*diff
        h_poly = GF.block_to_poly(self.auth_key)
        hash_subkey = GFElement(h_poly)
        y = GF.poly_to_block(GFElement([]) * hash_subkey)
        for i in range(len(ct)//16):
            y_xor_block = byte_xor(y,ct[i*16:16+i*16])
            block_poly = GF.block_to_poly(y_xor_block)
            y = hash_subkey * GFElement(block_poly)
            y = GF.poly_to_block(y)
        length_field = ad_len.to_bytes(8, byteorder='big') + ct_len.to_bytes(8, byteorder='big')
        y_xor_l = byte_xor(y, length_field)
        res = GFElement(GF.block_to_poly(y_xor_l)) * hash_subkey
        return GF.poly_to_block(res)

    def _slice_and_combine(self, ad,ct):
        #slices two bytstrings into 16 byte blocks without padding and appends length field for aes_gcm
        
        print("sliced ad block: ", slice_bytestring(ad,16))
        return slice_bytestring(ad, 16) + slice_bytestring(ct, 16) + [(len(ad)*8).to_bytes(8, byteorder='big')+(len(ct)*8).to_bytes(8, byteorder='big')]
    

    def _ghash(self, ct, ad=b''):
        #save original length
        
        h_poly = GF.block_to_poly(self.auth_key)
        hash_subkey = GFElement(h_poly)
        
        mul_blocks = self._slice_and_combine(ad, ct)
        y = b'\x00'*16
        for block in mul_blocks:
            y_xor_block = byte_xor(y, block)
            poly_block = GF.block_to_poly(y_xor_block)
            tmp = hash_subkey * GFElement(poly_block)
            y = GF.poly_to_block(tmp)
        return y

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
    #print(cipherino.ghash(ct))
    #print(cipherino._ghash(ct))
    #print(byte_xor(cipherino._ghash(ct), cipherino._aes_ecb_encrypt(cipherino.y.y0)))

    #nist test vector 1
    key = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    nonce = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    ad = b''
    pt = b''
    ct = b''
    auth_tag = b'X\xe2\xfc\xce\xfa~0a6\x7f\x1dW\xa4\xe7EZ'


    #cipherino = AES_128_GCM(key, int.from_bytes(nonce, byteorder='big'))
    #print(byte_xor(cipherino._ghash(ct), cipherino._aes_ecb_encrypt(cipherino.y.y0)))

    #nist test vector 2
    key = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    nonce = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    ad = b''
    pt = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    ct = b'\x03\x88\xda\xce`\xb6\xa3\x92\xf3(\xc2\xb9q\xb2\xfex'
    auth_tag = b'\xabnG\xd4,\xec\x13\xbd\xf5:g\xb2\x12W\xbd\xdf'

    #cipherino = AES_128_GCM(key, int.from_bytes(nonce, byteorder='big'))
    #print(byte_xor(cipherino._ghash(ct), cipherino._aes_ecb_encrypt(cipherino.y.y0)))


    #nist test vector 3
    key = b'\xfe\xff\xe9\x92\x86es\x1cmj\x8f\x94g0\x83\x08'
    nonce = b'\xca\xfe\xba\xbe\xfa\xce\xdb\xad\xde\xca\xf8\x88'
    ad = b''
    pt = b'\xd912%\xf8\x84\x06\xe5\xa5Y\t\xc5\xaf\xf5&\x9a\x86\xa7\xa9S\x154\xf7\xda.L0=\x8a1\x8ar\x1c<\x0c\x95\x95h\tS/\xcf\x0e$I\xa6\xb5%\xb1j\xed\xf5\xaa\r\xe6W\xbac{9\x1a\xaf\xd2U'
    ct = b'B\x83\x1e\xc2!wt$Kr!\xb7\x84\xd0\xd4\x9c\xe3\xaa!/,\x02\xa4\xe05\xc1~#)\xac\xa1.!\xd5\x14\xb2Tf\x93\x1c}\x8fjZ\xac\x84\xaa\x05\x1b\xa3\x0b9j\n\xac\x97=X\xe0\x91G?Y\x85'
    auth_tag = b"M\\*\xf3'\xcdd\xa6,\xf3Z\xbd+\xa6\xfa\xb4"

    #cipherino = AES_128_GCM(key, int.from_bytes(nonce, byteorder='big'))
    #print(byte_xor(cipherino._ghash(ct), cipherino._aes_ecb_encrypt(cipherino.y.y0)))

    #nist test vector 4
    key = b'\xfe\xff\xe9\x92\x86es\x1cmj\x8f\x94g0\x83\x08'
    nonce = b'\xca\xfe\xba\xbe\xfa\xce\xdb\xad\xde\xca\xf8\x88'
    ad = b'\xfe\xed\xfa\xce\xde\xad\xbe\xef\xfe\xed\xfa\xce\xde\xad\xbe\xef\xab\xad\xda\xd2'
    print(ad[:16])
    #ad = ad[:16] + b'\x00'*12 + ad[16:]
    pt = b'\xd912%\xf8\x84\x06\xe5\xa5Y\t\xc5\xaf\xf5&\x9a\x86\xa7\xa9S\x154\xf7\xda.L0=\x8a1\x8ar\x1c<\x0c\x95\x95h\tS/\xcf\x0e$I\xa6\xb5%\xb1j\xed\xf5\xaa\r\xe6W\xbac{9'
    ct = b'B\x83\x1e\xc2!wt$Kr!\xb7\x84\xd0\xd4\x9c\xe3\xaa!/,\x02\xa4\xe05\xc1~#)\xac\xa1.!\xd5\x14\xb2Tf\x93\x1c}\x8fjZ\xac\x84\xaa\x05\x1b\xa3\x0b9j\n\xac\x97=X\xe0\x91'
    auth_tag = b'[\xc9O\xbc2!\xa5\xdb\x94\xfa\xe9Z\xe7\x12\x1aG'
    #tag is not working for empty ad
    cipherino = AES_128_GCM(key, int.from_bytes(nonce, byteorder='big'))
    print("Test Vector 4: ", byte_xor(cipherino._ghash(ct), cipherino._aes_ecb_encrypt(cipherino.y.y0)))

    #nist test vector 5
    key = b'\xfe\xff\xe9\x92\x86es\x1cmj\x8f\x94g0\x83\x08'
    nonce = b'\xca\xfe\xba\xbe\xfa\xce\xdb\xad'
    ad = b'\xfe\xed\xfa\xce\xde\xad\xbe\xef\xfe\xed\xfa\xce\xde\xad\xbe\xef\xab\xad\xda\xd2'
    pt = b'\xd912%\xf8\x84\x06\xe5\xa5Y\t\xc5\xaf\xf5&\x9a\x86\xa7\xa9S\x154\xf7\xda.L0=\x8a1\x8ar\x1c<\x0c\x95\x95h\tS/\xcf\x0e$I\xa6\xb5%\xb1j\xed\xf5\xaa\r\xe6W\xbac{9'
    ct = b'a5;L(\x06\x93Jw\x7f\xf5\x1f\xa2*GUi\x9b*qO\xcd\xc6\xf87f\xe5\xf9{lt#s\x80i\x00\xe4\x9f$\xb2+\tuD\xd4\x89kBI\x89\xb5\xe1\xeb\xac\x0f\x07\xc2?E\x98'
    auth_tag = b'6\x12\xd2\xe7\x9e;\x07\x85V\x1b\xe1J\xac\xa2\xfc\xcb'

    #cipherino = AES_128_GCM(key, int.from_bytes(nonce, byteorder='big'))
    #print(byte_xor(cipherino._ghash(ct, ad), cipherino._aes_ecb_encrypt(cipherino.y.y0)))

    #nist test vector 6
    key = b'\xfe\xff\xe9\x92\x86es\x1cmj\x8f\x94g0\x83\x08'
    nonce = b'\x93\x13"]\xf8\x84\x06\xe5U\x90\x9cZ\xffRi\xaajz\x958SO}\xa1\xe4\xc3\x03\xd2\xa3\x18\xa7(\xc3\xc0\xc9QV\x80\x959\xfc\xf0\xe2B\x9akRT\x16\xae\xdb\xf5\xa0\xdejW\xa67\xb3\x9b'
    ad = b'\xfe\xed\xfa\xce\xde\xad\xbe\xef\xfe\xed\xfa\xce\xde\xad\xbe\xef\xab\xad\xda\xd2'
    pt = b'\xd912%\xf8\x84\x06\xe5\xa5Y\t\xc5\xaf\xf5&\x9a\x86\xa7\xa9S\x154\xf7\xda.L0=\x8a1\x8ar\x1c<\x0c\x95\x95h\tS/\xcf\x0e$I\xa6\xb5%\xb1j\xed\xf5\xaa\r\xe6W\xbac{9'
    ct = b'\x8c\xe2I\x98bV\x15\xb6\x03\xa03\xac\xa1?\xb8\x94\xbe\x91\x12\xa5\xc3\xa2\x11\xa8\xba&*<\xca~,\xa7\x01\xe4\xa9\xa4\xfb\xa4<\x90\xcc\xdc\xb2\x81\xd4\x8c|o\xd6(u\xd2\xac\xa4\x17\x03L4\xae\xe5'
    auth_tag = b'a\x9c\xc5\xae\xff\xfe\x0b\xfaF*\xf4<\x16\x99\xd0P'

    #cipherino = AES_128_GCM(key, int.from_bytes(nonce, byteorder='big'))
    #print(byte_xor(cipherino._ghash(ct), cipherino._aes_ecb_encrypt(cipherino.y.y0)))