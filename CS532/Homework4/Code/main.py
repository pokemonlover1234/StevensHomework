from P1.Harris import harris
from P1.NMS import nms
from P1.Depth import corners_to_depths, to_depths
from P1.Rank import rank_transform
from P1.MatchCorners import match_corners
from P1.RANSAC import RANSAC
from P1.Colors import color_map, image_map
from P1.ply import ply_write
from P2.Normal import compute_normals
import P1.Filter as Filter
import Image
import numpy as np

# Get indices of maximum n entries in array
def get_n_max_indices(array, n):
    indices = np.zeros((n, len(array.shape)))
    arr = array.copy()
    for i in range(n):
        indmax = np.unravel_index(np.argmax(arr), array.shape)
        indices[i] = np.array(indmax)
        arr[indmax] = np.min(arr)
    return indices

# Take ONLY the entries in array specified by indices
# Leave rest of entries in output at 0
def indices_select(array, indices):
    out = np.zeros(array.shape)
    for y, x in indices:
        a = int(y)
        b = int(x)
        out[a, b] = array[a, b]
    return out


def main():
    P1_images = [
        Image.get_image("../data/problem1/rgb1.png", True),
        Image.get_image("../data/problem1/rgb2.png", True),
        Image.get_image("../data/problem1/rgb3.png", True)
    ]
    P1_corners = [
        nms(harris(P1_images[0])),
        nms(harris(P1_images[1])),
        nms(harris(P1_images[2]))
    ]
    P1_depthmaps = [
        Image.get_image("../data/problem1/depth1.png"),
        Image.get_image("../data/problem1/depth2.png"),
        Image.get_image("../data/problem1/depth3.png")
    ]
    # Get top 100 corners
    P1_corners = [
        indices_select(P1_corners[0], get_n_max_indices(P1_corners[0], 100)),
        indices_select(P1_corners[1], get_n_max_indices(P1_corners[1], 100)),
        indices_select(P1_corners[2], get_n_max_indices(P1_corners[2], 100))
    ]
    # Get depths
    P1_depths = [
        corners_to_depths(P1_corners[0], Filter.crop_to(P1_depthmaps[0], P1_corners[0]), int((P1_depthmaps[0].shape[0] - P1_corners[0].shape[0]) / 2)),
        corners_to_depths(P1_corners[1], Filter.crop_to(P1_depthmaps[1], P1_corners[1]), int((P1_depthmaps[1].shape[0] - P1_corners[1].shape[0]) / 2)),
        corners_to_depths(P1_corners[2], Filter.crop_to(P1_depthmaps[2], P1_corners[2]), int((P1_depthmaps[2].shape[0] - P1_corners[2].shape[0]) / 2))
    ]
    P1_ranktransform = [
        Filter.crop_to(rank_transform(P1_images[0]), P1_corners[0]),
        Filter.crop_to(rank_transform(P1_images[1]), P1_corners[1]),
        Filter.crop_to(rank_transform(P1_images[2]), P1_corners[2])
    ]
    P1_cornermatch_21 = match_corners(P1_ranktransform[1],
                                      P1_depths[1],
                                      P1_ranktransform[0],
                                      P1_depths[0])
    P1_cornermatch_23 = match_corners(P1_ranktransform[1],
                                      P1_depths[1],
                                      P1_ranktransform[2],
                                      P1_depths[2])
    P1_cornermatch_21 = sorted(P1_cornermatch_21, key = lambda tup: tup[2])[:10]
    P1_cornermatch_23 = sorted(P1_cornermatch_23, key = lambda tup: tup[2])[:10]
    R12, t12 = RANSAC(P1_cornermatch_21)
    R32, t32 = RANSAC(P1_cornermatch_23)
    P1_coloredimages = [
        Image.get_image("../data/problem1/rgb1.png"),
        Image.get_image("../data/problem1/rgb2.png"),
        Image.get_image("../data/problem1/rgb3.png")
    ]
    P1_depths_colored = [
        color_map(P1_coloredimages[0], to_depths(P1_images[0], P1_depthmaps[0], 0)),
        color_map(P1_coloredimages[1], to_depths(P1_images[1], P1_depthmaps[1], 0)),
        color_map(P1_coloredimages[2], to_depths(P1_images[2], P1_depthmaps[2], 0)),
    ]
    P1_depths_colored_transformed = [
        image_map(P1_depths_colored[0], R12, t12),
        P1_depths_colored[1],
        image_map(P1_depths_colored[2], R32, t32)
    ]
    ply_write(P1_depths_colored_transformed, "../Output/model.ply")
    P2_image = Image.get_image("../data/problem2/rgbn.png")
    P2_depthmap = Image.get_image("../data/problem2/depthn.png")
    P2_depths = to_depths(P2_image, P2_depthmap, 0)
    P2_normals = compute_normals(P2_depths, P2_image)
    Image.save_image(P2_normals, "../output/normals.png")



if __name__ == "__main__":
    main()