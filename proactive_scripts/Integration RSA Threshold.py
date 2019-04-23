import random
import ShamirSS
import RSAFeldmanVSS
import RSA
import functools
import threading
import time
import math
import undeniableSignature
import additiveSignature
from operator import mul


import gensafeprime
from Crypto.Util import number
from math import gcd
from time import sleep

#For Threshold RSA
global additive_shares
global sub_shares
global share_status
global ciphertext
global partial_signatures

#For RSA
global first_primes_list
global encrypt_key
global ciphertext
global n

#For Feldman VSS
global vss_p    #All these are lists, ith element storing appropriate values corresponding to ith additive share
global vss_q
global gen
global commitment_list

#For additive share witness generation
global add_g
global witness_list

#For additive signature verification using Undeniable Signatures
global undeny_p
global undeny_g
global undeny_challenge
global undeny_verifier
global undeny_response

#For additive signature verification using Additive Signatures
global verify_sum
global verify_p
global verify_challenge
global verify_verifier
global verify_response
global verify_generator

def gen_add_g(g0,p):
    '''g0 is a high order element, p players'''
    global add_g
    global n
    
    #add_g = pow(g0,(math.factorial(p))**2,n)
    add_g =g0

    

class sender:

    def __init__(self):
        self.plaintext = None
        self.set_message()
        self.encrypt()

    def set_message(self):
        print("\nPlaintext:",end="")
        #inp = int(input())
        #self.plaintext = inp
        self.plaintext = 123456

    def encrypt(self):
        global ciphertext
        global encrypt_key
        
        ciphertext = eval_mod_exponent(self.plaintext,encrypt_key,n)
        print("\nCiphertext:",ciphertext,'\n')

