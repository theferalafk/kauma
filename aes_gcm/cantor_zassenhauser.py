from poly import Poly
from gcm_util import GF, GFElement
from os import urandom

class CZ:
    #hallo herr bauer, ich schaffe es nicht k2 weiter zu faktorisieren. die faktorisierung selbst stimmt aber für das gegebene polynom
    #ich weiß nicht woran es liegt und ich habe viele schritte in sage mitgerechnet
    #da ist irgendwo ein bug, dass ich nicht finde.....
    #entweder hab ich mein polynom nicht richtig gebaut oder es liegt an etwas anderem, es ist aber kurz vor abgabe also rip...
    def __init__(self, f: Poly):
        self.f = f
        self.degree = len(f.poly)-1


    def _randpoly(d):
        res = []
        for i in range(d):
            res.append(GF.block_to_poly(urandom(16)))
        return Poly(res)

    def cz_step(self, p : Poly):
        #möglicher fehler, ist d vom großen oder vom aktuellen polynom abhängig?
        q = 2**128
        h = CZ._randpoly(self.degree-1)
        g = h.powmod(((q-1)//3), self.f)+Poly([[0]])
        q = p.gcd(g)
        if (q.poly != [[0]] and q.poly != []) and q.poly != p.poly:
            k1 = q
            k2 = p//q
            return k1, k2
        else:
            return None

    def get_factor(self, p: Poly):
        poly = Poly(p.poly.copy())
        for i in range(20):
            if i %10==0:
                print('running', i)
            tmp = self.cz_step(poly)
            if tmp:
                k1, k2 = tmp
                return k1, k2
        return None

    def factor_poly(self):
        res = []
        rem = Poly(self.f.poly.copy())
        candidate=False
        while len(rem.poly)>2:
            hit = False
            while not hit:
                tmp = self.cz_step(rem)
                if tmp:
                    k1, k2 = tmp
                    print("current cands: ", k1.poly,k2.poly)
                    if len(k1.poly)==2:
                        candidate = k1.normalize()
                    if len(k2.poly)==2:
                        candidate = k2.normalize()
                    if candidate:
                        rem, tmp2 = divmod(rem, candidate)
                        if tmp2.poly == []:
                            hit = True   
            print("apppending....", candidate.poly)             
            res.append(candidate.poly)
            print("current state:", res)
        return res + rem.poly

    def factor_poly2(self):
        res = []
        rem = Poly(self.f.poly.copy())
        candidate=False
        active = True
        k1,k2 = self.get_factor(rem)
        print(k1.poly, k2.poly)
        k2_1, k2_2 = self.get_factor(k2)
        print(k2_1.poly, k2_2.poly)
        k2_2_1, k2_2_2 = self.get_factor(k2_2)
        print(k2_2_1.poly, k2_2_2.poly)
        return res + rem.poly

def poly_to_sage(poly):
    res = ''
    for i, p in enumerate(poly):
        res += '('
        for j in p:
            res += f'x^{j}+'
        res = res[:-1] + f')*X^{i}+'
    print(res)

def add_gf(a,b):
    res = Poly._element_to_int(a) ^ Poly._element_to_int(b)
    return Poly._int_to_element(res)


if __name__ == "__main__":
    nonce = b'\xca\xfe\xba\xbe\xfa\xce\xdb\xad\xde\xca\xf8\x88'
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
    msg4 = {
        'ct' : b'\xa8\x81\x1f\xd4\xea\xc0A\xf2\xdd\x18\nP\t\x07\xc15V>\xbbO}r\x17~\\\xca\tY\xe4\xdal\x1b\xaf\xcb:\x0eX\xa5!\xf4\xe9\xfb\xdf\xc5_\x98\xa5\x9b',
        'ad' : b'',
    }

    # TODO Poly takes long byte/b64 strings
    #ad + c0..c1


    tmp = msg1['tag']+16*b'\x00' + msg1["ct"]
    poly_string = [tmp[i:i+16] for i in range(0, len(tmp), 16)]
    a = Poly(Poly.bytes_to_list(poly_string))
    tmp = msg2['tag']+16*b'\x00' + msg2["ct"]
    poly_string = [tmp[i:i+16] for i in range(0, len(tmp), 16)]
    b = Poly(Poly.bytes_to_list(poly_string))
    #print(a+b)
    #poly_to_sage((a+b).poly)
    cz_poly = (a+b).normalize()
    #print(len(cz_poly.poly))
    cz = CZ(cz_poly)
    #print(cz_poly.poly)
    res = ''
    print(cz_poly.poly)
    #test = Poly([[], [], [4, 5, 6, 7, 8, 9, 12, 16, 18, 20, 23, 25, 28, 29, 31, 34, 35, 37, 38, 39, 40, 41, 42, 43, 49, 52, 56, 57, 67, 68, 69, 72, 74, 75, 76, 77, 78, 79, 80, 84, 87, 88, 90, 91, 92, 96, 97, 98, 99, 101, 102, 103, 104, 108, 114, 120, 121, 122, 126, 127], [1, 4, 9, 12, 15, 16, 18, 22, 23, 24, 27, 30, 33, 34, 35, 37, 38, 39, 40, 43, 44, 46, 49, 50, 53, 54, 57, 59, 60, 61, 62, 65, 70, 71, 72, 73, 74, 76, 77, 78, 81, 83, 85, 87, 88, 89, 90, 92, 93, 96, 99, 100, 101, 106, 109, 111, 113, 116, 117, 118, 120, 121, 123, 124, 127],[0]])
    #t, tt = divmod(test,Poly([[],[0]]))
    #print(t.poly, tt.poly)
    carry = cz.factor_poly2()
    #for cand in cands:
    #    print("candidate: ", cand)
    #c1=[0, 1, 3, 9, 10, 13, 15, 19, 20, 24, 26, 27, 29, 30, 32, 33, 35, 37, 39, 41, 42, 43, 44, 46, 47, 51, 52, 53, 54, 56, 58, 61, 63, 64, 67, 69, 72, 74, 77, 79, 80, 83, 85, 86, 88, 90, 93, 95, 96, 97, 98, 99, 101, 102, 104, 105, 109, 110, 111, 112, 113, 119, 123, 125, 126]
    #c2=[0, 2, 3, 4, 6, 7, 10, 12, 15, 18, 20, 23, 25, 26, 27, 29, 30, 32, 33, 35, 36, 37, 38, 39, 41, 43, 46, 50, 52, 58, 59, 60, 62, 63, 64, 66, 67, 69, 70, 71, 72, 77, 81, 82, 85, 87, 89, 90, 91, 93, 94, 95, 97, 99, 100, 101, 103, 105, 106, 107, 108, 109, 112, 113, 122, 123, 127]
    #c3=[2, 6, 7, 13, 15, 16, 19, 22, 25, 27, 30, 33, 34, 35, 36, 37, 39, 40, 42, 43, 46, 47, 49, 51, 56, 57, 65, 66, 72, 73, 76, 77, 78, 79, 80, 82, 85, 86, 90, 91, 92, 93, 94, 98, 99, 101, 102, 103, 104, 107, 108, 109, 110, 113, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126]
    #c4=[0]
    #carry = [[[1, 6, 7, 11, 13, 14, 15, 17, 19, 20, 23, 24, 25, 27, 29, 30, 33, 34, 36, 37, 40, 41, 44, 49, 51, 54, 58, 62, 63, 65, 66, 67, 68, 70, 72, 75, 76, 78, 83, 85, 87, 90, 91, 92, 94, 96, 97, 100, 101, 103, 106, 111, 112, 118, 122, 126], [0]]]
    l = (48*8).to_bytes(16,byteorder='big')
    y0 = []
    for h in carry:
        res = ''
        tmp = 16*b'\x00'+msg1["ct"]+l+msg1["tag"]
        poly_string = [tmp[i:i+16] for i in range(0, len(tmp), 16)]
        for i,blk in enumerate(poly_string):
            u = GF.block_to_poly(blk)
            exp = len(poly_string)-i-1
            H = h
            if len(h)==2:
                H = h[0]
            tmpo = (GFElement(H)**exp)*GFElement(u)
            res = add_gf(res, tmpo)
        y0.append(GF.poly_to_block(res))
    print(y0)


    for ci, h in enumerate(carry):
        tmp = 16*b'\x00'+msg3["ct"]+l+y0[ci]
        poly_string = [tmp[i:i+16] for i in range(0, len(tmp), 16)]
        for i,blk in enumerate(poly_string):
            u = GF.block_to_poly(blk)
            exp = len(poly_string)-i-1
            H = h
            if len(h)==2:
                H = h[0]
            tmpo = (GFElement(H)**exp)*GFElement(u)
            res = add_gf(res, tmpo)
        print(GF.poly_to_block(res))
    #for i in range(100):
    #    res = cz.cz_step(cz_poly)
    #    if res:
    #        break
    #k1, k2 = res
    #print(k1.poly)
    #print(k2.poly)
    #print(a.poly, len(a.poly))
    #print(b.poly, len(b.poly))
    #print(cz_poly.poly, len(cz_poly.poly))
