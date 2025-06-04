# ==== BEGIN CONTEXT HEADER ====
# The following file contains a solution to the challenge.
# SPOLIER ALERT : Stop here if you want to solve the challenge yourself.
# ==== END CONTEXT HEADER ====


# Constants
# SERVER_ADDR = "challenges.404ctf.fr" # PROD
SERVER_ADDR = "localhost" # TEST
SERVER_PORT = 32459

DEBUG = False
MSG_SIZE = 1024


import socket
import subprocess
import ast # Abstract Syntax Trees - helps Python applications to process trees of the Python abstract syntax grammar
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Util.number import long_to_bytes
from Crypto.Random import random as rd
import os

flag = os.getenv("flag") or "Flag{This_is_a_fake_flag_for_testing_purposes}"

class Curve:
    def __init__(self, a, b, p, g):
        self.a = a
        self.b = b
        self.p = p
        self.g = g

    def addPoints(self, P, Q):
        # Given two points on the curve, it is possible to define an addition operation between them, resulting in a third point that is also on the curve.
        # To find this point geometrically, we draw a line between the two given points, and continue it until it intersects the curve at a third point.
        # This point is reflected in relation to the 𝑋 axis, and the resulting point is defined as the result of the addition.
        # https://github.com/elikaski/ECC_Attacks?tab=readme-ov-file#points-addition

        a, p = self.a, self.p
        if P == (0, 0):
            return Q

        if Q == (0, 0):
            return P

        x1, y1, x2, y2 = P[0], P[1], Q[0], Q[1]
        if x1 == x2 and y1 == (-y2) % p:
            return 0, 0

        if x1 == x2 and y1 == y2:
            m = (3 * x1 ** 2 + a) * pow(2 * y1, -1, p) % p
        else:
            m = (y2 - y1) * pow(x2 - x1, -1, p) % p

        x3 = (m ** 2 - x1 - x2) % p
        y3 = (m * (x1 - x3) - y1) % p

        return x3, y3

    def pointMultiplication(self, k, P):
        # n * P = P + P + ... + P (n times)
        R = (0, 0)
        Q = P
        while k > 0:
            if k % 2 == 1:
                R = self.addPoints(R, Q)

            Q = self.addPoints(Q, Q)
            k = k // 2
            if k > 0: continue

        return R

Curves = {
    "secp112r1": Curve(0xdb7c2abf62e35e668076bead2088, 0x659ef8ba043916eede8911702b22, 0xdb7c2abf62e35e668076bead208b,
                       (0x09487239995a5ee76b55f9c2f098, 0xa89ce5af8724c0a23e0e0ff77500))    
    # 112-bit prime field Weierstrass curve.
    # A randomly generated curve. SEC2v1 states 'E was chosen verifiably at random as specified in ANSI X9.62 1 from the seed'.
    # Also known as: wap-wsg-idm-ecid-wtls6
    # y^2 ≡ x^3 + ax + b
    # a = 0xdb7c2abf62e35e668076bead2088
    # b = 0x659ef8ba043916eede8911702b22
    # p = 0xdb7c2abf62e35e668076bead208b
    # G = (0x09487239995a5ee76b55f9c2f098, 0xa89ce5af8724c0a23e0e0ff77500)
    # n = 0xdb7c2abf62e35e7628dfac6561c5
    # h = 0x01
    # https://neuromancer.sk/std/secg/secp112r1


    ,"secp160k1": Curve(0x0000000000000000000000000000000000000000, 0x0000000000000000000000000000000000000007,
                         0xfffffffffffffffffffffffffffffffeffffac73,
                         (0x3b4c382ce37aa192a4019e763036f4f5dd4d7ebb, 0x938cf935318fdced6bc28286531733c3f03c4fee))
    # 160-bit prime field Weierstrass curve.
    # A Koblitz curve.
    # Also known as: ansip160k1
    # y^2 ≡ x^3 + ax + b        
    # a = 0x0000000000000000000000000000000000000000
    # b = 0x0000000000000000000000000000000000000007
    # p = 0xfffffffffffffffffffffffffffffffeffffac73
    # G = (0x3b4c382ce37aa192a4019e763036f4f5dd4d7ebb, 0x938cf935318fdced6bc28286531733c3f03c4fee)
    # n = 0x0100000000000000000001b8fa16dfab9aca16b6b3
    # h = 0x1
    # https://neuromancer.sk/std/secg/secp160k1


    ,"secp160r2": Curve(0xfffffffffffffffffffffffffffffffeffffac70, 0xb4e134d3fb59eb8bab57274904664d5af50388ba,
                         0xfffffffffffffffffffffffffffffffeffffac73,
                         (0x52dcb034293a117e1f4ff11b30f7199d3144ce6d, 0xfeaffef2e331f296e071fa0df9982cfea7d43f2e))
    # 160-bit prime field Weierstrass curve.
    # A randomly generated curve. SEC2v1 states 'E was chosen verifiably at random as specified in ANSI X9.62 1 from the seed'.
    # Also known as: ansip160r2
    # y^2 ≡ x^3 + ax + b
    # a = 0xfffffffffffffffffffffffffffffffeffffac70
    # b = 0xb4e134d3fb59eb8bab57274904664d5af50388ba
    # p = 0xfffffffffffffffffffffffffffffffeffffac73
    # G = (0x52dcb034293a117e1f4ff11b30f7199d3144ce6d, 0xfeaffef2e331f296e071fa0df9982cfea7d43f2e)
    # n = 0x0100000000000000000000351ee786a818f3a1a16b
    # h = 0x01
    # https://neuromancer.sk/std/secg/secp160r2
}


