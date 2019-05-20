import random
from math import ceil
from decimal import *


def tncombine(shares,field_size,t=0): #Combines shares using Lagranges interpolation
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
        prod *= yj

        sums += Decimal(prod) % Decimal(field_size)

    return int(round(Decimal(sums),0)) % field_size


def polynom(x,coeff,field_size):
    '''Evaluates a polynomial in x with coeff being the coefficient matrix with a given x'''
    y = 0
    for i in range(len(coeff)):
        y += (x**(len(coeff)-i-1)) * coeff[i]
    return y % field_size


def coeff(t,secret,field_size):
    '''randomly generate a coefficient array for a polynomial with degree t-1 whose constant = secret'''

    coeff = []
    for i in range(t-1):
        coeff.append(random.randrange(0,field_size-1))
    coeff.append(secret)

    return coeff

def tnshares(n,m,secret,field_size):
    '''Split secret using SSS into n shares with threshold m'''

    cfs = coeff(m,secret,field_size)

    shares = []
    for i in range(1,n+1):

        #r = random.randrange(1,field_size-1) #Random share numbers not working

        shares.append([i,polynom(i,cfs,field_size)])

    return [shares,cfs]


