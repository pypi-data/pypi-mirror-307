
def string2int(pstring):
    tmp_ = []
    for i in pstring:
        if i=='X':
            tmp_.append(1)
        elif i=='Y':
            tmp_.append(2)
        elif i=='Z':
            tmp_.append(3)
        else:
            tmp_.append(0)
    return tmp_


def sblock2ndict(block, Hstring):
    tstring = ""
    for _ in block:
        tstring += str(_)+' '+str(Hstring[_])
        
    return tstring

def sblock2nqubit(block, Hstring):
    tstring = [0 for i in Hstring]
    for j_ in block:
        tstring[j_] = Hstring[j_]
    return tstring

def sblock2ncumu(block, Hstring):
    tstring = []
    for j_ in block:
        tstring.append(Hstring[j_])
    return tstring

def process_measure_bits(bitplist, bitolist):
    from typing import Optional, List, Any
    
    if isinstance(bitplist, List) and isinstance(bitplist[0], str):
        plist_int = [string2int(_) for _ in bitplist]
    elif isinstance(bitplist[0], List) and all(isinstance(bitplist[0][_], int) for _ in bitplist[0]):
        pass
    else:
        raise ValueError("Unrecognized measurement basis format")

    if isinstance(bitolist, List) and isinstance(bitolist[0], str):
        olist_int = [[1 if _ == '0' else -1 for _ in bits] for bits in bitolist]
    elif isinstance(bitolist[0], List) and all(isinstance(bitolist[0][_], int) for _ in bitolist[0]):
        
        if check_binary(bitolist):
            olist_int = [[1 if _ == 0 else -1 for _ in bits] for bits in bitolist]
        else:
            pass
        
    try:
        return plist_int, olist_int
    except:
        return bitplist, bitolist

def check_binary(list_of_list):
    for i in list_of_list:
        for j in i:
            if j == 0:
                return True
            elif j == -1:
                return False
    return False
