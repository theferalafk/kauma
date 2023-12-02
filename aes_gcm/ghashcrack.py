from aes_gcm.aes_128_gcm import AES_128_GCM
from aes_gcm.cantor_zassenhaus import CZ
from aes_gcm.poly import Poly
from aes_gcm.gcm_util import GFElement

class CrackMsg:
    #helper class for GHashCrack

    def __init__(self, ct, ad, tag):
        self.ct = ct
        self.ad = ad
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

    def _pad_and_reverse(blocks):
        res = []
        for block in blocks:
            tmp = block
            if len(block) < 16:
                tmp = block + b'\x00'*(16-len(block))
            res.append(tmp)
        return res[::-1]

    def construct_poly(self):
        #constructs two polys with msg1, msg2 of form ad0*X^n + ad1*X^(n-1) + ... ct0*X^(n-i) ... + LField*X + Tag and adds them
        a = Poly.bytes_to_list((AES_128_GCM._slice_and_combine(self.msg1.ad, self.msg1.ct)+[self.msg1.tag])[::-1])
        b = Poly.bytes_to_list((AES_128_GCM._slice_and_combine(self.msg2.ad, self.msg2.ct)+[self.msg2.tag])[::-1])
        return (Poly(a)+Poly(b)).normalize()

    def verify_mask(self,y0,h):
        if not (y0 and h):
            return False
        ghash = AES_128_GCM._ghash(AES_128_GCM._slice_and_combine(self.msg3.ad, self.msg3.ct), h)
        forged_tag = AES_128_GCM._byte_xor(ghash, y0)
        if forged_tag==self.msg3.tag:
            return True
        return False

    def crack(self):
        #tries to factor poly using cantor zassenhaus
        yo = self.construct_poly()
        cz = CZ(yo)
        candidates = []
        for i in range(3):
            candidates = cz.factor_poly()
            if len(yo.poly)-1==len(candidates):
                break
        print(len(yo.poly), len(candidates))
        for i in candidates:
            to_verify = AES_128_GCM._slice_and_combine(self.msg1.ad, self.msg1.ct)
            mask = self._ghash_xor(self.msg1.tag, to_verify, GFElement(i[0]))
            if self.verify_mask(mask,GFElement(i[0])):
                self.y0 = mask
                self.h = GFElement(i[0])
                return True
        return False
    
    def forge_auth_tag(self, ad, ct):
        #contructs a tag for given ad and ct, only works after crack() is used
        if not (self.h and self.y0):
            return False
        ghash_msg = AES_128_GCM._slice_and_combine(ad,ct)
        return self._ghash_xor(self.y0, ghash_msg, self.h)
