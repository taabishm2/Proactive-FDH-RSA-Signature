import fileOp
import RSAFeldmanVSS

def reconstruct_shamir(shares,i,t=0): #Do we have to mention which additive share these backups belong to? i.e. need for 'i'?
    '''Verify first using VSS and then reconstruct, i is index of the additive share for vss_p, etc'''

    vss_q = fileOp.read_list("FvssQ")[0]
    vss_p = fileOp.read_list("FvssP")[0]
    gen = fileOp.read_list("FvssGen")[0]
    commitment_list = fileOp.read_list("FvssCommitmentList")[0]

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
