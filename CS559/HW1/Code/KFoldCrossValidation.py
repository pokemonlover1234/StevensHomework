from operator import mod
from statistics import mode
import MiniBatchGradDescent
import RidgeRegression

# Splits dataset into K partitions
def split_dataset(K, data):
    points = len(data)
    per = points // K
    rem = points % K
    sets = []
    # Get K equal sized partitions, first remainder(points/K)
    # will contain one extra data point.
    for i in range(K):
        if i < rem:
            sets.append(data[i * per + i: (i + 1) * per + i + 1])
        else:
            sets.append(data[i * per + rem: (i + 1) * per + rem])
    return sets

def KFoldCrossValidation(K, data):
    sets = split_dataset(K, data)
    result_models = []
    model_average_err = []
    for i in range(K):
        print(f"Starting training with set {i + 1} of {K} as validation set.")
        validation_set = sets[i]
        training_data = []
        for j in range(K):
            if j != i:
                training_data.extend(sets[j])
        result_models.append(MiniBatchGradDescent.minibatch_descent(training_data))
        print(f"Training complete. Model: {result_models[i]}. Calculating error.")
        model_average_err.append(RidgeRegression.averageloss(validation_set, result_models[i]))
        print(f"Average squared error for this model on validation set: {model_average_err[i]}")
    print("KFold complete. Selecting best model...")
    least_error = None
    least_error_ind = None
    for i in range(K):
        if least_error is None or least_error > model_average_err[i]:
            least_error = model_average_err[i]
            least_error_ind = i
    return result_models[least_error_ind], least_error