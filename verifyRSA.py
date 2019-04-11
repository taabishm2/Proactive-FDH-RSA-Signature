import fileOp
import fdh

class verifier:

    def __init__(self):
        
        self.signature = fileOp.read_list_noint("Fsignature")[0]
        
        self.verify()

    def verify(self):

        ciphertext = fileOp.read_list("Fciphertext")[0]
        
        n = fileOp.read_list("FpublicKey")[0]
        
        public_key = fileOp.read_list("FpublicKey")[1]

        print("File to be checked:",end=" ")
        
        inp = input()

        inp = fileOp.read_large_data(inp)
        
        inp = fdh.fdh(inp,(len(bin(n))-2))
        
        signaturec = pow(ciphertext,public_key,n)
        
        if signaturec - int(inp,16) == 0:
            
            print("VERIFIED!")
            
        else:
            
            print("FAILED!")

v = verifier()
