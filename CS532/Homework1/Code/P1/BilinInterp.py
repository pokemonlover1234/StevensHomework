import numpy as np
from Image import get_image, save_image
from tqdm import trange
import math


# Converts a point in homography form (x, y, w)^T to (x, y) form.
def homog_to_pt(homog_pt):
    return np.array((homog_pt.T/homog_pt.T[0, 2])[0, 0:2].flat)


# Inverse warping is utilized.
def bilin_interp(imagepath, H, outputpath):
    oldimage = get_image(imagepath).astype(np.float64)
    bounds = oldimage.shape
    newimage = np.zeros((940, 500, 3))
    # Inverse of H used for reverse warping.
    iH = np.linalg.inv(H)
    for r in trange(940):
        for c in range(500):
            x, y = homog_to_pt(np.matmul(iH, np.matrix((c, r, 1)).T))
            # Since the values used in pixel calculations here start at 1
            # a negative 1 offset is necessary for array accesses.
            x -= 1
            y -= 1
            if x < 0 or x >= bounds[1] - 1 or y < 0 or y >= bounds[0] - 1:
                newimage[r, c] = [0, 0, 0]
            else:
                i = math.floor(x)
                j = math.floor(y)
                a = x - i
                b = y - j
                newimage[r, c] = (1 - a) * (1 - b) * oldimage[j, i] + \
                    a * (1 - b) * oldimage[j, i + 1] + \
                    a * b * oldimage[j + 1, i + 1] + \
                    (1 - a) * b * oldimage[j + 1, i]
    save_image(newimage.astype(np.uint8), outputpath)
