from aes_gcm.aes_128_gcm import AES_128_GCM
from aes_gcm.gcm_util import GF, GFElement
from aes_gcm.cantor_zassenhaus import CZ 
from aes_gcm.poly import Poly 
from aes_gcm.ghashcrack import GHashCrack, CrackMsg

import os
if __name__ == "__main__":

# tests for aes_gcm.util
#-----------------------------------------------------------------------------------------------------------------#    
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
    assert (GFElement([1,2,6,7,10])**100).element == [4, 5, 8, 10, 12, 14, 20, 21, 25, 26, 33, 35, 38, 43, 44, 45, 46, 47, 50, 51, 53, 54, 55, 56, 57, 58, 60, 61, 64, 67, 71, 72, 74, 75, 76, 77, 78, 80, 81, 82, 83, 85, 90, 93, 94, 95, 96, 98, 99, 101, 103, 104, 105, 109, 110, 112, 115, 118, 119, 120, 121, 123, 124, 127]
    for i in range(1000):
        a_block = os.urandom(16)
        b_block = os.urandom(16)
        a = GFElement(GF.block_to_poly(a_block))
        b = GFElement(GF.block_to_poly(b_block))
        assert a_block == GF.poly_to_block(GF.block_to_poly(a_block))
        assert b_block == GF.poly_to_block(GF.block_to_poly(b_block))
        assert a*b == b*a

