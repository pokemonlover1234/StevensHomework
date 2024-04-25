from tqdm import tqdm
import numpy as np

# A class representing the dataset. This is meant to be dataset-agnostic, so assumptions
# based on the dataset provided are not included in this class, except for an expectation
# regarding which column retains the actual result.

# Stores result and the actual data dictionary seperately
class Example():
    def __init__(self, Result, Data):
        self.Result = int(Result)
        self.Data = Data

    # Determine if an example is equivalent to another if 
    # what we check is restricted to a given attribute set.

    def equal_on_attr_set(self, attrs, other):
        for attr in attrs:
            if not self.Data[attr] == other.Data[attr]:
                return False
        return True

    def __str__(self):
        return f"Res: {self.Result}, Data: {self.Data}"

class Dataset():
    # Sets up the dataset, given a filename pointing to the raw dataset csv. Expects actual
    # result in first column of data. Expects attribute names to be first row.
    def __init__(self, filename="", preData = None):
        if preData is not None:
            self.data = preData
            return
        datafile = open(filename, "r")
        attrsRaw = datafile.readline()
        self.attrs = attrsRaw.strip().split(",")
        l = datafile.readlines()
        self.init_dataset(l)

    # Converts continuous data into buckets of size bucketSize, and returns a string
    # representing which bucket the data belongs to. If data is missing, sets bucket to empty.
    def bucket(rawVal, bucketSize):
        if rawVal == "":
            return ""
        Val = float(rawVal)
        return f"{(Val // bucketSize) * bucketSize}-{(Val // bucketSize + 1) * bucketSize}"
        
    # Apply bucketing to provided attribute, with provided size.
    # Assumes user provides a numeric attribute.
    def apply_bucketing(self, bucketAttr, bucketSize):
        for example in tqdm(self.data, desc = f"Bucketing Attribute \"{bucketAttr}\""):
            example.Data[bucketAttr] = Dataset.bucket(example.Data[bucketAttr], bucketSize)

    # Creates two different Dataset objects, one for training, one for testing.
    # Ratio is percentage of data to move to test set.
    def split_train_test(self, ratio):
        rand = np.random.default_rng(34525345243)
        dataPerm = rand.permutation(np.array(self.data))
        ind = int(np.floor(len(self.data) * ratio))

        testData = self.data[:ind]
        trainData = self.data[ind:]

        testDataFinal = Dataset(preData = testData)
        trainDataFinal = Dataset(preData = trainData)

        testDataFinal.attrs = self.attrs
        trainDataFinal.attrs = self.attrs

        return testDataFinal, trainDataFinal

    # Runs the initial loading of the dataset into the self.data array. Since this runs during
    # __init__, user can make assumption that self.data exists and is populated after class
    # instance is created.
    def init_dataset(self, lines):
        self.data = []
        for line in tqdm(lines, desc="Initial Data Load"):
            dataRaw = {attr: float(val) if val.replace('.','',1).replace('-','',1).isdigit() else val for attr, val in zip(self.attrs, line.strip().split(","))}
            Result = dataRaw[self.attrs[0]]
            del dataRaw[self.attrs[0]]
            self.data.append(Example(Result, dataRaw))
        del self.attrs[0]

    # getitem and len allow for some python primitives,
    # namely, [] syntax and len() to be used on this class

    def __getitem__(self, key):
        return self.data[key]
    
    def __len__(self):
        return len(self.data)

    # cond_len is a conditional length, counting
    # only the items that return true when passed
    # to the provided predicate function

    def cond_len(self, pred):
        return len([0 for ex in self.data if pred(ex)])

    # filterData and sortData perform the specified
    # operations on a copy of the data, returning a 
    # new Dataset object. pred defines the sorting/
    # filtering criteria.

    def filterData(self, pred):
        d = self.data.copy()
        d = [ex for ex in d if pred(ex)]
        n = Dataset(preData = d)
        n.attrs = self.attrs
        return n

    def sortData(self, pred):
        d = self.data.copy()
        d.sort(key = pred)
        n = Dataset(preData = d)
        n.attrs = self.attrs
        return n

    # Gives a default value of newVal to the specified
    # attribute, assigning newVal to that attribute on
    # all examples that do not provide a value for this
    # attribute. 

    def updateNull(self, attr, newVal):
        for ex in self.data:
            ex.Data[attr] = newVal if ex.Data[attr] == '' else ex.Data[attr]

    # Used for Adaboost, returns result and data arrays
    # without any attribute labeling. 
    # Also converts 0 in Results to -1

    def get_raw_data_arrays(self):
        results = [1 if ex.Result == 1 else -1 for ex in self.data]
        examples = [[ex.Data[attr] for attr in self.attrs] for ex in self.data]

        return examples, results

    def __str__(self):
        return f"[{', '.join(str(ex) for ex in self.data)}]"