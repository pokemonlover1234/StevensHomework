# All implemented in this script.
# Standalone solution meant only to produce the answers
# given in problem 4 in the pdf, so main.py does not 
# interact with this file.

import numpy as np
import math

tol = 0.001 # Convergence tolerance

# Assign dataset and initial means

Dataset = np.array([
    (5.5, 4.2),
    (5.1, 3.8),
    (4.7, 3.2),
    (5.9, 3.2),
    (4.9, 3.1),
    (5.0, 3.0),
    (4.6, 2.9),
    (6.0, 3.0),
    (6.2, 2.8),
    (6.7, 3.1)
])

Means = np.array([
    (6.2, 3.2),
    (6.6, 3.7),
    (6.5, 3.0)
])

# Readability constants

RED = 0
GREEN = 1
BLUE = 2

# Define assignments array. Value is index into Means 
# array. Set to RED to start but this is immediately
# updated in step 1 so doesn't matter

Assignments = np.repeat(RED, 10)

def euclidean_dist(pt1, pt2):
    return math.sqrt(np.sum(np.square(pt1 - pt2)))

# Get a point's assignment by closest mean

def get_pt_assignment(pt):
    return np.argmin(np.array([
        euclidean_dist(pt, Means[RED]), 
        euclidean_dist(pt, Means[GREEN]),
        euclidean_dist(pt, Means[BLUE])
    ]))

# Update point assignments

def assign_points():
    for i in range(10):
        Assignments[i] = get_pt_assignment(Dataset[i])

# Update means using numpy's boolean filter approach

def update_means():
    reds = Dataset[np.array(Assignments == RED)]
    greens = Dataset[np.array(Assignments == GREEN)]
    blues = Dataset[np.array(Assignments == BLUE)]
    Means[RED] = np.mean(reds, axis = 0)
    Means[GREEN] = np.mean(greens, axis = 0)
    Means[BLUE] = np.mean(blues, axis = 0)

# Run iterations of the algorithm to convergence. 
# Print interim results

def run_kmeans():
    old_means = Means.copy()
    i = 1
    while True:
        assign_points()
        update_means()
        print(f"Means after iteration {i}:\n\tRed: {Means[RED]}\n\tGreen: {Means[GREEN]}\n\tBlue: {Means[BLUE]}\n")
        if np.all(np.abs(Means - old_means) < tol):
            print(f"Converged at iteration {i - 1}")
            break
        i += 1
        old_means = Means.copy()

if __name__ == "__main__":
    run_kmeans()
    