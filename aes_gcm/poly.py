from gcm_util import GF, GFElement
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
    
    def _element_to_int(self, element):
        res = 0
        for exp in element:
            res += 2**exp
        return res

    def _int_to_element(self, e_int):
        res = []
        for i in range(129,-1,-1):
            if e_int > 2**i-1:
                res.append(i)
                e_int -= 2**i
        return res

    def __add__(self, _b):
        a = self.poly
        b = _b.poly
        res = []
        diff = len(a) - len(b)
        if diff<0:
            return _b+self
        if diff:
            for _ in range(diff):
                b.append([])
        for i, element in enumerate(a):
            e_int = self._element_to_int(element) ^ self._element_to_int(b[i])
            #print(f"{element}, {b[i]} -> int:{e_int} {bin(e_int)} -> {self._int_to_element(e_int)}")
            res.append(self._int_to_element(e_int))
        return res
    
    def __mul__(self, _b):
        a = self.poly
        b = _b.poly
        summands = []
        len(a)
        print("calc on ", a, b)
        for i, element_a in enumerate(a):
            # summanden werden hier berechnet
            tmp = []
            for j, element_b in enumerate(b):
                tmp.append(GFElement(element_a)*GFElement(element_b))
            summands.append([[]]*i + tmp)
        #hier müssen die dann aufaddiert werden und dann kommt res raus
        res = Poly([])
        for summand in summands:
            print(";)", summand)
            res = Poly(res+Poly(summand))
        return res.poly


k={
"a": [
"BAAAAAAAAAAAAAAAAAAAAA==",
"AgAAAAAAAAAAAAAAAAAAAA==",
"AcAAAAAAAAAAAAAAAAAAAA=="
],
"b": [
"JGAAAAAAAAAAAAAAAAAAAA==",
"AAgAAAAAAAAAAAAAAAAAAA==",
"EUAAAAAAAAAAAAAAAAAAAA=="
],
"result": [
"IGAAAAAAAAAAAAAAAAAAAA==",
"AggAAAAAAAAAAAAAAAAAAA==",
"EIAAAAAAAAAAAAAAAAAAAA=="
]
}

for key in ["a","b","result"]:
    a = k[key]
    pol = ''
    for i in range(3):
        pol = 'x^'+str(i)+str(GF.block_to_poly(base64.b64decode(a[i]))) + ' + ' + pol
    #print(pol)
    # a = x^2[7, 8, 9] + x^1[6] + x^0[5]
    # b = x^2[3, 7, 9] + x^1[12] + x^0[2, 5, 9, 10]
    # c = x^2[3, 8] + x^1[6, 12] + x^0[2, 9, 10]
#print(Poly.b64_to_list(k["a"]))
print(Poly.b64_to_list(k["a"]))
print(Poly.b64_to_list(k["b"]))
print(Poly(Poly.b64_to_list(k["b"]))+Poly(Poly.b64_to_list(k["a"])))
print(Poly.b64_to_list(k["result"]))
print(Poly(Poly.b64_to_list(k["b"]))*Poly(Poly.b64_to_list(k["a"])))
'''
F.<x>=GF(2^128)
R.<X>= PolynomialRing(F)
a = F.gen()
b = (a^9+a^8+a^7)*X^2 + (a^6)*X + a^5
c = (a^9+a^7+a^3)*X^2 + (a^12)*X + (a^2+a^5+a^9+a^10)
t = X^2*(a^7+a^8+a^9) + X^1*(a^6) + X^0*(a^5)
b+c

'''