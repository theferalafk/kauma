from util import round_rotation, test
from base64 import b64decode, b64encode


def encrypt_byte(byte, rotor_array):
    rotors = len(rotor_array)
    tmp = int.from_bytes(byte, byteorder='big')
    for i in range(rotors):
        tmp = rotor_array[i][tmp]
    tmp ^= 255
    for i in range(rotors-1,-1,-1):
        tmp = rotor_array[i].index(tmp)
    return tmp.to_bytes(1, byteorder='big')

if __name__ == "__main__":
    p = b64decode("RGFzIGlzdCBlaW4gVGVzdC4=")
    c = b64decode("lDEjvQHsKWD9c+dHIW++KRo=")
    print(p)
    print(c)
    print(encrypt_byte(b'D', test["rotors"]))


