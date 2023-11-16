class GF:
    def __init__(self, characteristic_polynomial=[0,1,2,7,128]):
        self._cp = characteristic_polynomial
        self._field_size = characteristic_polynomial[-1]

    def _poly_to_bitarray(a):
        #transform poly list to bit array
        res = [0]*(a[-1]+1)
        for exp in a:
                res[exp] = 1
        return res

    def _bitarray_to_poly(a, highest_exponent=False):
        #transform bit array to poly list
        res = []
        #in range(highest_exponent) so it does need to compute entire array in case e.g. hightest exponent=3 but array is [1,1,1,0,0,0,0,0,0,0,0,0,0,0]
        if not highest_exponent:
            highest_exponent=len(a)-1
        for i in range(highest_exponent+1):
            if a[i]==1:
                res.append(i)       
        return res 
    
    def _reduce_one(self, a):
        res = a
        for exp in self._cp:
            res[exp] ^= 1
        return res[:-1]

    def reduce(self, a):
        #reduces a given poly list into initialized the galios field
        #returns the result as an poly list
        #if element is already in the field
        if a[-1]<self._field_size:
            return a
        #if only one reduction is needed
        if a[-1]==self._field_size:
            return self._reduce_one(a)
        
        #more then one reduction
        tmp = GF._poly_to_bitarray(a)
        diff = a[-1] - self._field_size
        for i in range(diff,0,-1):
            #checks for leading 1 to reduce
            if tmp[-1]==1:
                #xor characteristic poly shifted to bit array
                for exp in self._cp:
                    tmp[exp+i] ^= 1
            tmp=tmp[:-1]
        return GF._bitarray_to_poly(tmp, self._field_size)
    

    
    def carry_less_mul_gf(self, a, b):
        #takes two poly form elements of a field and multiplies them carryless
        #returns a new poly form element
        #normalize a and b if needed
        if a[-1]>self._field_size-1:
            a = self.reduce(a)
        if b[-1]>self._field_size-1:
            b = self.reduce(b)

        accumulator = GF._poly_to_bitarray(a)
        #if accumulator is too small, pad with zeros
        acc_len = len(accumulator)
        if acc_len<self._field_size:
            accumulator += [0]*(self._field_size-acc_len)
        b_bitarray = GF._poly_to_bitarray(b)
        res = [0]*self._field_size
        for bit in b_bitarray:
            if bit==1:
                for i, bit in enumerate(accumulator):
                    res[i] ^= bit
            accumulator = [0] + accumulator
            if accumulator[-1]==1:
                accumulator = self._reduce_one(accumulator)
            else:
                accumulator = accumulator[:-1]

        return GF._bitarray_to_poly(res)
        
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
    def __init__(self, element, gf=GF()):
        self.gf = gf
        self.element = gf.reduce(element)

    def __mul__(self, a):
        #carryless mul on two gf elements, if the elements are not of the same gf, the multiplication uses the field of the first element e.g (a*b) field of a is used 
        return self.gf.carry_less_mul_gf(self.element, a.element)

class gcm_nonce:
    def __init__(self, nonce):
        #nonce should be max 96 bits and 1<=nonce<=2^64-1
        self.nonce = nonce
        self.counter = 0

    def __iter__(self):
        return self
    
    def __next__(self):
        self.counter += 1
        return self.nonce.to_bytes()


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

    # test for carry_less_mul_gf

    #known answer test 0
    a = [0,2,7]
    b = [2,6,7]
    res = gf.carry_less_mul_gf(a,b)
    assert res == gf.carry_less_mul_gf(b,a) == [3,4,5,7]
    a = GFElement([0,2,7],gf)
    b = GFElement([2,6,7],gf)
    assert a*b == b*a == [3,4,5,7]
    c = GFElement([1,2],gf)

    #known answer test 1
    a_block = b'\x8e6(\x0f\xa9\x1f7\xef\xd8\xfe\x0e\x07\x97\xdfu\x0b'
    b_block = b'\xb5\x0b\x13\xa0\xce\x1b\xcc\xe4-\xa2\xdf\xf5\xc3\x8c|<'
    a_times_b_block = b'\x92\x19\xefb+iMo\x12\xbfvT\x98Z\x9a\xb3'
    a_times_b_poly = [0, 3, 6, 11, 12, 15, 16, 17, 18, 20, 21, 22, 23, 25, 26, 30, 34, 36, 38, 39, 41, 42, 44, 47, 49, 52, 53, 55, 57, 58, 60, 61, 62, 63, 67, 70, 72, 74, 75, 76, 77, 78, 79, 81, 82, 83, 85, 86, 89, 91, 93, 96, 99, 100, 105, 107, 108, 110, 112, 115, 116, 118, 120, 122, 123, 126, 127]
    a = GFElement(GF.block_to_poly(a_block))
    b = GFElement(GF.block_to_poly(b_block))
    assert a_times_b_block == GF.poly_to_block(a_times_b_poly)
    assert a_times_b_poly == GF.block_to_poly(a_times_b_block)
    #also test if a and b are not of same length
    assert a*b == b*a == a_times_b_poly

    #statistical tests
    import os
    for i in range(10000):
        a_block = os.urandom(16)
        b_block = os.urandom(16)
        a = GFElement(GF.block_to_poly(a_block))
        b = GFElement(GF.block_to_poly(b_block))
        assert a_block == GF.poly_to_block(GF.block_to_poly(a_block))
        assert b_block == GF.poly_to_block(GF.block_to_poly(b_block))
        assert a*b == b*a
        
    print("All tests were passed successfully")

