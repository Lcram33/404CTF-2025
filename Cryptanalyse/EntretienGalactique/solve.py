# ==== BEGIN CONTEXT HEADER ====
# The following file contains a solution to the challenge.
# SPOLIER ALERT : Stop here if you want to solve the challenge yourself.
# ==== END CONTEXT HEADER ====


import numpy as np
import socket
from sympy import symbols, Eq, solve


def solve_cubic(a, b, c):
    # Définition des variables
    x, y, z = symbols('x y z')
    
    # Définition des équations
    eq1 = Eq(x + y + z, a)
    eq2 = Eq(x**2 + y**2 + z**2, b)
    eq3 = Eq(x**3 + y**3 + z**3, c)

    # Résolution symbolique
    solutions = solve((eq1, eq2, eq3), (x, y, z))

    sol = sorted(solutions[0])
    
    return sol

def solve_system(challenge_message):
    lines = challenge_message.splitlines()
    a = int(lines[0].split(' = ')[1])
    b = int(lines[1].split(' = ')[1])
    c = int(lines[2].split(' = ')[1])
    
    x, y, z = solve_cubic(a, b, c)

    return f"{int(round(x))},{int(round(y))},{int(round(z))}"

    

def run_client(server_ip, server_port):
    DEBUG = True
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((server_ip, server_port))

    while True:
        # Init - Prenom
        msg = client.recv(1024).decode()
        if not msg:
            break
        print('Received:' + msg)

        answer = "Jhon"
        answer += '\n'
        client.send(answer.encode("utf-8")[:1024])
        print(f"Sent: {answer}")

        # Challenge
        for _ in range(100):
            msg = client.recv(1024).decode()
            if not msg:
                break
            if DEBUG: print('Received:' + msg)

            answer = solve_system(msg)
            answer += '\n'
            client.send(answer.encode("utf-8")[:1024])
            if DEBUG: print(f"Sent: {answer}")

        msg = client.recv(1024).decode()
        if not msg:
            break
        print('Received:' + msg)

    client.close()
    print("Connection to server closed")


# run_client("localhost", 30069)
run_client("challenges.404ctf.fr", 30069)