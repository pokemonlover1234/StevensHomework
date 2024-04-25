# Convert a tuple of (2dx, 2dy, 3dx, 3dy, 3dz)
# to a 2-tuple containing color ((2dx, 2dy, 3dx, 3dy, 3dz), (r, g, b))
import numpy as np
from pytools import T


def color_map(image, depths):
    colormap = []
    # Point is the (2dx, 2dy, 3dx, 3dy, 3dz)
    # This part is one of the main reasons it's 
    # useful to have the 2d and 3d information paired
    # this way.
    for point in depths:
        colortuple = (point, image[int(point[1]), int(point[0])])
        colormap.append(colortuple)
    return colormap

# Apply transformations 
def image_map(depths, R, t):
    output = []
    for pt, color in depths:
        a, b, x, y, z = pt
        P = np.array([[x, y, z]]).T
        P_result = np.matmul(R, P) + t
        T = P_result.T.flatten()
        output.append(((a, b, T[0], T[1], T[2]), color))
    return output