# We are using the MLE solution to the generative
# model. We need 4 elements: gamma, mu1, mu2, and Sigma
# where:
#   gamma = p(C1)
#   mu1 = mean of C1
#   mu2 = mean of C1
#   Sigma = covariance matrix
# All of which have solutions in the MLE solution.
# Using the slides, this file defines the closed-form MLE solutions for the values,
# from which MLE(w) and MLE(w0) can be obtained. 

# The functions in this file take the data 
# already split into classes C1 and C2
# Functions expect the actual value of the result
# to already be removed, since they can be inferred
# from which class the point belongs in

# Does not expect a 1 in the first element of x

# Like P2_2, yn=1 = C1 = Benign
# yn=0 = C2 = malignant

import numpy as np
import math

def sigmoid(w, w0, x):
    try:
        return 1/(1+math.exp(-np.matmul(w, x.T) - w0))
    except OverflowError:
        #Occurs if -np.matmul(w, x.T) exceeds ~700.
        #If this happens, we can safely assume that
        #1+math.exp(~700) ~ INF
        #Thus 1/(~INF) ~ 0
        return 0

def MLE_gamma(C1, C2):
    return len(C1)/(len(C1) + len(C2))

# Since yn = 0 if C2, and mu1 considers C1,
# can just use C1 set here, since 0C2 = 0
def MLE_mu1(C1):
    return 1/len(C1) * np.sum(C1, axis=0)

# similarly, C2 has yn = 0, so 1 - yn = 1

def MLE_mu2(C2):
    return 1/len(C2) * np.sum(C2, axis=0)

# Again, math in slides assumes vertical vectors,
# so presence of transposes are reversed

def MLE_Sigma(C1, C2, mu1, mu2):
    N1 = len(C1)
    N2 = len(C2)
    N = N1 + N2
    C1M = C1 - mu1
    C2M = C2 - mu2
    S1 = np.matmul(np.matrix(C1M[0]).T, np.matrix(C1M[0]))
    for i in range(1, N1):
        S1 += np.matmul(np.matrix(C1M[i]).T, np.matrix(C1M[i]))
    
    S2 = np.matmul(np.matrix(C2M[0]).T, np.matrix(C2M[0]))
    for i in range(1, N2):
        S1 += np.matmul(np.matrix(C2M[i]).T, np.matrix(C2M[i]))
    
    S1 /= N1
    S2 /= N2

    return N1/N * S1 + N2/N + S2

def MLE_w0(mu1, mu2, Sigma, gamma):
    w00 = -1/2 * mu1
    w00 = np.matrix(w00)
    w00 = np.matmul(w00, np.linalg.inv(Sigma))
    w00 = np.matmul(w00, np.matrix(mu1).T)
   
    w01 = 1/2 * mu2
    w01 = np.matrix(w01)
    w01 = np.matmul(w01, np.linalg.inv(Sigma))
    w01 = np.matmul(w01, np.matrix(mu2).T)
    
    w02 = math.log(gamma/(1 - gamma))

    return w00 + w01 + w02

# Returns horizontal w

def MLE_w(Sigma, mu1, mu2):
    return np.matmul(np.linalg.inv(Sigma), np.matrix(mu1 - mu2).T).T

#returns w, w0

def do_MLE_Generative(C1, C2):
    mu1 = MLE_mu1(C1)
    mu2 = MLE_mu2(C2)
    gamma = MLE_gamma(C1, C2)
    Sigma = MLE_Sigma(C1, C2, mu1, mu2)
    return MLE_w(Sigma, mu1, mu2), MLE_w0(mu1, mu2, Sigma, gamma)

# get Recall, precision, accuracy

def rpa(w, w0, data):
    tp = 0
    fp = 0
    tn = 0
    fn = 0
    for point in data:
        res = sigmoid(w, w0, point[:-1])
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
