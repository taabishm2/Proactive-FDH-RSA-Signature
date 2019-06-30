import fileOp
import fdh

class verifier:


    def __init__(self):

        try:
            self.signature = fileOp.read_list_noint("Fsignature")[0]
        except:
            raise Exception("Failed to read Fsignature")

        self.verify()


        self.verify(fname)

    def verify(self,fname):

        ciphertext = fileOp.read_list("Fciphertext")[0]

        n = fileOp.read_list("FpublicKey")[0]

        public_key = fileOp.read_list("FpublicKey")[1]

        inp = fname

        inp = fileOp.read_binary_file(inp)

        inp = fdh.fdh(inp,(len(bin(n))-2))

        signaturec = pow(ciphertext,public_key,n)

        if signaturec - int(inp,16) == 0:

            print("VERIFIED!")

            return True

        else:

            print("FAILED!")

            return False

if __name__ == "__main__":

    v = verifier("picn.jpg")
