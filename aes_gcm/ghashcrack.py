from aes_gcm.aes_128_gcm import AES_128_GCM
from aes_gcm.cantor_zassenhaus import CZ
from aes_gcm.poly import Poly
from aes_gcm.gcm_util import GFElement
class CrackMsg:
    def __init__(self, ct, ad, tag):
        self.ct = [ct[i:i+16] for i in range(0, len(ct), 16)]
        self.ad = ad
        self.tag = tag

class GHashCrack:
    
    def __init__(self, msg1 : CrackMsg, msg2 : CrackMsg, msg3 : CrackMsg):
        self.msg1 = msg1
        self.msg2 = msg2
        self.msg3 = msg3
        self.h = False
        self.y0 = False

    def _gen_mask(self, tag, msg_blocks, h):
        ghash = AES_128_GCM._ghash(msg_blocks, h)
        return AES_128_GCM._byte_xor(ghash, tag)
    
    def construct_poly(self):

        msg1_l = [(len(self.msg1.ad)*8).to_bytes(8, byteorder='big')+(len(self.msg1.ct)*8).to_bytes(8, byteorder='big')]
        msg2_l = [(len(self.msg2.ad)*8).to_bytes(8, byteorder='big')+(len(self.msg2.ct)*8).to_bytes(8, byteorder='big')]

        ad_1 = [self.msg1.ad]
        ad_2 = [self.msg2.ad]

        if self.msg1.ad == b'' or self.msg1.ad == b'\x00'*16:
            ad_1 = []
        if self.msg2.ad == b'' or self.msg2.ad == b'\x00'*16:
            ad_2 = []
        
        poly_1 = Poly.bytes_to_list([self.msg1.tag]+msg1_l+self.msg1.ct[::-1]+ad_1)
        poly_2 = Poly.bytes_to_list([self.msg2.tag]+msg2_l+self.msg2.ct[::-1]+ad_2)
        return (Poly(poly_1) + Poly(poly_2)).normalize()

    def verify_mask(self,y0,h):
        ghash = AES_128_GCM._ghash(AES_128_GCM._slice_and_combine(self.msg3.ad,b''.join(self.msg3.ct)), h)
        forged_tag = AES_128_GCM._byte_xor(ghash, y0)
        if forged_tag==self.msg3.tag:
            return True
        return False

    def crack(self):
        cz = CZ(self.construct_poly())
        candidates = cz.factor_poly()
        for i in candidates:
            to_verify = AES_128_GCM._slice_and_combine(self.msg1.ad, b''.join(self.msg1.ct))
            mask = self._gen_mask(self.msg1.tag, to_verify, GFElement(i[0]))
            if self.verify_mask(mask,GFElement(i[0])):
                self.y0 = mask
                self.h = GFElement(i[0])
                break
        return True
    
    def forge_auth_tag(self, ad, ct):
        ghash_msg = AES_128_GCM._slice_and_combine(ad,ct)
        return self._gen_mask(self.y0, ghash_msg, self.h)
