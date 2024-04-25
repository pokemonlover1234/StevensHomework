# Sets up functions related to logistic regression
# Namely, the loss function, f(x) = sigmoid(x), and the gradient function.
# Note that w contains w0, the bias term, and x will contain 
# a 1 in the first slot to accomodate the math. 

# as in problem 1, w and x are horizontal but the math in the 
# slides assumes they are vertical, so transpose presence
# is reversed to accomodate.


import numpy as np
import math

# Returns result of the sigmoid function. Assumes that the
# actual result, yn, is not included in x

def sigmoid(w, x):
    try:
        return 1/(1+math.exp(-np.matmul(w, x.T)))
    except OverflowError:
        #Occurs if -np.matmul(w, x.T) exceeds ~700.
        #If this happens, we can safely assume that
        #1+math.exp(~700) ~ INF
        #Thus 1/(~INF) ~ 0
        return 0

# data is assumed to contain the actual diagnostic in the last index of each x
# dataset in text has it in 2nd, but it is adjusted in P2.2's dataset.py

# Class C1, yn = 1, is Benign, Class C2, yn = 0, is malignant
def loss(w, data):
    prod = 1
    for point in data:
        prod *= math.pow(sigmoid(w, point[:-1]), point[-1]) * math.pow(1 - sigmoid(w, point[:-1]), 1 - point[-1])
    return -math.log(prod)

# Computes the gradient of the loss function using the gradient function
# we derived/proved in 2.1

def gradient(w, batch):
    g = np.zeros(batch[0].shape[0]-1)
    for point in batch:
        g += (sigmoid(w, point[:-1]) - point[-1]) * point[:-1]
    return g

# Reports (recall, precision, accuracy) using 0.5 as a threshold point.

def rpa(w, data):
    tp = 0
    fp = 0
    tn = 0
    fn = 0
    for point in data:
        res = sigmoid(w, point[:-1])
        #Class C1, yn=1 is benign
        if res > 0.5 and point[-1] == 1:
            tn += 1
        elif res <= 0.5 and point[-1] == 1:
            fp += 1
        elif res > 0.5 and point[-1] == 0:
            fn += 1
        else:
            tp += 1
    return (tp/(tp+fn),tp/(tp+fp),(tp+tn)/(tp+tn+fp+fn))
