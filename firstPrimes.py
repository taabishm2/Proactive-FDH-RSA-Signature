import fileOp


def first_primes(t):
    '''Generate the first prime numbers upto t using Eratosthenes Seive'''
    
    first_primes_list = []
    
    test_lis = [i for i in range(2,t+1)]

    for i in test_lis:
        first_primes_list.append(i)

        for x in range(2,(t+1)//i+1):
            if x*i in test_lis:
                test_lis.remove(x*i)

    fileOp.write_list("FfirstPrimes",test_lis)

