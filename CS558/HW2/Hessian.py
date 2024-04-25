import Filter
import numpy as np
from tqdm import trange 

def threshold(det):
    return np.array([[pt if pt > 60 else 0 for pt in row] for row in det])


def get_responses(image):
    # "/8"s act as normalizations.
    xx = Filter.apply_filter(Filter.apply_filter(image, Filter.SOBEL_HORIZ/8), Filter.SOBEL_HORIZ/8)
    xy = Filter.apply_filter(Filter.apply_filter(image, Filter.SOBEL_HORIZ/8), Filter.SOBEL_VERT/8)
    yy = Filter.apply_filter(Filter.apply_filter(image, Filter.SOBEL_VERT/8), Filter.SOBEL_VERT/8)
    det = np.multiply(xx,yy) - np.multiply(xy,xy)
    det = threshold(det)
    det = Filter.nms(det)
    return det

def to_point_array(hessian):
    #Convert detected points into array of point tuples.
    points = []
    for r in range(np.shape(hessian)[0]):
        for c in range(np.shape(hessian)[1]):
            if hessian[r,c] != 0:
                points.append((c,r))
    return np.array(points)