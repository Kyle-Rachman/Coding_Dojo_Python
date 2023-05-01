def countdown(x):
    countlist = []
    for i in range(x,-1,-1):
        countlist.append(i)
    return countlist

def print_and_return(li):
    print(li[0])
    return li[1]

def first_plus_length(li):
    return li[0]+len(li)

def values_greater_than_second(li):
    savedvalues = []
    if len(li) < 2:
        return False
    
    for i in range(len(li)):
        if li[i] > li[1]:
            savedvalues.append(li[i])
    
    print(len(savedvalues))
    return savedvalues

def length_and_value(size,value):
    return [value] * size