from base64 import b64decode, b64encode

def rotation(rotation):
    result = rotation[1:]
    carry = rotation[0]
    result.append(carry)
    return [result, carry]

def bit_complement(byte):
    return int.from_bytes(byte)^255

if __name__ == "__main__":    
    a = [1,2,3,4,5,6,7,0]
    print(rotation(a))
    print(b64decode("RGFzIGlzdCBlaW4gVGVzdC4="))