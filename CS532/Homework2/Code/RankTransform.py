# Implements the Rank Transform on an image in 5x5 windows

import numpy as np
from tqdm import trange

def rank_transform(image):
    rank_t = np.zeros(image.shape)
    for r in trange(2,image.shape[0]-2, desc="Rank transform"):
        for c in range(2,image.shape[1]-2):
            # Gotta love numpy's syntax sugar.
            # This does an element-wise compare with the center of the window,
            # then since Python treats True as 1, and False as 0, the result is
            # as simple as summing the boolean values in the new array.
            rank_t[r, c] = (image[r-2:r+3,c-2:c+3] < image[r, c]).sum()
    return rank_t