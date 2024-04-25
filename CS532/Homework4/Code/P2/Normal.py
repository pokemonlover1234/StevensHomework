# Determine normals from (2dx, 2dy, 3dx, 3dy, 3dz)
# Output ((2dx, 2dy, 3dx, 3dy, 3dz), (a, b, c))
import numpy as np
from skspatial.objects import Plane
from skspatial.objects import Points
from tqdm import trange

def compute_normals(depths, image):
    pts = np.zeros((image.shape[0], image.shape[1], 3))
    # Convert depths list to depths array
    for x, y, X, Y, Z in depths:
        pts[int(y), int(x)] = [X, Y, Z]
    normals = np.zeros((image.shape[0], image.shape[1], 3))
    for y in trange(image.shape[0], desc="Determining normals"):
        for x in range(image.shape[1]):
            area = pts[max(0, y - 3): min(y + 4, image.shape[0] - 1), max(0, x - 3): min(x + 4, image.shape[1] - 1)]
            c = 0
            # Count number of actual depths available in area
            # Also build point matrix
            A = np.zeros((area.shape[0] * area.shape[1], 3))

            for a in range(area.shape[0]):
                for b in range(area.shape[1]):
                    X, Y, Z = area[a, b]
                    if X == 0 and Y == 0 and Z == 0:
                        continue
                    A[c] = [X, Y, Z]
                    c += 1
            # Abort if less than 3 points
            if c < 3:
                continue
            A = A[:c]
            points = Points(A)
            try:
                plane = Plane.best_fit(points)
            except ValueError:
                # Points colinear
                continue
            normal = np.array([plane.normal.round(3)]).T
            normals[y, x] = (((normal / (2 * np.linalg.norm(normal))) + np.array([[0.5, 0.5, 0.5]]).T) * 255).T.flatten()
    return normals