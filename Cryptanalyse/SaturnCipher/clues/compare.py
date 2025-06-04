# ==== BEGIN CONTEXT HEADER ====
# The following file is a MODIFIED version of the original challenge file.
# It contains the technical solution to solve the challenge, although being serverless and not optimized.
# SPOLIER ALERT : Stop here if you want to solve the challenge yourself.
# ==== END CONTEXT HEADER ====


from Crypto.Util.Padding import pad, unpad
import random


class Saturn:
    def __init__(self, k):
        self.key = k
        self.S = [
            0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76,
            0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0,
            0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15,
            0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75,
            0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84,
            0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF,
            0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8,
            0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2,
            0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73,
            0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB,
            0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79,
            0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08,
            0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A,
            0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E,
            0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF,
            0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16
        ]
        self.perm = [6, 0, 4, 5, 15, 1, 14, 11, 2, 12, 9, 13, 8, 10, 7, 3]

        # Create reverse S-box
        self.S_inv = [0] * len(self.S)
        for i, s in enumerate(self.S):
            self.S_inv[s] = i

        # Create reverse permutation
        self.perm_inv = [0] * len(self.perm)
        for i, p in enumerate(self.perm):
            self.perm_inv[p] = i

        self.N = 1337

    def AddKey(self, state):
        return bytes([x ^ y for x, y in zip(state, self.key)])

    def SubBytes(self, state):
        return bytes([self.S[x] for x in state ])
    
    def SubBytesInv(self, state):
        return bytes([self.S_inv[x] for x in state ])

    def Permute(self, state):
        state = bytes([state[self.perm[i]] for i in range(16)])
        return state
    
    def PermuteInv(self, state):
        state = bytes([state[self.perm_inv[i]] for i in range(16)])
        return state

    def Encrypt(self, x):
        state = x
        for _ in range(self.N):
            state = self.AddKey(state)
            state = self.SubBytes(state)
            state = self.Permute(state)
        return state

    def Decrypt(self, x):
        state = x
        for _ in range(self.N):
            state = self.PermuteInv(state)
            state = self.SubBytesInv(state)
            state = self.AddKey(state)

        return state



# Constants
BLOCK_SIZE = 16
SUB_CHAR = 'S'

# Crafted constants
charset = ''.join(chr(ord('a')+i) for i in range(26))
charset += charset.upper()
charset += ''.join(str(x) for x in range(10))
charset += "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"
charset_hex = [x.encode().hex() for x in charset]
p_box_enc_to_clear = [8, 12, 7, 10, 11, 9, 2, 15, 14, 0, 1, 3, 6, 5, 4, 13] # Generated with map_positions()


def count_common_bytes(hex1, hex2):
    # Split the hashes into pairs of 2 characters
    k = 2
    n = hex1
    hex1_lst = [n[i:i+k] for i in range(0,len(n),k)]

    n = hex2
    hex2_lst = [n[i:i+k] for i in range(0,len(n),k)]

    # Compare the two lists
    cmp_lst = [1 if x == y else 0 for x, y in zip(hex1_lst, hex2_lst)]
    return sum(cmp_lst), len(cmp_lst)

def create_last_block_candidates():
    candidates = list()

    for n in range(0, BLOCK_SIZE - 1):
        # Yes, up to 15 and not 16 as we use padding and the encrypted flag is 3 * 16 bytes long
        # Case when the last block is empty is treated separately
        word = SUB_CHAR * n + '}'
        padded_word = pad(word.encode('utf8'), BLOCK_SIZE)
        candidates.append(padded_word.hex())
    
    return candidates

def get_last_flag_block_length(encrypted_flag, S: Saturn):
    payloads = create_last_block_candidates()
    common_count_list = []
    for payload in payloads:
        enc = S.Encrypt(bytes.fromhex(payload)).hex()
        common_count, _ = count_common_bytes(enc, encrypted_flag)
        common_count_list.append(common_count)

    iterations = len(payloads)
    best_candidate = payloads[common_count_list.index(max(common_count_list))]
    
    return len(unpad(bytes.fromhex(best_candidate), BLOCK_SIZE)) - 1, iterations

