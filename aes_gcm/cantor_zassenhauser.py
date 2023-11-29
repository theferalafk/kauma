from aes_gcm.poly import Poly
from aes_gcm.gcm_util import GF, GFElement
from os import urandom

class CZ:
    #hallo herr bauer, ich schaffe es nicht k2 weiter zu faktorisieren. ich weiß nicht woran es liegt und ich habe viele schritte in sage mitgerechnet
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
        for i in range(10):
            tmp = self.cz_step(poly)
            if tmp:
                k1, k2 = tmp
                return k1, k2
        return None

    def factor_poly(self):
        res = []
        rem = Poly(self.f.poly.copy())
        tmp = self.get_factor(rem)
        active = True
        if tmp:
            k1, k2 = tmp
            #print(k1.poly, k2.poly)
            candidates = [k1, k2]
            while candidates:
                tmp = []
                for fraction in candidates:
                    if len(fraction.poly)>2:
                        new_candidates = self.get_factor(fraction)
                        if new_candidates:
                            nc1, nc2 = new_candidates
                            #print(nc1.poly, nc2.poly)
                            tmp += [nc1,nc2]
                        else:
                            break
                    else:
                        res.append(fraction.poly)
                
                candidates = tmp.copy()
        return res


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
    tmp = Poly.bytes_to_list([b'\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00', b'dj\xb3\xad*\xa0\xd3a\x02>L\x80\xc5\xed\x00\x95', b'\xec\x06\x05P:f\xa6\xf8\xc2!G\x81\xd1\xa7u5', b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00', b'\x1b\x00\x1b\xb3&\xfc\xba\x8a_\\\x0f\xfa)\xe7o9'][::-1])
    print(tmp)
    cz = CZ(Poly(tmp))
    for i in range(20):
        carry = cz.factor_poly()
        print(len(carry))
    for i in carry:
        print(GF.poly_to_block(i[0]))