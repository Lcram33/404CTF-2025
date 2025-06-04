# ==== BEGIN CONTEXT HEADER ====
# The following file was NOT MODIFIED and is the original challenge file.
# The file flag.txt contains a DUMMY flag for local testing purposes.
# ==== END CONTEXT HEADER ====


from Crypto.Util.number import isPrime, getPrime
import os

s = 512
a, b, M = getPrime(s // 8), getPrime(s // 8), 2**s

seed = int.from_bytes(os.urandom(s // 8)) % M
FLAG = open("flag.txt", "rb").read()

def gen():
    global seed
    seed = (a*seed + b) % M
    return seed

def genPrime():
    g = gen()
    while not isPrime(g): 
        g += 1
    return g

for _ in range(4):
    print("La Lunette Cosmico-Galactique est prête et pointée en direction du vaisseau ALIENS :")
    print("1. Mesurer le champ électromagnétique émanant du vaisseau")
    print("2. Intercepter une communication ALIEN")

    try:
        choice = int(input("Que faire ? :"))
    except:
        exit()

    if choice == 1:
        print("La lunette indique :", genPrime())
    elif choice == 2:
        seed = int.from_bytes(os.urandom(s // 8)) % M
        print("Mince les ALIENS semblent réactualiser leurs signature électromagnétique, mince alors >:(")

        e = 65537
        n1 = genPrime()*genPrime()
        n2 = genPrime()*genPrime()
        c1 = pow(int.from_bytes(FLAG[:len(FLAG)//2]), e, n1)
        c2 = pow(int.from_bytes(FLAG[len(FLAG)//2:]), e, n2)

        print(f"Message intercepté : {hex(n1)[2:]}-{hex(c1)[2:]}-{hex(n2)[2:]}-{hex(c2)[2:]}")

print("Les ALIENS se sont enfuis... ")