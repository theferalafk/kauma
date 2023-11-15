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
        #in range(highest_exponent) so it does need to compute entire array in case e.g. hightest exponent=3 but array is [1,1,1,0,0,0,0,0,0,0,0,0,0,0]
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



if __name__ == "__main__":

    # test for poly_to_block / block_to_poly

    #known answer test 0
    block= b'\x08\x81\x81\x00\x00 \x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    poly = [4, 8, 15, 16, 23, 42]
    assert GF.block_to_poly(block)==poly
    assert GF.poly_to_block(poly)==block

    #known answer test 1 
    block = b':G\xc5E\xf1\xd8\x7f\xfb\x7f<\x82\xd2\x0b\xbd:B'
    poly = [2, 3, 4, 6, 9, 13, 14, 15, 16, 17, 21, 23, 25, 29, 31, 32, 33, 34, 35, 39, 40, 41, 43, 44, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 62, 63, 65, 66, 67, 68, 69, 70, 71, 74, 75, 76, 77, 80, 86, 88, 89, 91, 94, 100, 102, 103, 104, 106, 107, 108, 109, 111, 114, 115, 116, 118, 121, 126]
    assert GF.block_to_poly(block)==poly
    assert GF.poly_to_block(poly)==block

    # test for _bitarray_to_poly / _poly_to_bitarray

    #known answer test 0
    poly = [0, 2, 3, 6, 8]
    bitarray = [1, 0, 1, 1, 0, 0, 1, 0, 1]
    assert GF._poly_to_bitarray(poly)==bitarray
    assert GF._bitarray_to_poly(bitarray,len(bitarray)-1)==poly

    #known answer test 1
    poly = [2, 4, 6, 7, 8, 13, 14]
    bitarray = [0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1]
    assert GF._poly_to_bitarray(poly)==bitarray
    assert GF._bitarray_to_poly(bitarray,len(bitarray)-1)==poly

    #known anser test 2
    poly = [2, 3, 4, 6, 9, 13, 14, 15, 16, 17, 21, 23, 25, 29, 31, 32, 33, 34, 35, 39, 40, 41, 43, 44, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 62, 63, 65, 66, 67, 68, 69, 70, 71, 74, 75, 76, 77, 80, 86, 88, 89, 91, 94, 100, 102, 103, 104, 106, 107, 108, 109, 111, 114, 115, 116, 118, 121, 126]
    bitarray = [0, 0, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1]
    assert GF._poly_to_bitarray(poly)==bitarray
    assert GF._bitarray_to_poly(bitarray,len(bitarray)-1)==poly

    # test for reduce

    #known answer test 1
    cp = [0, 2, 3, 6, 8]
    gf = GF(cp)
    full_size = [2, 4, 6, 7, 8, 13, 14]
    reduced = [3, 4, 5, 7]
    assert gf.reduce(full_size)==reduced

    print("All tests were passed successfully")