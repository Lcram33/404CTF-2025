# ==== BEGIN CONTEXT HEADER ====
# The following file contains a solution to the challenge.
# SPOLIER ALERT : Stop here if you want to solve the challenge yourself.
# ==== END CONTEXT HEADER ====


from Crypto.Util.Padding import pad, unpad
import socket
import random


# Constants
# SERVER_ADDR = "challenges.404ctf.fr" # PROD
SERVER_ADDR = "localhost" # TEST
SERVER_PORT = 30169

DEBUG = False
MSG_SIZE = 1024
BLOCK_SIZE = 16
SUB_CHAR = 'X'

# Crafted constants
charset = ''.join(chr(ord('a')+i) for i in range(26)) # a-z
charset += charset.upper() # A-Z
charset += ''.join(str(x) for x in range(10)) # 0-9
charset += "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"
charset_hex = [x.encode().hex() for x in charset]
p_box_enc_to_clear = [8, 12, 7, 10, 11, 9, 2, 15, 14, 0, 1, 3, 6, 5, 4, 13]


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
        padded_word = pad(word.encode(), BLOCK_SIZE)
        candidates.append(padded_word.hex())
    
    return candidates

def get_last_flag_block_length(encrypted_flag, client):
    payloads = create_last_block_candidates()
    common_count_list = []
    for payload in payloads:
        answer = "1"
        answer += '\n'
        client.send(answer.encode("utf-8")[:MSG_SIZE])
        if DEBUG: print(f"Sent: {answer}")

        msg = client.recv(MSG_SIZE).decode()
        if not msg:
            exit(1)
        if DEBUG: print('Received:' + msg)

        answer = payload
        answer += '\n'
        client.send(answer.encode("utf-8")[:MSG_SIZE])
        if DEBUG: print(f"Sent: {answer}")

        msg = client.recv(MSG_SIZE).decode()
        if not msg:
            exit(1)
        if DEBUG: print('Received:' + msg)

        enc = msg.split('>')[1].split('\n')[0].strip()

        common_count, _ = count_common_bytes(enc, encrypted_flag)
        common_count_list.append(common_count)

    iterations = len(payloads)
    best_candidate = payloads[common_count_list.index(max(common_count_list))]
    
    return len(unpad(bytes.fromhex(best_candidate), BLOCK_SIZE)) - 1, iterations

def brute_force_block(encrypted_flag, initial_word: bytes, client):
    iter = 0

    k = 2
    n = encrypted_flag
    encrypted_flag_lst = [n[i:i+k] for i in range(0,len(n),k)]

    # Initial candidate
    candidate = initial_word.hex()
    n = candidate
    candidate_lst = [n[i:i+k] for i in range(0,len(n),k)]

    # Encrypt the candidate
    answer = "1"
    answer += '\n'
    client.send(answer.encode("utf-8")[:MSG_SIZE])
    if DEBUG: print(f"Sent: {answer}")

    msg = client.recv(MSG_SIZE).decode()
    if not msg:
        exit(1)
    if DEBUG: print('Received:' + msg)

    answer = candidate
    answer += '\n'
    client.send(answer.encode("utf-8")[:MSG_SIZE])
    if DEBUG: print(f"Sent: {answer}")

    msg = client.recv(MSG_SIZE).decode()
    if not msg:
        exit(1)
    if DEBUG: print('Received:' + msg)

    enc_candidate = msg.split('>')[1].split('\n')[0].strip()
    
    iter += 1
    
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
        
        # Encrypt the new candidate
        answer = "1"
        answer += '\n'
        client.send(answer.encode("utf-8")[:MSG_SIZE])
        if DEBUG: print(f"Sent: {answer}")

        msg = client.recv(MSG_SIZE).decode()
        if not msg:
            exit(1)
        if DEBUG: print('Received:' + msg)

        answer = new_candidate
        answer += '\n'
        client.send(answer.encode("utf-8")[:MSG_SIZE])
        if DEBUG: print(f"Sent: {answer}")

        msg = client.recv(MSG_SIZE).decode()
        if not msg:
            exit(1)
        if DEBUG: print('Received:' + msg)

        enc_new_candidate = msg.split('>')[1].split('\n')[0].strip()
        
        if count_common_bytes(enc_new_candidate, encrypted_flag) > count_common_bytes(enc_candidate, encrypted_flag):
            candidate = new_candidate
            enc_candidate = enc_new_candidate

            n = candidate
            candidate_lst = [n[i:i+k] for i in range(0,len(n),k)]

            n = enc_candidate
            enc_candidate_lst = [n[i:i+k] for i in range(0,len(n),k)]
        
        iter += 1

    return bytes.fromhex(candidate).decode('utf8'), iter

#############################################

# Main program

iterations = 0

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER_ADDR, SERVER_PORT))

# Init - Get encrypted flag
msg = client.recv(MSG_SIZE).decode()
if not msg:
    exit(1)
if DEBUG: print('Received:' + msg)

answer = "2"
answer += '\n'
client.send(answer.encode("utf-8")[:MSG_SIZE])
if DEBUG: print(f"Sent: {answer}")

msg = client.recv(MSG_SIZE).decode()
if not msg:
    exit(1)
if DEBUG: print('Received:' + msg)

encrypted_flag = msg.split('>')[1].split('\n')[0].strip()


# Split flag
encrypted_flag_blocks = [encrypted_flag[i:i+(2 * BLOCK_SIZE)] for i in range(0, len(encrypted_flag), 2 * BLOCK_SIZE)]

# Step 1 - Get the first flag block
word = "404CTF{"
word += SUB_CHAR * (BLOCK_SIZE - len(word))
word = word.encode()
flag_first, first_iter = brute_force_block(encrypted_flag_blocks[0], word, client)
print(f"Flag first block found after {first_iter} iterations : {flag_first}")
iterations += first_iter

# Step 2 - Get the middle flag block
word = BLOCK_SIZE * SUB_CHAR
word = word.encode()
flag_middle, middle_iter = brute_force_block(encrypted_flag_blocks[1], word, client)
print(f"Flag middle block found after {middle_iter} iterations : {flag_middle}")
iterations += middle_iter

if flag_middle.endswith('}'): # the middle block is 16 bytes long
    print("Flag middle block ends with '}'")

    print(f"Final flag : {flag_first + flag_middle}")
    print("Total iterations :", iterations)
    
    client.close()
    print("Connection to server closed")
    
    exit(0)

# Step 2 - Get the last flag block
flag_length, iter_length = get_last_flag_block_length(encrypted_flag_blocks[2], client)
print(f"Flag last part length found after {iter_length} iterations : {flag_length}")
iterations += iter_length

word = SUB_CHAR * flag_length + '}'
word = pad(word.encode(), BLOCK_SIZE)
flag_last, last_iter = brute_force_block(encrypted_flag_blocks[2], word, client)
print(f"Flag last block found after {last_iter} iterations : {flag_last}")
iterations += last_iter

print(f"Final flag : {flag_first + flag_middle + flag_last}")
print("Total iterations :", iterations)


# Close the connection
client.close()
print("Connection to server closed")