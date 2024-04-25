import numpy as np
import math

# Side length of voxels in meters.
# 0.002 Used in final
# 0.025 Used in testing for speed
VOXEL_DIMENSION = 0.002


def vec_len(vec):
    tot = 0
    for p in vec:
        tot += p * p
    return math.sqrt(tot)


# Creates a voxel grid accessible using meter-based coordinates
# Size of grid is 5m by 6m by 2.5m. x and y access based on
# center (x:-2.5 to 2.5, y:-3 to 3), z based on 0 (z:0 to 2.5)
class VoxelGrid():
    def __init__(self):
        self.grid = np.zeros((math.ceil(5/VOXEL_DIMENSION),
                              math.ceil(6/VOXEL_DIMENSION),
                              math.ceil(2.5/VOXEL_DIMENSION),
                              3), np.uint8)

    # Converts voxel locations in the form (X, Y, Z), where X, Y, and Z are in
    # meters, to array values and returns the voxel value at that location.
    def get_voxel(self, voxel_x, voxel_y, voxel_z):
        if(voxel_x < -2.5 or voxel_x > 2.5 or voxel_y < -3
           or voxel_y > 3 or voxel_z < 0 or voxel_z > 2.5):
            print("Error: Voxel coordinates outside range. ")
            return None
        grid_x = math.floor((voxel_x+2.5)/VOXEL_DIMENSION)
        grid_y = math.floor((voxel_y+3)/VOXEL_DIMENSION)
        grid_z = math.floor((voxel_z)/VOXEL_DIMENSION)
        # If grid points are exactly at far edge, get actual last voxel
        # instead of nonexistent one.
        if voxel_x == 2.5:
            grid_x -= 1
        if voxel_y == 3:
            grid_y -= 1
        if voxel_z == 2.5:
            grid_z -= 1
        return self.grid[grid_x, grid_y, grid_z]

    # Converts voxel locations in the form (X, Y, Z), where X, Y, and Z are in
    # meters, to array values and sets the value of the voxel at that location
    # new_value is of the form [r,g,b]
    def set_voxel(self, voxel_x, voxel_y, voxel_z, new_value):
        if(voxel_x < -2.5 or voxel_x > 2.5 or voxel_y < -3
           or voxel_y > 3 or voxel_z < 0 or voxel_z > 2.5):
            print("Error: Voxel coordinates outside range. ")
            return None
        grid_x = math.floor((voxel_x+2.5)/VOXEL_DIMENSION)
        grid_y = math.floor((voxel_y+3)/VOXEL_DIMENSION)
        grid_z = math.floor((voxel_z)/VOXEL_DIMENSION)
        # If grid points are exactly at far edge, get actual last voxel
        # instead of nonexistent one.
        if voxel_x == 2.5:
            grid_x -= 1
        if voxel_y == 3:
            grid_y -= 1
        if voxel_z == 2.5:
            grid_z -= 1
        self.grid[grid_x, grid_y, grid_z] = new_value

    # Converts grid indices to voxel coordinates in meters.
    # Since this object expects to be accessd by meter-based
    # coordinates, this is necessary if looping through the grid.
    # Loses some precision, but that is inherent in a grid of voxels.
    # Returns coords of center of voxel.
    def index_to_coords(self, i, j, k):
        X = i * VOXEL_DIMENSION - 2.5 + VOXEL_DIMENSION / 2
        Y = j * VOXEL_DIMENSION - 3 + VOXEL_DIMENSION / 2
        Z = k * VOXEL_DIMENSION + VOXEL_DIMENSION / 2
        # Necessary if voxel size doesn't evenly divide the grid size.
        X = 2.5 if X > 2.5 else X
        Y = 3 if Y > 3 else Y
        Z = 2.5 if Z > 2.5 else Z
        return X, Y, Z

    # Determine voxel color from cameras. Uses crude estimation of
    # ray marching.
    def calc_color(self, voxel_x, voxel_y, voxel_z, cameras):
        if(voxel_x < -2.5 or voxel_x > 2.5 or voxel_y < -3
           or voxel_y > 3 or voxel_z < 0 or voxel_z > 2.5):
            print("Error: Voxel coordinates outside range. ")
            return None

        color_cams = []

        for cam in cameras:
            # Obtain a vector from the provided coords to the camera center
            vec_pt_to_cam = (cam.center - [[voxel_x], [voxel_y],
                             [voxel_z], [1]])[:3]
            vec_pt_to_cam = vec_pt_to_cam.astype(np.float32)
            # Set indicator color (so we dont discard a camera for intersecting
            # source voxel)
            self.set_voxel(voxel_x, voxel_y, voxel_z, [128, 128, 128])
            # Set length of vector to 2/3 * voxel dimension.
            vec_pt_to_cam = vec_pt_to_cam / (vec_len(vec_pt_to_cam)) * \
                2 / 3 * VOXEL_DIMENSION
            # Crude approximation of ray-march using resized
            # vec_pt_to_cam as step. Misses some corners, but
            # I hope effect of this is decreased as model
            # resolution increases.
            pt = np.array([[voxel_x], [voxel_y],
                           [voxel_z]]).astype(np.float32)
            seen = True
            while(pt[0, 0] >= -2.5 and pt[0, 0] <= 2.5
                  and pt[1, 0] >= -3 and pt[1, 0] <= 3
                  and pt[2, 0] >= 0 and pt[2, 0] <= 2.5):
                here = self.get_voxel(pt[0, 0], pt[1, 0], pt[2, 0])
                # If voxel is free or the indicator, increment ray-
                # march and continue.
                if np.array_equal(here, [128, 128, 128]) or \
                   np.array_equal(here, [0, 0, 0]):
                    pt += vec_pt_to_cam
                    continue
                # If voxel is any other color, that means it is occupied.
                # Either [255, 255, 255], internal or no assigned color,
                # or an assigned color (there is prevention of setting
                # an occupied and color-assigned voxel to [128, 128, 128]
                # or [0, 0, 0])
                seen = False
                break
            if seen:
                color_cams.append(cam)

        r = 0
        g = 0
        b = 0
        leng = len(color_cams)
        # Safety net. If no cameras see this voxel,
        # return black.
        if leng == 0:
            return [0, 0, 1]
        # Obtain final color from average of colors from cameras that
        # see the voxel.
        for cam in color_cams:
            color = cam.get_image_color(voxel_x, voxel_y, voxel_z)
            r += int(color[0]) * color[0]
            g += int(color[1]) * color[1]
            b += int(color[2]) * color[2]
        color = [int(math.sqrt(r/leng)),
                 int(math.sqrt(g/leng)),
                 int(math.sqrt(b/leng))]
        # Prevent indicator color
        color = [129, 128, 128] if color == [128, 128, 128] else color
        color = [0, 0, 1] if color == [0, 0, 0] else color
        return color