"""
def map_positions():
    p_box = []
    
    base_block = b"\x00" * 16
    changing_byte = 'FF'
    key_str = '92 92 61 62 ac 2e 77 2d 44 f8 39 c2 b1 0e 39 47'
    key = bytes.fromhex(key_str)
    S = Saturn(key)
    
    base_enc = S.Encrypt(base_block)
    
    # First iteration
    block_str = 30 * '0' + changing_byte
    block = bytes.fromhex(block_str)
    enc = S.Encrypt(block)

    mask = bytes([x ^ y for x, y in zip(enc, base_enc)])
    pos = mask.index([x for x in mask if x != 0][0])
    p_box.append(pos)

    for _ in range(15):
        block_str = hex(int(block_str, 16) << 8)[2:]
        block_str = block_str.zfill(32)
        block = bytes.fromhex(block_str)
        enc = S.Encrypt(block)

        mask = bytes([x ^ y for x, y in zip(enc, base_enc)])
        pos = mask.index([x for x in mask if x != 0][0])
        p_box.append(pos)
    
    p_box_clear_to_enc = p_box[::-1] # We started from the last byte !

    p_box_enc_to_clear = [0] * len(p_box_clear_to_enc)
    for i, p in enumerate(p_box_clear_to_enc):
            p_box_enc_to_clear[p] = i

    return p_box_enc_to_clear
"""

def brute_force_flag_first_block(encrypted_flag, S: Saturn):
    iter = 0

    k = 2
    n = encrypted_flag
    encrypted_flag_lst = [n[i:i+k] for i in range(0,len(n),k)]

    # Initial candidate
    word = "404CTF{"
    word += SUB_CHAR * (BLOCK_SIZE - len(word))
    candidate = word.encode('utf8').hex()
    n = candidate
    candidate_lst = [n[i:i+k] for i in range(0,len(n),k)]

    enc_candidate = S.Encrypt(bytes.fromhex(candidate)).hex()
    n = enc_candidate
    enc_candidate_lst = [n[i:i+k] for i in range(0,len(n),k)]

    memory_random = {}
    while enc_candidate != encrypted_flag:
        # Update the candidate
        new_candidate_lst = [0] * len(candidate_lst)
        for i in range(len(enc_candidate_lst)):
            if enc_candidate_lst[i] == encrypted_flag_lst[i]:
                new_candidate_lst[p_box_enc_to_clear[i]] = candidate_lst[p_box_enc_to_clear[i]]
        for i in range(len(new_candidate_lst)): # Fill the rest with random chars
            if new_candidate_lst[i] == 0:
                if i not in memory_random:
                    memory_random[i] = list()

                random_byte_hex = random.choice(charset_hex)
                while random_byte_hex in memory_random[i]:
                    random_byte_hex = random.choice(charset_hex)
                
                new_candidate_lst[i] = random_byte_hex
                memory_random[i].append(random_byte_hex)

        new_candidate = ''.join(new_candidate_lst)
        enc_new_candidate = S.Encrypt(bytes.fromhex(new_candidate)).hex()
        if count_common_bytes(enc_new_candidate, encrypted_flag) > count_common_bytes(enc_candidate, encrypted_flag):
            candidate = new_candidate
            enc_candidate = enc_new_candidate

            n = candidate
            candidate_lst = [n[i:i+k] for i in range(0,len(n),k)]

            n = enc_candidate
            enc_candidate_lst = [n[i:i+k] for i in range(0,len(n),k)]
        
        iter += 1

    return bytes.fromhex(candidate).decode('utf8'), iter

def brute_force_flag_middle_block(encrypted_flag, S: Saturn):
    iter = 0

    k = 2
    n = encrypted_flag
    encrypted_flag_lst = [n[i:i+k] for i in range(0,len(n),k)]

    # Initial candidate
    word = BLOCK_SIZE * SUB_CHAR
    candidate = word.encode('utf8').hex()
    n = candidate
    candidate_lst = [n[i:i+k] for i in range(0,len(n),k)]

    enc_candidate = S.Encrypt(bytes.fromhex(candidate)).hex()
    n = enc_candidate
    enc_candidate_lst = [n[i:i+k] for i in range(0,len(n),k)]

    memory_random = {}
    while enc_candidate != encrypted_flag:
        # Update the candidate
        new_candidate_lst = [0] * len(candidate_lst)
        for i in range(len(enc_candidate_lst)):
            if enc_candidate_lst[i] == encrypted_flag_lst[i]:
                new_candidate_lst[p_box_enc_to_clear[i]] = candidate_lst[p_box_enc_to_clear[i]]
        for i in range(len(new_candidate_lst)): # Fill the rest with random chars
            if new_candidate_lst[i] == 0:
                if i not in memory_random:
                    memory_random[i] = list()

                random_byte_hex = random.choice(charset_hex)
                while random_byte_hex in memory_random[i]:
                    random_byte_hex = random.choice(charset_hex)
                
                new_candidate_lst[i] = random_byte_hex
                memory_random[i].append(random_byte_hex)

        new_candidate = ''.join(new_candidate_lst)
        enc_new_candidate = S.Encrypt(bytes.fromhex(new_candidate)).hex()
        if count_common_bytes(enc_new_candidate, encrypted_flag) > count_common_bytes(enc_candidate, encrypted_flag):
            candidate = new_candidate
            enc_candidate = enc_new_candidate

            n = candidate
            candidate_lst = [n[i:i+k] for i in range(0,len(n),k)]

            n = enc_candidate
            enc_candidate_lst = [n[i:i+k] for i in range(0,len(n),k)]
        
        iter += 1

    return bytes.fromhex(candidate).decode('utf8'), iter


