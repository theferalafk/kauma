def _rotation(rotation):
    result = rotation[1:]
    carry = rotation[0]
    result.append(carry)
    return [result, carry]

def round_rotation(rotor_array):
    result = []
    carried_byte = 0
    for i in range(len(rotor_array)):
        if carried_byte == 0:
            tmp = _rotation(rotor_array[i])
            result.append(tmp[0])
            carried_byte = tmp[1]
        else:
            result.append(rotor_array[i])
            carried_byte = 1
    return result
