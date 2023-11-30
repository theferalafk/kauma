from aes_gcm.gcm_util import GF, GFElement
import base64



class Poly:
    def __init__(self, element_list):
        self.poly = element_list
    
    def b64_to_list(b64list):
        res = []
        for element in b64list:
            res.append(GF.block_to_poly(base64.b64decode(element)))
        return res

    def bytes_to_list(byte_list):
        res = []
        for element in byte_list:
            res.append(GF.block_to_poly(element))
        return res
    
    def _element_to_int(element):
        res = 0
        for exp in element:
            res += 2**exp
        return res

    def _int_to_element(e_int):
        res = []
        for i in range(129,-1,-1):
            if e_int > 2**i-1:
                res.append(i)
                e_int -= 2**i
        return res[::-1]

    def __add__(self, _b):
        a = self.poly.copy()
        b = _b.poly.copy()
        res = []
        diff = len(a) - len(b)
        if diff<0:
            return _b+self
        if diff:
            for _ in range(diff):
                b.append([])
        for i, element in enumerate(a):
            e_int = Poly._element_to_int(element) ^ Poly._element_to_int(b[i])
            res.append(Poly._int_to_element(e_int))
        return Poly(res)
    
    def __mul__(self, _b):
        a = self.poly
        b = _b.poly
        summands = []
        for i, element_a in enumerate(a):
            # summanden werden hier berechnet
            tmp = []
            for element_b in b:
                tmp.append(GFElement(element_a)*GFElement(element_b))
            summands.append([[]]*i + tmp)
        #hier müssen die dann aufaddiert werden und dann kommt res raus
        res = Poly([])
        for summand in summands:
            res += Poly(summand)
        return res
 
    def __divmod__(self, _b):
        if _b.poly == [] or _b.poly == [[]]:
            return Poly([]), Poly([])
        a_degree = len(self.poly)
        b_degree = len(_b.poly)
        res = []
        tmp = self.poly.copy()
        b0_inverse = ~GFElement(_b.poly[-1])
        if a_degree < b_degree:
            return (Poly([]), self)
        ending_on_zero = 0
        for i in range(len(tmp),0,-1):
            poly = tmp[i-1]
            #check if coefficient is 0
            if b_degree > i:
                break
            if poly == []:
                tmp = tmp[:-1]
                res.append([])
                ending_on_zero += 1
                continue
            if b_degree > i:
                break
            #check if division is already done
            quotient = GFElement(poly) * b0_inverse
            res.append(quotient)
            poly_tmp = Poly(tmp)
            to_add = Poly([[]]*(i-b_degree)+(_b * Poly([quotient])).poly)
            tmp = (poly_tmp + to_add).poly[:-1]
            ending_on_zero = 0
        res += [[]]*ending_on_zero
        #test if tmp is empty, used to pad zeroes 
        tmp_clean = Poly([])
        for polies in tmp:
            if polies:
                tmp_clean = Poly(tmp)
        return Poly(list(reversed(res))), tmp_clean

    def __floordiv__(self, b):
        res, _ = divmod(self,b)
        return res
    
    def __mod__(self, b):
        _, res = divmod(self,b)
        return res

    def normalize(self):
        return self//Poly([self.poly[-1]])

    def gcd(self,_b):
        tmp = Poly([[0]])
        #avoid call by reference stuff
        a = Poly(self.poly.copy())
        b = Poly(_b.poly.copy())

        if len(a.poly) == 0:
            return b
        if len(b.poly) == 0:
            return a
        while b.poly != []:
            tmp = a % b
            a = b
            b = tmp
        if a.poly == []:
            return Poly([[0]]) 
        return a.normalize()
    
    def __pow__(self, exp):
        res = Poly([[0]])
        for i in range(exp.bit_length()-1,-1,-1):
            res = res*res
            if (exp>>i)&1:
                res = res*self
        return res
    
    def powmod(self, exp, mod):
        res = Poly([[0]])
        for i in range(exp.bit_length()-1,-1,-1):
            res = res*res
            if (exp>>i)&1:
                res = res*self
            _ , res = divmod(res, mod)
        return res
