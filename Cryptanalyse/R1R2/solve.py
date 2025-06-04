# ==== BEGIN CONTEXT HEADER ====
# The following file contains a solution to the challenge.
# SPOLIER ALERT : Stop here if you want to solve the challenge yourself.
# ==== END CONTEXT HEADER ====


import math


def extract_ci(t: int):
    z = (t >> 1022) & 1
    info_1 = (t >> 511) & ((1 << 511) - 1)
    info_2 = t & ((1 << 511) - 1)
    return z, info_1, info_2

def solve_system(d, e):
    # d = b + c => b = d - c
    # e = b * c => e = (d - c) * c => c^2 - d*c + e = 0
    # We can use the quadratic formula to solve for c

    # Calculate discriminant
    delta = d**2 - 4*e

    sqrt_delta = math.isqrt(delta)
    c1 = (d + sqrt_delta) // 2
    c2 = (d - sqrt_delta) // 2

    # Then calculate coresponding b values
    b1 = d - c1
    b2 = d - c2

    return (b1, c1) if b1 > c1 else (b2, c2)

def decrypt_password(ciphertext: bytes) -> str:
    blocks = [ciphertext[i:i+128] for i in range(0, len(ciphertext), 128)]

    # Extract x and y for each block
    x_lst = []
    y_lst = []
    for block in blocks:
        r = int.from_bytes(block, 'big')
        z, y, x = extract_ci(r)
        if z == 1:
            y = -y
        
        x_lst.append(x)
        y_lst.append(y)
    
    # Calculate d and e
    x1 = x_lst[0]
    x2 = x_lst[1]
    y1 = y_lst[0]
    y2 = y_lst[1]

    d = (y1 - y2 - x1 ** 2 + x2 ** 2) // (x2 - x1)
    e = y1 - x1 ** 2 + d * x1

    b, c = solve_system(d, e)

    # Reconstruct the password
    password = b''
    b = b.to_bytes((b.bit_length() + 7) // 8, 'big')
    c = c.to_bytes((c.bit_length() + 7) // 8, 'big')
    for i in range(max(len(b), len(c))):
        if i < len(b):
            password += b[i:i+1]
        if i < len(c):
            password += c[i:i+1]
    return password.decode()



if __name__ == "__main__":
    # real flag
    enc_flag = "40f1b6e577b2bb6aa703387a15d2738ad50c795972342bdbb4b32946bcf7b72fbbdfb41884883df6589bf0e1e73a01f4f0d13a60146ac87c146de846bb98407d80000000000000000000000000000000000000000000000000000000000000000c4df9ca82064c5b97e3e5013732439d6139195456b94e581b7a22f1510f926c4117ca4ed6a10c5d37b5d400dca883d001564774dbbce5c198c5ff83fe7af851fc3820a17947e71689812f6113dd3893250a14320a8f49c46bde754a188efd3000000000000000000000000000000000000000000000000000000000000000000f6336ee243e9a18cd74b182ff23f87f8bbac8912b57cd3ab25faffcaa18ea3940d748f2696de5597ec5df6d12826fc2b37d8e926af7a39afe74cb0950460da1a33112d89029e1a9334ea4c19d36cab027d4b360f240139de4ebd58ebfb05681800000000000000000000000000000000000000000000000000000000000000029e03851f31bd96e478b63347dc9a369a5d0569dc00ffe07cc3ad2d8293a9bf0"

    # test flag
    # enc_flag = "00000000000000000000000000000000000002133601bf94af26c27c5563c021f72251e2fc9aa340c0998f25b5355778d9e23b906f1128c2e6b49d68b3c07b3b80000000000000000000000000000000000000000000000000000000000000000000000000000000001d32bc4b9fc11b29b111f9730e319ad7e32d3eea999e8400000000000000000000000000000000000000c6ff42da7bcb94e1d0a2360d734976681272f00008d6cf62dd57ca3b00317ca5e82be7812b9f098bacde10433800000000000000000000000000000000000000000000000000000000000000000000000000000000005bb04a0be1c68313a87769613dc4373e15d185a6e079b500000000000000000000000000000000000001a85c414829daa50ead5ace04cd83d2130ad4c755f154bbf899cbd6806172d6f737eacfdf7ac397719564b575880000000000000000000000000000000000000000000000000000000000000000000000000000000000203f745dfd4e09eebd5533e69bffb405c2bd5fd11d4fc5"

    print(decrypt_password(bytes.fromhex(enc_flag)))