# ==== BEGIN CONTEXT HEADER ====
# The following file contains all the elements to solve the challenge, but does not solve it.
# SPOLIER ALERT : Stop here if you want to solve the challenge yourself.
# ==== END CONTEXT HEADER ====


from Crypto.Random.random import randint
import json
import os
import zlib

from secret import FLAG


class LCG:
	def __init__(self, a, b, m, seed):
		self.state = seed
		self.a = a
		self.b = b
		self.m = m

	def next(self):
		s = self.state
		self.state = (self.a * self.state + self.b) % self.m

		return self.state

def generate_watermark(watermarking_bits, size):
	m = 2 ** 64
	b = 2 * randint(2, m - 1) + 1
	a = 2 * randint(2, m - 1) + 1
	# they stay constant throughout the generation process, great

	while a % 8 != 5: # Ensure a is of the form 8k + 5
		a = 2 * randint(2, m - 1) + 1

	stream = []
	for i, bit in enumerate(watermarking_bits):
		seed = randint(2, m - 1) # will need to be reversed for each bit, ez
		l = LCG(a, b, m + bit, seed)
		for _ in range(size):
			stream.append((l.next() >> 11) & 1)

	return stream


# My functions

def decode_watermark(compressed_watermark, size):
	watermark_json = zlib.decompress(bytes.fromhex(compressed_watermark)).decode()
	watermark = json.loads(watermark_json)
	decoded_bits = list()

	bit_blocks = [watermark[i:i + size] for i in range(0, len(watermark), size)]
	
	for i, bit_block in enumerate(bit_blocks):
		nb_1 = sum(bit_block)
		nb_0 = size - nb_1
		bit = int(nb_0 != nb_1) # observed for a few executions ! Does not work all the time but fairly often.
		decoded_bits.append(bit) # enough to flag !
	
	decoded_bytes = [int("".join(map(str, decoded_bits[i:i+8])), 2).to_bytes(1, "big") for i in range(0, len(decoded_bits), 8)]
	
	return b"".join(decoded_bytes)

def gen_chall():
	size = 2**12
	random_watermark = os.urandom(16)
	print(f"Random watermark bytes: {random_watermark.hex()}")  # Debugging line
	random_watermark = "".join([format(b, "08b") for b in random_watermark]) # Convert bytes to bits
	random_watermark_bits = list(map(int, list(random_watermark))) # Convert string of bits to list of integers
	watermark = json.dumps(
		generate_watermark(random_watermark_bits, size)
	)

	return zlib.compress(watermark.encode()).hex()

def main():
	size = 2**12
	chall = gen_chall()
	decoded = decode_watermark(chall, size)

	print(decoded.hex())

if __name__ == "__main__":
	main()