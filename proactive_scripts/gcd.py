#GCD

#using repeated subtractions:
def gcd1(a,b):
    while a != 0:
        a,b = min(a,b),max(a,b)
        b =  b-a
    return b

#using repeated divisions
def gcd2(a,b):
    a,b = min(a,b),max(a,b)
    while b%a != 0:
        b = b%a
        a,b = min(a,b),max(a,b)
    return a
        
        
        
