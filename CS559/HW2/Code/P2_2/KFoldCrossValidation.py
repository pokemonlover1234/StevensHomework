import numpy as np
from .LogisticRegression import *
from .GradientDescent import *

# Creates K = 5 partitions of the training data and 
# runs K-fold cross validation on them.

def split_trainingset(K, training_data):
    rand = np.random.default_rng(1723059183)
    indices = []
    l = training_data.shape[0]
    per = l // K
    rem = l % K
    for i in range(1,K):
        if i < rem:
            indices.append(per * i + i)
        else:
            indices.append(per * i + rem)
    return np.split(rand.permutation(training_data), indices)

def KFoldCrossValidation(K, data):
    sets = split_trainingset(K, data)
    result_models_stoch = []
    result_models_mini = []
    model_average_err_stoch = []
    model_average_err_mini = []
    for i in range(K):
        print(f"Starting training with set {i + 1} of {K} as validation set.")
        validation_set = sets[i]
        training_data = []
        for j in range(K):
            if j != i:
                training_data.extend(sets[j])
        result_models_stoch.append(stoch_descent(training_data))
        print(f"Stochastic Training complete. Model: {result_models_stoch[i]}. Calculating error.")
        model_average_err_stoch.append(loss(result_models_stoch[i], validation_set))
        print(f"Error for this model on validation set: {model_average_err_stoch[i]}")
        rpat = rpa(result_models_stoch[i], validation_set)
        print(f"Recall, precision, accuracy on validation set: {rpat}")
        result_models_mini.append(minibatch_descent(training_data))
        print(f"Minibatch Training complete. Model: {result_models_mini[i]}. Calculating error.")
        model_average_err_mini.append(loss(result_models_mini[i], validation_set))
        print(f"Error for this model on validation set: {model_average_err_mini[i]}")
        rpat = rpa(result_models_mini[i], validation_set)
        print(f"Recall, precision, accuracy on validation set: {rpat}")
    print("KFold complete. Selecting best model...")
    least_error_mini = None
    least_error_stoch = None
    least_error_ind_mini = None
    least_error_ind_stoch = None
    for i in range(K):
        if least_error_mini is None or least_error_mini > model_average_err_mini[i]:
            least_error_mini = model_average_err_mini[i]
            least_error_ind_mini = i
        if least_error_stoch is None or least_error_stoch > model_average_err_stoch[i]:
            least_error_stoch = model_average_err_stoch[i]
            least_error_ind_stoch = i
    return result_models_stoch[least_error_ind_stoch], least_error_stoch, result_models_mini[least_error_ind_mini], least_error_mini