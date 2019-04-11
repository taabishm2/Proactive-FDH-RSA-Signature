from math import ceil
from hashlib import sha256

def fdh(string, n=2048):
    '''full domain hash of 'string' using SHA256 with digest of n-1 bits'''
    
    result = []
    
    for i in range(ceil(n/256)): #produce enough sha256 digests to make total 1024 composite digest
        
        result.append( sha256((string+str(i)).encode()).hexdigest() )
        
    result = ''.join(result)[:-1]
    
    return result
