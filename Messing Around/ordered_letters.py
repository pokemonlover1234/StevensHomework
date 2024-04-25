import numpy as np

leng = 1
letters = np.array([chr(ord("A") + i) for i in range(26)])
cur_arr = np.array([letters[0]])

print("")

sz = 0

with open("letters.txt", "w") as f:
    while True:
        try:
            i = -1
            f.write("".join(cur_arr))
            f.write("\n")
            while i > -leng - 1 and cur_arr[i] == letters[-1]:
                cur_arr[i] = letters[0]
                i -= 1
            if i == -leng - 1:
                leng += 1
                cur_arr = np.insert(cur_arr, 0, letters[0])
            else:
                cur_arr[i] = letters[np.where(letters == cur_arr[i])[0][0]+1]
            # sz += len(cur_arr)
            # print("".join(cur_arr) + f"; at {len(cur_arr)} letters; size = {sz} bytes", end="")
            # print("\x1b[1A\x1b[2K")
        except KeyboardInterrupt:
            break