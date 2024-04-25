import numpy as np

# [:, :-1] removes the actual result element.

def get_m(train_class):
    return 1 / len(train_class) * np.sum(train_class[:,:-1], axis=0)

def get_S(train_class, class_m):
    # With numpy, [[...],[...],...] - [,,,] = [[...]-,,, , [...]-,,, , ...]
    ptminusm = train_class[:,:-1] - class_m
    # Note, since x and m are supposed to be vertical normally,
    # .T is used to get them to be vertical, and absence for the
    # horizontal.
    S = np.matmul(np.matrix(ptminusm[0]).T,np.matrix(ptminusm[0]))
    for elem in ptminusm[1:]:
        S += np.matmul(np.matrix(elem).T,np.matrix(elem))
    return S

def get_w_lda_and_thresh(C1, C2):
    tC1 = np.array(C1)
    tC2 = np.array(C2)
    m_C1 = get_m(tC1)
    m_C2 = get_m(tC2)
    S_neg = get_S(tC1, m_C1)
    S_pos = get_S(tC2, m_C2)
    S_W = S_neg + S_pos
    w = np.matmul(np.linalg.inv(S_W), m_C2 - m_C1)
    # Normalize w so ||w|| = 1
    w_normal = w / np.linalg.norm(w)
    threshold = 1/2 * (np.matmul(w_normal, np.matrix(m_C1).T) + np.matmul(w_normal, np.matrix(m_C2).T))
    return w_normal, threshold


def eval_train(w_LDA, C1, C2, testset, threshold):
    right_C1 = 0
    wrong_C1 = 0
    right_C2 = 0
    wrong_C2 = 0
    right_test = 0
    wrong_test = 0
    for elem in testset:
        f = np.matmul(np.matrix(w_LDA), np.matrix(elem[:-1]).T).flat[0]
        res = 1 if f > threshold else 0
        if ((res == 1 and elem[13] > 0) or (res == 0 and elem[13] == 0)):
            right_test += 1
        else:
            wrong_test += 1
    for elem in C1:
        f = np.matmul(np.matrix(w_LDA), np.matrix(elem[:-1]).T).flat[0]
        res = 1 if f > threshold else 0
        if res == 0:
            right_C1 += 1
        else:
            wrong_C1 += 1
    for elem in C2:
        f = np.matmul(np.matrix(w_LDA), np.matrix(elem[:-1]).T).flat[0]
        res = 1 if f > threshold else 0
        if res == 1:
            right_C2 += 1
        else:
            wrong_C2 += 1
    
    perf_C1 = (right_C1)/(wrong_C1+right_C1)*100
    perf_C2 = (right_C2)/(wrong_C2+right_C2)*100
    perf_test = (right_test)/(wrong_test+right_test)*100
    print(f"Results of training: Chosen w gets:\n\t{perf_C1}% of C1 correct\n\t{perf_C2}% of C2 correct\n\t{perf_test}% of test set correct.")
    
def do_LDA(C1, C2, testset):
    w_LDA, thresh = get_w_lda_and_thresh(C1, C2)
    print(f"Chosen w: {w_LDA}\nDetermined threshold: {thresh.flat[0]}")
    eval_train(w_LDA, C1, C2, testset, thresh)
