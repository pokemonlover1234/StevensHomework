# Last couple of homeworks I only used functions to manipulate data, but
# after seeing the solution for gradient descent that was shown in class
# I realized that classes that could store data was a really good idea,
# so I started using classes for this homework.

import Dataset
import P3.DecisionTree as P3DecisionTree
import P4.AdaBoost as P4AdaBoost
import P5.NeuralNetwork as P5NeuralNetwork

def main():
    # P3BData = Dataset.Dataset(filename = "../train.csv")
    # P3BData.apply_bucketing("Age", 10)
    # P3BData.apply_bucketing("Fare", 25)
    # P3Data = Dataset.Dataset(filename = "../train.csv")
    # P3TestData, P3TrainData = P3Data.split_train_test(0.2)
    # P3BTestData, P3BTrainData = P3BData.split_train_test(0.2)
    # P3TreeBIG = P3DecisionTree.DecisionTree(P3BTrainData, splitSelectType="InfGainBucket")
    # P3TreeBIG.train_tree()
    # P3TreeTIG = P3DecisionTree.DecisionTree(P3TrainData, splitSelectType="InfGainThreshold", thresholdAttrs=["Age", "Fare"])
    # P3TreeTIG.train_tree()
    # print(f"Information Gain Thresholded Tree train data accuracy: {P3DecisionTree.evaluate_tree(P3TreeTIG, P3BTrainData)}")
    # print(f"Information Gain Thresholded Tree testing data accuracy: {P3DecisionTree.evaluate_tree(P3TreeTIG, P3BTestData)}")
    # print(f"Information Gain Bucketed Tree train data accuracy: {P3DecisionTree.evaluate_tree(P3TreeBIG, P3BTrainData)}")
    # print(f"Information Gain Bucketed Tree testing data accuracy: {P3DecisionTree.evaluate_tree(P3TreeBIG, P3BTestData)}")
    # P3BTreeG = P3DecisionTree.DecisionTree(P3BTrainData, splitSelectType="GiniBucket")
    # P3BTreeG.train_tree()
    # print(f"Gini Index Bucketed Tree train data accuracy: {P3DecisionTree.evaluate_tree(P3BTreeG, P3BTrainData)}")
    # print(f"Gini Index Bucketed Tree testing data accuracy: {P3DecisionTree.evaluate_tree(P3BTreeG, P3BTestData)}")
    # P3TreeTG = P3DecisionTree.DecisionTree(P3TrainData, splitSelectType="GiniThreshold", thresholdAttrs=["Age", "Fare"])
    # P3TreeTG.train_tree()
    # print(f"Gini Index Thresholded Tree train data accuracy: {P3DecisionTree.evaluate_tree(P3TreeTG, P3TrainData)}")
    # print(f"Gini Index Thresholded Tree testing data accuracy: {P3DecisionTree.evaluate_tree(P3TreeTG, P3TestData)}")
    #P4AdaBoost.train_ada(P3BTrainData, P3BTestData)
    P5NeuralNetwork.train_hiddenlayer_nodecount("../mnist-1.pkl.gz")
if __name__ == "__main__":
    main()