

def removeBin(*value):
    print(value)
    value_new = []
    for iterate in value:
        if len(iterate) > 2:
            iterate_stripped = iterate[2:]
            return_iterate = '0' * (8-len(iterate[2:])) + iterate_stripped
            print('debug', return_iterate)
            value_new.append(return_iterate)
        elif len(iterate) <= 2:
            return_iterate = '0' * 8
            print('debug', return_iterate)
            value_new.append('0' * 8)
        elif len(iterate) == 10:
            return_iterate = iterate[2:]
            print('debug', return_iterate)
            value_new.append(return_iterate)
    value_return = ''
    for i in value_new:
        value_return += i
    return value_return

value1 = '0b00000001'
value2 = '0b000000111'
value = removeBin(value1, value2)
print(value)