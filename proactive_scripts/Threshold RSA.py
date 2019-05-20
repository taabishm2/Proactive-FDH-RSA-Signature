import random
import ShamirSS
import RSA
import functools
import threading
import time
from operator import mul

global additive_shares
global sub_shares
global share_status
global ciphertext
global partial_signatures
global n

share_status = {}   #For storing share status, updated as and when needed. Used to determine failure and activate share back up

def background(f): #Runs function under @background in the background
    '''
    a threading decorator
    use @background above the function you want to run in the background
    '''
    def backgrnd_func(*a, **kw):
        threading.Thread(target=f, args=a, kwargs=kw).start()
    return backgrnd_func

def additive_sharing(n,m,g):
    '''Employs additive sharing to divide a secret 'm' into 'n' shares
    g (=0 or 1) indicates whether or not the global shares are to be updated '''

    global additive_shares
    additive_shares_new = []
    for i in range(n-1):
        additive_shares_new.append(random.randrange(0,m//n))
    additive_shares_new.append(m - sum(additive_shares_new))

    if g == 1:      #if argument g=1, additive sharing is in global scope
        additive_shares = additive_shares_new
        return
    else:           #if argument g=0, additive sharing is for locally generating an additive sharing set
        return additive_shares_new

def threshold_additive_shares(shares,t,n):
    '''Divides all elements in the shares list into t-n threshold shares using Shamir SS into n sub-shares with threshold t'''
    global sub_shares
    sub_shares = []

    for i in shares:
        sub_shares.append(ShamirSS.tnshares(n,t,i)) #Generate using VSS
    return

def proac_refresh():
    '''Refreshes all shares in list old_shares'''
    global additive_shares
    
    old_shares = additive_shares
    n = len(old_shares)
    new_shares = [0 for _ in range(n)]
    for i in old_shares:
        share_div = additive_sharing(n,i,0)
        new_shares = [a+b for a,b in zip(new_shares,share_div)]
    additive_shares = new_shares

def signature_generation(shares):
    '''Generates share signatures, n = pq'''
    global additive_shares
    global partial_signatures
    global n

    partial_signatures = []

    for i in range(len(shares)):
        partial_signatures.append(RSA.eval_mod_exponent(ciphertext,additive_shares[i],m))

def signature_verify(sign):
    global partial_signatures
    global n

    if sign == functools.reduce(mul, partial_signatures, 1)%n:
        return True
    else:
        return False
        
@background
def time_period():
    while True:
        print(additive_shares)
        time.sleep(10)  #Shares refreshed every 10 seconds
        print("Refreshed shares")
        proac_refresh()
        
    
additive_sharing(10,12345,1)
threshold_additive_shares(additive_shares,2,3)
time_period()   #Calls the share refreshing function to run in the background






#Main program
##
##start_time = time.time()
##t_count = 0
##
##while True:
##
##    if time.time() - start_time() / 10 > t_count:
##        t_count = time.time() - start_time() / 10
##        print("Refreshing Shares")
##        proac_refresh(*)
##
##    #do stuff here

    
    
