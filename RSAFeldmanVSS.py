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
    return vss_q

def pick_p(vss_q,n=0):
    '''find nearest prime greater than n such that p|(q-1), field for commitments'''

    global vss_p
    s = vss_q
    i = 2

    while True:
        p = nextprime.next_prime(s)
        if (p-1) % vss_q == 0:
            vss_p = p
            return vss_p
        else:
            i += 1
            s *= i


def pick_gen(p,q):
    global gen
    a = random.randrange(1,p-1)

    gen = pow(a,((p-1)//q),p)
    return gen

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

def reconstruct_shamir(shares,i,t=0): #Do we have to mention which additive share these backups belong to? i.e. need for 'i'?
    '''Verify first using VSS and then reconstruct, i is index of the additive share for vss_p, etc'''
    global vss_q

    res = True
    for si in shares:
        if RSAFeldmanVSS.verify_share(si,gen[i],vss_p[i],commitment_list[i]) == False:
            res = False
            break

    if res == False:
        print("Share:",si,"invalid")
        raise Exception("Backup Reconstruction Failed")
        return
    else:
        return (ShamirSS.tncombine(shares,vss_q[i],t))


def feldmanvss(t,n,m):
    '''Split secret m into n shares with reconstruction threshold = t'''

    global vss_p,vss_q,gen

    vss_q = pick_q(m)   #Pick prime order group for commitments

    vss_p = pick_p(vss_q)    #Pick prime order group for coefficents

    gen = pick_gen(vss_p,vss_q)   #Pick generator

    s = (shamir_poly(n,t,m))    #Returns an array of shares generated and an array of coefficents for commitment generation
    shares = s[0]
    coeffs = s[1]

    commitments(t,coeffs)       #Generates 't' commitments for verification using the coefficients

    return [shares,commitment_list,vss_p,vss_q,gen]

def invoke_backup():
    global share_status
    global additive_shares
    global sub_shares

    for i in range(len(share_status)):
        if not share_status[i]:
            print("Share index:",i,"damaged")
            print("Restore from",additive_shares[i],"to",end=" ")
            additive_shares[i] = reconstruct_shamir(sub_shares[i],i,t=0)
            print(additive_shares[i])

def debug():
    '''FOR DEBUGGING ONLY'''

    pick_q(1000000)
    pick_p(vss_q)
    #print(vss_p,vss_q)

    res = True

    for t in range(1,10):

       n = random.randrange(t,999)
       sec = random.randrange(1,999999)

       pick_gen(vss_p,vss_q)

       print("Generator Done",gen)

       s = (shamir_poly(n,t,sec))

       print("Shamir Done")

       shares = s[0]
       coeffs = s[1]

       commitments(t,coeffs)

       print("Commitments")

       shares.append([random.randrange(1,999),random.randrange(1,999)%vss_q])
       shares.append([random.randrange(1,999),random.randrange(1,999)%vss_q])


       t = []
       for i in shares:
           if verify_share(i,gen,vss_p,commitment_list):
               t.append(True)
           else:
               t.append(False)

       v = [True for i in range(n)]
       v += [False,False]


       if t != v:
           print(shares[-1],shares[-2])
           print(shares[shares[-1][0]-1],shares[shares[-2][0]-1])
           res = False
           break

    print(res)


#debug()
