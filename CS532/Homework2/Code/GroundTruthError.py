# Computes the error of the disp map provided to the ground truth.

import numpy as np

def GroundTruthErr(GroundTruth, DispMap):
    GroundTruthDiv = np.round((GroundTruth / 4))
    Diff = np.abs(GroundTruthDiv-DispMap)
    return (Diff > 1).sum()/(GroundTruth.shape[0]*GroundTruth.shape[1])

def GroundTruthErrPKRN(GroundTruth, DispMap, PKRN):
    GroundTruthDiv = np.round((GroundTruth / 4))
    Median = np.median(PKRN)
    Diff = np.abs(GroundTruthDiv-DispMap)
    Keep = (PKRN > Median)
    Kept = np.count_nonzero(Keep)
    return np.logical_and(Diff > 1, Keep).sum() / Kept, Kept