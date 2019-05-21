def signature_generation():
    '''Generates share signatures, n = pq'''

    additive_shares = fileOp.read_list("FadditiveShares")[0]
    ciphertext = fileOp.read_list("Fciphertext")[0]
    n = fileOp.read_list("FpublicKey")[0]

    partial_signatures = []

    for i in range(len(additive_shares)):
        partial_signatures.append(pow(ciphertext,additive_shares[i],n))

    fileOp.write_list("FpartialSignatures",partial_signatures)


def signature_verify():
    '''sign = secret'''

    n = fileOp.read_list("FpublicKey")[0]
    partial_signatures = fileOp.read_list("FpartialSignatures")[0]

    signature_generation()

    if s.plaintext == functools.reduce(mul, partial_signatures, 1)%n:
        return True
    else:
        return False
