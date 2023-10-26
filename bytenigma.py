from util import round_rotation


def _encrypt_byte(byte, rotor_array):
    #takes a byte and a rotor list as an input and encrypts it
    tmp = byte
    #forward mapping
    for rotors in rotor_array:
        tmp = rotors[tmp]
    tmp ^= 255
    #reverse mapping
    for rotors in reversed(rotor_array):
        tmp = rotors.index(tmp)
    return tmp.to_bytes(1, byteorder='big')

def encrypt(byte_string, rotor_array):
    #takes a byte string and a rotor configuration as an input and return the encrypted byte string
    result = []
    tmp_rotor_array = rotor_array
    #encrypting input string byte by byte
    for i in byte_string:
        result.append(_encrypt_byte(i, tmp_rotor_array))
        tmp_rotor_array = round_rotation(tmp_rotor_array)
    return b''.join(result)




