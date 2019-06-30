def find_coprime(a,n):
    '''Find a random coprime of a which is < n'''

    r = random.randrange(2,n)
    while True:
        if gcd(r,a) == 1:
            return r
        elif r == a-1:
            r = random.randrange(2,a-1)
        else:
            r += 1
