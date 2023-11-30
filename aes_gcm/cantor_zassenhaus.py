from aes_gcm.poly import Poly
from aes_gcm.gcm_util import GF
from os import urandom

class CZ:
    #tries to factories a poly of class Poly 
    def __init__(self, f: Poly):
        self.f = f
        self.degree = len(f.poly)-1


    def _randpoly(d):
        res = []
        for i in range(d):
            res.append(GF.block_to_poly(urandom(16)))
        return Poly(res)

    def cz_step(self, p : Poly):
        #implementation of cantor zassenhaus
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

    def _get_factor(self, p: Poly):
        #tries 10 times to factor poly
        poly = Poly(p.poly.copy())
        for i in range(10):
            tmp = self.cz_step(poly)
            if tmp:
                k1, k2 = tmp
                return k1, k2
        return None

    def factor_poly(self):
        #tries to factor a poly until only factor of degree 1 are remaining
        res = []
        rem = Poly(self.f.poly.copy())
        tmp = self._get_factor(rem)
        tries = 0
        if tmp:
            k1, k2 = tmp
            candidates = [k1, k2]
            while candidates and tries<100:
                tmp = []
                for fraction in candidates:
                    if len(fraction.poly)>2:
                        new_candidates = self._get_factor(fraction)
                        if new_candidates:
                            nc1, nc2 = new_candidates
                            tmp += [nc1,nc2]
                        else:
                            break
                    else:
                        res.append(fraction.poly)
                tries+=1
                candidates = tmp.copy()
        return res
