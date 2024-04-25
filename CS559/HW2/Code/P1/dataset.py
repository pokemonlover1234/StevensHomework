# Load in the dataset, split into test and training sets,
# and returns sets to caller.

import numpy as np
import math

def read_set(filename):
    data = []
    with open(filename, "r") as dataset:
        instances = dataset.readlines()
        for datapoint in instances:
            data.append([float(x) if x != "?" else -9.0 for x in datapoint.strip().split(",")])
    return data

def split_train_test(data):
    # Fixed-seed for deterministic result.
    rand = np.random.default_rng(1015987133450)
    testset, trainset = np.split(rand.permutation(data), [math.floor(len(data)/5)])
    return testset, trainset

def split_train_to_class(trainset):
    C1 = [t for t in trainset if t[13] == 0]
    C2 = [t for t in trainset if t[13] != 0]
    return C1, C2

def get_dataset_processed(filename):
    data = read_set(filename)
    testset, trainset = split_train_test(data)
    C1, C2 = split_train_to_class(trainset)
    return C1, C2, testset