class GF:
    def __init__(self,  characteristic_polynomial=[0,1,2,7], field_size=128):
        self.cp = characteristic_polynomial
        self.field_size = field_size

    def reduce(self, a):
        #reduces a given byte block into initialized the galios field
        return a
        #tmp = int.from_bytes(a)
        #while len(tmp)>self.field_size-1:
        #    tmp = 123
        #return tmp.to_bytes()
    

    def block_to_poly(block : bytes):
        number = int.from_bytes(block, byteorder='big')
        res = []
        for i in range(len(block)*8):
            if number>>i&1:
                res = [127-i] + res
        return res

    def poly_to_block(poly : list):
        number = 0
        for i in poly:
            number += 1<<127-i
        return number.to_bytes(16, byteorder='big')

class GFElement:
    def __init__(self,element,gf=GF()):
        self.gf = gf
        self.element = gf.reduce(element)

    def __mul__(self, a):
        pass




poly2block = b'\x08\x81\x81\x00\x00 \x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
block2poly = b':G\xc5E\xf1\xd8\x7f\xfb\x7f<\x82\xd2\x0b\xbd:B'
tmp = GF.block_to_poly(block2poly)
print(tmp)
print(GF.block_to_poly(poly2block))