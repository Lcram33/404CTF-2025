# ==== BEGIN CONTEXT HEADER ====
# The following file is a small server implementation to locally simulate the challenge following server :
# nc challenges.404ctf.fr 30169
#
# It is NOT part of the original challenge.
# ==== END CONTEXT HEADER ====



import socket
import subprocess
import threading
import signal
import sys

def handle_client(conn, addr):
    print(f"Connexion établie depuis {addr}")
    process = subprocess.Popen(["python3", "SaturnCipher.py"], stdin=conn, stdout=conn, stderr=conn)
    process.wait()
    conn.close()

def start_server(host, port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)
    print(f"Serveur en écoute sur {host}:{port}")

    def signal_handler(sig, frame):
        print("Fermeture du serveur...")
        server.close()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    while True:
        try:
            conn, addr = server.accept()
            client_thread = threading.Thread(target=handle_client, args=(conn, addr))
            client_thread.start()
        except socket.error as e:
            print(f"Erreur de socket : {e}")
            break

if __name__ == "__main__":
    HOST = "localhost"
    PORT = 30169
    start_server(HOST, PORT)
