import random
from math import gcd

def find_coprime(a):
    '''Find a random coprime of a which is < a'''

    r = random.randrange(2,a-1)
    while True:
        if gcd(r,a) == 1:
            return r
        elif r == a-1:
            r = random.randrange(2,a-1)
        else:
            r += 1
