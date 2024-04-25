ciphers = [
    "000d16251c07044b36171c0307280858291403500a2003450029001e5930070e52",
    "0d0d15713c49000a2c521d120f224f0125004d00163d100011380d0359330a0b4d",
    "151f00221a04064b2d1c0a571a2f021d6a050c145326054505231311102a084701",
    "0d091c71020c4308231c4f1a0f2d0a582c0003501c295624103e0008592a001001",
    "1d480d3e050c43052d521c031b220a163e550e111d6f04001328410e112d1c4701",
    "00000425551e0c1e2e164f150b661e0d2301085016221404003e00090a2d010001",
    "181d063a1c051a4b0d263f5707354f082f070b15103b1a1c523f04190b211b4701",
    "1001013f0149220930131d571d2716583e1d0802166f0104016c005a1a251b0449",
    "19091c3310491a0e365226570a2f0b163e551d110a6f171106290f0e102b014701",
    "030d45221d06160726521d120f2a03016a190403072a18450623413b1b360e1501",
    "1a090d71020c430a30174f13012f011f6a02081c1f6f010c06240e0f0d64070253"
]
# Turn cipher strings into bytestrings
cipherbytes = [bytes.fromhex(c) for c in ciphers]

# Define some helper functions

def byte_xor(ba1, ba2):
    return bytes([a ^ b for a, b in zip(ba1, ba2)])

cipherxors = {}

for i in range(len(cipherbytes)):
    for j in range(len(cipherbytes)):
        if i != j:
            cipherxors.update({(i, j): byte_xor(cipherbytes[i], cipherbytes[j])})

# From problem definition, we know that spaces are very common. 
# We also know that space xor alphabet characater = case switch
# Problem says punctuation might be present. 
# If there is a space, then one of 3 possibles in xors with other ciphers
# byte > 63 = case switch
# byte = 0: Another space
# byte > 0 and < 32: Another type of punctuation
# Punctuation is much less likely than spaces. So if a given cipher xor all other ciphers gives 
# mostly bytes == 0 or > 63, can safely guess that ciphertext positions is a space
# and guess any <32 and >0 
# From this, for each ciphertext at each position, for all other ciphertexts, guess space positions using 
# criteria above
# we can also assume the character is NOT the punctuation that is in byte > 63

spaceguesses = [[] for _ in range(len(cipherbytes))]

for ci in range(33):
    for i in range(len(cipherbytes)):
        charcount = 0
        for j in range(len(cipherbytes)):
            if i == j:
                continue
            char = cipherxors[(i,j)][ci]
            if char == 0 or (char > 64 and char < 91) or (char > 96 and char < 123):
                charcount += 1
        if charcount > 8:
            spaceguesses[i].append(ci)

print(spaceguesses)

# Make key position guesses based on guessed spaced positions. If multiple possible keys then guess those positions in at least one cipher have punctuation.
# ki = byte of k at position i where space is guessed
# cj = ciphertext where guessed space is present
# cji = ith character in cj
# pj = plaintext of cj
# pji = ith character of pj
# 0x20 = hex of space character
# cji = pji xor ki (which is guessed to be) cji = 0x20 xor ki
# therefore
# ki ~ 0x20 xor cji
keyposguesses = [set() for _ in range(33)]

for i in range(len(cipherbytes)):
    for sp in spaceguesses[i]:
        kguess = 0x20 ^ cipherbytes[i][sp]
        keyposguesses[sp].add(kguess)

print(keyposguesses)

# Test if AT MOST one guess in key guesses. 
allmostone = True
for guesses in keyposguesses:
    if len(guesses) > 1:
        allmostone = False
        break

# If it IS all one, print so
# and use that assumption later to get most of the key guess
# Then construct known guess key with 0s elsewhere. 
# Then print mostly decrypted ciphers to check assumptions (this is visual, not based on code)
# If mostly decrypted text makes sense, make logical guesses on missing characters and manually determine missing bytes of key
key = []
missing = []
if allmostone:
    print("All positions with guesses have at most one guessed key byte")
    print("Partial decryption obtained:")
    key = bytearray(33)
    missing = []
    for i, guess in enumerate(keyposguesses):
        if len(guess) == 1:
            key[i] = guess.pop()
        else:
            missing.append(i + 1)
    print(f"Known Partial Key: {key}")
    for i in range(len(cipherbytes)):
        print(f"{byte_xor(cipherbytes[i], key)}")
    print(f"Missing key bytes at characters {missing}")

# Code-based cryptanalysis result:
        
