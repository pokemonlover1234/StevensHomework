import numpy as np
import math
from tqdm import trange
def estimate_affine(matches):
    #Use the center of each match as a point to estimate affine transform
    bounds = np.shape(matches[0][0])
    s = math.floor(bounds[0]/2)
    A = np.matrix([
        [matches[0][0][0], matches[0][0][1], 0, 0, 1, 0],
        [0, 0, matches[0][0][0], matches[0][0][1], 0, 1],
        [matches[1][0][0], matches[1][0][1], 0, 0, 1, 0],
        [0, 0, matches[1][0][0], matches[1][0][1], 0, 1],
        [matches[2][0][0], matches[2][0][1], 0, 0, 1, 0],
        [0, 0, matches[2][0][0], matches[2][0][1], 0, 1]
    ])
    b = np.matrix([matches[0][1][0],matches[0][1][1],matches[1][1][0],matches[1][1][1],matches[2][1][0],matches[2][1][1]]).T
    #Use built in least squares equation solver
    x,_,_,_ = np.linalg.lstsq(A,b, rcond=None)
    return x

def get_inliers_and_avg_error(match_list, solved_affine, inlier_max_dist):
    #Define an inlier match as one where, when the affine transformation is applied
    #to the center point of the first patch, it is within inlier_max_dist of the 
    #center of the second patch.
    inliers = []
    total_error = 0
    for match in match_list:
        pt_prime = np.matmul(np.matrix([
            [match[0][0],match[0][1],0,0,1,0],
            [0,0,match[0][1],match[0][1],0,1]
        ]),solved_affine).T
        pt_actual_prime = np.matrix([match[1][0], match[1][1]])
        dist = math.sqrt(math.pow(pt_prime.flat[0] - pt_actual_prime.flat[0],2)+math.pow(pt_prime.flat[1] - pt_actual_prime.flat[1],2))
        if dist <= inlier_max_dist:
            inliers.append(match)
        total_error += dist
    return (inliers, total_error/len(match_list))

def apply_RANSAC(h_list, image1, image2, inlier_file):
    param_s = 3
    param_t = 20
    param_p = 0.999
    param_n = 50000
    param_d = 4
    h_list = np.array(h_list, dtype=object)
    ransac = trange(param_n, desc = 'Running RANSAC...')
    best_guess = None
    guesses = 1
    with open(inlier_file, "w+") as inlier_out:
        for _ in ransac:
            sample = np.array(h_list[np.random.choice(h_list.shape[0], param_s, replace=False), :])
            fit = estimate_affine(sample)
            inliers, avg_err = get_inliers_and_avg_error(h_list, fit, param_t)
            inliers = np.array(inliers)
            if len(inliers) >= param_d and (best_guess is None or avg_err < best_guess[1]): 
                best_guess = (fit, avg_err) 
                inlier_out.write(f"Guess {guesses}\n\n")
                inlier_out.write(f"Guessed vertical affine:\n {fit}\n\nInliers:\n\n")
                for inlier in inliers:
                    inlier_out.write(f"  {inlier}\n")
                inlier_out.write(f"\n Average reprojection error per match in pixels: {avg_err}\n\n")
                guesses += 1
    return best_guess[0]