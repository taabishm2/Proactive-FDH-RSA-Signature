#Background Proactivization

import threading
import random
import time
import IntegrationRSA

global n
global import_shares

global additive_shares

def additive_sharing(p,m,g):
    '''Employs additive sharing to divide a secret 'm' into 'p' shares
    g (=0 or 1) indicates whether or not the global shares are to be updated '''

    global additive_shares
    global n
    
    additive_shares_new = []
    
    for i in range(p-1):
        additive_shares_new.append(random.randrange(0,m+1))     #FIX to pick values 0 to m and roll around with modulo

    s = m - sum(additive_shares_new)

    while s < 0: s += n
    
    additive_shares_new.append(s)

    if g == 1:      #if argument g=1, additive sharing is in global scope
        additive_shares = additive_shares_new
        return
    else:           #if argument g=0, additive sharing is for locally generating an additive sharing set
        return additive_shares_new


def background(f): #Runs function under @background in the background
    '''
    a threading decorator
    use @background above the function you want to run in the background
    '''
    def backgrnd_func(*a, **kw):
        threading.Thread(target=f, args=a, kwargs=kw).start()
    return backgrnd_func


def timed_function(input_shares,f):
    '''Refreshes all shares in list old_shares,share field size is f'''

    global import_shares
    
    old_shares = import_shares
    n = len(old_shares)
    new_shares = [0 for _ in range(n)]
    for i in old_shares:
        share_div = additive_sharing(n,i,0)
        new_shares = [(a+b)%f for a,b in zip(new_shares,share_div)]
    import_shares = new_shares
    IntegrationRSA.additive_shares = import_shares
    print("REFRESHED!:",import_shares)

@background

def proactive_timer(inp_shares,f):
    '''f is field size for shares == n = p.q'''
    global n
    global import_shares
    n = f
    import_shares = inp_shares
    while True:
        timed_function(inp_shares,f)
        time.sleep(1)  #Shares refreshed every 3 seconds