def translate(curveName: str) -> Curve:
    try:
        return Curves[curveName]
    except KeyError:
        print("Using a custom curve !") # DEBUG

        # Since I have to return a curve, I'll create my own !
        return Curve(0xbb0480e1f010abb2e69e7d72df5d75a23a15bc73710df25b6da04121f904e4f5,
                     0xfa2bddcca24c1d80baf26cb1e1f04cf78e995c675543c9692e959f83b470a03,
                     0xf7fda1b2f0c9ea506e8a125766fd9e5046fd5716630c84f526fea8ce10497829,
                     (0x735d07d96821ec8bff37eb23c31081ea526ddc10abe22375518c44e043a39db0,
                      0x97e570cf7c177584ddd036d9181a3f5f83307f60c92b539a2d4f479d9c9ad4bd)
                    )
        # y^2 ≡ x^3 + ax + b
        # a = 0xbb0480e1f010abb2e69e7d72df5d75a23a15bc73710df25b6da04121f904e4f5
        # b = 0xfa2bddcca24c1d80baf26cb1e1f04cf78e995c675543c9692e959f83b470a03
        # p = 0xf7fda1b2f0c9ea506e8a125766fd9e5046fd5716630c84f526fea8ce10497829, ~256 bits !
        # G = (0x735d07d96821ec8bff37eb23c31081ea526ddc10abe22375518c44e043a39db0, 0x97e570cf7c177584ddd036d9181a3f5f83307f60c92b539a2d4f479d9c9ad4bd)

def createToken(name: str, destination: int) -> str:
    secureCurves = {1: "secp112r1", 2: "secp160k1", 3: "secp160r2"}
    try:
        return "{'curve':'" + secureCurves[destination] + "','name':'" + name + "'}"
    except KeyError:
        return "{}"

def generateKey(token: dict) -> ((int, int), int):
    curve = translate(token['curve'])
    d = rd.randint(2, curve.p - 1) # this is the private key
    return curve.pointMultiplication(d, curve.g), d
    # we return d * G where G is the generator point of the curve

def encryptData(d: int, data: str, username: str) -> (bytes, bytes):
    cipher = AES.new(pad(long_to_bytes(d),32)[:32], AES.MODE_CBC, IV=pad(username.encode(), 16)[:16])
    # does not look crackable at first glance, we should then find the private key d
    return cipher.encrypt(pad(data.encode(), 16))


# Custom code

def decryptData(d: int, data: bytes, username: str) -> (bytes, bytes):
    cipher = AES.new(pad(long_to_bytes(d),32)[:32], AES.MODE_CBC, IV=pad(username.encode(), 16)[:16])
    return unpad(cipher.decrypt(data), 16).decode()

def test():
    # User controlled input
    payload = "toto','curve':'evil_curve','name':'bob"
    name = payload
    destination = 1 # 1 => secp112r1, 2 => secp160k1, 3 => secp160r2

    token = createToken(name, destination)
    if token == "{}":
        print("Token invalide ! Vérifier les paramètres")
        return

    try:
        token = ast.literal_eval(token)
        publicPoint, d = generateKey(token)
        print(f"publicPoint = {publicPoint}")
    except Exception as e:
        print(f"Erreur de génération du point : {str(e)}")
        return

    ciphertext = encryptData(d, flag, token["name"])
    print(f"enc flag = {ciphertext.hex()}")

    # Decrypting the flag
    try:
        decrypted = decryptData(d, ciphertext, token["name"])
        print(f"Decrypted flag: {decrypted}")
    except Exception as e:
        print(f"Erreur de déchiffrement : {str(e)}")
        return

def solve():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((SERVER_ADDR, SERVER_PORT))

    if not DEBUG:
        print("Solving, this can take up to 10-15 seconds.")

    # First step : send crafted payload as name to set the custom curve
    payload = "toto','curve':'evil_curve','name':'bob"

    info_msg = client.recv(MSG_SIZE)
    if not info_msg:
        return
    if DEBUG: print("Received:" + info_msg.decode())

    answer = payload
    answer += '\n'
    client.send(answer.encode("utf-8")[:MSG_SIZE])
    if DEBUG: print(f"Sent: {answer}")

    info_msg = client.recv(MSG_SIZE)
    if not info_msg:
        return
    if DEBUG: print("Received:" + info_msg.decode())

    # Send the destination
    answer = "1"
    answer += '\n'
    client.send(answer.encode("utf-8")[:MSG_SIZE])
    if DEBUG: print(f"Sent: {answer}")

    # Receive the public point and encryted flag
    msg = client.recv(MSG_SIZE).decode()
    if not msg:
        return
    if DEBUG: print('Received:' + msg)

    P_string = msg.split("point: ")[1].split("\n")[0].strip()
    xP = P_string.split(", ")[0][1:]
    yP = P_string.split(", ")[1][:-1]

    enc_flag = msg.split("dire: ")[1].strip()
    
    # Close the connection
    client.close()
    print("Connection to server closed")

    # Break the key - call sage program from here
    process = subprocess.Popen(' '.join(["sage", "break.sage", xP, yP]), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, text=True)
    output, error = process.communicate()
    key = output.strip()

    # Decrypt the flag
    try:
        d = int(key)
        name = "bob"
        decrypted = decryptData(d, bytes.fromhex(enc_flag), name)
        print(f"Decrypted flag: {decrypted}")
    except Exception as e:
        print(f"Erreur de déchiffrement : {str(e)}")
        return


if __name__ == "__main__":
    # test()
    solve()