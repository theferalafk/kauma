class GF:
    def __init__(self,  characteristic_polynomial=[0,1,2,7,128]):
        self._cp = characteristic_polynomial
        self._field_size = characteristic_polynomial[-1]

    def _poly_to_bitarray(a):
        #transform poly list to bit array
        res = [0]*(a[-1]+1)
        for exp in a:
            res[exp] = 1
        return res

    def _bitarray_to_poly(a, highest_exponent=128):
        #transform bit array to poly list
        res = []
        for i in range(highest_exponent+1):
            if a[i]==1:
                res.append(i)       
        return res 

    def reduce(self, a):
        #reduces a given poly list into initialized the galios field
        #returns the result as an poly list

        tmp = GF._poly_to_bitarray(a)
        
        diff = a[-1] - self._field_size
        #print("current round:  -", list(reversed(tmp)))
        for i in range(diff,0,-1):
        #check if bit array needs to be reduced
            #xor characteristic poly shifted to bit array
            for exp in self._cp:
                tmp[exp+i] ^= 1
            #print("current round: ", i, list(reversed(tmp)))
            if not 1 in tmp[self._field_size:]:
                break
        #print(list(reversed(tmp)), self._field_size)
        return GF._bitarray_to_poly(tmp, self._field_size)
        
    

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
print(GF.poly_to_block(tmp))
print(GF.poly_to_block([4,8,15,16,23,42]))


cp = GF._bitarray_to_poly([1,0,1,1,0,0,1,0,1],8)
print(cp)
gf = GF(cp)
red = GF._bitarray_to_poly([0,0,1,0,1,0,1,1,1,0,0,0,0,1,1], len([0,0,1,0,1,0,1,1,1,0,0,0,0,1,1])-1)
print(gf.reduce(red))
print(GF._bitarray_to_poly([0,0,0,1,1,1,0,1],7))