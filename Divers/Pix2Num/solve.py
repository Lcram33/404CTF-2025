# ==== BEGIN CONTEXT HEADER ====
# The following file contains a solution to the challenge.
# SPOLIER ALERT : Stop here if you want to solve the challenge yourself.
# ==== END CONTEXT HEADER ====


import sys
from PIL import Image
import random

sys.set_int_max_str_digits(100000)

WIDTH = 400
HEIGHT = 200

def convert_image_to_number(image_path):
    image = Image.open(image_path).convert('L')
    pixels = list(image.getdata())
    binary_representation = ''.join(['1' if pixel == 255 else '0' for pixel in pixels])
    return int(binary_representation,2)

def convert_number_to_image(number, output_path):
    binary_str = bin(number)[2:]
    binary_lst = list(binary_str)

    pixels = [255 if bit == '1' else 0 for bit in binary_lst]

    image = Image.new('L', (WIDTH, HEIGHT))
    image.putdata(pixels)
    image.save(output_path)

def encrypt_number(number,key):
    new_number = 0
    shift = 0
    while number:
        block = (number & 0xFFFF_FFFF_FFFF_FFFF) ^ key # take the 64 least significant bits
        new_number |= (block << shift) # populate new number with the encrypted block
        number >>= 64 # shift the number to the right by 64 bits, so we can process the next block
        shift += 64 # move to the next block
    return new_number

def decrypt_number(number, key):
    return encrypt_number(number, key)

def find_key(number):
    # Let's suppose the last pixels are white, so the last bits are 0, therefore the XOR operation gives the key !
    # (we initially tried the first pixels with no luck, so we tried the last ones after)
    binary_str = bin(number)[2:]
    binary_lst = list(binary_str)

    key = int(''.join(binary_lst[-64:]),2)

    return key


data = None
with open('number.txt', 'r') as file:
    data = file.read().strip()
number = int(data)

key = find_key(number)

new_number = decrypt_number(number, key)

convert_number_to_image(new_number, 'output.png')