# Implements AdaBoost using sklearn's decision trees

from sklearn import tree
from sklearn.preprocessing import OrdinalEncoder
import numpy as np
import matplotlib.pyplot as plt
import math
from tqdm import trange, tqdm
import math

def sigmoid(alpha):
    return 1/(1+math.exp(-alpha))

class AdaBoost():
    def __init__(self, data):
        self.X, self.Y = data.get_raw_data_arrays()
        # Necessary because we have categorical features.
        self.enc = OrdinalEncoder()
        self.enc.fit(self.X)
        self.X = self.enc.transform(self.X)
        self.weights = np.repeat(1/len(self.Y),len(self.Y))
        self.trees = []
        self.alphas = []

    def encode(self, X):
        return self.enc.transform(X)

    # Evaluates the current tree on the test set
    # Returns error rate
    def eval_current_tree(self):
        tree = self.trees[-1]
        predictions = tree.predict(self.X)
        return np.sum(np.equal(predictions, self.Y)) / len(self.Y)
    
    # Same as above, except returns predictions.

    def current_tree_predict_dataset(self):
        return self.trees[-1].predict(self.X)

    def get_current_e(self):
        tree = self.trees[-1]
        e = np.sum(self.weights * (np.not_equal(self.current_tree_predict_dataset(), self.Y))) / np.sum(self.weights)
        return e
        
    def get_current_alpha(self):
        e = self.get_current_e()
        return 1 / 2 * math.log((1-e)/e)

    def perform_adastep(self):
        clf = tree.DecisionTreeClassifier()
        clf = clf.fit(self.X, self.Y, self.weights)
        self.trees.append(clf)
        alpha = self.get_current_alpha()
        self.alphas.append(alpha)
        predictions = self.current_tree_predict_dataset()
        alpha_array = np.repeat(alpha, len(self.Y))
        alpha_weight_array = alpha_array * np.array([-1 if y == py else 1 for y, py in zip(self.Y, predictions)])
        self.weights *= 1 / np.sum(self.weights) * np.exp(alpha_weight_array)

    # Predicts an example

    def ada_predict(self, x):
        predictor = 0
        x = self.encode([list(x)])
        for alpha, tree in zip(self.alphas, self.trees):
            predictor += alpha * tree.predict(x)
        return np.sign(predictor)

    # Evaluates current tree.

    def ada_error(self, data):
        X, Y = data.get_raw_data_arrays()
        errors = 0
        for x, y in tqdm(zip(X, Y), leave=False, desc="Performing Error Calculation", total = len(X)):
            if self.ada_predict(x) != y:
                errors += 1
        return errors / len(Y)

def train_ada(train, test):
    Ada = AdaBoost(train)
    errors_train = []
    errors_test = []
    Rounds = np.arange(1, 501)
    for i in trange(500):
        Ada.perform_adastep()
        errors_train.append(Ada.ada_error(train))
        errors_test.append(Ada.ada_error(test))
    print(f"Lowest Training Error: {min(errors_train)}")
    print(f"Lowest Testing Error: {min(errors_test)}")
    print(f"Last Training Error: {errors_train[-1]}")
    print(f"Last Testing Error: {errors_test[-1]}")
    plt.plot(Rounds, errors_train)
    plt.title('Train Error over Ada rounds')
    plt.xlabel('Rounds')
    plt.ylabel('Train Error')
    plt.show()
    plt.plot(Rounds, errors_test)
    plt.title('Testing Error over Ada rounds')
    plt.xlabel('Rounds')
    plt.ylabel('Test Errors')
    plt.show()
