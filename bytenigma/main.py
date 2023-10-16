from util import round_rotation
from base64 import b64decode, b64encode


def _encrypt_byte(byte, rotor_array):
    tmp = byte
    for rotors in rotor_array:
        tmp = rotors[tmp]
    tmp ^= 255
    for rotors in reversed(rotor_array):
        tmp = rotors.index(tmp)
    return tmp.to_bytes(1, byteorder='big')

def encrypt(byte_string, rotor_array):
    result = b''
    tmp_rotor_array = rotor_array
    for i in byte_string:
        result += _encrypt_byte(i, tmp_rotor_array)
        tmp_rotor_array = round_rotation(tmp_rotor_array)
    return result




