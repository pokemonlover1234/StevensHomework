# Non-maximum suppression
import numpy as np
from tqdm import trange


def nms(image):
    output = np.zeros((image.shape[0] - 2, image.shape[1] - 2))
    for y in trange(1, image.shape[0] - 1, desc="Non-maximum suppression", leave=False):
        for x in range(1, image.shape[1] - 1):
            pixel = image[y, x]
            output[y - 1, x - 1] = pixel if pixel == np.max(image[y - 1: y + 2, x - 1: x + 2]) else 0
    return output
