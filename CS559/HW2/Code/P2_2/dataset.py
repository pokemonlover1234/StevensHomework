import numpy as np
import math

# Reads the dataset. Moves the second element to end, converts it to 1 if "B"
# and 0 if "M" for logistic regression result classes. Places a 1 at the start
# for the bias term.

# Removes first element as that is an id number and shouldn't be considered.

def read_set(filename):
    data = []
    with open(filename, "r") as dataset:
        instances = dataset.readlines()
        for datapoint in instances:
            data.append([float(x) for x in datapoint.strip().split(",")[1:] if x != "M" and x != "B"])
            data[-1].insert(0,1)
            data[-1].append(1 if datapoint.strip().split(",")[1] == "B" else 0)
    return np.array(data)

def split_train_test(data):
    # Fixed-seed for deterministic result.
    rand = np.random.default_rng(4324525485986)
    testset, trainset = np.split(rand.permutation(data), [math.floor(len(data)/5)])
    return testset, trainset

def get_dataset_processed(filename):
    data = read_set(filename)
    return split_train_test(data)