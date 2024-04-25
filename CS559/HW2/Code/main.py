from P1.dataset import get_dataset_processed as get_p1_dataset
from P1.Fisher import do_LDA

from P2_2.dataset import get_dataset_processed as get_p2_2_dataset
from P2_2.KFoldCrossValidation import KFoldCrossValidation as P2KFold
from P2_2.LogisticRegression import loss as logisticloss, rpa as logisticrpa

from P2_3.dataset import get_dataset_processed as get_p2_3_datset
from P2_3.KFoldCrossValidation import KFoldCrossValidation as P3KFold
from P2_3.ProbGenerModel import rpa

from P3.dataset import get_dataset_processed as get_p3_dataset
from P3.NaiveBayes import evaluate_model


def main():
    trainC1, trainC2, testset = get_p1_dataset("../processed.cleveland.data")
    do_LDA(trainC1, trainC2, testset)
    # Results for problem 1: Output of do_LDA
    # Chosen w: [[ 4.37725902e-03  6.74351296e-01  3.88990594e-01  9.94197607e-03
    # 5.98772208e-04 -1.48337775e-01  1.20918685e-01 -7.10796144e-03     
    # 4.95241402e-01  5.73658028e-02  2.19786069e-01  2.15629942e-01     
    # 1.17410686e-01]]
    # Determined threshold: 3.7235726510281584
    # Results of training: Chosen w gets:
    #     86.61417322834646% of C1 correct
    #     81.89655172413794% of C2 correct
    #     81.66666666666667% of test set correct.

    testsetp2_2, trainsetp2_2 = get_p2_2_dataset("../wdbc.data")
    best_stoch, err_stoch, best_mini, err_mini = P2KFold(5, trainsetp2_2) 
    print(f"Best stochastic model: w = {best_stoch}\n\tModel Error on training set = {err_stoch}\nBest Minibatch model: w = {best_mini}\n\tModel Error on training set = {err_mini}")
    print("Evaluating models on test set...")
    testerr_mini = logisticloss(best_mini, testsetp2_2)
    testerr_stoch = logisticloss(best_stoch, testsetp2_2)
    print(f"Evaluation complete.\n\tStochastic Model Error on Test Set: {testerr_stoch}\n\tMinibatch Model Error on Test Set: {testerr_mini}")
    print(f"Recall, Precision, Accuracy on test set: \n\tStochastic Model: {logisticrpa(best_stoch, testsetp2_2)}\n\tMinibatch Model: {logisticrpa(best_mini, testsetp2_2)}")
    # Output of this section present in P2_2/P2_2Output.txt

    testsetp2_3, trainsetp2_3 = get_p2_3_datset("../wdbc.data")
    best_model, perf_model = P3KFold(5, trainsetp2_3)
    rpat = rpa(best_model[0], best_model[1], testsetp2_3)
    print(f"Best model:\n\tw = {best_model[0]}\n\tw0 = {best_model[1]}\n\tTest Set Recall: {rpat[0]}\n\tTest Set Precision: {rpat[1]}\n\tTest Set Accuracy: {rpat[2]}\n\tPerf Metric (R*P*A): {rpat[0]*rpat[1]*rpat[2]}")
    # Output of this section present in P2_3/P2_3Output.txt

    p3trainC1, p3trainC2, p3test = get_p3_dataset("../a2-q3/pg1661.txt", "../a2-q3/pg31100.txt")
    accuracy = evaluate_model(p3trainC1, p3trainC2, p3test)
    print(f"Accuracy of Naive Bayes Model (right/(right + wrong)) = {accuracy}")
if __name__ == "__main__":
    main()