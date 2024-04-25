# Compute the rank transform
import numpy as np


def rank_transform(image):
    output = np.zeros((image.shape[0] - 4, image.shape[1] - 4))
    for y in range(2, image.shape[0] - 2):
        for x in range(2, image.shape[1] - 2):
            output[y - 2, x - 2] = np.sum(image[y - 2: y + 3, x - 2: x + 3] < image[y, x])
    return output