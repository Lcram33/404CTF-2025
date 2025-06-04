# ==== BEGIN CONTEXT HEADER ====
# The following file contains a solution to the challenge.
# SPOLIER ALERT : Stop here if you want to solve the challenge yourself.
# ==== END CONTEXT HEADER ====


import socket
import json
import zlib
import time


# Constants
SERVER_ADDR = "localhost" # TEST
# SERVER_ADDR = "challenges.404ctf.fr" # PROD
SERVER_PORT = 31207

DEBUG = False
MSG_SIZE = 1024


def decode_watermark(compressed_watermark, size):
	watermark_json = zlib.decompress(bytes.fromhex(compressed_watermark)).decode()
	watermark = json.loads(watermark_json)
	decoded_bits = list()

	bit_blocks = [watermark[i:i + size] for i in range(0, len(watermark), size)]
	
	for bit_block in bit_blocks:
		nb_1 = sum(bit_block)
		nb_0 = size - nb_1
		bit = int(nb_0 != nb_1)
		decoded_bits.append(bit)
	
	return ''.join(map(str, decoded_bits))


# Main program
def client():
    final_msg = ""
    while "Congratz" not in final_msg:
        if final_msg != "":
            timeout = 1 if SERVER_ADDR == "localhost" else 5
            print(f"Waiting {timeout}s before reconnecting.")
            time.sleep(timeout)
        
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((SERVER_ADDR, SERVER_PORT))

        # Step 1 - Get watermarked data
        info_msg = client.recv(len("Welcome to Spacemark ! Can you guess my secret data used to generate the watermark ?"))
        if not info_msg:
            return
        if DEBUG:
            print("Received:" + info_msg.decode())
            print()
        
        msg_lst = list()
        i = 0
        msg_part = ''
        while ">>>" not in msg_part:
            time.sleep(0.2)  # Wait for the server to be ready
            msg_part = client.recv(10 * MSG_SIZE).decode()
            msg_lst.append(msg_part)
            i += 1
            if not msg_part:
                return
            if DEBUG:
                print(f"Received part {i} (len = {len(msg_part)}): {msg_part[:20]}[...]{msg_part[-30:]}")
                print()
        
        msg = ''.join(msg_lst).strip()

        chall = msg.split('\n')[0]
        size = 2**12
        solved_watermark = decode_watermark(chall, size)

        answer = solved_watermark
        answer += '\n'
        client.send(answer.encode())
        if DEBUG: print(f"Sent: {answer}")

        # Step 2 - Get the flag
        final_msg = client.recv(MSG_SIZE).decode()
        if not final_msg:
            return
        print("Received:" + final_msg)

        if "Nope" in final_msg:
            real_watermark = final_msg.split("\n")[1].strip()
            i = 0
            for x, y in zip(real_watermark, solved_watermark):
                if x != y:
                    print(f"Mismatch at index {i}: expected {x}, got {y}")
                i += 1

        # Close the connection
        client.close()
        print("Connection to server closed")

    print("Flag received ! End of program.")

if __name__ == "__main__":
    client()