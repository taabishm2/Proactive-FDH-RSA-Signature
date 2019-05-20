import nextprime
import random
import VSSShamirSS
import math

global vss_p
global vss_q
global gen
global commitment_list

def pick_q(n):
    '''find nearest prime greater than n, field for polynomial'''
    global vss_q
    
    vss_q = nextprime.next_prime(n)

def pick_p(n=0):
    '''find nearest prime greater than n such that p|(q-1), field for commitments'''

    global vss_p
    global vss_q
    s = vss_q
    i = 2
    
    while True:
        p = nextprime.next_prime(s)
        if (p-1) % vss_q == 0:
            vss_p = p
            return
        else:
            i += 1
            s *= i


def pick_gen(p,q): 
    global gen
    a = random.randrange(1,p-1)

    gen = pow(a,((p-1)//q),p)
    return
   
            
def shamir_poly(n,t,secret):
    '''pick t-n shamir shares with field size vss_q'''
    global vss_q

    return (VSSShamirSS.tnshares(n,t,secret,vss_q))

def commitments(t,coeff):
    '''generate t commitments'''
    global gen
    global vss_p
    global commitment_list
    commitment_list = []

    for i in range(t):
        commitment_list.append(pow(gen,coeff[i],vss_p)%vss_p)

def verify_share(si,gen,vss_p,commitment_list):
    '''verify share si with generator = gen, vss_p and commitments in commitment_list'''
    
    lhs = pow(gen,si[1],vss_p)
    
    rhs = 1
    for i in range(len(commitment_list)):
        rhs *= pow(commitment_list[len(commitment_list)-i-1],(si[0]**i),vss_p)
    rhs = rhs % vss_p
    if lhs == rhs:
        return True
    else:
        return False

def feldmanvss(t,n,m):
    '''Split secret m into n shares with reconstruction threshold = t'''
    global vss_p
    global vss_q

    pick_q(m)   #Pick prime order group for commitments 
    pick_p()    #Pick prime order group for coefficents
    pick_gen(vss_p,vss_q)

    s = (shamir_poly(n,t,m))  #Returns an array of shares generated and an array of coefficents for commitment generation
    shares = s[0]
    coeffs = s[1]

    commitments(t,coeffs)

    return [shares,commitment_list,vss_p,vss_q,gen]

def feldmanverify(si,gen,vss_p,commitment_list):
    return verify_share(si,gen,vss_p,commitment_list)

        
##pick_q(1000000)
##pick_p()
###print(vss_p,vss_q)
##
##res = True
##
##for t in range(1,10):
##
##    n = random.randrange(t,999)
##    sec = random.randrange(1,999999)
##
##    pick_gen(vss_p,vss_q)
##
##    #print("Generator Done",gen)
##    
##    s = (shamir_poly(n,t,sec))
##
##    #print("Shamir Done")
##    
##    shares = s[0]
##    coeffs = s[1]
##
##    commitments(t,coeffs)
##
##    #print("Commitments")
##
##    shares.append([random.randrange(1,999),random.randrange(1,999)%vss_q])
##    shares.append([random.randrange(1,999),random.randrange(1,999)%vss_q])
##
##
##    t = []
##    for i in shares:
##        if verify_share(i):
##            t.append(True)
##        else:
##            t.append(False)
##
##    v = [True for i in range(n)]
##    v += [False,False]
##
##    
##    if t != v:
##        print(shares[-1],shares[-2])
##        print(shares[shares[-1][0]-1],shares[shares[-2][0]-1])
##        res = False
##        break
##
##print(res)
