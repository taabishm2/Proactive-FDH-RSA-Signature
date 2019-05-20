import fileOp
import random

def additive_sharing(m,p):
    '''Employs additive sharing to divide a secret 'm' into 'p' shares '''

    n = fileOp.read_list("FpublicKey")[0] #Fetch RSA Modulus from file

    additive_shares_new = []

    for i in range(p-1):    #FIX: If m < p: cannot pick values

        additive_shares_new.append(random.randrange(0,m//p))     #Picks additive shares randomly between 0 to (total_value)/(no_of_shares) - FIX THIS: Increase field size to allow shares between 0 to m

    s = m - sum(additive_shares_new)

    while s < 0: s += n

    additive_shares_new.append(s)

    return additive_shares_new

def generate(private_key):
    '''Start additive share generation with the specified number of shares'''

    add_shares_num = 10     #FIX: Read from file

    share_lis = additive_sharing(private_key,add_shares_num)

    fileOp.write_list("FadditiveShares",share_lis)

if __name__ == '__main__':

    #For testing only
    print(additive_sharing(123,10))
