# ==== BEGIN CONTEXT HEADER ====
# The following file was NOT MODIFIED and is the original challenge file.
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

		return s


def generate_watermark(watermarking_bits, size):
	m = 2 ** 64
	b = 2 * randint(2, m - 1) + 1
	a = 2 * randint(2, m - 1) + 1

	while a % 8 != 5:
		a = 2 * randint(2, m - 1) + 1

	stream = []
	for bit in watermarking_bits:
		seed = randint(2, m - 1)
		l = LCG(a, b, m + bit, seed)
		for _ in range(size):
			stream.append((l.next() >> 11) & 1)

	return stream



print("Welcome to Spacemark ! Can you guess my secret data used to generate the watermark ?")
size = 2**12

random_watermark = os.urandom(16)

random_watermark = "".join([format(b, "08b") for b in random_watermark])
random_watermark_bits = list(map(int, list(random_watermark)))

watermark = json.dumps(
	generate_watermark(random_watermark_bits, size)
)

print(zlib.compress(watermark.encode()).hex())

print("So, what's the watermark ?")

guess = input(">>>")

if guess == random_watermark:
	print(f"Congratz ! {FLAG}")
else:
	print("Nope...")
	print(random_watermark)

exit()