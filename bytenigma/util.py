def rotation(rotation):
    result = rotation[1:]
    carry = rotation[0]
    result.append(carry)
    return [result, carry]

def round_rotation(rotor_array):
    result = []
    carried_byte = 0
    for i in range(len(rotor_array)):
        if carried_byte == 0:
            tmp = rotation(rotor_array[i])
            result.append(tmp[0])
            carried_byte = tmp[1]
        else:
            result.append(rotor_array[i])
            carried_byte = 1
    return result

def bit_complement(byte):
    return int.from_bytes(byte, byteorder="little")^255

if __name__ == "__main__":    
    a = [[4, 6, 1, 2, 3, 7, 5, 0],[5, 0, 6, 3, 4, 1, 7, 2]]

    for i in range(11):
        a = round_rotation(a)
        print(a)