# All positions with guesses have at most one guessed key byte
# Partial decryption obtained:
# Known Partial Key: bytearray(b'\x00heQuick\x00row\x00FoxJumpsOverLazyD\x00g!')
# b'\x00esting 6est\x07ng can you read t\x07is'
# b'\rep I ca, re\x0fd you perfectly w\nll'
# b'\x15wesome -ne \x1aime pad is workin\x08  '
# b'\ray we c#n m\x0fke fun of Abrar n\x00w '
# b'\x1d hope n- st\x1bdent can read thi\x1c  '
# b'\x00hat wou.d b\x0b quite embarrassi\x01g '
# b'\x18uckily \rTP \x07s perfectly secre\x1b  '
# b'\x10idnt Ab0ar \x1day there was a ca\x1bch'
# b'\x19aybe ye6 I \nidnt pay attentio\x01  '
# b'\x03e shoul& re\x0flly listen to Abr\x0er '
# b'\x1aah we a0e d\x01ing well without \x07er'
# Missing key bytes at characters [1, 9, 13, 31]

# Some characters that were decrypted don't make sense. Assume later that these were due to punctuation being guessed as spaces. 
# For now, guess obviously missing key bytes (printed by program, as these are the bytes that had no guess).

# For character 1:  
# Take third partial decryption. First word is "\x15wesome". Make guess that \x15 should be capital A.
# Capital A is hex 0x41. Cipher is 0x15. Key byte is 0x41 xor 0x15 = 0x54
key[0] = 0x54
missing.remove(1)
for i in range(len(cipherbytes)):
    print(f"{byte_xor(cipherbytes[i], key)}")
print(f"Missing key bytes at characters {missing}")

# New decrypt progress. 
# b'Testing 6est\x07ng can you read t\x07is'
# b'Yep I ca, re\x0fd you perfectly w\nll'
# b'Awesome -ne \x1aime pad is workin\x08  '
# b'Yay we c#n m\x0fke fun of Abrar n\x00w '
# b'I hope n- st\x1bdent can read thi\x1c  '
# b'That wou.d b\x0b quite embarrassi\x01g '
# b'Luckily \rTP \x07s perfectly secre\x1b  '
# b'Didnt Ab0ar \x1day there was a ca\x1bch'
# b'Maybe ye6 I \nidnt pay attentio\x01  '
# b'We shoul& re\x0flly listen to Abr\x0er '
# b'Nah we a0e d\x01ing well without \x07er

# For character 9: 
# Take second partial decryption. 3rd word is "ca,". Make guess that , should be lowercase n. 
# Lowervase n is hex 0x6E. Cipher is 0x2C. Key byte is 0x6E xor 0x2C = 0x42
key[8] = 0x42
for i in range(len(cipherbytes)):
    print(f"{byte_xor(cipherbytes[i], key)}")
missing.remove(9)
print(f"Missing key bytes at characters {missing}")

# b'Testing test\x07ng can you read t\x07is'
# b'Yep I can re\x0fd you perfectly w\nll'
# b'Awesome one \x1aime pad is workin\x08  '
# b'Yay we can m\x0fke fun of Abrar n\x00w '
# b'I hope no st\x1bdent can read thi\x1c  '
# b'That would b\x0b quite embarrassi\x01g '
# b'Luckily OTP \x07s perfectly secre\x1b  '
# b'Didnt Abrar \x1day there was a ca\x1bch'
# b'Maybe yet I \nidnt pay attentio\x01  '
# b'We should re\x0flly listen to Abr\x0er '
# b'Nah we are d\x01ing well without \x07er'

# Take character 13
# Guessing lowercase i from first ciphertext. 
# Key = 0x69 xor 0x07 = 0x6e
key[12] = 0x6e
for i in range(len(cipherbytes)):
    print(f"{byte_xor(cipherbytes[i], key)}")
missing.remove(13)
print(f"Missing key bytes at characters {missing}")

# b'Testing testing can you read t\x07is'
# b'Yep I can read you perfectly w\nll'
# b'Awesome one time pad is workin\x08  '
# b'Yay we can make fun of Abrar n\x00w '
# b'I hope no student can read thi\x1c  '
# b'That would be quite embarrassi\x01g '
# b'Luckily OTP is perfectly secre\x1b  '
# b'Didnt Abrar say there was a ca\x1bch'
# b'Maybe yet I didnt pay attentio\x01  '
# b'We should really listen to Abr\x0er '
# b'Nah we are doing well without \x07er'

# Finally, deducing character 31
# Guessing h from message 1
# key = 0x68 xor 0x07 = 0x6f
key[30] = 0x6f
for i in range(len(cipherbytes)):
    print(f"{byte_xor(cipherbytes[i], key)}")
missing.remove(31)
print(f"Missing key bytes at characters {missing}")

print(key)

# Final decryption
# b'Testing testing can you read this'
# b'Yep I can read you perfectly well'
# b'Awesome one time pad is working  '
# b'Yay we can make fun of Abrar now '
# b'I hope no student can read this  '
# b'That would be quite embarrassing '
# b'Luckily OTP is perfectly secret  '
# b'Didnt Abrar say there was a catch'
# b'Maybe yet I didnt pay attention  '
# b'We should really listen to Abrar '
# b'Nah we are doing well without her'

# Key is 