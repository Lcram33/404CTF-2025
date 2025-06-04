# ==== BEGIN CONTEXT HEADER ====
# The following file contains a solution to the challenge.
# SPOLIER ALERT : Stop here if you want to solve the challenge yourself.
# ==== END CONTEXT HEADER ====


import os
import socket
import subprocess


# Constants
SERVER_ADDR = "localhost" # TEST
# SERVER_ADDR = "challenges.404ctf.fr" # PROD
SERVER_PORT = 32460

DEBUG = False
MSG_SIZE = 1024


# Main program

def solve():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((SERVER_ADDR, SERVER_PORT))

    if not DEBUG:
        print("Solving, this can take up to 10-15 seconds.")

    # Init - Printing the banner
    info_msg = client.recv(MSG_SIZE)
    if not info_msg:
        return
    if DEBUG: print("Received:" + info_msg.decode())

    info_msg = client.recv(MSG_SIZE)
    if not info_msg:
        return
    if DEBUG: print("Received:" + info_msg.decode())

    if SERVER_ADDR == "localhost": # yup, needed in local...
        info_msg = client.recv(MSG_SIZE)
        if not info_msg:
            return
        if DEBUG: print("Received:" + info_msg.decode())

    # Step 1 - Enter security level
    answer = "277182" # see solution.py
    answer += '\n'
    client.send(answer.encode("utf-8")[:MSG_SIZE])
    if DEBUG: print(f"Sent: {answer}")

    info_msg = client.recv(MSG_SIZE)
    if not info_msg:
        return
    if DEBUG: print("Received:" + info_msg.decode())


    # Step 2 - Get the zero block ciphertext
    answer = "1"
    answer += '\n'
    client.send(answer.encode("utf-8")[:MSG_SIZE])
    if DEBUG: print(f"Sent: {answer}")

    info_msg = client.recv(MSG_SIZE)
    if not info_msg:
        return
    if DEBUG: print("Received:" + info_msg.decode())

    answer = "00" * 16
    answer += '\n'
    client.send(answer.encode("utf-8")[:MSG_SIZE])
    if DEBUG: print(f"Sent: {answer}")

    msg = client.recv(MSG_SIZE).decode()
    if not msg:
        return
    if DEBUG: print('Received:' + msg)

    encrypted_zero = msg.split(':')[1].split('\n')[0].strip()


    # Step 3 - Get the ciphertext to reverse
    answer = "2"
    answer += '\n'
    client.send(answer.encode("utf-8")[:MSG_SIZE])
    if DEBUG: print(f"Sent: {answer}")

    msg = client.recv(MSG_SIZE).decode()
    if not msg:
        return
    if DEBUG: print('Received:' + msg)

    ciphertext_to_crack = msg.split('>>>')[1].split('\n')[0].strip()


    # Step 4 - Crack the ciphertext and send the plaintext

    # call sage program from here
    process = subprocess.Popen(' '.join(["sage", "break.sage", encrypted_zero, ciphertext_to_crack]), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, text=True)
    output, error = process.communicate()
    guess = output.strip()

    answer = guess
    answer += '\n'
    client.send(answer.encode("utf-8")[:MSG_SIZE])
    if DEBUG: print(f"Sent: {answer}")

    client.recv(MSG_SIZE) # buggy banner
    client.recv(1014) # buggy banner

    # Step 5 - Get the flag :)
    msg = client.recv(MSG_SIZE).decode()
    if not msg:
        return
    print('Received:' + msg)


    # Close the connection
    client.close()
    print("Connection to server closed")

if __name__ == "__main__":
    solve()