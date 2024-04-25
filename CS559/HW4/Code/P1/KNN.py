import numpy as np
from functools import cmp_to_key
from tqdm import tqdm

# Sufficient to compare square of distance, 
# so no square roots necessary
def dist(X1, X2):
    dist = (X1 - X2) ** 2
    return np.sum(dist)

# Sorts list, assuming None is greater than all.
# Sorts of form [ (a, b), (c, d), ...]
def none_cmp(a, b):
    x = a[0]
    y = b[0]
    if x is None and y is None:
        return 0
    if x is None:
        return 1
    if y is None:
        return -1
    if x < y:
        return -1
    if x > y:
        return 1
    return 0

none_cmpkey = cmp_to_key(none_cmp)

def eval_KNN(trainset, validset, K):
    # Return number of validation errors.
    err = 0
    # For each validation example, get K closest training examples
    # and guess the most numerous class. Increment error if incorrect.
    for validex in tqdm(validset, desc="Evaluating", leave=False):
        minsqdist = [ ( None, None ) ] * K
        for trainex in trainset:
            X1 = trainex['X']
            X2 = validex['X']
            d = dist(X1, X2)
            # Because of sorting, biggest error will be on the rightmost slot
            # Can only consider biggest error, because if new dist is smaller
            # than any error in the list, the biggest error would be pushed
            # out anyway.
            if none_cmp((d, trainex), minsqdist[-1]) == -1:
                minsqdist[-1] = (d, trainex)
                minsqdist = sorted(minsqdist, key=none_cmpkey)
        guesses = [ex['Y'] for (_, ex) in minsqdist]
        vals, counts = np.unique(guesses, return_counts=True)
        mode_value = np.argwhere(counts == np.max(counts))
        guess = vals[mode_value].flatten().tolist()[0]
        if guess != validex['Y']:
            err += 1
    return err
