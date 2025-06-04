# ==== BEGIN CONTEXT HEADER ====
# The following file was NOT MODIFIED and is the original challenge file.
# ==== END CONTEXT HEADER ====


from flag import FLAG



charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789{}-!"
n = len(charset)

def encrypt(message):
    encrypted = []
    for char in message:
        if char in charset:
            x = charset.index(char)
            y = pow(2, x, n+1)
            encrypted.append(charset[y])
    return ''.join(encrypted)

print("ENCRYPTED FLAG : ", encrypt(FLAG)) 


# ENCRYPTED FLAG : 828x6Yvx2sOnzMM4nI2sQ 

