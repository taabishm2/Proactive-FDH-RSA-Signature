import RSAFeldmanVSS
import fileOp


def threshold_additive_shares():
    '''Divides all elements in the shares list into t-n threshold shares using Feldman VSS into n sub-shares with threshold t'''

    shares = fileOp.read_list("FadditiveShares")
    t,n = 3,5       #Generates a (3,5) threshold scheme FIX: Read from file

    sub_shares, commitment_list = [], []
    vss_p, vss_q, gen = [], [], []

    for i in shares:

        feld = RSAFeldmanVSS.feldmanvss(t,n,i)

        sub_shares.append(feld[0])      #Generate using VSS
        commitment_list.append(feld[1])
        vss_p.append(feld[2])
        vss_q.append(feld[3])
        gen.append(feld[4])

    fileOp.write_list("FvssP",vss_p)
    fileOp.write_list("FvssQ",vss_q)
    fileOp.write_list("FvssGen",gen)
    fileOp.write_list("FvssSubShares",sub_shares)
    fileOp.write_list("FvssCommitmentList",commitment_list)

    return

