import numpy as np

class Dataset():
    def __init__(self, filename):
        self.data = None
        self.load_dataset(filename)

    def add_datapoint(self, feature):
        X = feature[:-1]
        Y = feature[-1]
        # Store datapoints as an array of tuples with named fields
        extype = np.dtype([('X', np.float64, (len(X))), ('Y', np.unicode_, 3)])
        if self.data is None:
            self.data = np.empty((0), dtype=extype)
        self.data = np.append(self.data, [np.array((X, Y), dtype=extype)])


    def load_dataset(self, filename):
        dataset = []
        with open(filename, 'r') as dataset:
            examples = dataset.readlines()
            for example in examples:
                # Discard the name
                features = example.strip().split(" ")[1:]
                # Since there are multiple spaces, discard the spaces
                # and build the example array
                X = []
                for feature in features:
                    if feature == "":
                        continue
                    X.append(feature)
                self.add_datapoint(X)
        
    def split_dataset(self, K):
        rand = np.random.default_rng(313414321)
        perm = rand.permutation(self.data)
        permMost = perm
        extype = self.data.dtype
        permRem = np.empty((0), extype)
        # Guarantee np.split doesn't error.
        if perm.shape[0] % K != 0:
            permMost = perm[:perm.shape[0] // K * K]
            permRem = perm[perm.shape[0] // K * K:]
        splits = np.split(permMost, K)
        # Allocate remainder elements to beginning elements
        i = 0
        for elem in permRem:
            splits[i] = np.append(splits[i], np.array([elem], dtype=extype))
            i += 1
        return splits