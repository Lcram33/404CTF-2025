import subprocess


pwd_len = 20
password = pwd_len * [' ']

pos = [5, 12, 0, 18, 7, 3, 9, 16, 14, 1, 19, 6, 15, 8, 4, 11, 10, 17, 2, 13]
val = [90, 111, 102, 49, 37, 77, 121, 118, 110, 97, 120, 97, 77, 51, 80, 75, 78, 37, 86, 64]

for p, v in zip(pos, val):
    password[p] = chr(v)

password = ''.join(password)
subprocess.run(['./chall2', password], check=True)