# tests for aes_gcm.aes_128_gcm
#----------------------------------------------------------------------------------------------------------------#
    #known answer test 0
    key     = b'\xfe\xff\xe9\x92\x86es\x1cmj\x8f\x94g0\x83\x08'
    nonce   = b'\xca\xfe\xba\xbe\xfa\xce\xdb\xad\xde\xca\xf8\x88'
    pt      = b'\xd912%\xf8\x84\x06\xe5\xa5Y\t\xc5\xaf\xf5&\x9a\x86\xa7\xa9S\x154\xf7\xda.L0=\x8a1\x8ar\x1c<\x0c\x95\x95h\tS/\xcf\x0e$I\xa6\xb5%'
    ct      = b'B\x83\x1e\xc2!wt$Kr!\xb7\x84\xd0\xd4\x9c\xe3\xaa!/,\x02\xa4\xe05\xc1~#)\xac\xa1.!\xd5\x14\xb2Tf\x93\x1c}\x8fjZ\xac\x84\xaa\x05'
    auth_tag= b'Qh\xa0S\xa2FQ\x85\xf6\xb1\x9e\xc2e\xa4\xe8\x8b'
    y0      = b'\xca\xfe\xba\xbe\xfa\xce\xdb\xad\xde\xca\xf8\x88\x00\x00\x00\x01'
    h       = b'\xb8;S7\x08\xbfS]\n\xa6\xe5)\x80\xd5;x'

    ciphero = AES_128_GCM(key, nonce)
    assert ciphero.auth_key == h
    assert ciphero.y0 == y0
    assert ciphero._encrypt(pt) == ct
    assert ciphero._auth_tag(ct) == auth_tag

    cipherino = AES_128_GCM(key, nonce)
    assert cipherino._encrypt(ct) == pt


    #known answer test 1 (nist test vector 1)
    key     = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    nonce   = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    ad      = b''
    pt      = b''
    ct      = b''
    auth_tag= b'X\xe2\xfc\xce\xfa~0a6\x7f\x1dW\xa4\xe7EZ'
    y0      = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01'
    h       = b'f\xe9K\xd4\xef\x8a,;\x88L\xfaY\xca4+.'

    ciphero = AES_128_GCM(key, nonce)
    assert ciphero.auth_key == h
    assert ciphero.y0 == y0
    assert ciphero._encrypt(pt) == ct
    assert ciphero._auth_tag(ct, ad) == auth_tag

    cipherino = AES_128_GCM(key, nonce)
    assert cipherino._encrypt(ct) == pt

    #known answer test 2 (nist test vector 2)
    key     = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    nonce   = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    ad      = b''
    pt      = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    ct      = b'\x03\x88\xda\xce`\xb6\xa3\x92\xf3(\xc2\xb9q\xb2\xfex'
    auth_tag= b'\xabnG\xd4,\xec\x13\xbd\xf5:g\xb2\x12W\xbd\xdf'
    y0      = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01'
    h       = b'f\xe9K\xd4\xef\x8a,;\x88L\xfaY\xca4+.'

    ciphero = AES_128_GCM(key, nonce)
    assert ciphero.auth_key == h
    assert ciphero.y0 == y0
    assert ciphero._encrypt(pt) == ct
    assert ciphero._auth_tag(ct, ad) == auth_tag

    cipherino = AES_128_GCM(key, nonce)
    assert cipherino._encrypt(ct) == pt


    #known answer test 3 (nist test vector 3)
    key     = b'\xfe\xff\xe9\x92\x86es\x1cmj\x8f\x94g0\x83\x08'
    nonce   = b'\xca\xfe\xba\xbe\xfa\xce\xdb\xad\xde\xca\xf8\x88'
    ad      = b''
    pt      = b'\xd912%\xf8\x84\x06\xe5\xa5Y\t\xc5\xaf\xf5&\x9a\x86\xa7\xa9S\x154\xf7\xda.L0=\x8a1\x8ar\x1c<\x0c\x95\x95h\tS/\xcf\x0e$I\xa6\xb5%\xb1j\xed\xf5\xaa\r\xe6W\xbac{9\x1a\xaf\xd2U'
    ct      = b'B\x83\x1e\xc2!wt$Kr!\xb7\x84\xd0\xd4\x9c\xe3\xaa!/,\x02\xa4\xe05\xc1~#)\xac\xa1.!\xd5\x14\xb2Tf\x93\x1c}\x8fjZ\xac\x84\xaa\x05\x1b\xa3\x0b9j\n\xac\x97=X\xe0\x91G?Y\x85'
    auth_tag= b"M\\*\xf3'\xcdd\xa6,\xf3Z\xbd+\xa6\xfa\xb4"
    y0      = b'\xca\xfe\xba\xbe\xfa\xce\xdb\xad\xde\xca\xf8\x88\x00\x00\x00\x01'
    h       = b'\xb8;S7\x08\xbfS]\n\xa6\xe5)\x80\xd5;x'

    ciphero = AES_128_GCM(key, nonce)
    assert ciphero.auth_key == h
    assert ciphero.y0 == y0
    assert ciphero._encrypt(pt) == ct
    assert ciphero._auth_tag(ct, ad) == auth_tag

    cipherino = AES_128_GCM(key, nonce)
    assert cipherino._encrypt(ct) == pt

    #known answer test 4 (nist test vector 4)
    key     = b'\xfe\xff\xe9\x92\x86es\x1cmj\x8f\x94g0\x83\x08'
    nonce   = b'\xca\xfe\xba\xbe\xfa\xce\xdb\xad\xde\xca\xf8\x88'
    ad      = b'\xfe\xed\xfa\xce\xde\xad\xbe\xef\xfe\xed\xfa\xce\xde\xad\xbe\xef\xab\xad\xda\xd2'
    pt      = b'\xd912%\xf8\x84\x06\xe5\xa5Y\t\xc5\xaf\xf5&\x9a\x86\xa7\xa9S\x154\xf7\xda.L0=\x8a1\x8ar\x1c<\x0c\x95\x95h\tS/\xcf\x0e$I\xa6\xb5%\xb1j\xed\xf5\xaa\r\xe6W\xbac{9'
    ct      = b'B\x83\x1e\xc2!wt$Kr!\xb7\x84\xd0\xd4\x9c\xe3\xaa!/,\x02\xa4\xe05\xc1~#)\xac\xa1.!\xd5\x14\xb2Tf\x93\x1c}\x8fjZ\xac\x84\xaa\x05\x1b\xa3\x0b9j\n\xac\x97=X\xe0\x91'
    auth_tag= b'[\xc9O\xbc2!\xa5\xdb\x94\xfa\xe9Z\xe7\x12\x1aG'
    y0      = b'\xca\xfe\xba\xbe\xfa\xce\xdb\xad\xde\xca\xf8\x88\x00\x00\x00\x01'
    h       = b'\xb8;S7\x08\xbfS]\n\xa6\xe5)\x80\xd5;x'

    ciphero = AES_128_GCM(key, nonce)
    assert ciphero.auth_key == h
    assert ciphero.y0 == y0
    assert ciphero._encrypt(pt) == ct
    assert ciphero._auth_tag(ct, ad) == auth_tag

    cipherino = AES_128_GCM(key, nonce)
    assert cipherino._encrypt(ct) == pt

    #known answer test 5 (nist test vector 5)
    key     = b'\xfe\xff\xe9\x92\x86es\x1cmj\x8f\x94g0\x83\x08'
    nonce   = b'\xca\xfe\xba\xbe\xfa\xce\xdb\xad'
    ad      = b'\xfe\xed\xfa\xce\xde\xad\xbe\xef\xfe\xed\xfa\xce\xde\xad\xbe\xef\xab\xad\xda\xd2'
    pt      = b'\xd912%\xf8\x84\x06\xe5\xa5Y\t\xc5\xaf\xf5&\x9a\x86\xa7\xa9S\x154\xf7\xda.L0=\x8a1\x8ar\x1c<\x0c\x95\x95h\tS/\xcf\x0e$I\xa6\xb5%\xb1j\xed\xf5\xaa\r\xe6W\xbac{9'
    ct      = b'a5;L(\x06\x93Jw\x7f\xf5\x1f\xa2*GUi\x9b*qO\xcd\xc6\xf87f\xe5\xf9{lt#s\x80i\x00\xe4\x9f$\xb2+\tuD\xd4\x89kBI\x89\xb5\xe1\xeb\xac\x0f\x07\xc2?E\x98'
    auth_tag= b'6\x12\xd2\xe7\x9e;\x07\x85V\x1b\xe1J\xac\xa2\xfc\xcb'
    y0      = b'\xc4:\x83\xc4\xc4\xba\xde\xc45L\xa9\x84\xdb%/}'
    h       = b'\xb8;S7\x08\xbfS]\n\xa6\xe5)\x80\xd5;x'

    ciphero = AES_128_GCM(key, nonce)
    assert ciphero.auth_key == h
    assert ciphero.y0 == y0
    assert ciphero._encrypt(pt) == ct
    assert ciphero._auth_tag(ct, ad) == auth_tag

    cipherino = AES_128_GCM(key, nonce)
    assert cipherino._encrypt(ct) == pt

    #known answer test 6 (nist test vector 6)
    key     = b'\xfe\xff\xe9\x92\x86es\x1cmj\x8f\x94g0\x83\x08'
    nonce   = b'\x93\x13"]\xf8\x84\x06\xe5U\x90\x9cZ\xffRi\xaajz\x958SO}\xa1\xe4\xc3\x03\xd2\xa3\x18\xa7(\xc3\xc0\xc9QV\x80\x959\xfc\xf0\xe2B\x9akRT\x16\xae\xdb\xf5\xa0\xdejW\xa67\xb3\x9b'
    ad      = b'\xfe\xed\xfa\xce\xde\xad\xbe\xef\xfe\xed\xfa\xce\xde\xad\xbe\xef\xab\xad\xda\xd2'
    pt      = b'\xd912%\xf8\x84\x06\xe5\xa5Y\t\xc5\xaf\xf5&\x9a\x86\xa7\xa9S\x154\xf7\xda.L0=\x8a1\x8ar\x1c<\x0c\x95\x95h\tS/\xcf\x0e$I\xa6\xb5%\xb1j\xed\xf5\xaa\r\xe6W\xbac{9'
    ct      = b'\x8c\xe2I\x98bV\x15\xb6\x03\xa03\xac\xa1?\xb8\x94\xbe\x91\x12\xa5\xc3\xa2\x11\xa8\xba&*<\xca~,\xa7\x01\xe4\xa9\xa4\xfb\xa4<\x90\xcc\xdc\xb2\x81\xd4\x8c|o\xd6(u\xd2\xac\xa4\x17\x03L4\xae\xe5'
    auth_tag= b'a\x9c\xc5\xae\xff\xfe\x0b\xfaF*\xf4<\x16\x99\xd0P'
    y0      = b';\xabux\n1\xc0Y\xf8=*Du/\x98d'
    h       = b'\xb8;S7\x08\xbfS]\n\xa6\xe5)\x80\xd5;x'

    ciphero = AES_128_GCM(key, nonce)
    assert ciphero.auth_key == h
    assert ciphero.y0 == y0
    assert ciphero._encrypt(pt) == ct
    assert ciphero._auth_tag(ct, ad) == auth_tag

    cipherino = AES_128_GCM(key, nonce)
    assert cipherino._encrypt(ct) == pt

