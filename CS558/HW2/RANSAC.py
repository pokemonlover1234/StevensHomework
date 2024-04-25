from PIL import Image, ImageDraw
import math
import numpy as np
from tqdm import trange, tqdm
import Filter
import Hessian

def total_least_squares(sample):
    #Step 1: Get UTU, given by 5th set of notes.
    x_array = sample[:,0]
    y_array = sample[:,1]
    x_minus_avg = x_array-np.average(x_array)
    y_minus_avg = y_array-np.average(y_array)
    utu00 = np.sum(x_minus_avg**2)
    utu11 = np.sum(y_minus_avg**2)
    utu01 = utu10 = np.sum(np.multiply(x_minus_avg,y_minus_avg))
    utu = np.array([
        [utu00, utu01],
        [utu10, utu11]
    ])
    #Step 2: get normal eigenvector related to smallest eigenvalue.
    values, vectors = np.linalg.eig(utu)
    min_vector = vectors[:, np.where(values == np.min(values))[0][0]]
    #Step 3: get d
    d = min_vector[0] * np.average(x_array) + min_vector[1] * np.average(y_array)
    #Step 4: return a,b,d, eigenvalue (to rank fit)
    return (min_vector[0],min_vector[1],-d,np.min(values))

def get_inliers(points, fit, param_t):
    a, b, d, _ = fit
    inliers = []
    for pt in points:
        x, y = pt
        dist = abs(a * x + b * y + d)/math.sqrt(a**2+b**2)
        if dist <= param_t:
            inliers.append(pt)
    return inliers

def get_N(points, param_s, param_p, param_t):
    N = np.count_nonzero(points)
    samples = 0
    e = 0.5
    mi = 0
    bar = tqdm(desc = 'Finding optimal N...', total = N, leave = False)
    while N > samples:
        sample_points = points[np.random.choice(points.shape[0], param_s, replace=False), :]
        fit = total_least_squares(np.array(sample_points))
        inliers = get_inliers(points, fit, param_t)
        inlier_ratio = len(inliers)/len(points)
        if inlier_ratio > mi:
            e = 1 - inlier_ratio
            mi = inlier_ratio
            N = math.log(1 - param_p)/math.log(1 - math.pow(1 - e, param_s))
        samples += 1
        bar.total = math.ceil(N)
        bar.update(1)
    return math.ceil(N)


def apply_RANSAC(hessian, image):
    hessian = Filter.unbound_image(hessian, np.shape(image))
    points = Hessian.to_point_array(hessian)
    points_source = np.copy(points)
    param_s = 2
    param_t = 8
    param_p = 0.999
    param_n = 50000
    param_d = 12
    lines = []
    im = Image.fromarray(image)
    draw = ImageDraw.Draw(im)
    ransac = trange(param_n, desc = 'Running RANSAC... Found 0 Lines')
    for _ in ransac:
        sample = np.array(points_source[np.random.choice(points_source.shape[0], param_s, replace=False), :])
        fit = total_least_squares(sample)
        inliers = get_inliers(points, fit, param_t)
        inliers = np.array(inliers)
        if len(inliers) >= param_d:
            lines.append((total_least_squares(inliers),inliers))
            points_source = np.array([pt for pt in points_source if not any([np.array_equal(s, pt) for s in inliers])])
            ransac.set_description(f'Running RANSAC... Found {len(lines)} Lines.')
            if(len(points_source) < param_d):
                print("Not enough remaining outliers to form another line. Breaking out early.")
                break
    best_lines = sorted(lines, key = lambda x: x[0][-1])
    for i in range(min(4, len(best_lines))):
        pts = sorted(best_lines[i][1], key = lambda x: x[0])
        draw.line([pts[0][0],pts[0][1],pts[-1][0],pts[-1][1]], width = 1)
        for pt in pts:
            bounds = [pt[0] - 1, pt[1] - 1, pt[0] + 2, pt[1] + 2]
            draw.rectangle(bounds, width = 1)
    return im
