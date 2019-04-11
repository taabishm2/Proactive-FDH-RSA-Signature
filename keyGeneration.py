#Key generation

import fileOp
import coprime
import modInverse

def gen_keys():

    p,q = fileOp.read_list("FprimesPQ")
    n = fileOp.read_list("FmodulusRSA")[0]
    toit_n = (p-1)*(q-1)
    #Public Key Generation
    public_key = coprime.find_coprime(toit_n)

    fileOp.write_list("FpublicKey",[n,public_key])
    
    #Private key Generation
    private_key = modInverse.modular_inverse(public_key,toit_n) % toit_n

    fileOp.write_list("FprivateKey",[n,private_key])

