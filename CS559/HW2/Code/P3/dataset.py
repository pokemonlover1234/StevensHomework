import random
from tqdm import tqdm, trange

def read_set(file_doyle, file_austen):
    C1 = []
    C2 = []
    with open(file_doyle, "r") as doyle:
        with open(file_austen, "r") as austen:
            d = doyle.readlines()
            a = austen.readlines()
            for l in tqdm(d, desc="Loading Doyle"):
                for word in l.split():
                    C1.append(''.join([c for c in word if c.isalnum()]))
            for l in tqdm(a, desc="Loading Austen"):
                for word in l.split():
                    C2.append(''.join([c for c in word if c.isalnum()]))
    return C1, C2

# Sets up a test set, removing it from the training dataset

def split_train_test(C1, C2):
    test_set = []
    C1f = C1.copy()
    C2f = C2.copy()
    random.seed(445248524)
    for i in trange(16,21, desc="Accumulating test set"):
        for _ in trange(250, leave=False):
            s = random.randint(0, len(C1f) - i)
            tmp = []
            tmp.extend(C1f[:s])
            tmp.extend(C1f[s+i:])
            C1f = tmp
            test_set.append((C1f[s:s+i], 1))
            s = random.randint(0, len(C2f) - i)
            tmp = []
            tmp.extend(C2f[:s])
            tmp.extend(C2f[s+i:])
            C2f = tmp
            test_set.append((C2f[s:s+i], 2))
    return C1f, C2f, test_set

def get_dataset_processed(file_doyle, file_austen):
    C1, C2 = read_set(file_doyle, file_austen)
    return split_train_test(C1, C2)