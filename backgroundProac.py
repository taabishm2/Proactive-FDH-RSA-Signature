import refreshShares
import additiveShares
import partialSignatures

def background(f): #Runs function under @background in the background
    '''
    a threading decorator
    use @background above the function you want to run in the background
    '''
    def backgrnd_func(*a, **kw):
        threading.Thread(target=f, args=a, kwargs=kw).start()
    return backgrnd_func

@background
def proactive_timer():
    '''f is field size for shares == n = p.q'''

    n = fileOp.read_list("FpublicKey")[0]
    additive_shares = fileOp.read_list("FadditiveShares")[0]

    while True:

        refreshShares.refresh_shares()
        additiveShares.additive_signature()

        print("Original:",additive_shares)

        time.sleep(15)  #Shares refreshed every 3 seconds

        #Verify all signatures
        add_sig_ver = partialSignatures.signature_verify()

        #Detect Faulty Additive share (if any)
        if not add_sig_ver:
            additive_signature_verify()

            #Invoke Share reconstruction if faulty share present
            invoke_backup()
