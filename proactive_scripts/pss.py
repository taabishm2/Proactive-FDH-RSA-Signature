import math
import random

from hashlib import sha256
from functools import reduce


def str_to_int(s):
    
    lst = []
    
    for ch in s:
        
        hv = hex(ord(ch)).replace('0x', '')
        
        if len(hv) == 1:
            
            hv = '0'+hv
            
        lst.append(hv)
    
    hexa = reduce(lambda x,y:x+y, lst)
    
    print(hexa)


def int_to_str(s):
    
    return s and chr(int(s[:2], base=16)) + toStr(s[2:]) or ''


def gen_seed(size):

    return(random.randrange(0,pow(2,size*8)-1))

def mgf(string,size):

    result = []
    
    for i in range(math.ceil(size/256)):
        
        result.append( sha256((string+str(i)).encode()).hexdigest() )
        
    result = ''.join(result)[:size]
    
    return result

def int_to_octet(val):

    bval = bin(val)[2:]
    
    l = len(bval)
    
    if (l+8)%8 != 0: bval = '0'*(8-l%8) + bval
    
    octet = ''

    for i in range(0,len(bval),8):

        o = hex(int(bval[i:i+8],2))[2:]

        if len(o) < 2:

            o = '0' + o

        octet += o

    return octet

def octet_to_int(val):

    res = ''

    for i in range(0,len(val),2):

        byte = val[i:i+2]
        print(byte)

        res += str(int(byte,16))

    return int(res)
          
def pss_encode(message,seed,olen):

    slen = (len(bin(seed))-2)//8

    bseed = bin(seed)[2:]
    mseed = bin(seed)[2:]

    message = tooctet(message)
    seed = tooctet(seed)

    w = mgf((seed+message),slen)

    expandedw = mgf(w,olen-slen)

    seedMask = expandedw[:slen]

    remainingMask = expandedw[slen+1:]

    maskedSeed = toint(seed) ^ toint(seedMask)

    maskedSeed = tooctet(maskedSeed)

    t = w + maskedSeed + remainingMask

    pss_decode(message,toint(t),slen,olen)

    return toint(t)

def pss_decode(message,f,slen,olen):

    t = tooctet(f)

    w = t[:slen]

    maskedSeed = t[slen+1 : 2*slen+1]

    remainingMask = t[2*slen + 2:]

    expandedw = mgf(w,olen-slen)

    seedMask = expandedw[:slen]

    remainingMask2 = expandedw[slen+1:]

    seed = toint(seedMask) ^ toint(maskedSeed)

    seed = tooctet(seed)

    wn = mgf((seed+message),slen)

    if wn != w or remainingMask2 != remainingMask:

        print("INVALID!")

    else:

        print("VALID!")

