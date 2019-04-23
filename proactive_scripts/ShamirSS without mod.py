import random
from math import ceil
from decimal import *

global field_size
field_size = 1999

def tncombine(shares,t=0): #Combines shares using Lagranges interpolation
    '''shares is an array of shares being combined, t is the threshold in the scheme'''
    sums = 0
    prod_arr = []
    if len(shares) < t:
        raise Exception("Shares provided less than threshold. Secret generation not possible")
    for j in range(len(shares)):
        xj,yj = shares[j][0],shares[j][1]
        prod = Decimal(1)
        for i in range(len(shares)):
            xi = shares[i][0]
            if i != j: prod *= Decimal(Decimal(xi)/(xi-xj))
            #print("xi,xi,yj,prod",xi,xj,yj,prod)
        prod *= yj
        #print("n prod:",prod)
        sums += Decimal(prod)
        #print("sums:",sums)
    return int(round(Decimal(sums),0))
            

def polynom(x,coeff):
    '''Evaluates a polynomial in x with coeff being the coefficient matrix with a given x'''
    y = 0
    for i in range(len(coeff)):
        y += (x**(len(coeff)-i-1)) * coeff[i]
    return y

def code(key):
    '''Converts string key into a numeric code'''
    res = []
    for i in key:
        res.append(str(ord(i.upper())))
    return int(''.join(res))

def coeff(t,secret):
    '''randomly generate a coefficient array for a polynomial with degree t-1 whose constant = secret'''
    global field_size

    coeff = []
    for i in range(t-1):
        coeff.append(random.randrange(0,field_size))
    coeff.append(secret)
    #print("Coeff:",coeff)
    return coeff

def tnshares(n,m,secret):
    '''Split secret using SSS into n shares with threshold m'''
    global field_size

    cfs = coeff(m,secret)
    shares = []
    for i in range(1,n+1):
        r = random.randrange(1,field_size)
        shares.append([r,polynom(r,cfs)])
    #print("Shares:",shares)
    return shares

##def main():
##    print("1.Generate Shares 2.Reconstruct Secret")
##    i = int(input())
##    if i == 1:
##        print("Participants: ",end=" ")
##        n = int(input())
##        print("Threshold:    ",end=" ")
##        m = int(input())
##        print("Secret:       ",end=" ")
##        secret = int(input())
##        share = tnshares(n,m,secret)
##        for s in share:
##            print(s[0],s[1])
##        return
##    elif i == 2:
##        print("Threshold: ",end=" ")
##        thres = int(input())
##        print("No. of attempting shares: ",end=" ")
##        s_no = int(input())
##        s_arr = []
##        for c in range(1,s_no+1):
##            print("Enter share number:",end=" ")
##            share_no = int(input())
##            print("Enter share value:",end="")
##            inp = int(input())
##            s_arr.append([share_no,inp])
##        print("Secret is :",tncombine(s_arr,thres))
##        return
##        
##while True:
##    main()
##
##    
