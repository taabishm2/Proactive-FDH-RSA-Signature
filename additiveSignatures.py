def additive_signature():

    global verify_sum,verify_p,verify_challenge,verify_verifier,verify_response,verify_generator

    verify_challenge, verify_response = [],[]

    verify_p = additiveSignature.init(n)
    verify_sum = additiveSignature.pick_sum(max(additive_shares)+1)
    verify_challenge,verify_verifier, verify_generator = additiveSignature.challenge(additive_shares,verify_p,verify_sum)  #instead of passing shares, reuse witness generated g^di values


def additive_signature_verify():
    global verify_sum,verify_p,verify_challenge,verify_verifier,verify_response,verify_generator,share_status

    verify_response = additiveSignature.response(verify_challenge,additive_shares,verify_p,verify_sum,verify_verifier,verify_generator)
    share_status = verify_response

    print("ADDITIVE SHARE STATUS:",verify_response)

    if verify_response.count(True) != add_shares_no:
        print("INVALID SIGNATURE!\nALERT: INVOKE BACKUP")
