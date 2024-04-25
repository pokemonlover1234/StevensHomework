# Implements a 1-hidden-layer Neural Network

import numpy as np
import gzip
import pickle
from tqdm import trange
import matplotlib.pyplot as plt
from sklearn.neural_network import MLPClassifier

def list_to_min(l):
    return np.min(l)

def train_hiddenlayer_nodecount(datafile):
    # Load dataset
    f = gzip.open(datafile, 'rb')
    train_set, valid_set, test_set = pickle.load(f, encoding='latin1')
    f.close()
    # Split up sets into X and Y arrays
    train_x, train_y = train_set
    valid_x, valid_y = valid_set
    test_x, test_y = test_set
    # Define error tracking lists and minimum error trackers
    trainerr = []
    validerr = []
    testerr = []
    minvaliderr = None
    minvaliderri = None
    mintesterr = None
    minvaliderri = None
    mintrainerr = None
    minvaliderri = None
    # Train neural networks with a hidden layer containing hn nodes, for hn from 1 to 50
    for hn in trange(1, 51):
        # Creates the neural network. Chooses it's parameters to be what we learned in class (i.e. 1 hidden layer, logistic activation, stochastic gradient descent)
        clf = MLPClassifier(hidden_layer_sizes=(hn,), activation="logistic", solver="sgd", learning_rate='adaptive', max_iter=500, random_state=35135253, learning_rate_init=0.1)
        # Stores list of errors for plotting later
        thistrainerr = []
        thisvaliderr = []
        thistesterr = []
        # Tracks minimum errors for this network
        thismintrainerr = None
        thisminvaliderr = None
        # Used in early stopping to track non improvement of errors
        nonimprovetrain = 0
        nonimprovevalid = 0
        # Tolerance of learning. Improvements less than this are treated as non improvement
        tol = 0.0001
        # Run a training iteration, store the errors on this iteration, then update
        # non improvement tracking, and stop if necessary
        for i in trange(500, leave=False, desc=f"Training with {hn} hidden nodes"):
            clf.partial_fit(train_x, train_y, classes=[0,1,2,3,4,5,6,7,8,9])
            thistrainerr.append(1-clf.score(train_x, train_y))
            thisvaliderr.append(1-clf.score(valid_x, valid_y))
            thistesterr.append(1-clf.score(test_x, test_y))
            nonimprovetrain = nonimprovetrain + 1 if thismintrainerr is not None and thismintrainerr - thistrainerr[-1] < tol else 0
            nonimprovevalid = nonimprovevalid + 1 if thisminvaliderr is not None and thisminvaliderr - thisvaliderr[-1] < tol else 0
            thismintrainerr = thistrainerr[-1] if thismintrainerr is None or thismintrainerr > thistrainerr[-1] else thismintrainerr
            thisminvaliderr = thisvaliderr[-1] if thisminvaliderr is None or thisminvaliderr > thisvaliderr[-1] else thisminvaliderr
            # Early stop if training error OR validation error have not improved by at least tol in the last 5 iterations
            if nonimprovetrain == 5 or nonimprovevalid == 5:
                break
        # Store error lists and update overall minimum errors
        trainerr.append(thistrainerr)
        validerr.append(thisvaliderr)
        testerr.append(thistesterr)
        if mintesterr is None or min(thistesterr) < mintesterr:
            mintesterr = min(thistesterr)
            mintesterri = hn - 1
        if minvaliderr is None or min(thisvaliderr) < minvaliderr:
            minvaliderr = min(thisvaliderr)
            minvaliderri = hn - 1
        if mintrainerr is None or min(thistrainerr) < mintrainerr:
            mintrainerr = min(thistrainerr)
            mintrainerri = hn - 1
    # Create a list of minimum errors per network
    minvaliderrs = []
    mintrainerrs = []
    mintesterrs = []
    for l in trainerr:
        mintrainerrs.append(list_to_min(l))
    for l in validerr:
        minvaliderrs.append(list_to_min(l))
    for l in testerr:
        mintesterrs.append(list_to_min(l))
    
    # Plot everything
    plt.plot(np.arange(1, len(validerr[minvaliderri]) + 1), validerr[minvaliderri])
    plt.title(f'Validation Error over network with minimum validation error ({minvaliderri + 1} hidden nodes)')
    plt.xlabel('Iterations')
    plt.ylabel('Validation Error')
    plt.show()
    plt.plot(np.arange(1, len(testerr[mintesterri]) + 1), testerr[mintesterri])
    plt.title(f'Test Error over network with minimum testing error ({mintesterri + 1} hidden nodes)')
    plt.xlabel('Rounds')
    plt.ylabel('Test Errors')
    plt.show()
    plt.plot(np.arange(1, len(trainerr[mintrainerri]) + 1), trainerr[mintrainerri])
    plt.title(f'Training Error over network with minimum training error ({mintrainerri + 1} hidden nodes)')
    plt.xlabel('Rounds')
    plt.ylabel('Test Errors')
    plt.show()
    plt.plot(np.arange(1, 51), mintrainerrs, '-b', label = "Train Error")
    plt.plot(np.arange(1, 51), minvaliderrs, '-g', label = "Validation Error")
    plt.plot(np.arange(1, 51), mintesterrs, '-r', label = "Testing Error")
    plt.legend()
    plt.title("Minimum errors as a function of hidden node count")
    plt.xlabel("Number of nodes in hidden layer")
    plt.ylabel("Minimum error")
    plt.show()

    print(f"Minimum Errors: \n\tTrain: {np.min(np.min(trainerr))}\n\tValidation:{np.min(np.min(validerr))}\n\tTest:{np.min(np.min(testerr))}")