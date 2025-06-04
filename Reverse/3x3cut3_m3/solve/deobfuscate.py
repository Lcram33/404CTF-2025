import base64

def decode_base64(encoded_str):
    """Decode a Base64 encoded string."""
    try:
        decoded_bytes = base64.b64decode(encoded_str)
        return decoded_bytes.decode('utf-8')
    except (base64.binascii.Error, UnicodeDecodeError) as e:
        print(f"Decoding error: {e}")
        return None

def deobfuscate_code(encoded_str):
    decoded = decode_base64(encoded_str.split('"')[1][::-1])
    if "SendKeys" in decoded: # Found by executing the script and getting error
        return decoded
    else:
        return deobfuscate_code(decoded)

def main():
    encoded = ""
    with open("3x3cut3_m3.ps1", "r") as f:
        encoded = f.read().strip()
    
    deobfuscated = deobfuscate_code(encoded)

    with open("dobf_3x3cut3_m3.ps1", "w") as f:
        f.write(deobfuscated)
    
    print("Deobfuscation complete. Output written to dobf_3x3cut3_m3.ps1")

if __name__ == "__main__":
    main()