#Since we have 26 datapoints per feature, model is w, a vector of 26 values.
#Feature is a single feature/

ALPHA = 1

def f(w, x):
    res = 0
    for i in range(26):
        res += w[i] * x[i]
    return res


def RidgeLoss(data, model):
    loss = 0
    regularization = 0
    for coeff in model:
        regularization += ALPHA * (coeff * coeff)
    for datapt in data:
        #index 26 is expected value
        sumterm= f(model, datapt) - datapt[26]
        loss += sumterm * sumterm
    return loss + regularization

def averageloss(data, model):
    return RidgeLoss(data, model)/len(data)