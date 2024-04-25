import numpy as np
import math
from tqdm import trange


# Yields a randomly generated positive definite matrix
# by generating a randomly sized symmetric matrix with
# positive diagonal elements
def pd_generator(seed=None, minsize=2, maxsize=30):
    r = np.random.default_rng(seed)
    while True:
        # Choose a random size between minsize and maxsize
        s = math.floor((maxsize - minsize) * r.random() + minsize)
        # Generate a fully random array
        res = r.standard_normal(size=(s, s))
        # Convert to symmetric matrix
        res = (res + res.T)/2
        # Ensure diagonal dominance
        # Reference: https://en.wikipedia.org/wiki/Diagonally_dominant_matrix
        for i in range(s):
            res[i, i] = np.sum(np.abs(res[i, np.arange(s) != i])) + r.random()
        yield res


# Sylvester's Criterion
def sylvesters(A):
    s = A.shape[0]
    for i in range(1, s+1, 1):
        if np.linalg.det(A[:i, :i]) <= 0:
            return False
    return True


# Run 1 million tests
def main():
    g = pd_generator()
    for _ in trange(1000000):
        A = next(g)
        assert sylvesters(A)


if __name__ == "__main__":
    main()
