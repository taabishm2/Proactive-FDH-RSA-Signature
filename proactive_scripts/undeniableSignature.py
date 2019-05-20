import nextprime
import random
import modinverse

def init(n):
    '''generate prime group with order > n, returns [group_size,generator]'''

    p = nextprime.next_prime(n)
    g = random.randrange(2,p-1)
    return n   #assuming g is as generated in Threshold RSA

def challenge(witness_list,signature_list,p,add_gen,ciphertext):
    '''generate challenge and vezrifier, return as [challenge(list),verifier(int)]'''

    challenge = []

    a = random.randrange(2,p-1)
    b = random.randrange(2,p-1)
    verifier = ((pow(add_gen,a,p)*pow(ciphertext,b,p))%p)

    for i in range(len(witness_list)):
        challenge.append((pow(witness_list[i],a,p)*pow(signature_list[i],b,p))%p)

    return [challenge,verifier]

def response(challenge,share,p,verifier):
    '''generates response by a party holding a 'share' to the challenge[i] for all additive shares'''

    res = []
    
    for i in range(len(challenge)):
        response = pow(challenge[i],modinverse.modular_inverse(share[i],p-1),p)
        if response == verifier:
            res.append(True)
        else:
            res.append(False)
    return res
    
        
    
