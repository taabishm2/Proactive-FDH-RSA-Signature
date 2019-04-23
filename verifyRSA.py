import fileOp
import fdh

class verifier:

    def __init__(self):

        try:
            self.signature = fileOp.read_list_noint("Fsignature")[0]
        except:
            raise Exception("Failed to read Fsignature")

        self.verify()

    def verify(self):

        ciphertext = fileOp.read_list("Fciphertext")[0]
        
        n = fileOp.read_list("FpublicKey")[0]
        
        public_key = fileOp.read_list("FpublicKey")[1]

        print("Filename of file to be checked (with extension):",end=" ")
        
        inp = input()

        inp = fileOp.read_binary_file(inp)
        
        inp = fdh.fdh(inp,(len(bin(n))-2))
        
        signaturec = pow(ciphertext,public_key,n)
        
        if signaturec - int(inp,16) == 0:
            
            return True
            
        else:
            
            return False

if __name__ == "__main__":

    v = verifier()
