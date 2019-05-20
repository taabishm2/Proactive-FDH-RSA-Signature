import fileOp
import fdh
import modInverse
import initRSAsignature
import coprime

global public_key, private_key, n


class signer:

    def __init__(self,fname):

        global public_key, private_key, n

        public_key = fileOp.read_list("FpublicKey")[1]

        n, private_key = fileOp.read_list("FprivateKey")    #FIX: Reconstruct using Shamir and rest

        self.set_message(fname)

        self.sign()

    def set_message(self,fname):

        inp = fname

        inp = fileOp.read_binary_file(inp)

        inp = fdh.fdh(inp,(len(bin(n))-2))

        fileOp.write_list("Fsignature",[inp])


    def sign(self):

        signature = fileOp.read_list_noint("Fsignature")[0]

        signature = int(signature[1:-1],16)

        ciphertext = pow(signature, private_key, n)

        fileOp.write_list("Fciphertext",[ciphertext])

        print("Signed!")

if __name__ == "__main__":

    s = signer("pico.jpg")
