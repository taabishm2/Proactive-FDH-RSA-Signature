#Key generation

import fileOp
import coprime
import modInverse

import additiveShares
import thresholdShares

def gen_keys():

    p,q = fileOp.read_list("FprimesPQ")
    n = fileOp.read_list("FmodulusRSA")[0]
    toit_n = (p-1)*(q-1)    #Euler Toitent Function on RSA Modulus

    #Public Key Generation
    public_key = coprime.find_coprime(toit_n)   #Find public key which is coprime to Toitent Value
    fileOp.write_list("FpublicKey",[n,public_key])

    #Private key Generation
    private_key = modInverse.modular_inverse(public_key,toit_n) % toit_n
    fileOp.write_list("FprivateKey",[n,private_key])

    #Generate additive shares for private keys
    additiveShares.generate(private_key)

    #Make additive share's backup threshold shares using Feldman VSS
    thresholdShares.threshold_additive_shares()

if __name__ == '__main__':
    gen_keys()
