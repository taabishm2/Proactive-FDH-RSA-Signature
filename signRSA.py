import fileOp
import fdh
import modInverse
import initRSAsignature
import coprime

global public_key, private_key, n


class signer:

    def __init__(self):

        global public_key, private_key, n

        public_key = fileOp.read_list("FpublicKey")[1]

        n, private_key = fileOp.read_list("FprivateKey")
        
        self.set_message()
        
        self.sign()

    def set_message(self):

        print("File to be signed:",end=" ")
        
        inp = input()

        inp = fileOp.read_large_data(inp)
        
        inp = fdh.fdh(inp,(len(bin(n))-2)) 
        
        fileOp.write_list("Fsignature",[inp])


    def sign(self):

        signature = fileOp.read_list_noint("Fsignature")[0]
        
        signature = int(signature[1:-1],16)
        
        ciphertext = pow(signature, private_key, n)

        fileOp.write_list("Fciphertext",[ciphertext])


s = signer()
