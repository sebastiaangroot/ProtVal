value = bin(1)
print(value)

if len(value) != 10 and len(value) > 2:
    value_stripped = value[2:]
    return_value = '0' * (8-len(value[2:])) + value_stripped
    print('debug', return_value)
    #return valueen2
elif len(value) != 10 and len(value) == 2:
    return_value = '0' * 8
    print('debug', return_value)
    #return '0' * 8
elif len(value) == 10:
    return_value = value
    print('debug', return_value)
    #return value