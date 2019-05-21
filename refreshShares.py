def refresh_shares():
    '''Refreshes all shares in list old_shares,share field size is f'''

    additive_shares = fileOp.read_list("FadditiveShares")[0]
    n = fileOp.read_list("FpublicKey")[0]


    old_shares = additive_shares
    l = len(old_shares)
    new_shares = [0 for _ in range(l)]
    for i in old_shares:
        share_div = additive_sharing(l,i,0)
        new_shares = [(a+b) for a,b in zip(new_shares,share_div)]
    additive_shares = new_shares

    fileOp.write_list("FadditiveShares",additive_shares)

    threshold_additive_shares()
