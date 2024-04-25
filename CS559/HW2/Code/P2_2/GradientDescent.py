from .LogisticRegression import *
import numpy as np
import math 

BASE_LEARN_RATE = 0.00001

def get_batches(data, batch_size = 50):
    def batches_generator():
        i = 0
        while i * batch_size < len(data):
            yield data[i*batch_size: (i + 1) * batch_size]
            i += 1
        return
    return batches_generator

def minibatch_descent(trainingset):
    w = np.array([0] * (len(trainingset[0]) - 1), np.float64)
    print("Starting Minibatch Gradient Descent")
    for i in range(50):
        if i % 10 == 0:
            print(f"Iteration {i}/50")
        batches_generator = get_batches(trainingset, batch_size = 50)
        accumulate_grad = np.array([0.0000000001] * (len(trainingset[0]) - 1))
        for batch in batches_generator():
            grad = gradient(w, batch)
            accumulate_grad += grad ** 2
            # With numpy, c/[arr] = [c/arr[1], ...]
            # np.multiply is element-wise mutiplication, 
            # np.multiply([a,b,c],[d,e,f]) = [ad,be,cf]
            # So, this is equivalent to my implementation of 
            # Adagrad in HW1, using numpy's array semantics.
            w -= np.multiply(np.divide(BASE_LEARN_RATE/math.sqrt(i+1),np.sqrt(1/(i+1)*accumulate_grad)), grad)
    return w

# Implements stochastic gradient descent

def stoch_descent(trainingset):
    w = np.array([0] * (len(trainingset[0])-1), np.float64)
    print("Starting Stochastic Gradient Descent")
    rand = np.random.default_rng(4584590235)
    for i in range(50):
        data = rand.permutation(trainingset)
        for example in data:
            grad = gradient(w, [example])
            # Decided to just use decreasing learnrate rather
            # than Adagrad here because I wasn't sure how 
            # well that would work considering how stochastic
            # descent functions.
            w -= BASE_LEARN_RATE/math.sqrt(i+1) * grad
    return w