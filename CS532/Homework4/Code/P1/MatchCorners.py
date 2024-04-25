# Match corners, using SAD on rank transformed images
import numpy as np


# r1, r2 = rank transformed images
# c1, c2 = list of corners with depth
def match_corners(r1, c1, r2, c2):
    output = []
    for x1, y1, x31, y31, z31 in c1:
        x1 = int(x1)
        y1 = int(y1)
        min_dist = None
        min_corner = None
        for x2, y2, x32, y32, z32 in c2:
            x2 = int(x2)
            y2 = int(y2)
            dist = np.sum(np.abs(r1[y1 - 5: y1 + 6, x1 - 5: x1 + 6] - \
                                 r2[y2 - 5: y2 + 6, x2 - 5: x2 + 6]))
            if min_dist is None or dist < min_dist:
                min_dist = dist
                min_corner = (x2, y2, x32, y32, z32)
        output.append([(x1, y1, x31, y31, z31), min_corner, min_dist])
    return output