# tests for aes_gcm.cantor_zassenhaus
#-----------------------------------------------------------------------------------------------------------------#

    inputvector = Poly.bytes_to_list([b'\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00', b'dj\xb3\xad*\xa0\xd3a\x02>L\x80\xc5\xed\x00\x95', b'\xec\x06\x05P:f\xa6\xf8\xc2!G\x81\xd1\xa7u5', b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00', b'\x1b\x00\x1b\xb3&\xfc\xba\x8a_\\\x0f\xfa)\xe7o9'][::-1])
    expected_factors = [[[0, 1, 2, 3, 6, 10, 12, 14, 15, 16, 17, 21, 26, 27, 29, 30, 32, 33, 34, 37, 39, 40, 41, 44, 45, 47, 49, 55, 59, 60, 61, 63, 68, 74, 80, 83, 85, 86, 87, 89, 91, 92, 94, 95, 96, 97, 101, 103, 105, 106, 107, 108, 110, 111, 113, 115, 117, 120, 121, 123, 124, 126, 127], [0]], [[0, 2, 3, 4, 6, 9, 14, 17, 18, 22, 26, 29, 30, 34, 36, 42, 43, 48, 49, 51, 56, 58, 59, 66, 67, 69, 71, 74, 75, 77, 78, 79, 80, 82, 83, 87, 88, 89, 90, 92, 95, 98, 99, 100, 101, 102, 104, 105, 107, 108, 109, 113, 116, 117, 119, 121, 122, 125, 126, 127], [0]], [[0, 2, 3, 4, 10, 11, 12, 14, 15, 17, 19, 22, 23, 26, 27, 29, 30, 31, 36, 40, 42, 43, 44, 45, 46, 47, 49, 51, 54, 55, 57, 59, 60, 61, 63, 68, 70, 72, 74, 77, 78, 80, 81, 82, 85, 87, 90, 92, 95, 96, 104, 105, 107, 109, 111, 114, 115, 116, 118, 119, 121, 122, 123, 124], [0]], [[0, 3, 5, 10, 11, 12, 17, 21, 22, 24, 28, 30, 32, 33, 34, 36, 37, 38, 39, 40, 41, 42, 46, 51, 55, 56, 59, 63, 66, 67, 69, 71, 72, 76, 77, 78, 79, 80, 84, 85, 86, 87, 91, 92, 94, 95, 96, 98, 99, 100, 101, 102, 104, 107, 108, 109, 110, 111, 114, 118, 121, 123, 127], [0]]]
    cz = CZ(Poly(inputvector))
    for i in range(20):
        factors = cz.factor_poly()
        assert sorted(factors)==expected_factors
                
                


# tests for aes_gcm.ghashcrack
#-----------------------------------------------------------------------------------------------------------------#
    msg1 = { 
        'ct' : b'B\x83\x1e\xc2!wt$Kr!\xb7\x84\xd0\xd4\x9c\xe3\xaa!/,\x02\xa4\xe05\xc1~#)\xac\xa1.!\xd5\x14\xb2Tf\x93\x1c}\x8fjZ\xac\x84\xaa\x05',
        'ad' : b'',
        'tag': b'Qh\xa0S\xa2FQ\x85\xf6\xb1\x9e\xc2e\xa4\xe8\x8b'
    }
    msg2 = {
        'ct' : b'\x8a\xa3=\xc5\xfb\xd1P\xe3\xcc\t\nP\t\x07\xc15!I\xcc8}r\x17~\\\xca\tY\xe4\xdal\x1b\xa4p\x81\xbeX\xa5!\xf4\xe9\xfb\xdf\xc5_\x98\xa5\x9b',
        'ad' : b'',
        'tag': b'\xd4\xa8\xe9\xe3\xabLY\x16\xec\xef%\x15\x08W\xcdC'
    }
    msg3 = {
        'ct' : b'0\x19\x87]cI\xc1\xf2\xdd\x18\nP\t\x07\xc15V>\xbbN(\x15G\x19\x0f\xca\tY\xe4\xdal\x1b\xaf\xcb;o\xc8-\xee\xd7`9\xe0]_\x98\xa5\x9b',
        'ad' : b'',
        'tag': b'\xae\xd9\xe0`\xa4\xdfO\xba\xd3op\x97\xd3\xf8\xfd\x7f',
    }
    msg1 = CrackMsg(msg1["ct"], msg1["ad"], msg1["tag"])
    msg2 = CrackMsg(msg2["ct"], msg2["ad"], msg2["tag"])
    msg3 = CrackMsg(msg3["ct"], msg3["ad"], msg3["tag"])

    test = GHashCrack(msg1,msg2,msg3)
    test.crack()
    assert test.forge_auth_tag(b'', b'0\x19\x87]cI\xc1\xf2\xdd\x18\nP\t\x07\xc15V>\xbbN(\x15G\x19\x0f\xca\tY\xe4\xdal\x1b\xaf\xcb;o\xc8-\xee\xd7`9\xe0]_\x98\xa5\x9b') == b'\xae\xd9\xe0`\xa4\xdfO\xba\xd3op\x97\xd3\xf8\xfd\x7f'
    assert test.forge_auth_tag(b'', b'\xa8\x81\x1f\xd4\xea\xc0A\xf2\xdd\x18\nP\t\x07\xc15V>\xbbO}r\x17~\\\xca\tY\xe4\xdal\x1b\xaf\xcb:\x0eX\xa5!\xf4\xe9\xfb\xdf\xc5_\x98\xa5\x9b') == b'\xb7\x0f\xe5{\xaf\x14\xf8}\x1e\x9a2\x95;P\xa2\xef'


# tests for aes_gcm poly
#-----------------------------------------------------------------------------------------------------------------#
    d, m = divmod(Poly([[],[],[],[],[1,2,3,4],[2,5,7,9]]), Poly([[],[],[1,2,3],[1],[5]]))
    assert d.poly == [[0, 1, 3, 5, 121, 122, 124, 126], [2, 5, 125, 126]] and m.poly == [[], [], [0, 1, 3, 5, 122, 126], [5, 7, 122, 123, 125, 126, 127]]

    print("All tests passed")