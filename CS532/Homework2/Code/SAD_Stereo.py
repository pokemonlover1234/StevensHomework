# Implements the SAD disparity map stereo algorithm, with custom window size.
# Assumes odd window size
# Assumes rank transforms are equal in shape
# Searches for each matching window along entirety of epipolar line
# Slides mentioned taking rectification for granted, so assume
# all epipolar lines across each row. 
# Winner-take-all, lowest difference takes the cake

# Also computes PRKN measure simultaneously


import numpy as np
from tqdm import trange

def SAD(RankTransform1, RankTransform2, windowSize):
    SAD_dispmap = np.zeros(RankTransform1.shape)
    PKRN = np.zeros(RankTransform1.shape)
    offset = int((windowSize-1)/2)
    for r in trange(offset, RankTransform1.shape[0]-offset, desc="Computing SAD on rank transforms"):
        for c in range(offset, RankTransform1.shape[1]-offset):
            min_SAD = np.nan
            min_SAD_2 = np.nan
            disparity = 0
            # Uses the problem assumption that disparity is from 0 to 63
            for c2 in range(max(offset, c - 63), c+1):
                SAD = abs(RankTransform1[r-offset:r+offset+1, c-offset:c+offset+1] - RankTransform2[r-offset:r+offset+1, c2-offset:c2+offset+1]).sum()
                disparity = c - c2 if np.isnan(min_SAD) or SAD < min_SAD else disparity
                min_SAD_2 = min_SAD if np.isnan(min_SAD) or SAD < min_SAD else min_SAD_2
                min_SAD = SAD if np.isnan(min_SAD) or SAD < min_SAD else min_SAD
            SAD_dispmap[r, c] = disparity
            PKRN[r, c] = min_SAD_2/min_SAD if min_SAD > 0 and not np.isnan(min_SAD_2) else np.inf # Will be closer to 1 the closer 2nd smallest is to smallest.
                
    return SAD_dispmap, PKRN


#Normalizes to range of 0-255
#To be divided by 4 when processed.

def normalize_SAD(SAD):
    norm = 4
    return (SAD*norm).astype(np.uint8)
            