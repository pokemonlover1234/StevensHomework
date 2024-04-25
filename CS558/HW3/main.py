import Harris
import Matching
import Image
import Filter
import Gaussian
import RANSAC
import Warp
import numpy as np
from scipy import ndimage
def main():
    tower_left = Image.get_image("uttower_left.jpg", True)
    tower_right = Image.get_image("uttower_right.jpg", True)
    tower_left = Filter.apply_filter(tower_left, Gaussian.gaussian_filter(1))
    tower_right = Filter.apply_filter(tower_right, Gaussian.gaussian_filter(1))
    #Remove outer pixels due to difficulties with nms on that area.
    harris_left = Harris.apply_haris(tower_left)
    harris_right = Harris.apply_haris(tower_right)
    harris_left_nms = np.zeros(np.shape(tower_left))
    harris_right_nms = np.zeros(np.shape(tower_right))
    harris_left_nms[1:-1,1:-1] = Filter.nms(harris_left)[1:-1,1:-1]
    harris_right_nms[1:-1,1:-1] = Filter.nms(harris_right)[1:-1,1:-1]
    Image.save_image(harris_left, "tower_left_harris.jpg")
    Image.save_image(harris_left_nms, "tower_left_harris_nms.jpg")
    Image.save_image(harris_right, "tower_right_harris.jpg")
    Image.save_image(harris_right_nms, "tower_right_harris_nms.jpg")
    ncc_im, ncc_h = Matching.ncc(tower_left, tower_right, Harris.to_point_array(harris_left_nms), Harris.to_point_array(harris_right_nms))
    Image.save_image(ncc_im, "NCC_matches.jpg")
    guess_best = RANSAC.apply_RANSAC(ncc_h[0:20], harris_left, harris_right, "RANSAC_putative_top20.txt")
    guess_with_rand = RANSAC.apply_RANSAC(ncc_h, harris_left, harris_right, "RANSAC_putative_top20andrand30.txt")
    pan1 = Warp.warp(Image.get_image("uttower_left.jpg"), Image.get_image("uttower_right.jpg"), guess_best)
    pan2 = Warp.warp(Image.get_image("uttower_left.jpg"), Image.get_image("uttower_right.jpg"), guess_with_rand)
    pan1 = pan1.astype(np.uint8)
    pan2 = pan2.astype(np.uint8)
    Image.save_image(pan1, "Panorama_a1.jpg")
    Image.save_image(pan2, "Panorama_a1a2.jpg")
if __name__ == "__main__":
    main()