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

#Perform edge copying to pad image for filtering
def pad_image(pad_by, image):
    #Get size of image
    bounds = np.shape(image)
    #Cast pad_by, otherwise lots of complaints about wanting ints instead of floats.
    pad_by = int(pad_by)
    #Create the padded array
    padded = np.zeros((bounds[0] + 2 * pad_by, bounds[1] + 2 * pad_by))
    #Time for some fun python array manipulation magic!
    #This is magnitudes more efficient than a loop-based approach
    #Note, access by im[row,column]
    #Step 1: Copy image into proper position in padded array
    padded[pad_by:bounds[0]+pad_by,pad_by:bounds[1]+pad_by] = image
    #Step 2: Expand corners of image in pad_by x pad_by corners in padded array.
    padded[0:pad_by,0:pad_by] = image[0,0] # Top Left
    padded[0:pad_by,bounds[1]+pad_by:] = image[0,bounds[1]-1] # Top Right
    padded[bounds[0]+pad_by:,0:pad_by] = image[bounds[0]-1,0] # Bottom Left
    padded[bounds[0]+pad_by:,bounds[1]+pad_by:] = image[bounds[0]-1,bounds[1]-1] # Bottom Right
    #Step 3: Expand edges into pad_by x edge length edges of padded array. 
    #The matrix -> transpose (.T) transitions on the right side of the 
    #first two assignments allow for a row vector to convert to a column vector
    #so that the expansion over to the left side works properly.
    padded[pad_by:bounds[0]+pad_by,0:pad_by] = np.matrix(image[:,0]).T # Left edge
    padded[pad_by:bounds[0]+pad_by,bounds[1] + pad_by:bounds[1] + pad_by * 2] = np.matrix(image[:, bounds[1] - 1]).T # Right edge
    padded[0:pad_by,pad_by:bounds[1]+pad_by] = image[0,:] # Top edge
    padded[bounds[0] + pad_by:bounds[0] + pad_by * 2, pad_by:bounds[1]+pad_by] = image[bounds[0] - 1,:] # Bottom edge
    return padded

def apply_filter(image, filter):
    filter_bounds = int((np.shape(filter)[0] - 1) / 2)
    bounds = np.shape(image)
    #Get the edge-copied image
    padded = pad_image(filter_bounds, image)
    #Create a result array
    result = np.zeros(bounds)
    #Loop over the pixels.
    for r in trange(bounds[0], desc="Applying Filter...", leave=False):
        for c in range(bounds[1]):
            #Take the dot product of the window in padded and the filter, and place in result
            #The trickery with .flat and np.array is due to a quirk with numpy's dotproduct
            #function, where it does matrix mult for 2d arrays for some reason.
            result[r, c] = np.array(padded[r:r+filter_bounds*2+1,c:c+filter_bounds*2+1].flat).dot(filter.flat)
    return result

#Non-maximum suppression of a 3x3 area
def nms(arr):
    bounds = np.shape(arr)
    detsub = [[arr[x,y] if arr[x,y] == np.max(arr[x-1:x+2,y-1:y+2]) else 0 for y in range(1,bounds[1]-1)] for x in trange(1, bounds[0]-1, desc='Applying Non-maximum Suppresion', leave=False)]
    result = np.copy(arr)
    result[1:bounds[0]-1,1:bounds[1]-1] = detsub
    return np.array(result)