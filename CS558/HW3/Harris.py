import numpy as np
import Filter
import Gaussian
from tqdm import trange,tqdm

def responses(image):
    padded = Filter.pad_image(3, image)
    gaussian = Gaussian.gaussian_filter(1)
    bounds = np.shape(image)
    partial_x = Filter.apply_filter(padded, Filter.SOBEL_HORIZ * 1/8)
    partial_y = Filter.apply_filter(padded, Filter.SOBEL_VERT * 1/8)
    xx = np.multiply(partial_x,partial_x)
    xy = np.multiply(partial_x,partial_y)
    yy = np.multiply(partial_y,partial_y)
    M = np.zeros(bounds)
    for r in trange(bounds[0], desc = 'Calculating Harris'):
        for c in range(bounds[1]):
            tl = np.sum(np.multiply(xx[r:r+7,c:c+7], gaussian))
            trbl = np.sum(np.multiply(xy[r:r+7,c:c+7], gaussian))
            br = np.sum(np.multiply(yy[r:r+7,c:c+7], gaussian))
            window_M = np.matrix([[tl,trbl],[trbl,br]])
            R = np.linalg.det(window_M) - 0.05 * (np.trace(window_M) ** 2)
            M[r,c] = R
    return M

#Threshold based on a normalized result value from 1 to 1000
def threshold(c_resp):
    m = np.max(c_resp)
    return np.array([[c if c * 1000/m > 10 else 0 for c in r] for r in c_resp])

def top_1000(c_resp):
    count = 0
    resp = np.zeros(np.shape(c_resp))
    prog = tqdm(desc = "Getting top 1000", total=1000, leave=False)
    while count < 1000:
        m = np.max(c_resp)
        i,j = np.where(c_resp==m)
        c_resp[i,j] = 0
        resp[i,j] = m
        count += 1
        prog.update()
    prog.close()
    return resp
def apply_haris(image):
    res = top_1000(threshold(responses(image)))
    return res

def to_point_array(harris):
    #Convert detected corners into array of point tuples.
    points = []
    for r in range(np.shape(harris)[0]):
        for c in range(np.shape(harris)[1]):
            if harris[r,c] != 0:
                points.append((c,r))
    return np.array(points)