def brute_force_flag_last_block(flag_length, encrypted_flag, S: Saturn):
    iter = 0

    k = 2
    n = encrypted_flag
    encrypted_flag_lst = [n[i:i+k] for i in range(0,len(n),k)]

    # Initial candidate
    word = SUB_CHAR * flag_length + '}'
    candidate = pad(word.encode('utf8'), BLOCK_SIZE).hex()
    n = candidate
    candidate_lst = [n[i:i+k] for i in range(0,len(n),k)]

    enc_candidate = S.Encrypt(bytes.fromhex(candidate)).hex()
    n = enc_candidate
    enc_candidate_lst = [n[i:i+k] for i in range(0,len(n),k)]

    memory_random = {}
    while enc_candidate != encrypted_flag:
        # Update the candidate
        new_candidate_lst = [0] * len(candidate_lst)
        for i in range(len(enc_candidate_lst)):
            if enc_candidate_lst[i] == encrypted_flag_lst[i]:
                new_candidate_lst[p_box_enc_to_clear[i]] = candidate_lst[p_box_enc_to_clear[i]]
        for i in range(len(new_candidate_lst)): # Fill the rest with random chars
            if new_candidate_lst[i] == 0:
                if i not in memory_random:
                    memory_random[i] = list()

                random_byte_hex = random.choice(charset_hex)
                while random_byte_hex in memory_random[i]:
                    random_byte_hex = random.choice(charset_hex)
                
                new_candidate_lst[i] = random_byte_hex
                memory_random[i].append(random_byte_hex)

        new_candidate = ''.join(new_candidate_lst)
        enc_new_candidate = S.Encrypt(bytes.fromhex(new_candidate)).hex()
        if count_common_bytes(enc_new_candidate, encrypted_flag) > count_common_bytes(enc_candidate, encrypted_flag):
            candidate = new_candidate
            enc_candidate = enc_new_candidate

            n = candidate
            candidate_lst = [n[i:i+k] for i in range(0,len(n),k)]

            n = enc_candidate
            enc_candidate_lst = [n[i:i+k] for i in range(0,len(n),k)]
        
        iter += 1

    return unpad(bytes.fromhex(candidate), BLOCK_SIZE).decode('utf8'), iter


# Main program

# For testing, will be managed by the server
key_str = '92 92 61 62 ac 2e 77 2d 44 f8 39 c2 b1 0e 39 47'
key = bytes.fromhex(key_str)
S = Saturn(key)
with open('flag.txt', 'rb') as f:
    SECRET_FLAG = f.read().strip()
padded_flag = pad(SECRET_FLAG, 16)
flag_blocks = [padded_flag[i:i+16] for i in range(0, len(padded_flag), 16)]
enc_blocks = list(map(S.Encrypt, flag_blocks))
encrypted_flag = b"".join(enc_blocks).hex()

# Clear variables to avoid conflicts
del padded_flag
del flag_blocks
del enc_blocks
del SECRET_FLAG


#############################################

# Main program

iterations = 0

# Split flag
encrypted_flag_blocks = [encrypted_flag[i:i+32] for i in range(0, len(encrypted_flag), 32)]

# Step 1 - Get the first flag block
flag_first, first_iter = brute_force_flag_first_block(encrypted_flag_blocks[0], S)
print(f"Flag first block found after {first_iter} iterations : {flag_first}")
iterations += first_iter

# Step 2 - Get the middle flag block
flag_middle, middle_iter = brute_force_flag_middle_block(encrypted_flag_blocks[1], S)
print(f"Flag middle block found after {middle_iter} iterations : {flag_middle}")
iterations += middle_iter

if flag_middle.endswith('}'):
    print("Flag middle block ends with '}'")
    print(f"Final flag : {flag_first + flag_middle}")
    print("Total iterations :", iterations)
    exit(0)

# Step 2 - Get the last flag block
flag_length, iter_length = get_last_flag_block_length(encrypted_flag_blocks[2], S)
print(f"Flag last part length found after {iter_length} iterations : {flag_length}")
iterations += iter_length

flag_last, last_iter = brute_force_flag_last_block(flag_length, encrypted_flag_blocks[2], S)
print(f"Flag last block found after {last_iter} iterations : {flag_last}")
iterations += last_iter

print(f"Final flag : {flag_first + flag_middle + flag_last}")
print("Total iterations :", iterations)