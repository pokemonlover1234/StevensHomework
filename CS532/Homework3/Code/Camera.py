import numpy as np
from sympy import Matrix
from numba import jit, types, float64, int64


# Uses projection matrix to convert meter coordinates
# to an x,y point, and reverse. Also provides accessor
# functions to get information from the camera's image
# and silhouette from voxel coordinates.
class Camera():
    def __init__(self, P, image, silhouette):
        self.P = P
        self.image = image
        self.silhouette = silhouette
        C = Matrix(P)
        C = C.nullspace()[0]
        C = C/C[3]
        self.center = np.matrix(C)

    # Returns X, Y coordinates of voxel (in meters)
    # in camera's image. Does NOT check image bounds,
    # but does check voxel bounds.
    @jit(types.UniTuple(int64, 2)(float64[:, :], float64, float64, float64),
         nopython=True, cache=True)
    def project(P, x, y, z):
        if(x < -2.5 or x > 2.5 or y < -3
           or y > 3 or z < 0 or z > 2.5):
            print("Error: Voxel coordinates outside range. ")
            return (-1, -1)
        pt = np.array([x, y, z, 1])
        # Some less efficient matrix mult to allow for numba to
        # significantly increase overall efficiency by compiling
        # this function to machine code
        # Speedup is about 3.5x
        homogenous_coords = [np.sum(np.multiply(P[0, :], pt)),
                             np.sum(np.multiply(P[1, :], pt)),
                             np.sum(np.multiply(P[2, :], pt))]
        X = int(homogenous_coords[0] / homogenous_coords[2])
        Y = int(homogenous_coords[1] / homogenous_coords[2])
        return X, Y

    # Returns true if voxel is in this camera's silhouette
    # false if not. x, y, z in meters.
    # Returns None if pixel is outside image bounds
    def get_silhouette_presence(self, x, y, z):
        if(x < -2.5 or x > 2.5 or y < -3
           or y > 3 or z < 0 or z > 2.5):
            print("Error: Voxel coordinates outside range. ")
            return None
        X, Y = Camera.project(self.P, x, y, z)
        if(X >= self.silhouette.shape[1] or X < 0 or
           Y >= self.silhouette.shape[0] or Y < 0):
            return None
        silhouettept = self.silhouette[Y, X]
        if(silhouettept > 0):
            return True
        return False

    # Gets the color of the pixel corresponding to the provided
    # voxel. x, y, z in meters.
    # Returns None if pixel is outside image bounds
    def get_image_color(self, x, y, z):
        if(x < -2.5 or x > 2.5 or y < -3
           or y > 3 or z < 0 or z > 2.5):
            print("Error: Voxel coordinates outside range. ")
            return None
        X, Y = Camera.project(self.P, x, y, z)
        if(X >= self.image.shape[1] or X < 0 or
           Y >= self.image.shape[0] or Y < 0):
            return None
        return self.image[Y, X]
