from aes_128_gcm import AES_128_GCM
from cantor_zassenhauser import CZ
from poly import Poly
from gcm_util import GFElement
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
        
        poly_1 = Poly.bytes_to_list([msg1.tag]+msg1_l+self.msg1.ct[::-1]+ad_1)
        poly_2 = Poly.bytes_to_list([msg2.tag]+msg2_l+self.msg2.ct[::-1]+ad_2)
        return (Poly(poly_1) + Poly(poly_2)).normalize()

    def verify_mask(self,y0,h):
        ghash = AES_128_GCM._ghash(AES_128_GCM._slice_and_combine(msg3.ad,b''.join(msg3.ct)), h)
        forged_tag = AES_128_GCM._byte_xor(ghash, y0)
        if forged_tag==msg3.tag:
            return True
        return False

    def crack(self):
        cz = CZ(self.construct_poly())
        candidates = cz.factor_poly()
        for i in candidates:
            to_verify = AES_128_GCM._slice_and_combine(msg1.ad, b''.join(msg1.ct))
            mask = self._gen_mask(self.msg1.tag, to_verify, GFElement(i[0]))
            if self.verify_mask(mask,GFElement(i[0])):
                self.y0 = mask
                self.h = GFElement(i[0])
                break
        return True
    
    def forge_auth_tag(self, ad, ct):
        ghash_msg = AES_128_GCM._slice_and_combine(ad,ct)
        return self._gen_mask(self.y0, ghash_msg, self.h)


if __name__ == "__main__":
    msg1 = { 
        'ct' : b'B\x83\x1e\xc2!wt$Kr!\xb7\x84\xd0\xd4\x9c\xe3\xaa!/,\x02\xa4\xe05\xc1~#)\xac\xa1.!\xd5\x14\xb2Tf\x93\x1c}\x8fjZ\xac\x84\xaa\x05',
        'ad' : b'',
        'tag': b'Qh\xa0S\xa2FQ\x85\xf6\xb1\x9e\xc2e\xa4\xe8\x8b'
    }
    msg2 = {
        'ct' : b'\x8a\xa3=\xc5\xfb\xd1P\xe3\xcc\t\nP\t\x07\xc15!I\xcc8}r\x17~\\\xca\tY\xe4\xdal\x1b\xa4p\x81\xbeX\xa5!\xf4\xe9\xfb\xdf\xc5_\x98\xa5\x9b',
        'ad' : b'',
        'tag': b'\xd4\xa8\xe9\xe3\xabLY\x16\xec\xef%\x15\x08W\xcdC'
    }
    msg3 = {
        'ct' : b'0\x19\x87]cI\xc1\xf2\xdd\x18\nP\t\x07\xc15V>\xbbN(\x15G\x19\x0f\xca\tY\xe4\xdal\x1b\xaf\xcb;o\xc8-\xee\xd7`9\xe0]_\x98\xa5\x9b',
        'ad' : b'',
        'tag': b'\xae\xd9\xe0`\xa4\xdfO\xba\xd3op\x97\xd3\xf8\xfd\x7f',
    }
    msg1 = CrackMsg(msg1["ct"], msg1["ad"], msg1["tag"])
    msg2 = CrackMsg(msg2["ct"], msg2["ad"], msg2["tag"])
    msg3 = CrackMsg(msg3["ct"], msg3["ad"], msg3["tag"])

    test = GHashCrack(msg1,msg2,msg3)
    test.crack()
    print(test.forge_auth_tag(b'', b'0\x19\x87]cI\xc1\xf2\xdd\x18\nP\t\x07\xc15V>\xbbN(\x15G\x19\x0f\xca\tY\xe4\xdal\x1b\xaf\xcb;o\xc8-\xee\xd7`9\xe0]_\x98\xa5\x9b'))
    print(test.forge_auth_tag(b'', b'\xa8\x81\x1f\xd4\xea\xc0A\xf2\xdd\x18\nP\t\x07\xc15V>\xbbO}r\x17~\\\xca\tY\xe4\xdal\x1b\xaf\xcb:\x0eX\xa5!\xf4\xe9\xfb\xdf\xc5_\x98\xa5\x9b'))

    