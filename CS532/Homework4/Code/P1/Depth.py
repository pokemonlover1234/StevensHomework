# Depth calculation
import numpy as np
from tqdm import trange

S = 5000

K = np.matrix([
    [525.0, 0, 319.5],
    [0, 525.0, 239.5],
    [0, 0, 1]
])

# Converts corners to 5-tuples
# [2dx, 2dy, 3dx, 3dy, 3dz]
# Useful to have both 2d and 3d information available in later steps
# offset included because changing image sizes puts reference frame
# out of original. Equal to (orig size - new size) / 2
# offset used only in context of depth estimation
def corners_to_depths(corners, depthmap, offset): 
    pixels = np.argwhere(corners)
    pts = np.zeros((100,5), dtype=np.float64)
    i = 0
    for y, x in pixels:
        depth = depthmap[y, x]
        if depth == 0:
            continue
        pt = 1 / S * depth * np.matmul(np.linalg.inv(K),np.matrix([x + offset, y + offset, 1]).T)
        pts[i] = [int(x), int(y), pt.T.flat[0], pt.T.flat[1], pt.T.flat[2]]
        i += 1
    return pts[:i]

def to_depths(image, depthmap, offset): 
    pts = np.zeros((image.shape[0] * image.shape[1],5), dtype=np.float64)
    i = 0
    for y in trange(image.shape[0], leave=False, desc="Determining all depths"):
        for x in range(image.shape[1]):
            depth = depthmap[y, x]
            if depth == 0:
                continue
            pt = 1 / S * depth * np.matmul(np.linalg.inv(K),np.matrix([x + offset, y + offset, 1]).T)
            pts[i] = [int(x), int(y), pt.T.flat[0], pt.T.flat[1], pt.T.flat[2]]
            i += 1
    return pts[:i]
