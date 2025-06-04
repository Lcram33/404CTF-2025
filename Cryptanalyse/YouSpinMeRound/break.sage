# From the following writeup:
# https://vozec.fr/aes/analyse-lineaire-aes/

from sage.all import *
import sys

class aes_linear:
    def __init__(self, zero_ciphertext, ciphertext_to_reverse):
        # AES(P) = A*P+B
        self.P = self.plain2vect(16 * b'\x00')
        self.AES_P = self.plain2vect(zero_ciphertext)
        self.recover_A()
        self.recover_B()
        self.AES_P2 = self.plain2vect(ciphertext_to_reverse)

    def plain2vect(self,data):
        return vector([int(x) for x in "{:08b}".format(int(data.hex(),16)).zfill(128)])

    def vect2plain(self,data):
        k = int(''.join([str(x) for x in data]),2)
        return k.to_bytes((k.bit_length() +7) // 8, "big")

    def recover_A(self):
        I = matrix.identity(GF(2),8)
        Z = matrix(GF(2),8)
        X = matrix(GF(2),8,[
            [0,1,0,0,0,0,0,0],
            [0,0,1,0,0,0,0,0],
            [0,0,0,1,0,0,0,0],
            [1,0,0,0,1,0,0,0],
            [1,0,0,0,0,1,0,0],
            [0,0,0,0,0,0,1,0],
            [1,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0]
        ])

        C = block_matrix([
            [X,X+I,I,I],
            [I,X,X+I,I],
            [I,I,X,X+I],
            [X+I,I,I,X],
        ])

        sig0 = block_matrix([[I,Z,Z,Z],[Z,Z,Z,Z],[Z,Z,Z,Z],[Z,Z,Z,Z]])
        sig1 = block_matrix([[Z,Z,Z,Z],[Z,I,Z,Z],[Z,Z,Z,Z],[Z,Z,Z,Z]])
        sig2 = block_matrix([[Z,Z,Z,Z],[Z,Z,Z,Z],[Z,Z,I,Z],[Z,Z,Z,Z]])
        sig3 = block_matrix([[Z,Z,Z,Z],[Z,Z,Z,Z],[Z,Z,Z,Z],[Z,Z,Z,I]])

        S = block_matrix([
            [sig0,sig1,sig2,sig3],
            [sig3,sig0,sig1,sig2],
            [sig2,sig3,sig0,sig1],
            [sig1,sig2,sig3,sig0],
        ])

        Z2 = matrix(GF(2),32)
        M = block_matrix([
            [C,Z2,Z2,Z2],
            [Z2,C,Z2,Z2],
            [Z2,Z2,C,Z2],
            [Z2,Z2,Z2,C],
        ])

        R = M*S
        A = S*R**9

        self.R = R
        self.S = S
        self.A = A

    def recover_B(self):
        self.B = self.AES_P - self.A*self.P

    """ Does not work
    def break_key(self):
        I  = matrix.identity(GF(2),8)
        I2 = matrix.identity(GF(2),8*4)
        Z  = matrix(GF(2),8)
        Z2 = matrix(GF(2),8*4)

        T = block_matrix([
            [Z,I,Z,Z],
            [Z,Z,I,Z],
            [Z,Z,Z,I],
            [I,Z,Z,Z]
        ])

        U = block_matrix([
            [I2,Z2,Z2,T],
            [I2,I2,Z2,T],
            [I2,I2,I2,T],
            [I2,I2,I2,T+I2],
        ])

        V = U**10
        for i in range(10):
            V += self.S * (self.R**i) * (U**(9-i))
        V_inv = V.inverse()


        
        # cipher = myAES()
        # cipher.key = [0]*16
        # cipher.subKeys = cipher.expandKey(cipher.key)
        # K = cipher.encrypt(self.P)
        K = self.K

        K = self.plain2vect(bytes(K))
        r = self.AES_P

        k = V_inv * (K + r).change_ring(GF(2))
        return self.vect2plain(k)
        """

    # here, we only need to get the original plaintext !
    def reverse_plaintext(self):
        """Caclulate P2 = A^-1 * (C2 - B) ==> reversing AES(P2)"""

        P2 = self.A.inverse() * (self.AES_P2 - self.B)

        return self.vect2plain(P2)

# Main program
args = sys.argv[1:]

enc_zero = bytes.fromhex(args[0])
enc = bytes.fromhex(args[1])

exp = aes_linear(
    zero_ciphertext=enc_zero,
    ciphertext_to_reverse=enc
)
reversed_plaintext = exp.reverse_plaintext()

print(reversed_plaintext.hex()) # calling program will read this