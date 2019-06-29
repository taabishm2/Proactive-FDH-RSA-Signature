import fileOp
import additiveShares
import thresholdShares

def refresh_shares():
    '''Refreshes all shares in list old_shares,share field size is f'''

    additive_shares = fileOp.read_list("FadditiveShares")
    n = fileOp.read_list("FmodulusRSA")[0]

    old_shares = additive_shares
    l = len(old_shares)
    new_shares = [0 for _ in range(l)]

    #Refresh previous additive shares
    for i in old_shares:
        share_div = additiveShares.additive_sharing(i,l)
        new_shares = [(a+b) for a,b in zip(new_shares,share_div)]

    #Update new refreshed shares
    fileOp.write_list("FadditiveShares",new_shares)

    #Threshold on new shares
    print("Running")
    thresholdShares.threshold_additive_shares()
    print("Done")

def proactive_timer():
    '''f is field size for shares == n = p.q'''
    global n
    global additive_shares
    while True:

        refresh_shares()
        additive_signature()

        print("Original:",additive_shares)

        time.sleep(15)  #Shares refreshed every 3 seconds

        #Verify all signatures
        add_sig_ver = signature_verify()

        #Detect Faulty Additive share (if any)
        if not add_sig_ver:
            additive_signature_verify()

            #Invoke Share reconstruction if faulty share present
            invoke_backup()

if __name__ == '__main__':
    refresh_shares()
