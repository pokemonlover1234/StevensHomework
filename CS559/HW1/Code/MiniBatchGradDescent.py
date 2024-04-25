# Using L2 regularized loss function
# Gradient using chain-rule
# Loss = sum(f-y)^2 + w^tw
# sum2*(f-y)xi+2w
# where f is wTx

import RidgeRegression
import math

BASE_LEARN_RATE = 0.000001

# Splits the given dataset into batches. 
def get_batches(data, batch_size = 50):
    def batches_generator():
        i = 0
        while i * batch_size < len(data):
            yield data[i*batch_size: (i + 1) * batch_size]
            i += 1
        return
    return batches_generator

def gradient(data, guess_w):
    grad = [0] * 26
    for pt in data:
        part = 2 * (RidgeRegression.f(guess_w, pt) - pt[26])
        partx = [part * elem for elem in pt]
        grad = [x + g for x, g in zip(partx, grad)]
    grad = [(g + 2 * w) * 1 / len(data) for g, w in zip(grad, guess_w)]
    return grad
        
def minibatch_descent(data):
    w = [0] * 26
    print(f"Starting gradient descent.")
    for i in range(50):
        if i % 10 == 0:
            print(f"Iteration {i}/50")
        batches_generator = get_batches(data, batch_size = 50)
        accumulate_grad = [0.00000001]*26
        for batch in batches_generator():
            grad = gradient(batch, w)
            accumulate_grad = [a + (g*g) for a, g in zip(accumulate_grad, grad)]
            # Update the model. Uses Adagrad to apply learning rate.
            w = [elem - (BASE_LEARN_RATE/(math.sqrt(i + 1)))/(math.sqrt(1/(i+1)*accumulate_grad[j]))*g for j, (elem, g) in enumerate(zip(w, grad))]
    return w