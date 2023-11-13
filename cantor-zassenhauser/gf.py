class GF:
    def __init__(self,  characteristic_polynomial=[0,1,2,7]):
        self.cp = characteristic_polynomial

    def reduce(self, a):
        return a

    def block_to_poly(a):
        pass

    def poly_to_block(a):
        pass

class GFElement:
    def __init__(self,element,gf=GF()):
        self.gf = gf
        self.element = gf.reduce(element)

    def __mul__(self, a):
        return 1


a = GFElement([1,2,3])
b = GFElement([2,3,4])