import numpy as np
import math
from tqdm import trange

#Step 1: Initialization

#Note: it is sufficient to just get the centroid locations.
#They are calculated based on the given 50x50 segments. 

#Returns the centroid locations, and uninitialzed colors
def init(image):
    b = image.shape
    centroidlocs = np.zeros((int(math.ceil(b[0]/50)), int(math.ceil(b[1]/50)), 5))
    for y in range(centroidlocs.shape[0]):
        for x in range(centroidlocs.shape[1]):
            if y < centroidlocs.shape[0] - 1 and x < centroidlocs.shape[1] - 1:
                centroidlocs[y,x] = np.append([y*50 + 25, x*50 + 25], np.average(image[y*50:y*50 + 50, x*50:x*50+50], axis=(0,1)))
            elif y < centroidlocs.shape[0] - 1 and x == centroidlocs.shape[1] - 1:
                centroidlocs[y,x] = np.append([y*50 + 25, x*50 + int(math.ceil((b[1] % 50 if b[1] % 50 != 0 else 50)/2))], np.average(image[y*50:y*50 + 50, x*50:x*50+50], axis=(0,1)))
            elif y == centroidlocs.shape[0] - 1 and x < centroidlocs.shape[1] - 1:
                centroidlocs[y,x] = np.append([y*50 + int(math.ceil((b[0] % 50 if b[0] % 50 != 0 else 50)/2)),x*50 + 25], np.average(image[y*50:y*50 + 50, x*50:x*50+50], axis=(0,1)))
            else:
                centroidlocs[y,x] = np.append([y*50 + int(math.ceil((b[0] % 50 if b[0] % 50 != 0 else 50)/2)),x*50 + int(math.ceil((b[1]%50 if b[1] % 50 != 0 else 50)/2))], np.average(image[y*50:y*50 + 50, x*50:x*50+50], axis=(0,1)))
    return centroidlocs

#Step 2: Local Shift

#Note: Square root is slow, so since sqrt(x) < sqrt(y) <-> x < y,
#just comparing the sum of squares of magnitudes is sufficient.
#Meaning, sum of squares of directional gradients for each channel
#is the result.

#Returns: updated relcentroids with new centroid locations
def local_shift(image, centroids):
    newcentroids = np.copy(centroids)
    for cy in trange(centroids.shape[0], leave=False, desc="Local Shift"):
        for cx in range(centroids.shape[1]):
            y,x, _, _, _ = centroids[cy, cx]
            x = int(x)
            y = int(y)
            grad_sqr_arr = np.zeros((3,3))
            for i in [-1,0,1]:
                for j in [-1,0,1]:
                    grad_sqr_arr[i+1, j+1] = np.sum((image[y + i + 1, x + j] - image[y + i - 1, x + j])**2
                                                    + (image[y + i, x + j + 1] - image[y + i, x + j - 1])**2)
            min_gradient_rel_pos = np.array(np.unravel_index(grad_sqr_arr.argmin(), grad_sqr_arr.shape)) - 1
            newcentroids[cy, cx, :2] = [y + min_gradient_rel_pos[0], x + min_gradient_rel_pos[1]]
    return newcentroids

#Step 3: Centroid Update

def get_pixel_assignment(pixel, x, y, centroids):
    mindist = None
    mincentroid = [None, None]
    for cy in range(centroids.shape[0]):
        for cx in range(centroids.shape[1]):
            if np.sum((centroids[cy,cx, :2] - [y, x])**2) > 10000:
                continue
            #Numpy array of shape n divided by array of shape n does element-wise division. This performs the scaling
            dist = np.sum(((centroids[cy,cx]/[COLOR_SCALING_FACTOR,COLOR_SCALING_FACTOR,1,1,1]) - np.append(np.array([y,x])/COLOR_SCALING_FACTOR, pixel))**2)
            if mindist is None or dist < mindist:
                mindist = dist
                mincentroid = [cy, cx]
    return mincentroid, mindist

COLOR_SCALING_FACTOR = 2
#Returns: Updated centroids. 
def update_centroids(image, centroids):
    accumulator = np.zeros((centroids.shape[0], centroids.shape[1], 6))
    for y in trange(image.shape[0], leave=False, desc="Updating centroids"):
        for x in trange(image.shape[1], leave=False, desc=""):
            #Since here we are simply using the distances to get accumulator output
            #and not to return assigned pixels, keeping which is the mimimum rather
            #than all distances and using argmin as in KMeans is sufficient.
            mincentroid, mindist = get_pixel_assignment(image[y,x], x, y, centroids)
            accumulator[mincentroid[0],mincentroid[1]] += np.append(np.append([y, x], image[y, x]), 1) if mindist is not None else 0
    newcentroids = np.copy(centroids)
    for cy in range(centroids.shape[0]):
        for cx in range(centroids.shape[1]):
            newcentroids[cy, cx] = accumulator[cy,cx,:5]/accumulator[cy,cx,5]
    return newcentroids

def output(image, centroids):
    outtemp = np.zeros(image.shape)
    for y in trange(image.shape[0], desc="Generating Initial Output"):
        for x in range(image.shape[1]):
            c,_ = get_pixel_assignment(image[y,x], x, y, centroids)
            outtemp[y,x] = centroids[c[0],c[1]][2:]
    out = np.copy(outtemp)
    for y in trange(image.shape[0], desc="Generating Boundaries"):
        for x in range(image.shape[1]):
            if y == 0 and x == 0:
                if np.count_nonzero(outtemp[0:2,0:2] - outtemp[0,0]) > 0:
                    out[0,0] = 0
            elif y == 0 and x > 0:
                if np.count_nonzero(outtemp[0:2,x-1:x+2] - outtemp[0,x]) > 0:
                    out[0,x] = 0
            elif y > 0 and x == 0:
                if np.count_nonzero(outtemp[y-1:y+2,0:2] - outtemp[y, 0]) > 0:
                    out[y,0] = 0
            else:
                if np.count_nonzero(outtemp[y-1:y+2,x-1:x+2] - outtemp[y,x]) > 0:
                    out[y,x] = 0
    return out
def do_SLIC(image, max_iter=3):
    c = init(image)
    c = local_shift(image, c)
    iteration = 1
    while(iteration <= max_iter):
        newc = update_centroids(image, c)
        if(np.array_equal(np.floor(c), np.floor(newc))):
            break
        c = newc
        iteration += 1
    return output(image, c)