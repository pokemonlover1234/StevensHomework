from P1.CrossValidation import cross_validation as knn_cross_validation
from P1.Dataset import Dataset as knn_data
from P5.EM import EM
import numpy as np

def main():
    # data = knn_data("../yeast.data")
    # knn_model, knn_err, knn_k = knn_cross_validation(10, 10, data)
    # print(f"Best model K: {knn_k}\nBest model error = {knn_err}")
    EM_data = np.loadtxt("../a4-q5-data/multigauss.txt")
    e = EM(EM_data, 5, 100)
    e.run_to_completion()
    e.show_plot()

if __name__ == "__main__":
    main()