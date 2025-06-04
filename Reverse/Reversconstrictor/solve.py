def decrypt_password(ciphertext):
    def encrypt_key(key):
        for _ in range(100):
            key <<= 1
            key ^= CONST
            key >>= 1
            key &= MASK
            key -= OFFSET
            key ^= CONST
            key <<= 1
            key += 4324354
            key >>= 1
        key = abs(key)
        encrypted_bytes = key.to_bytes((key.bit_length() + 7) // 8, byteorder='big')
        return encrypted_bytes

    CONST = 28822426245224264980979321341345830828356797782055329828562090481380116178932605047916536097759912367507574811007140506795012665313071649493970094581868771201400995139374360577815608383329090103210656811239441222567030843263175788045939510447941542030750571932256144094323129497438168350642218592361235189388565721332503735143045072480576796605508643464856724395849208355789353984327745285879034330837484467961665782705864897713128496005106869640456653659559683849265346017315593794571762231394086134713064707220190583043994656101899455622598958597972721263137718293457676368185324168958757297967087684
    MASK = 109051226663159329753852712655361641732299866997884252194334358336942491585415479875295813282055589726130083576518139892456534344478282750316593419244506314188673419372046405908627553201165095804542555714314672295089748281211620003277814236498206175511101163526217782040005646393337007890354251307329101818031816904956050245603083420859836404091717206011901780489732016582515541865280619889684277395118340072030441380240101696073919110415984233261149866579378832210321108153068228794726382510988474475602148132965289631295957683363624794221017463029077341994983080187012597951461555452400067297865364263
    OFFSET = 30192244264443276570339417266820821425000308120852003855173657187210512774975257998930431381307567916542287355804911140923844613245045835307895499468937998079600051550088167870781968330783540846793847843565906160661919016260958589152016311435717470936180510788226717267994601294202007594965057260235235670775632982187962998589201876115127904069810375748935472032501147620317590198256980636488859805187975959355302150868894406858968080766062052395340075809777559133433991365763567236747759028423915038949095093046477455353960143902941004723715753803085977215629377804159634990715729987578541999707000127

    def decode_password(encoded_bytes):
        x_list = [110, -34, -230]
        password = []
        for i in range(0, len(encoded_bytes), 6):
            y1 = encoded_bytes[i] * 256 + encoded_bytes[i+1]
            y2 = encoded_bytes[i+2] * 256 + encoded_bytes[i+3]
            y3 = encoded_bytes[i+4] * 256 + encoded_bytes[i+5]

            y_values = [y1, y2, y3]

            # Brute force all possible (b, c) pairs
            found = False
            for b in range(11, 256):
                for c in range(0, 11):
                    d = b + c
                    e = b * c
                    try:
                        r_check = []
                        for x in x_list:
                            y = x**2 - d * x + e
                            if y <= 0 or y >= 65536 or y in r_check:
                                break
                            r_check.append(y)
                        else:
                            if sorted(r_check) == sorted(y_values):
                                password.append((b - 11) * 11 + c)
                                found = True
                                break
                    except:
                        continue
                if found:
                    break
            if not found:
                raise ValueError(f"Unable to decode segment: {y_values}")
        return bytes(password)

    # Recompute the encryption key bytes
    key_input = 95976165392371447739857811656653673143121600389071811768266881989291151289664268756563021450590842202471722647397942271310305361018612287905884505900356120817470
    key_bytes = encrypt_key(key_input)

    # XOR to retrieve encoded password bytes
    encoded_bytes = bytes([a ^ b for a, b in zip(ciphertext, key_bytes)])

    # Decode to original password
    return decode_password(encoded_bytes)

ciphertext = b'\xe9J\x1aB\xe2\xc5\xf3S\'\xd6>\n$\x94\x1a\x07\'F\xc6\xa1\x07\xb7\xcc\xec\xe1\x84\xec\xac\xe4\xd64\x8f\xc3\x12\x04\x16$n\x15\xec\xe1\xaee5\xc7\xecOX"\x98EO\x1f2\xb4\x15\xc4\xed\xf4\xcd$\xd3\xd3u\xc2\xf8\xc6\xae\x06\x08\xcd\xff\xe0(\xe9\xb0\xe7\xde6\x90\xcc\xfd\x02}%\x1a\x1a\xc9#\x10\xc2\x86\x06\x08\xcd\xfe&\xb8K\x0f)\x9a\xb6\xb9\x02\x17\xa0\xd8\xe4]\x98\xf5*\x154<\x06\x875\xbd\x05@\xe6\x88\xe3&6%\xcc\x18\x06\\%\xa4\x1a7!\xfe\xc3\xae\x06\x08\xcd\xff\xe2\x18\xe2x\xe0\x927x\r\xfa\xa6\xbd\xe67\x97\xf7\xe5)f\x94\xc8\xbdv\r\xef\x12\x1bZ\xe8e\xf3S\'\xd6>\n"8\x1be\x9c\xdf\xe8\x9b\x06\xb7\x0b3V\x1f\xedN\x87\xbbI!C>8z%\xc0\xeaM\xb5\xd1p\xd1\x0f|A\xd7B\x03\xc54\xd5T\xb9\xfd\x88;\xbf\x10\x81L\x90L\x0b\xff\xed\xe1\xe5dQ\xc4\x17\xd5\xafUl\xec'

original_password = decrypt_password(ciphertext)

print(original_password.decode('ascii'))