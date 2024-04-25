from hashlib import sha256

key = bytearray(b'TheQuickBrownFoxJumpsOverLazyDog!')
day = 4
while day != 25:
    day += 1
    key = bytearray(sha256(key).digest())
    key.append(0x21)
    print(f"Key on October {day}: {key.hex()}")
