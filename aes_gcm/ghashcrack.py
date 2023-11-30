from aes_gcm.aes_128_gcm import AES_128_GCM
from aes_gcm.cantor_zassenhaus import CZ
from aes_gcm.poly import Poly
from aes_gcm.gcm_util import GFElement

class CrackMsg:
    #helper class for GHashCrack
    def _slice_msg(msg):
        return [msg[i:i+16] for i in range(0, len(msg), 16)]

    def __init__(self, ct, ad, tag):
        self.ct = CrackMsg._slice_msg(ct)
        self.ad = CrackMsg._slice_msg(ad)
        self.tag = tag

class GHashCrack:
    
    def __init__(self, msg1 : CrackMsg, msg2 : CrackMsg, msg3 : CrackMsg):
        self.msg1 = msg1
        self.msg2 = msg2
        self.msg3 = msg3
        self.h = False
        self.y0 = False

    def _ghash_xor(self, tag, msg_blocks, h):
        #performs ghash for msg block under hash key h 
        ghash = AES_128_GCM._ghash(msg_blocks, h)
        return AES_128_GCM._byte_xor(ghash, tag)
    
    def construct_poly(self):
        #constructs two polys with msg1, msg2 of form ad0*X^n + ad1*X^(n-1) + ... ct0*X^(n-i) ... + LField*X + Tag and adds them
        msg1_l = [(len(self.msg1.ad)*8).to_bytes(8, byteorder='big')+(len(self.msg1.ct)*8).to_bytes(8, byteorder='big')]
        msg2_l = [(len(self.msg2.ad)*8).to_bytes(8, byteorder='big')+(len(self.msg2.ct)*8).to_bytes(8, byteorder='big')]

        ad_1 = self.msg1.ad[::-1]
        ad_2 = self.msg2.ad[::-1]

        #avoid leading zeros if ad is 0
        if self.msg1.ad == b'' or self.msg1.ad == b'\x00'*16:
            ad_1 = []
        if self.msg2.ad == b'' or self.msg2.ad == b'\x00'*16:
            ad_2 = []
        
        poly_1 = Poly.bytes_to_list([self.msg1.tag]+msg1_l+self.msg1.ct[::-1]+ad_1)
        poly_2 = Poly.bytes_to_list([self.msg2.tag]+msg2_l+self.msg2.ct[::-1]+ad_2)
        return (Poly(poly_1) + Poly(poly_2)).normalize()

    def verify_mask(self,y0,h):
        if not (y0 and h):
            return False
        ghash = AES_128_GCM._ghash(AES_128_GCM._slice_and_combine(self.msg3.ad,b''.join(self.msg3.ct)), h)
        forged_tag = AES_128_GCM._byte_xor(ghash, y0)
        if forged_tag==self.msg3.tag:
            return True
        return False

    def crack(self):
        #tries to factor poly using cantor zassenhaus
        cz = CZ(self.construct_poly())
        candidates = cz.factor_poly()
        for i in candidates:
            to_verify = AES_128_GCM._slice_and_combine(self.msg1.ad, b''.join(self.msg1.ct))
            mask = self._ghash_xor(self.msg1.tag, to_verify, GFElement(i[0]))
            if self.verify_mask(mask,GFElement(i[0])):
                self.y0 = mask
                self.h = GFElement(i[0])
                break
        return True
    
    def forge_auth_tag(self, ad, ct):
        #contructs a tag for given ad and ct, only works after crack() is used
        if not (self.h and self.y0):
            return False
        ghash_msg = AES_128_GCM._slice_and_combine(ad,ct)
        return self._ghash_xor(self.y0, ghash_msg, self.h)
