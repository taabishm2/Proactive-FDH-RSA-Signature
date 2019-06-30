def additive_signature():

    global verify_sum,verify_p,verify_challenge,verify_verifier,verify_response,verify_generator

    verify_challenge, verify_response = [],[]

    verify_p = additiveSignature.init(n)
    verify_sum = additiveSignature.pick_sum(max(additive_shares)+1)
    verify_challenge,verify_verifier, verify_generator = additiveSignature.challenge(additive_shares,verify_p,verify_sum)  #instead of passing shares, reuse witness generated g^di values


def additive_signature_verify():
    global verify_sum,verify_p,verify_challenge,verify_verifier,verify_response,verify_generator,share_status

    verify_response = additiveSignature.response(verify_challenge,additive_shares,verify_p,verify_sum,verify_verifier,verify_generator)
    share_status = verify_response

    print("ADDITIVE SHARE STATUS:",verify_response)

    if verify_response.count(True) != add_shares_no:
        print("INVALID SIGNATURE!\nALERT: INVOKE BACKUP")

import nextprime
import random
import modinverse

def init(n):
    '''generate prime group with order > n'''

    p = nextprime.next_prime(n)
    return n

def pick_sum(p):
    '''pick a sum such that di+di_dash = sum and p < sum < 2p'''

    return random.randrange(p,2*p)

def challenge(shares,p,c):
    '''generate challenge and vezrifier, return as [challenge(list),verifier(int)]'''

    challenge = []

    a = random.randrange(2,p)
    verifier = pow(a,c,p)
    for di in shares:
        challenge.append(pow(a,di,p))

    return [challenge,verifier,a]

def response(challenge,share,p,c,verifier,gen):
    '''generates response by a party holding a 'share' to the challenge[i] for all additive shares'''

    res = []
    for i in range(len(challenge)):
        response = (pow(gen,c-share[i],p)*challenge[i])%p
        if response == verifier:
            res.append(True)
        else:
            res.append(False)
    return res
