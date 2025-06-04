# ==== BEGIN CONTEXT HEADER ====
# The following file contains a solution to the challenge.
# SPOLIER ALERT : Stop here if you want to solve the challenge yourself.
# ==== END CONTEXT HEADER ====


FLAG = "828x6Yvx2sOnzMM4nI2sQ"



charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789{}-!"
n = len(charset)

def encrypt(message):
    encrypted = []
    for char in message:
        if char in charset:
            x = charset.index(char)
            y = pow(2, x, n+1)
            if y == n: # This is a fix to allow encoding of every character (we got "IndexError: string index out of range")
                y = 0
            encrypted.append(charset[y])
    return ''.join(encrypted)

def decrypt(message):
    charset_rev = encrypt(charset) # This a monoalphabetic substitution cipher ! We just need to map the characters

    decrypted = []
    for char in message:
        if char in charset_rev:
            x = charset_rev.index(char)
            decrypted.append(charset[x])
    return ''.join(decrypted)

print("ENCRYPTED FLAG : ", decrypt(FLAG)) 


# ENCRYPTED FLAG : 828x6Yvx2sOnzMM4nI2sQ