# ==== BEGIN CONTEXT HEADER ====
# The following file contains a part of the solution to the challenge. (1/2)
# SPOLIER ALERT : Stop here if you want to solve the challenge yourself.
# ==== END CONTEXT HEADER ====

from Crypto.Util.number import isPrime
import os
import json


class LCG: # challenge code refactored to a class for better organization
    def __init__(self, a, b, seed, M):
        self.a = a
        self.b = b
        self.seed = seed
        self.M = M

    def gen(self):
        self.seed = (self.a * self.seed + self.b) % self.M
        return self.seed

    def genPrime(self):
        g = self.gen()
        while not isPrime(g): 
            g += 1
        return g


# Custom code start here
# With inspiration from:
# https://msm.lt/posts/cracking-rngs-lcgs/

def modinv(a, n):
    b, c = 1, 0
    while n:
        q, r = divmod(a, n)
        a, b, c, n = n, c, b - q*c, r
    # at this point a is the gcd of the original inputs
    if a == 1:
        return b
    raise ValueError("Not invertible")

def crack_unknown_increment(states, modulus, multiplier):
    increment = (states[1] - states[0]*multiplier) % modulus
    return modulus, multiplier, increment

def crack_unknown_multiplier(states, modulus):
    multiplier = (states[2] - states[1]) * modinv(states[1] - states[0], modulus) % modulus
    return crack_unknown_increment(states, modulus, multiplier)

def find_state_from_prime(g):
    candidates = [g]
    g -= 1
    while not isPrime(g): 
        candidates.append(g)
        g -= 1
    
    return candidates

def reverse_LCG(p1, p2, p3, M):
    for s1 in find_state_from_prime(p1):
        for s2 in find_state_from_prime(p2):
            for s3 in find_state_from_prime(p3):
                try:
                    _, a, b = crack_unknown_multiplier([s1, s2, s3], M)
                    
                    # a and b must be 64 bits
                    if a.bit_length() > 64 or b.bit_length() > 64:
                        continue
                    
                    return a, b, s1
                except ValueError:
                    continue

def reverse_seed(a, b, M, s1, number_of_states):
    rev_state = s1
    for _ in range(number_of_states):
        rev_state = (rev_state - b) * modinv(a, M) % M

    return rev_state

def decrypt_rsa(p, q, c, n, e=65537):
    phi = (p - 1) * (q - 1)
    d = modinv(e, phi)
    return pow(c, d, n).to_bytes((c.bit_length() + 7) // 8, 'big')
    
def main():
    # Load data
    with open("data.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    
    M = 2**512
    c1 = data["c1"]
    c2 = data["c2"]
    n1 = data["n1"]
    n2 = data["n2"]
    p1 = data["p1"]
    p2 = data["p2"]
    p3 = data["p3"]
    a = None
    b = None
    s1 = None
    seed = None

    # If we restart after a failure, we can use the previous values
    if "a" in data:
        a = data["a"]
    if "b" in data:
        b = data["b"]
    if "s1" in data:
        s1 = data["s1"]
    if "seed" in data:
        seed = data["seed"]


    # Reverse LCG parameters if not provided
    if a is None or b is None or s1 is None:
        print("Reversing LCG parameters. This will take a while...") # Up to 1 hour !
        a, b, s1 = reverse_LCG(p1, p2, p3, M)

        # Logging if something goes wrong
        line1 = f"Reversed LCG parameters:\na={a}\nb={b}\ns1={s1}"
        with open("crack-lcg.log", "w", encoding="utf-8") as f:
            f.write(line1 + "\n")
        print(line1)
    

    # Reverse the seed
    if seed is None:
        print("Reversing seed...")
        seed = reverse_seed(a, b, M, s1, 5)
        # 5 is the number of states we want to reverse
        # 4 calls for encryption + 1st measure
        
        # Logging if something goes wrong
        line2 = f"Reversed seed:\nseed={seed}"
        with open("crack-lcg.log", "a", encoding="utf-8") as f:
            f.write(line2 + "\n")
        print(line2)


    # Re-generate the primes
    lcg = LCG(a, b, seed, M)
    p1, q1 = lcg.genPrime(), lcg.genPrime()
    p2, q2 = lcg.genPrime(), lcg.genPrime()
    
    m1 = decrypt_rsa(p1, q1, c1, n1)
    m2 = decrypt_rsa(p2, q2, c2, n2)
    flag = m1 + m2

    print("Flag: " + flag.decode())


if __name__ == "__main__":
    main()