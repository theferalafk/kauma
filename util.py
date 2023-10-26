def _rotation(rotation):
    #takes a list as an input and rotates it left, the left most element gets appended most right
    #return the new array and the former left most element
    result = rotation[1:]
    carry = rotation[0]
    result.append(carry)
    return [result, carry]

def round_rotation(rotor_array):
    #takes a list of rotors as an input and returns a new list for the next round
    result = []
    #first rotor has to be rotated
    carried_byte = 0
    for i in range(len(rotor_array)):
        #checks if rotor needs to be rotated
        if carried_byte == 0:
            tmp = _rotation(rotor_array[i])
            result.append(tmp[0])
            carried_byte = tmp[1]
        else:
            #no rotation
            result.append(rotor_array[i])
            carried_byte = 1
    return result
