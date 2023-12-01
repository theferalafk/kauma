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
    for i in range(3):
        factors = cz.factor_poly()
        assert sorted(factors)==expected_factors
# tests for aes_gcm poly
#-----------------------------------------------------------------------------------------------------------------#
    d, m = divmod(Poly([[],[],[],[],[1,2,3,4],[2,5,7,9]]), Poly([[],[],[1,2,3],[1],[5]]))
    assert d.poly == [[0, 1, 3, 5, 121, 122, 124, 126], [2, 5, 125, 126]] and m.poly == [[], [], [0, 1, 3, 5, 122, 126], [5, 7, 122, 123, 125, 126, 127]]
    #operations got tested with sage

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

    #test vectors by frereit
    msg1 = {'ct': b'\x99h9E\x932/\x19\x88\xeb\x1d\xd9\x92d8\x7f\xc6\x8c7\xcfG\xdd\x19\xb7\xd1\xa5\xbd\xc8\x96\xbd\'"B\x8a3fe\xd7\xf0\\\x04Q&j\xf6\xfer\xd1', 'ad': b'', 'tag': b'(#\x07{\xa2\x17)\xfb\xff\x11\xa6\xc1!(\xc15'}
    msg2 = {'ct': b'\x89\x85T;Ju\x0ff\x0bE\x88`\x16\x84\xdd\x98\x8fh\xf7\xeah\xa7\xc0tp\x86\x11\xc9/\xd6\x0eo\xed\x91\xa7@\xff\xb5n\xc7K\x03\xeb6 y\xf9)', 'ad': b'', 'tag': b'me\x99gW\xd9\x02\x83\x89\xedk\xee\x97j\x8b\xe8'}
    msg3 = {'ct': b'a\x16\t\xca\xe4e\xf0\xa1Z\xe8\x14\xecB\x98\xe6\xdd\xae\xd9*N\x82+\x99\x80@\x9f\xba/`\xbf\xbc\xe4\xa4\x16H@\x1e\x14\xd3\xa5\xa4E9\x93h5\xf8j', 'ad': b'', 'tag': b' \x84L\xd7((\xaee-\xc1\xd5u\xea\xfd1T'}
    msg4 = {'ct': b"\x92\xb2'q\x1f\x90\xdf\xd4\xda\xcf\xe8f\x1f\xf8\xfa\xb5\x8a^\x08m\x89\xa4\xe7\xd3\xed\r\x029T\xc4\xb0\x9e\xb1\xdb1}\xfd,\x0e\xb9\x11\xb4zm\x03\x05\x0c\x11", 'ad': b'', 'tag': b'\xff\xeb\xef\xc4\x92\x9a@\xc8/\x17\xc2;\xbf\x02\x90.'}

    msg1 = CrackMsg(msg1["ct"], msg1["ad"], msg1["tag"])
    msg2 = CrackMsg(msg2["ct"], msg2["ad"], msg2["tag"])
    msg3 = CrackMsg(msg3["ct"], msg3["ad"], msg3["tag"])

    test = GHashCrack(msg1,msg2,msg3)
    test.crack()
    assert test.forge_auth_tag(msg4["ad"], msg4["ct"])==msg4["tag"]


    msg1 = {'ct': b'\x8b\xfc\x82jP\x90\x8d;\x95\x92\xb1\xc3q$\x8a\x8a\xdfTb3C\xe5\xdb\x99N\xd2\\\x85\xbb\xca+a\x00\xdf\xa9\xe1w\x8f\x91\xf8', 'ad': b'', 'tag': b'\xdaZ\xef<]\x8ak\x11t\xe1\x9e-X\xe6\xc8q'}
    msg2 = {'ct': b'\xa4\xc4y\xa6\x94\x13\xb2|I\xbc\xe4B\xc7\x81\xcbg\xcd}\x9d\x04!DLT\x8f\xf2\xaa\xdeg\xc8\x8fN\xb4\xdb=\x0bSx\x01\xf9', 'ad': b'', 'tag': b'\xeb \xfeUJ\x15Ae\\~\xbdC$\x7f\x0f\xff'}
    msg3 = {'ct': b'\x1am\xec\x9e\x08\x8b\n\xed\x85!\xafb\xceg\xfeH\x8d\\\\F5^0\x85\xe4\x11\x88\xc5U\xd0\x7f\xe2\xf9\xaa\xbcML\x13\xe4\xfc', 'ad': b'', 'tag': b'Ayq\x8c\xb1\x8c\x8a\x98\xa8z\t.S\x0f\x00\xbf'}
    msg4 = {'ct': b"\x8a\xcd\x82\xa4\xcf\xa4i\x1f\\1\x1c\\\x7fU\xfa\x15_\xec\x0eH\xa2'\x8c\x12b:L\xeb\xe2^ma=X\xd6\xb4\x9eJ\xde\xdc", 'ad': b'', 'tag': b'\x93\xec\xa3F\xd1\xcb;&8`\x16\xc9\xd0@\x03\x8d'}

    msg1 = CrackMsg(msg1["ct"], msg1["ad"], msg1["tag"])
    msg2 = CrackMsg(msg2["ct"], msg2["ad"], msg2["tag"])
    msg3 = CrackMsg(msg3["ct"], msg3["ad"], msg3["tag"])

    test = GHashCrack(msg1,msg2,msg3)
    test.crack()
    assert test.forge_auth_tag(msg4["ad"], msg4["ct"])==msg4["tag"]
    

    msg1 = {'ct': b'', 'ad': b'\x80\xe0s\x10\xb4\x07\xa1\x15\xed\xce?\xe6\xb1\xa1Zd\x16\xc5\xd4v3\xfdG\x02\x8c5\x1f\xf4\xe2[\xcc\x0f2\xe9=\xack\xb3=;\xf5\x17\xa8\xbf\xcc\x81]q', 'tag': b'\x01\xc8\xb4\xbf\x13\x06\xf6\xa9\xddJj\x9e>n?G'}
    msg2 = {'ct': b'', 'ad': b'\x9e\xe3\xb1z\x19\x99\xa1h~6\xc0\x96k3\xa1\xe5\x84\xad\xec\xc7\xd3:V\xbaYT\xfc\xf4\x1fb&nQXk\xf8\t\xa5Ar\xe7\x10\xe2/D\xbf`\xde', 'tag': b'\xa6\x94\xb7\xd0\x9e\xde\x10\xca4\x19(\xb6\xbf\x1d\x0e\xdd'}
    msg3 = {'ct': b'', 'ad': b'=\x97i\xdbF\xd8\xe1\xa4^(s9\r#D\xbdI\xf94\x02.\x8e\x89\xff\xc8\xf7\x02Z\x86\x11\x95\n\x9fE\xe33"\x1f\xf1\x01(\xd4du\xf5\xec\x81\x0c', 'tag': b'|.\xb4\xdfq\xfcf\xd0\x7f9\x82\x96\xb7L\xf4\xa2'}
    msg4 = {'ct': b'', 'ad': b'\xeb\x84\xf1\xeb\xf95\x94\x82\xb0\x0c\x94\x8au\x19\x8b?\x8e+\xed\x97|\x0c\xba\xa9x\x98R`\x8b\x05\x943\xd8p5\xa2\xa4o\x89\x95#\xca\x11\xd9\x0b >\xe4', 'tag': b'\xfe%\xe5\xf7\xe1u:\x98\x95\x85\xeeRn\x99\xfey'}

    msg1 = CrackMsg(msg1["ct"], msg1["ad"], msg1["tag"])
    msg2 = CrackMsg(msg2["ct"], msg2["ad"], msg2["tag"])
    msg3 = CrackMsg(msg3["ct"], msg3["ad"], msg3["tag"])

    test = GHashCrack(msg1,msg2,msg3)
    test.crack()
    assert test.forge_auth_tag(msg4["ad"], msg4["ct"])==msg4["tag"]


    msg1 = {'ct': b'\x0e\x96\x95\x1e0\x1c\xe0\x1dB\xa2\xc8\x87\xe9r\x9b\xe6\x05\xd1\xbe\x18\x84\xfa\xa2 u\x81\xe6\xeb\xb2O\xed\x0b', 'ad': b'\x08\x88\xa4.x\x81\x93\xf6f\xd1\x03\xfa\xa7\x13e\x1e', 'tag': b"\xe7f<\xb9<\x9f\xae\xa4Q\x08\xbe4!'q\x89"}
    msg2 = {'ct': b'\x16\xf2\xf9h\xc1\xc1\xad\xbdI\xcd\xff\xb9\xed\x14(\xf42\xca\xa3\xdas\xb3\xf4\xff%\xd7\xd8#0eMG', 'ad': b'\x9d\x0b\x0eI\xc8\xbf\x00IwQ\xcfH\xf9;\x9a\xb3', 'tag': b'IM\x13\\}\x97t%j\x9b\xf7i-\xc3\xe8\xd4'}
    msg3 = {'ct': b'n\x86\x06\xe1\x82[k(/\xe5\xa2\xf5%l\xd3\xd6jh\x1e\xf9\xe8\xa7\x07&!\xa4\x04G\x8f\xd3q\xbe', 'ad': b'\x9f\x1f\xa1n\xad\x00dNE\x8aJ\x82\x8c\x01\x13\xce', 'tag': b'\xf8z\xce\x8c\xffadv\xf3\xf5\x03S+L\x1d\x89'}
    msg4 = {'ct': b'9L\xe9+\x85u\xf5\xc1\xffX$K/\xd9\x1a\x85\xb79\x9e\x0b\xd3\x81\x18\xfb\x96\xd7\x8d\x08\x13\xee)K', 'ad': b'\x15e"\xe8_\x8c\x91Ri\x93\tP\x8d\xc2\xab\x17', 'tag': b'\xecRE[\xe4\x8fo\xb6\x8c\xf6\x87?d\x05\xa5\xc2'}

    msg1 = CrackMsg(msg1["ct"], msg1["ad"], msg1["tag"])
    msg2 = CrackMsg(msg2["ct"], msg2["ad"], msg2["tag"])
    msg3 = CrackMsg(msg3["ct"], msg3["ad"], msg3["tag"])

    test = GHashCrack(msg1,msg2,msg3)
    test.crack()
    assert test.forge_auth_tag(msg4["ad"], msg4["ct"])==msg4["tag"]


    msg1 = {'ct': b'\xe1\xb3m\xbd/0\x7fS)\x984)\xd9%\xf7\xb7/[\xf0^', 'ad': b'\x17\xd1\x9c\xdc\xbe\xb2\x19\xef\xebJ', 'tag': b'\xeb$\xe7\x1bU\x88p\xce7\xc9)7\x11\xb8Y\x94'}
    msg2 = {'ct': b'\x98V\x8d\x91x\xdd\x08\xe0+{\xf7Q^\xa1\xb3\xa2d.Q\xd9', 'ad': b'\x1d0\x17E}s)\xeb\x14 ', 'tag': b'\xdc\xb7\xd7\x80\xf1_.\x8d\xf7r,\x1c\xbb\x10\xb7\x0c'}
    msg3 = {'ct': b'\x7f\xfb\xeb\xfe\x94\xad\x00R\x8b\xc5\xd9K\xf8;u[\x95\x833\xa2', 'ad': b'\x7f\xa7~\\Y\xea\xe1\xcb\xed\x83', 'tag': b'\x96\xd7\xd0C\x80\xfc\xdd\xd1\xdfxSO\xe5\xf8\xe0\xdd'}
    msg4 = {'ct': b'n\x90\x1c\x9b+\xd4\xf4M\xa4C\x0c\xbc\x16\xb4\xd63:\xccG\x9f', 'ad': b'\xf0M\xea\x84xoz\x06\xe2\x98', 'tag': b'\xb6\xd1c\x1e\xa7l\x18s^\x91\xdc\xf0\xb4\xb2\xe9\x1b'}

    msg1 = CrackMsg(msg1["ct"], msg1["ad"], msg1["tag"])
    msg2 = CrackMsg(msg2["ct"], msg2["ad"], msg2["tag"])
    msg3 = CrackMsg(msg3["ct"], msg3["ad"], msg3["tag"])

    test = GHashCrack(msg1,msg2,msg3)
    test.crack()
    assert test.forge_auth_tag(msg4["ad"], msg4["ct"])==msg4["tag"]


    msg1 = {'ct': b'P\x80\xa0q\x86N\x9e8\x08rs\xac\xec\xf5YJ:::\xf8\x91=\xe8kf\xfa(\x1c\xe6_\xef2K^f\xf1\xdd\\+\xe2\xbfHCX\x02\xcen\xb9\xb0@O\xae\xad\xf7\xea\x01\x15\xf4\x00\xa8\xd7\xb8\xa2\xb0', 'ad': b'', 'tag': b'\xe2\xc0V\xaf\x1d"F\x9a\x85\xd3\x8au\x9a\x18\xee\''}
    msg2 = {'ct': b'\xffC{Io\x83;\x07\x84\xc3\xab\xdfh"\x1e\x01\x1cs\xad\xa13\x00\xeb\xc7FlC\xf9\xb6|\xb7\xa2\xe6\xf2\xca8S4o\xbaZ\x8a\x1e\xcd\xc9AS\x8b', 'ad': b'', 'tag': b'Sx\\\xa9\x9e\xf9\xaa3\xdd\x8bT\x8e7\x88\x11\xee'}
    msg3 = {'ct': b'\xf7\x89\xf85\xa1\x17\x8d\xbc\xa4x\x17\r\xce p\xba\xc7\xac\xe8\xc6\x13\x9e\x07\x1e"\xc4c\xc3g>\x1e\xc2\x98\xcf\x151W\x88,\x01\x9c"\xe1\x0b\xcey\xf3*', 'ad': b'', 'tag': b'\x16\x04\tq\xec\x10&\x18\x1e\x1d\xba$\xce\x11\xd7\xd1'}
    msg4 = {'ct': b'\x03\xc2\x8d\xf9\xf8\x8c\x17\xc4\x9e\x8d\xd9\xfal\xad[\x05\x0fvT\xb3\x08\xaa\xa7i\x14\xbfVvO\x9f@Q\xfa\xc9\xe5\x8dZ\xfa\xb4\xb3\x03J\x86\x9f\xba\xad:L', 'ad': b'', 'tag': b'3\xa2\x15D\xdc\xc1X`I\x8f\xe5\x1c\x94\x9anF'}
    
    msg1 = CrackMsg(msg1["ct"], msg1["ad"], msg1["tag"])
    msg2 = CrackMsg(msg2["ct"], msg2["ad"], msg2["tag"])
    msg3 = CrackMsg(msg3["ct"], msg3["ad"], msg3["tag"])

    test = GHashCrack(msg1,msg2,msg3)
    test.crack()
    assert test.forge_auth_tag(msg4["ad"], msg4["ct"])==msg4["tag"]    

    #test vectors by johndoe31415

    msg1 = {'ct': b'\x91\x84c\xb7\xfalE\xcaX4\xc2\x80\xc6t\xf1\xef\xf1\x82\xf6;DjO', 'ad': b'', 'tag': b'zX\xed\xb3\x18A\x99\xa6Y\xa6f\x10\x14X7\xfb'}
    msg2 = {'ct': b'\x9d\xa7\x0cA-\xd3Bf\xc8\xbe\x16y\xae\xd3K\xfd\xbef\xe1\x8b\xd1\xd6\xf4&', 'ad': b'\xd9\xb1\xb1\x17\x97\x10\x9d', 'tag': b'D\x85\xcb\xe2\xb1\xf7\x91T\xb7z\x0cMMG\xd3\x11'}
    msg3 = {'ct': b'\xb9\x1dF\xbd\xdb\xa7\x04g\xe2\xcb%\x01\x8b\xb2\xf2\xdeR%', 'ad': b'\xfc\xad,\xea\xf1\x14\xe1\xb3\xd0\x90\x90\xe4\x80', 'tag': b'\xf9#;9\x98+\xd8\x15\xda\t\xc3\x9f\xd0e\x19\xc0'}
    msg4 = {'ct': b'\xfc3~\xbe@\rU\xb4ouH\xee', 'ad': b'\x08\xa4\xae\x00\x80', 'tag': b'\x9d\xe5}\xe1\xfck\xa9\xe5a\t\xdaE4\x19aS'}
    msg1 = CrackMsg(msg1["ct"], msg1["ad"], msg1["tag"])
    msg2 = CrackMsg(msg2["ct"], msg2["ad"], msg2["tag"])
    msg3 = CrackMsg(msg3["ct"], msg3["ad"], msg3["tag"])

    test = GHashCrack(msg1,msg2,msg3)
    test.crack()
    assert test.forge_auth_tag(msg4["ad"], msg4["ct"])==msg4["tag"] 



    msg1 = {'ct': b'\x8c\xcf;\xdf\xb8\x1d\xc3X\x11\xed\xe0\xbd\xcb\xecj\xf2I5\x055\xdd\xb3\xebi\xaem\xdc\xdc\xeb\x9e', 'ad': b'\x15y\xe9 v', 'tag': b'nO,\xa1\x03i\xc4\x85\x85\xc8\xea4\xadn\xbb\x9f'}
    msg2 = {'ct': b'\x8dC i\xed0\x0bQ\x99\xe3\xf2o\x88\x1f', 'ad': b'\x13\xfe', 'tag': b'jh\xf7H\xbb:\x04\x97\x891\xe2}\xa9\xed{\xac'}
    msg3 = {'ct': b'{3\x91\xb8L\xe45\xec\xbd\xe3\xd3n4\xf3\xb5P\xc8\xe3\x8b\x170\x87\xb6\xd1\x90\xf7\xbe7\x17\xedv\xa8\xadu', 'ad': b'\xf7\x83\x07\xec\xb4?\x07\xefl\xd7', 'tag': b"KB\x0brN\xb9\x00b\xd1>\xc2\x100''\xf0"}
    msg4 = {'ct': b'\x031\xb7\x04\xfc>s\xd3\x1b\x9a\xb0S<\x19;\xc5', 'ad': b'\x10\xa9|', 'tag': b'\x1aP]\xda\xdd\x84\xcf\x88\xeaq\xc1\xb7\xbc\x0f\xb4\xf5'}
    msg1 = CrackMsg(msg1["ct"], msg1["ad"], msg1["tag"])
    msg2 = CrackMsg(msg2["ct"], msg2["ad"], msg2["tag"])
    msg3 = CrackMsg(msg3["ct"], msg3["ad"], msg3["tag"])

    test = GHashCrack(msg1,msg2,msg3)
    test.crack()
    assert test.forge_auth_tag(msg4["ad"], msg4["ct"])==msg4["tag"] 



    msg1 = {'ct': b'\xb4R\xe6\xab\xea\x80|\x8d*\xd43\x99', 'ad': b'\xb5\x07c', 'tag': b'\x98\xf5\xd85\x87\xab\xe1\xb2\xe3=f\xaf\x85\x81\xb3{'}
    msg2 = {'ct': b'/\xf5o\x86>\xec\xe4\xfe\x08\xd0\xf9t?C\x9a\x95Y\xf9\xda\xb3Z\xe5\x06\xb5\xae', 'ad': b'\x97\xd0\xcfJ\xfe2', 'tag': b'\x19\xd6\xb6\xcf\x1e\x15\xb1\xbe(\xd5\x86A}\r\xf4D'}
    msg3 = {'ct': b'\xe4i\xab\xe0\xc4\xd6\x95\x01l\x8a?k\xb7B_|\x9e\xcf\xe2\xdc9|l', 'ad': b'\x91', 'tag': b')\xc6\xefPr?U\x03\x02\xcbe\x06QE\xd1\x95'}
    msg4 = {'ct': b'[^\xa9~x\xb7\x81\xb2\x92A:\xe6\x98\xf8\x18\x14\r\xf9\x95\x99@l\x98\x00*\xd6\x18\xd7\xaf', 'ad': b'\x95\x16\x83\x9fk\x8dk \x1cZ\xe8', 'tag': b'|\xc2\x07\xad\xca\x13Q\xc2\xcb\x00\xdb\xf1onA\x96'}
    msg1 = CrackMsg(msg1["ct"], msg1["ad"], msg1["tag"])
    msg2 = CrackMsg(msg2["ct"], msg2["ad"], msg2["tag"])
    msg3 = CrackMsg(msg3["ct"], msg3["ad"], msg3["tag"])

    test = GHashCrack(msg1,msg2,msg3)
    test.crack()
    assert test.forge_auth_tag(msg4["ad"], msg4["ct"])==msg4["tag"] 



    msg1 = {'ct': b']?]\xca{qvS:\x82K\xea\x8b[\xaf\xec0q\xe2\xabM\xd3\x9b\xe7\xa3\x9f\xf8e3\x18\x13\x19\xb5[1\xb5', 'ad': b'oW\xb7\x1b\x85\xa4\xe7\xc6\xaa\x8b\xf7l\r', 'tag': b'\x17\xf0\x9e\xc0/\xbe`\xefTD]\x9fT\x0f6\x92'}
    msg2 = {'ct': b'h\xe1\xc3!\x94\x05\x84d\xfa\x8e=\x10K%\xa2\xed\x99\xa7\x93i\x84B\xf5\xee\x9d\xee\xba\xa6\x02\xd8\x9eP\x8e', 'ad': b'@$\x96d\x95\x0f\xa4\xc0\x13m\xe1\xe9Q.\x8bU\xac\xde', 'tag': b'd^\x85\xa4r\xc7\x06F\x1f5j}#\x9a\x94P'}
    msg3 = {'ct': b'\x98<S\x9aw\xacd\r\xbe\x1eM.\xc3\xed\xe7\xa3\x91\\K\xeb\xbd;\xc8\xd8\x8c7\x87O\xf4', 'ad': b'\xfc\x06', 'tag': b'\xa7\x0b\x07\xd2\xc1\x933>\xef\x0f\x82\xc1\xacw\xc2\xc1'}
    msg4 = {'ct': b'\xedc\x13:Ogfd\x93\x85\xd7:\xa7\xc7\xb8\xdaO\t\xea\xac\x9a2z\xd4w\x7f\xcf"N\x99|\x9d\xc5\xdc\x81N e', 'ad': b'\x02\xbe;\xaad\xb3\xc9\xf0\x1a`\x11j', 'tag': b'\x9a`7WC\xc4#L\xa7\xa2\xcf\x01\x96\xd4U\x87'}
    msg1 = CrackMsg(msg1["ct"], msg1["ad"], msg1["tag"])
    msg2 = CrackMsg(msg2["ct"], msg2["ad"], msg2["tag"])
    msg3 = CrackMsg(msg3["ct"], msg3["ad"], msg3["tag"])

    test = GHashCrack(msg1,msg2,msg3)
    test.crack()
    assert test.forge_auth_tag(msg4["ad"], msg4["ct"])==msg4["tag"] 



    msg1 = {'ct': b'\xf1\t\xbc\x9a\xf2]/\xe1N\x85\x1d\xdf\x87\xb9>\xdd\xed-\xef\xbcfxY\xb4\x06Z\xe2\xe8\x9f\x91\xdb\xbbd-\x1c\xa8\xba8\x80', 'ad': b'8e\xa9\x16\x97\xa2', 'tag': b'\xaf\xb2\xa2\xbdK\xc7\\&\xc8\xb4\xb6\xb3*\xd0\x8c\xe3'}
    msg2 = {'ct': b'\xc7ZO\xe6<\xa5\x12%H\xbfy\xb0j\xb3\x88\nK', 'ad': b'\xc4R%\xda%\xb4\x8e\xb8bs\x1d\xbcJ', 'tag': b'K\xf4i\xc4\xfbZb\xb5\xabi`\x8bV\x84\xef\xbe'}
    msg3 = {'ct': b'\x8b\xea\xf3\x9b\xda/\x82\xe3\xf3\x86\xa0\xe1\x0cu|\xf6\x7f\xbb2\xe8\xbb\x00\xddg\xe1\x06\xac\t[\x93\xc2\x00\xaeCt~X\x07\xf1', 'ad': b'\x8f\xdbE\xc7\x18\x8a;\x9a\x07b\xdc:5+\xea', 'tag': b"c\xc1A\x96\x01\xbf&\x8b'\xff0\x04D\x8a\x88o"}
    msg4 = {'ct': b'\x1a7\xafF\x03\xf1w\x0f\x99\xd1\x005\xbb', 'ad': b'\x15\xbe', 'tag': b'\xec9P\x98oq\xd01a-r\xe6\nl\xe4M'}
    msg1 = CrackMsg(msg1["ct"], msg1["ad"], msg1["tag"])
    msg2 = CrackMsg(msg2["ct"], msg2["ad"], msg2["tag"])
    msg3 = CrackMsg(msg3["ct"], msg3["ad"], msg3["tag"])

    test = GHashCrack(msg1,msg2,msg3)
    test.crack()
    assert test.forge_auth_tag(msg4["ad"], msg4["ct"])==msg4["tag"] 



    msg1 = {'ct': b'\xa1\xe3{\x0es\x02\xd46\x9d\x86\x18\xab\xb6\xc6!\xc0', 'ad': b'', 'tag': b'\xe9\x89g%\xdf\x05\x80" \xd9\x1b:\xd7\r\xb3-'}
    msg2 = {'ct': b'V\xde2\xef\x19#gdQ2!\xed', 'ad': b',^\x98hkT\x06\xde\xa5\xc6y', 'tag': b'\x87\xeb\x7fdGF\xedo\x98\xbdA\xdd\x14\x19\x8c\xf2'}
    msg3 = {'ct': b'#\tG\xffQ\x06f3T\xad\xcd\xf1\xc4d\xf7', 'ad': b'}\xb4\xb2n\xdf\xc9q', 'tag': b'\xa9\x81]%"L4\x02\x1b\x13g\x85\x1d];N'}
    msg4 = {'ct': b'\xb1Fo\xaf\x88\xcc{qZC?\xd45\x08\xe8gH\xae(\xb4\xc8\x93\x99\xdby', 'ad': b'+\x02\x1a\xf4\xb3\x8e\xfb\xb5\x1eO\r^]', 'tag': b'\xf0\x08\xbb\x11\x15l\xcf\x9e`c\xf6\xc6\x03^\\2'}
    msg1 = CrackMsg(msg1["ct"], msg1["ad"], msg1["tag"])
    msg2 = CrackMsg(msg2["ct"], msg2["ad"], msg2["tag"])
    msg3 = CrackMsg(msg3["ct"], msg3["ad"], msg3["tag"])

    test = GHashCrack(msg1,msg2,msg3)
    test.crack()
    assert test.forge_auth_tag(msg4["ad"], msg4["ct"])==msg4["tag"] 



    msg1 = {'ct': b"'\xb0\xe4\xceIz\xc2\x0fV\xba\x9b", 'ad': b'/BC\xca', 'tag': b'\xec\xc6\x0bl\xd6k6\t\xf1+Z\x97\xf3*\xc1E'}
    msg2 = {'ct': b'6\x96\xf0\x03c\x07\x9e\x88\xa6\xeb8\x0ew\x8d\xfbA', 'ad': b'\xc7\xd9\xb9Z\xd0\x84T~', 'tag': b'E-\xbf7c_\xe4\x14.\x85\x8d\xa5\xf69I\x94'}
    msg3 = {'ct': b'\xe8\xe6\x01\x00\x91\xad\x8dC!\x9b%\x1f(,\x1a\xb4\xc3B\x90\x98"\x15\x07\x16\x8fAg\xdc)\xbc\x9f\x9c(\x9a8\xaf\x08\xda\x9a', 'ad': b'\xfdGQ\xb0[', 'tag': b'\xec\x1bR\xe9\xb7\x90\xc5;L\xd5\xfbM\xec\\\xee\x83'}
    msg4 = {'ct': b'~\xe4,\xa9\x1fZ\xae6$\xa3\x83\x1d\x7fh\r+\xcd\xdf\x13\x9e\x00%\xac^~P\xa1', 'ad': b'\xe8\xa1\xe0\x04', 'tag': b'\xa3\xaa\xf4/\xcd{\x88\x19\x84\x80#f\xc4\xbf\xa5\xe3'}
    msg1 = CrackMsg(msg1["ct"], msg1["ad"], msg1["tag"])
    msg2 = CrackMsg(msg2["ct"], msg2["ad"], msg2["tag"])
    msg3 = CrackMsg(msg3["ct"], msg3["ad"], msg3["tag"])

    test = GHashCrack(msg1,msg2,msg3)
    test.crack()
    assert test.forge_auth_tag(msg4["ad"], msg4["ct"])==msg4["tag"] 



    msg1 = {'ct': b'E\x07"\x00\x7f\xa3\x9d\x8fvj\xe0f\xb3\x03\xc6\x05\xf8z\x86|\xdd\x07v\xb3\xc5ar\xefB\xe4\xb04\xae\x17', 'ad': b'\x87\xd1\xe1\xf1\xad}Tg', 'tag': b'\x84\xc6%\xd0\xf9\x8da_\x90\xec@\x9a1\x02\xbb\x97'}
    msg2 = {'ct': b',?\xa1[\xff\xb8\\%o821\xe4\x9f)>$', 'ad': b'\x84\xd8\xfb\\\x8a\xc2\x06*R\xfd\x8e<\x90\xe8iU\x8a\xd2\x1a\xd3', 'tag': b"9\x8f\xdbd%hA\x19\x07\xca'\xfc)\xf7\xf5\xa0"}
    msg3 = {'ct': b't\x9e*t\t\xab^\xa2\x9e5\x1a,\xdc-\xfd\x01B\x16D\xfd\xf2', 'ad': b'\xf5\x99\xe17', 'tag': b'^T\xd9\xe0\x87\xe4\xbc\x01R0d7\xed\xcc\x88U'}
    msg4 = {'ct': b'`\x95\x8dx\x96u-e\xd3\x14\xb1\xf6\xe2\xfd', 'ad': b'1sf8\x82o\x967\x13\x0e', 'tag': b'\xbdOM\x12Vhv\xa4\x88\xd8\xeb8\xcd\xf9X\xb1'}
    msg1 = CrackMsg(msg1["ct"], msg1["ad"], msg1["tag"])
    msg2 = CrackMsg(msg2["ct"], msg2["ad"], msg2["tag"])
    msg3 = CrackMsg(msg3["ct"], msg3["ad"], msg3["tag"])

    test = GHashCrack(msg1,msg2,msg3)
    test.crack()
    assert test.forge_auth_tag(msg4["ad"], msg4["ct"])==msg4["tag"] 



    msg1 = {'ct': b'\x18\x1c\x7f|\xee\x0b\x93\xf8JsK\xb7n\x98', 'ad': b'\xa1\x9d\x02', 'tag': b'P\xcf\xa6\x87d\x94\x16\x86\xc3\xb0\xdam\x06F\x95\x1a'}
    msg2 = {'ct': b'\xc0<k\xf2\tKS\x1f_\xe7\xeb\xcem', 'ad': b']]\xb3\xb9\xda\xf0\x92\xb8\xf8\xf4\xb3QZ\x8c', 'tag': b'i\xd0\x85F\\}V\x9d\xae\x0c\x06}\x1f\xac\x90+'}
    msg3 = {'ct': b'V\xd7\x18a\xac\xbc\xc4/\x16\x87(\xf8_\x0f+', 'ad': b'\xcf\xcc\xba\xd1z=', 'tag': b'\x93}5\x7fZi\x8d\xfcv-\xa4I)~\x96/'}
    msg4 = {'ct': b'qB\xd3\xf1x\x12\xb0QC%\xcb\xfc\x15\xfb\xf8\xf2Y\xf7hge\xaf', 'ad': b'd\x13\xc5\xed-\x93-\x10\x13\x9a\xb5-\x8e', 'tag': b'\x93M\xe2\xd9v?\x87\x84\x15\x93\x81E\xc5\x9c4L'}
    msg1 = CrackMsg(msg1["ct"], msg1["ad"], msg1["tag"])
    msg2 = CrackMsg(msg2["ct"], msg2["ad"], msg2["tag"])
    msg3 = CrackMsg(msg3["ct"], msg3["ad"], msg3["tag"])

    test = GHashCrack(msg1,msg2,msg3)
    test.crack()
    assert test.forge_auth_tag(msg4["ad"], msg4["ct"])==msg4["tag"] 



    msg1 = {'ct': b'\xbf_W\xe3\x10)\xdb+Z\x16\xfaI\xe0\xd3?\x7fa\xe4\xd7\xbbp\xab\xf5\x03\x15\x8e\xb7\x15', 'ad': b"\xfb\x7fm'gs\xae~\xac\xa7*\xd7\xed\xa4v\xce", 'tag': b'\xce\x1eN/f\xcf\xe9\xae\xa8\xb0\xdd\xbe\xf3\x91\x90\x81'}
    msg2 = {'ct': b'\x18z\xb4i\x03OH;\x8d\x02M\x99r\x07=T2}\xc7\xe9UY\x9ac\x86[d\xe2\xc74\xef\xdbi\x14c;\xa7', 'ad': b'0\xea', 'tag': b'8\x93\xc5c\xbe\x98\\\xbb\t@\x189@r\x89\x18'}
    msg3 = {'ct': b'F\xd8L\x0ev\xe0\xf8\xa0d\x1a;\x0b6r*7k\x17\x97\xaa\xe6\xde5\x1cx\\\x95#', 'ad': b'\xe0\xb0\xc1,', 'tag': b'\x90\xa0cS\x15Ck\xcf\x12\xcf-\xeaelv\xaf'}
    msg4 = {'ct': b'\x0ff}\x89\x8eLV\x8bn\x13{n', 'ad': b'\xc0\xa8go\xbefx\x97+)Z\x91\xb3G\x1b\xaa\xdb8\x92', 'tag': b'\xef\x83\x89\x0f\xba\xe2\x8ejQ\xc2\xd3\xc4\xf7@\xf2\xdf'}
    msg1 = CrackMsg(msg1["ct"], msg1["ad"], msg1["tag"])
    msg2 = CrackMsg(msg2["ct"], msg2["ad"], msg2["tag"])
    msg3 = CrackMsg(msg3["ct"], msg3["ad"], msg3["tag"])

    test = GHashCrack(msg1,msg2,msg3)
    test.crack()
    assert test.forge_auth_tag(msg4["ad"], msg4["ct"])==msg4["tag"]
    print("All tests passed")
