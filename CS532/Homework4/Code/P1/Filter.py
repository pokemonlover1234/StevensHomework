import numpy as np
from tqdm import trange

# Define filters used

Ix = np.matrix([
    [-1, 0, 1],
    [-1, 0, 1],
    [-1, 0, 1]
])

Iy = Ix.T

# Used to reduce size by ignoring outer pixels

gaussian = 1 / 273 * np.matrix([
    [1, 4, 7, 4, 1],
    [4, 16, 26, 16, 4],
    [7, 26, 41, 26, 7],
    [4, 16, 26, 16, 4],
    [1, 4, 7, 4, 1]
])

# Define filter function

def filter_im(input, filter):
    offset = int((filter.shape[0] - 1) / 2)
    output = np.zeros((input.shape[0] - 2 * offset, input.shape[1] - 2 * offset))
    for y in trange(offset, input.shape[0] - offset, desc="Filtering", leave=False):
        for x in range(offset, input.shape[1] - offset):
            output[y - offset, x - offset] = np.sum(np.multiply(input[y - offset: y + offset+1, x - offset: x + offset + 1], filter))
    return output

# crop image to size of other. 
# Difference must be even
def crop_to(image, other):
    s1 = other.shape[0]
    s2 = image.shape[0]
    diff = s2 - s1
    if diff < 0 or diff % 2 == 1:
        print("Other image not smaller or difference not even.")
        return
    output = image.copy()
    diff = int(diff / 2)
    output = output[diff: -diff, diff: -diff]
    return output