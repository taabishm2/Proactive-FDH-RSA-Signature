import random
import fileOp

def random_n(n):
    '''Generate random n-bit prime number'''
    return(random.randrange(2**(n-1)+1,2**n-1))

def gen_prime_1(n):

    try:
        first_primes_list = fileOp.read_list("FfirstPrimes")
    except Exception as e:
        raise Exception("Couldn't read FfirstPrimes from File")


    while True:
        sample = random_n(n) #Randomly choose n bit number

        for i in first_primes_list:
            if sample%i == 0:   #Divisibility test with pre-generated primes
                break

            if sample < (first_primes_list[-1])**2:
                if i > sample**(1/2):   #If all primes less than sqrt(sample) can't divide then sample is prime

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

    for i in range(20): #number of trials. Higher implies higher probablility of sample being prime

        a = random.randrange(2, n)
        if trial_composite(a):
            return False

    return True

def gen_prime_2(n):
    '''Incorporates all tests to generate prime of n bits'''

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
            #print("RABIN FAILED")
            continue

        #print("RABIN PASSED")
        return sample

def fermat_test(p,a=2):
    '''Using base (a) = 2'''
    if a**(p-1) % p == 1 % p:
        return True
    else:
        return False

def crypto_prime(n):
    return number.getPrime(n)

def erik_tews_SSL_prime(n):
    return gensafeprime.generate(n)

