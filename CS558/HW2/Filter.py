import numpy as np
from tqdm import trange
SOBEL_HORIZ = np.array([
    [-1, -2, -1],
    [0,0,0],
    [1,2,1]
])

SOBEL_VERT = np.array([
    [-1,0,1],
    [-2,0,2],
    [-1,0,1]
])

#Filter application similar to hw1, except ignoring pixels for which pixels of filter
#are outside boundary.
def apply_filter(image, f):
    im = np.copy(image)
    filter_bounds = int((np.shape(f)[0] - 1) / 2)
    bounds = np.array(np.shape(im))
    bounds[0] -= filter_bounds * 2
    bounds[1] -= filter_bounds * 2
    #Get the edge-copied image
    #Create a result array
    result = np.zeros(bounds)
    #Loop over the pixels.
    for r in trange(bounds[0], desc = 'Applying filter', leave=False):
        for c in range(bounds[1]):
            #Take the dot product of the window in padded and the filter, and place in result
            #The trickery with .flat and np.array is due to a quirk with numpy's dotproduct
            #function, where it does matrix mult for 2d arrays for some reason.
            result[r, c] = np.round(np.array(im[r:r+filter_bounds*2+1,c:c+filter_bounds*2+1].flat).dot(f.flat))
    result2 = np.copy(result)
    return result2

# Place the filtered image into the bounds of the original image, with zeros.
def unbound_image(filtered, orig_bounds):
    bounds = np.shape(filtered)
    diff = (int((orig_bounds[0] - bounds[0])/2), int((orig_bounds[1] - bounds[1])/2))
    new = np.zeros(orig_bounds)
    new[diff[0] : diff[0] + bounds[0], diff[1] : diff[1] + bounds[1]] = filtered
    return new

#Non-maximum suppression of a 3x3 area
def nms(arr):
    bounds = np.shape(arr)
    detsub = [[arr[x,y] if arr[x,y] == np.max(arr[x-1:x+2,y-1:y+2]) else 0 for y in range(1,bounds[1]-1)] for x in trange(1, bounds[0]-1, desc='Applying Non-maximum Suppresion', leave=False)]
    result = np.copy(arr)
    result[1:bounds[0]-1,1:bounds[1]-1] = detsub
    return np.array(result)