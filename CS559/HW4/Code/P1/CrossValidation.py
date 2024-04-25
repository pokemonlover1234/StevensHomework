import numpy as np
from P1.KNN import eval_KNN
from tqdm import trange

def cross_validation(K, KNN_MAXK, data):
    split = data.split_dataset(K)
    model_best = None
    model_best_err = None
    model_best_K = None
    # For each KNN k from 1 to 10, run k-fold cross validation with
    # K=10. Choose the best overall model.
    for i in trange(1, KNN_MAXK + 1, desc="Cross Validation of KNN"):
        for j in trange(K, desc="Evaluating this K", leave=False):
            validation = split[j]
            conc = []
            conc.extend([arr for arr in split[:j]])
            conc.extend([arr for arr in split[j+1:]])
            train = np.concatenate(conc)
            err = eval_KNN(train, validation, i) / len(validation)

            if model_best_err is None or err < model_best_err:
                model_best_err = err
                model_best = train
                model_best_K = i
    return model_best, model_best_err, model_best_K