class receiver:   #Receiver Class Described

    def __init__(self): #Constructor
        global n
        global encrypt_key
        global additive_shares #####Cross functions
        
        self.p, self.q = None, None #The two prime numbers chosen (Hide somehow)
        n = None   #n = pq
        self.decrypt_key = None   #d is the private decryption key
        self.toit_n = None   #represents Euler toitent function for n
        self.plaintext = None #Stores decrypted message
        
        self.generate_prime_pair()
        self.gen_encrypt_key()
        self.gen_decrypt_key()

        print("\nDistributing decryption key")
        additive_sharing(5,self.decrypt_key,1) #####Cross functions Generate 5 additive shares
        print("\nGenerating threshold shares") #####Cross functions Generate 3-4 thresholds for all 5 additive shares
        #threshold_additive_shares(additive_shares,3,4)
        #print("\nRunning Proactivizer")
        #proactive_timer() 

    def generate_prime_pair(self,b=512):
        '''n = number of bits used for the prime generation'''
        global n
        
        self.p = gen_prime_2(b)    
        self.q = gen_prime_2(b)
        n = self.p * self.q
        self.toit_n = (self.p-1)*(self.q-1) #Calculate Euler Toitent of n

    def gen_decrypt_key(self):
        global encrypt_key
        
        self.decrypt_key = modular_inverse(encrypt_key,self.toit_n) % self.toit_n

    def decrypt(self):
        global ciphertext
        global n

        self.plaintext = eval_mod_exponent(ciphertext,self.decrypt_key,n)
        print("Plaintext:",self.plaintext)

    def gen_encrypt_key(self):  #generate random coprimes wrt toit_n
        global encrypt_key

        encrypt_key = find_coprime(self.toit_n)
    
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
        additive_shares_new.append(random.randrange(0,m//n)) ###BUGGGG: if m < n: randrange throws exception
    additive_shares_new.append(m - sum(additive_shares_new))

    if g == 1:      #if argument g=1, additive sharing is in global scope
        additive_shares = additive_shares_new
        return
    else:           #if argument g=0, additive sharing is for locally generating an additive sharing set
        return additive_shares_new

def threshold_additive_shares(shares,t,n):
    '''Divides all elements in the shares list into t-n threshold shares using Feldman VSS into n sub-shares with threshold t'''
    global sub_shares
    global vss_p
    global vss_q
    global gen
    global commitment_list
    
    sub_shares = []
    commitment_list = []
    vss_p = []
    vss_q = []
    gen = []

    for i in shares:

        feld = RSAFeldmanVSS.feldmanvss(t,n,i)
        
        sub_shares.append(feld[0]) #Generate using VSS
        commitment_list.append(feld[1])
        vss_p.append(feld[2])
        vss_q.append(feld[3])
        gen.append(feld[4])
        
    return

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

def signature_generation():
    '''Generates share signatures, n = pq'''
    global additive_shares
    global partial_signatures
    global ciphertext
    global n

    partial_signatures = []

    for i in range(len(additive_shares)):
        partial_signatures.append(pow(ciphertext,additive_shares[i],n))

def signature_verify(sign):
    '''sign = secret'''
    global partial_signatures
    global n

    if sign == functools.reduce(mul, partial_signatures, 1)%n:
        return True
    else:
        return False

def witness_generation(shares):
    global add_g
    global witness_list
    global n

    witness_list = []

    for di in shares:
        witness_list.append(pow(add_g,di,n))

def witness_verification():
    global partial_signatures
    global witness_list
    global ciphertext
    global add_g
    global share_status
    global n

    for i in range(len(partial_signatures)):
        print("DL1:",math.log(partial_signatures[i]%n,ciphertext))
        print("DL2:",math.log(witness_list[i]%n,add_g))
        if math.log(partial_signatures[i],ciphertext) == math.log(witness_list[i],add_g):
            share_status[i] = True
        else:
            share_status[i] = False      

def invoke_backup():    #How this invokes?
    global share_status
    global additive_shares
    global sub_shares

    for i in range(len(share_status)):
        if not share_status[i]:
            print("Share index:",i,"damaged")
            additive_shares[i] = reconstruct_shamir(sub_shares[i],i,t=0)



def undeny_signature():

    global undeny_p,n,undeny_challenge,undeny_verifier,witness_list,partial_signatures,ciphertext,additive_shares,add_g
    
    undeny_challenge, undeny_response = [],[]
    
    undeny_p = undeniableSignature.init(n)
    undeny_challenge,undeny_verifier = undeniableSignature.challenge(witness_list,partial_signatures,undeny_p,add_g,ciphertext)
    res = undeniableSignature.response(undeny_challenge,additive_shares,undeny_p,undeny_verifier)
    print(undeny_p,add_g,undeny_challenge,undeny_verifier,undeny_response)
    print(res)

def additive_signature():

    global verify_sum,verify_p,verify_challenge,verify_verifier,verify_response,verify_generator

    verify_challenge, verify_response = [],[]

    verify_p = additiveSignature.init(n)
    verify_sum = additiveSignature.pick_sum(123456)
    verify_challenge,verify_verifier, verify_generator = additiveSignature.challenge(additive_shares,verify_p,verify_sum)  #instead of passing shares, reuse witness generated g^di values 
    verify_response = additiveSignature.response(verify_challenge,additive_shares,verify_p,verify_sum,verify_verifier,verify_generator)
    print(verify_response)



def modular_inverse(a, m):  
    m0 = m 
    y = 0
    x = 1
  
    if (m == 1) : 
        return 0
  
    while (a > 1) : 
        q = a // m 
        t = m 
        m = a % m 
        a = t 
        t = y 
        y = x - q * y 
        x = t 
  
    if (x < 0) : 
        x = x + m0 
  
    return x


def eval_mod_exponent(x, y, p) : 
    res = 1  
    x = x % p  
  
    while (y > 0) : 
        if ((y & 1) == 1) : 
            res = (res * x) % p 
  
        y = y >> 1
        x = (x * x) % p 
    return res 
        


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

def crypto_prime(n):
    return number.getPrime(n)

def erik_tews_SSL_prime(n):
    return gensafeprime.generate(n)

def first_primes(t):
    '''Generate the first prime numbers upto t using Eratosthenes'''
    global first_primes_list
    first_primes_list = []
    
    test_lis = [i for i in range(2,t+1)]

    for i in test_lis:
        first_primes_list.append(i)

        for x in range(2,(t+1)//i+1):
            if x*i in test_lis:
                test_lis.remove(x*i)

def gen_prime_1(n):

    while True:
        sample = random_n(n) #Randomly choose n bit number
        
        for i in first_primes_list:
            if sample%i == 0:
                break
            if sample < 4000000:
                if i > sample**(1/2):
                    return sample
        else: return sample

def miller_rabin_test(n):
    """ Miller-Rabin primality test. """
    
    if n==0 or n==1 or n==4 or n==6 or n==8 or n==9:
        return False
    if n==2 or n==3 or n==5 or n==7:
        return True
    
    s = 0
    d = n-1
    while d%2==0:
        d >>= 1 #Bitwise Right Shift. Same as dividing d by 2
        s+=1
    assert(2**s * d == n-1)
 
    def trial_composite(a):
        if pow(a, d, n) == 1:
            return False
        for i in range(s):
            if pow(a, 2**i * d, n) == n-1:
                return False
        return True  
 
    for i in range(20): #number of trials
        a = random.randrange(2, n)
        if trial_composite(a):
            return False
 
    return True 
        
def gen_prime_2(n):
    '''Incorporates all tests to generate prime'''
    
    while True:
        sample = gen_prime_1(n) #Generate Random No. based on small prime division

        #print("TESTING:",sample)

        #Fermat Takes too long, thus disabled. Enable to add Fermat Test
        '''
        if fermat_test(sample) == False:    #Apply Fermat Test
            print("   FERMAT FAILED   ") 
            continue
        '''
        
        if miller_rabin_test(sample) == False:  #Apply Miller Rabin Test
            #print("   RABIN FAILED   ")
            continue
        
        #print("   PASSED   ")
        return sample

def fermat_test(p,a=2):
    '''Using base (a) = 2'''
    if a**(p-1) % p == 1 % p:
        return True
    else:
        return False

def random_n(n):
    return(random.randrange(2**(n-1)+1,2**n-1))









        
@background
def proactive_timer():
    while True:
        print(additive_shares)
        time.sleep(3)  #Shares refreshed every 10 seconds
        print("Refreshed shares")
        proac_refresh()
        





first_primes(2000) #Generate primes upto 2000. Increase for more filtered values





print("Receiver")
r = receiver()
print("Sender")
s = sender()
print("Signature Generation")
#signature_generation()
#print("Signature Verification")
#signature_verify(12)
#print("add_gen calculation")
gen_add_g(31,5)
#print("Witness generation")
#witness_generation(additive_shares)
#print("Additive Signature Verify")
#additive_signature()


    
##additive_sharing(10,12345,1)
##threshold_additive_shares(additive_shares,2,3)
##time_period()   #Calls the share refreshing function to run in the background






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

    
    
