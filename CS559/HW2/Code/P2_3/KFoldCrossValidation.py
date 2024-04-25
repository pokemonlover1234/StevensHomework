import numpy as np
from .dataset import split_train_class
from .ProbGenerModel import do_MLE_Generative, rpa

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
    result_models = []
    model_perf = []
    for i in range(K):
        print(f"Starting training with set {i + 1} of {K} as validation set.")
        validation_set = sets[i]
        training_data = []
        for j in range(K):
            if j != i:
                training_data.extend(sets[j])
        C1, C2 = split_train_class(training_data)
        w, w0 = do_MLE_Generative(C1, C2)
        result_models.append([w, w0])
        print(f"MLE complete. Model: {result_models[i]}. Calculating RPA.")
        rpat = rpa(result_models[i][0], result_models[i][1], validation_set)
        print(f"Recall, precision, accuracy on validation set: {rpat}")
        print(f"Performance Metric (R*P*A): {rpat[0]*rpat[1]*rpat[2]}")
        model_perf.append(rpat[0]*rpat[1]*rpat[2])
    print("KFold complete. Selecting best model...")
    best_perf = None
    best_perf_ind = None
    for i in range(K):
        if best_perf is None or best_perf < model_perf[i]:
            best_perf = model_perf[i]
            best_perf_ind = i

    return result_models[best_perf_ind], best_perf