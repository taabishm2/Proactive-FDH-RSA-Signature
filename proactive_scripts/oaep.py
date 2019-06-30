import random
import hashlib
import fdh

global div

def pad(m,l):

    global div

    r = random.randrange(pow(2,l)-1)

    m0 = m * pow(2,l-len(bin(m))+2)

    div = pow(2,l-len(bin(m))+2)
    
    x = m0 ^ fdh.fdh(r,l)
    
    y = r ^ fdh.fdh(x,l)

    return [x,y]

def un_pad(x,y,l):

    global div
    
    r = y ^ fdh.fdh(x,l)

    m0 = x ^ fdh.fdh(r,l)

    return m0//div

l = pad(123,15)

print(un_pad(l[0],l[1],15))
