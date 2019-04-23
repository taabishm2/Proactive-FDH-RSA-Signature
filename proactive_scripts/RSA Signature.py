import random
import gensafeprime
from Crypto.Util import number
from math import gcd
from time import sleep
from hashlib import sha256

global first_primes_list
global encrypt_key
global ciphertext
global n

global r #used for message padding of 256 bit SHA digest before RSA
global sign #sign decided 

class verifier:

    def __init__(self):
        self.signature = None
        self.verify()

    def verify(self):
        global ciphertext
        global n
        global encrypt_key
        global sign
        
        self.signature = (pow(ciphertext,encrypt_key,n))
        
        print("\nSigner Message Hash:\n",self.signature,'\n')
        if sign == self.signature:
            print("VERIFIED!")
        else:
            print("FAILED!")

class signer:

    def __init__(self): 
        global n
        global encrypt_key
        
        self.p, self.q = None, None 
        n = None  
        self.decrypt_key,self.toit_n,self.plaintext = None,None,None

        
        print("Generating primes...")
        self.generate_prime_pair()
        self.gen_encrypt_key()
        self.gen_decrypt_key()
        self.set_message()
        self.sign()

    def set_message(self):
        
        inp = (fdh())
        self.plaintext = inp

    def generate_prime_pair(self,b=1024):   #1025 bit primes
        '''n = number of bits used for the prime generation'''
        global n
        
        self.p = gen_prime_2(b)    
        self.q = gen_prime_2(b)
        n = self.p * self.q
        self.toit_n = (self.p-1)*(self.q-1)

    def gen_decrypt_key(self):
        global encrypt_key
        
        self.decrypt_key = modular_inverse(encrypt_key,self.toit_n) % self.toit_n

    def sign(self):
        global ciphertext
        global encrypt_key
        
        ciphertext = pow(self.plaintext,self.decrypt_key,n)


    def gen_encrypt_key(self):
        global encrypt_key
        encrypt_key = find_coprime(self.toit_n)
    

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


def fdh():
    '''full domain hash'''
    global sign

    print("\nEnter signature:",end="")
    string = input()
    result = []
    for i in range(2048//256): #produce enough sha256 digests to make total 1024 composite digest
        result.append( sha256((string+str(i)).encode()).hexdigest() )
    result = ''.join(result)[:-1]
    int_result = int(result,16)
    sign = int_result
    print("\nSet hash to:\n",sign)
    return (int_result)
          

def padding(msg):
    '''Pads the message (assumed 256 bit) to a 2047 bit message by xoring with random value which is returned'''
    global r
    
    msg_padded_zeroes = msg * pow(2,1791)               #pad message with zeroes for padding
    
    r = random.randrange(pow(2,2047-1),pow(2,2047)-1)   #random 2047 bit value to be xored to
    print("\nZEROOOO\n",msg_padded_zeroes)    
    msg_padded = msg_padded_zeroes ^ r                  #xoring
    
    return int(msg_padded)

 
def un_pad(msg):
    '''Removes padding applied by paddin() function'''

    global r
    msg_zeroes = msg ^ r
    msg = bin(msg_zeroes)[:258]
    return int(msg,2)




first_primes(2000) #Generate primes upto 2000. Increase for more filtered values

print("RSA Encryption/Decryption")

r1 = signer()
s = verifier()
 
