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
