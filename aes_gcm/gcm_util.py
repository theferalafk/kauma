class GF:
    def __init__(self, characteristic_polynomial=[0,1,2,7,128], order=2**128):
        self.cp = characteristic_polynomial
        self._field_size = characteristic_polynomial[-1]
        self.order = order

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
        for exp in self.cp:
            res[exp] ^= 1
        return res[:-1]

    def reduce(self, a):
        #reduces a given poly list into initialized the galios field
        #returns the result as an poly list
        #if element is already in the field
        if len(a)==0:
            return a
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
                for exp in self.cp:
                    tmp[exp+i] ^= 1
            tmp=tmp[:-1]
        return GF._bitarray_to_poly(tmp, self._field_size)
    

    
    def carry_less_mul_gf(self, a, b):
        #takes two poly form elements of a field and multiplies them carryless
        #returns a new poly form element
        #normalize a and b if needed
        if len(a)==0 or len(b)==0:
            return [] 
        if a[-1]>self._field_size-1:
            a = self.reduce(a)
        if b[-1]>self._field_size-1:
            b = self.reduce(b)

        accumulator = GF._poly_to_bitarray(a)
        #if accumulator is too small, pad with zeros
        #maybe change pcl mul qdq
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
    
    def __pow__(self, exp):
        res = GFElement([0])
        for i in range(exp.bit_length()-1,-1,-1):
            res = GFElement(res*res)
            if (exp>>i)&1:
                res = GFElement(res*self)
        return res
    
    def __invert__(self):
        #GFElement inverse because of fermat
        return self**(self.gf.order-2)
    
class gcm_nonce:
    def __init__(self, nonce):
        #nonce should be max 96 bits and 1<=nonce<=2^64-1
        self.nonce = int.from_bytes(nonce, byteorder='big')
        self.counter = 1

    def __iter__(self):
        return self
    
    def __next__(self):
        self.nonce += 1
        return self.nonce.to_bytes(16,byteorder='big')

