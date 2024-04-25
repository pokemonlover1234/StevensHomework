import numpy as np
import math
from PIL import Image
from tqdm import trange
import Image as Im
def solution_to_affine(warp_solution):
    w1,w2,w3,w4,t1,t2 = warp_solution
    return np.matrix([
        [w1,w2,t1],
        [w3,w4,t2],
        [0, 0, 1]
    ], dtype = float)

def point_warp(y, x, affine):
    pt = np.matrix([x,y,1]).T
    pt_prime = np.matmul(affine,pt).flat
    return pt_prime

def panorama(image1, warped_image2, offset_x, offset_y):
    b = np.shape(image1)
    b2 = np.shape(warped_image2)
    offset_x = int(offset_x)
    offset_y = int(offset_y)
    if abs(offset_x) > b[1] and offset_x < 0:
        size_x = b2[1] + abs(offset_x)
    else:
        size_x = b[1] + b2[1] + offset_x
    size_y = max(b[0],b2[0]) + abs(offset_y)
    p_size = (size_y,size_x,3)
    image1_set = np.zeros(p_size, dtype=np.uint8)
    image2_set = np.zeros(p_size, dtype=np.uint8)
    if offset_y < 0:
        if(offset_x < -b[1]):
            off = abs(offset_x + b[1])
            image1_set[-b[0]:,off:b[1]+off] = image1
        else:
            image1_set[-b[0]:,0:b[1]] = image1
        if offset_x == 0:
            image2_set[-b2[0]+offset_y:offset_y,-b2[1]+offset_x:] = warped_image2
        elif offset_x > 0:
            image2_set[-b2[0]+offset_y:offset_y,-b2[1]:] = warped_image2
        else:
            image2_set[-b2[0]+offset_y:offset_y,-b2[1]+offset_x:offset_x] = warped_image2
    else:
        if(offset_x < -b[1]):
            off = abs(offset_x + b[1])
            image1_set[0:b[0],off:b[1]+off] = image1
        else:
            image1_set[0:b[0]:,0:b[1]] = image1
        if offset_x == 0:
            image2_set[offset_y:b2[0]+offset_y,-b2[1]+offset_x:] = warped_image2
        elif offset_x > 0:
            image2_set[offset_y:b2[0]+offset_y,-b2[1]:] = warped_image2
        else:
            image2_set[offset_y:b2[0]+offset_y,-b2[1]+offset_x:offset_x] = warped_image2
    panorama = np.zeros(p_size, dtype=np.uint8)

    for y in trange(size_y, desc = 'Stitching images...'):
        for x in range(size_x):
            if(np.array_equal(image1_set[y,x], [0,0,0]) and np.array_equal(image2_set[y,x], [0,0,0])):
                panorama[y,x,:] = [0,0,0]
            elif(np.array_equal(image1_set[y,x], [0,0,0])):
                panorama[y,x,:] = image2_set[y,x]
            elif(np.array_equal(image2_set[y,x], [0,0,0])):
                panorama[y,x,:] = image1_set[y,x]
            else:
                r = math.floor(math.sqrt(image1_set[y,x,0] ** 2 / 2 + image2_set[y,x,0] ** 2 / 2))
                g = math.floor(math.sqrt(image1_set[y,x,1] ** 2 / 2 + image2_set[y,x,0] ** 2 / 2))
                b = math.floor(math.sqrt(image1_set[y,x,2] ** 2 / 2 + image2_set[y,x,0] ** 2 / 2))
                panorama[y,x,:] = [r,g,b]

    return panorama


def warp(image1, image2, warp):
    #Convert solution matrix to affine warp matrix
    affine = solution_to_affine(warp)
    #Calculate bounds by warping corner points to get corners, 
    #then extrapolating bounds from those points. Note: some 
    #could be negative. Will consider that and keep in mind
    #During overlap.
    bounds = np.shape(image2)
    top_left = point_warp(0, 0, affine)
    top_right = point_warp(0, bounds[1], affine)
    bottom_left = point_warp(bounds[0], 0, affine)
    bottom_right = point_warp(bounds[0], bounds[1], affine)
    min_x = min(top_left[0], top_right[0], bottom_left[0], bottom_right[0])
    max_x = max(top_left[0], top_right[0], bottom_left[0], bottom_right[0])
    min_y = min(top_left[1], top_right[1], bottom_left[1], bottom_right[1])
    max_y = max(top_left[1], top_right[1], bottom_left[1], bottom_right[1])
    bounds_y = max_y - min_y
    bounds_x = max_y - min_y
    Tinv = np.linalg.inv(affine)
    Tinvtuple = (Tinv[0,0],Tinv[0,1], Tinv[0,2], Tinv[1,0],Tinv[1,1],Tinv[1,2])
    im_warped = Image.fromarray(image2)
    im_warped = im_warped.transform((math.ceil(bounds_x), math.ceil(bounds_y)), Image.AFFINE, Tinvtuple)
    Im.save_image(np.array(im_warped), "test.jpg")

    return panorama(image1, np.array(im_warped), affine[0,2], affine[1,2])