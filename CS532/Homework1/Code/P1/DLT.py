import numpy as np
correspondences = [
    [(246, 51), (1, 1)],
    [(404, 74), (500, 1)],
    [(22, 194), (1, 940)],
    [(280, 280), (500, 940)]
]


# Calculates Ai from the correspondence index
# Assuming wi = 1, wprimei = 1
def A(index):
    thispoint = correspondences[index]
    xi = np.array([thispoint[0][0], thispoint[0][1], 1])
    xprimei = np.array([thispoint[1][0], thispoint[1][1], 1])
    return np.matrix([
        [0, 0, 0,
            -xi[0], -xi[1], -xi[2],
            xprimei[1]*xi[0], xprimei[1]*xi[1], xprimei[1]*xi[2]],
        [xi[0], xi[1], xi[2],
            0, 0, 0, -xprimei[0]*xi[0],
            -xprimei[0]*xi[1], -xprimei[0]*xi[2]]
    ])


# Uses hardcoded correspondences to run DLT
# algorithm and returns homography.
def DLT():
    # Combines steps 1 and 2
    Amat = np.concatenate((A(0), A(1), A(2), A(3)))
    # Step 3
    _, _, vh = np.linalg.svd(Amat)
    v = vh.T
    col = v.shape[1]
    h = v[:, col-1]
    # Step 4
    H = np.reshape(h, (3, 3))
    return H

# Used to test returned homography on original corresponces as
# a sanity check to make sure I implemented the algorithm
# properly. No longer needed but included here for historical reasons.

# def test():
#     H = DLT()
#     for index in range(4):
#         thispoint = correspondences[index]
#         x = np.matrix([thispoint[0][0],thispoint[0][1],1]).T
#         print(np.matmul(H, x)/np.matmul(H, x).T[0,2])
