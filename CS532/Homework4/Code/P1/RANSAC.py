import numpy as np
import math


def distance(R, t, P1, P2):
    # Get expected P2 from given P1, R, t, then determine
    # distance from actual P2
    P2_p = np.matmul(R, P1) + t
    dist = math.sqrt(math.pow(P2[0, 0] - P2_p[0, 0], 2) + \
                     math.pow(P2[1, 0] - P2_p[1, 0], 2) + \
                     math.pow(P2[2, 0] - P2_p[2, 0], 2))
    return dist

def get_model(P11, P12, P13, P21, P22, P23):
    # Compute model given by the 6 points
    v11 = P11 - P12
    v12 = P12 - P13
    v21 = P21 - P22
    v22 = P22 - P23
    R_p = np.matmul(np.array([v21.T.ravel(), v22.T.ravel(), np.cross(v21.T.ravel(), v22.T.ravel())]).T,
                    np.linalg.inv(np.array([v11.T.ravel(), v12.T.ravel(), np.cross(v11.T.ravel(), v12.T.ravel())]).T))
    U, S, Vt = np.linalg.svd(R_p)
    R = np.matmul(U, Vt)
    t = P21 - np.matmul(R, P11)
    return R, t

# Perform adaptive RANSAC
def RANSAC(matches):
    e = 0.5
    N = math.inf
    sample_count = 0
    r = np.random.default_rng(341532125)
    thresh = 20
    T = (1 - e) * len(matches)
    largest_S = []
    best_Rt = None
    p = 0.95
    while N > sample_count:
        sample = r.choice(len(matches), 3, replace=False)
        _, _, x, y, z = matches[sample[0]][1]
        P21 = np.array([[x, y, z]]).T
        _, _, x, y, z = matches[sample[0]][0]
        P11 = np.array([[x, y, z]]).T
        _, _, x, y, z = matches[sample[1]][1]
        P22 = np.array([[x, y, z]]).T
        _, _, x, y, z = matches[sample[1]][0]
        P12 = np.array([[x, y, z]]).T
        _, _, x, y, z = matches[sample[2]][1]
        P23 = np.array([[x, y, z]]).T
        _, _, x, y, z = matches[sample[2]][0]
        P13 = np.array([[x, y, z]]).T
        R, t = get_model(P11, P12, P13, P21, P22, P23)
        inliers = []
        for match in matches:
            _, _, x, y, z = match[1]
            P1 = np.array([[x, y, z]]).T
            _, _, x, y, z = match[0]
            P2 = np.array([[x, y, z]]).T
            if distance(R, t, P1, P2) < thresh:
                inliers.append(matches)
        if len(inliers) > T:
            return R, t
        else:
            if len(inliers) > len(largest_S):
                largest_S = inliers
                best_Rt = R, t
        e = 1 - (len(inliers) / len(matches))
        N = math.log(1 - p) / math.log(1 - math.pow(1 - e, sample_count))
        sample_count += 1
        T = (1 - e) * len(matches)
    return best_Rt