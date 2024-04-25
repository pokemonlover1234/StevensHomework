import math

# Defines a Node class, which defines the attribute name it splits on, and a dictionary
# linking values to either a Prediction, or another Node. Also stores a data subset that
# it was trained on, minus the attributes it knows the value of.

class DecisionNode():
    # A Node stores which attribute it is split on, and a dictionary to nodes that it splits to.
    # It does store which value it represents, but only for string output.

    # It does store the data it is given, but that data is only used when splitting on the node.

    # Stores a list of remaining attributes that have not been split on yet. This list will
    # include splitAttr if it is assigned, but not splitAttrSelf.

    # finalized being true hard-stops any splitting on that node.

    def __init__(self, data, attrs, splitAttrSelf = None, thresholding = False):
        self.splitAttr = None
        self.splitAttrSelf = splitAttrSelf
        self.nodeDict = None
        self.data = data
        self.attrs = attrs
        self.finalized = False
        self.splitVal = None
        # In case of thresholded information gain algorithm, need to know if attr is thresholded
        self.thresholding = thresholding

    # Update attributes of a node to indictate it has been split on.

    def set_node_as_split(self, nodeDict, attr):
        self.splitAttr = attr
        self.nodeDict = nodeDict


    # Returns a prediction for the node, based on its data. Returns 1 if number of results 
    # with 1 is greater than half of the examples in the node. 

    def static_prediction(self):
        return int(self.data.cond_len(lambda ex: ex.Result == 1) > len(self.data) // 2)

    # Recursively traverse the tree until a node is not split on, then return that node's 
    # static prediction

    def get_node_prediction(self, inputExample = None):
        if self.nodeDict is None:
            return self.static_prediction()
        else:
            try:
                if self.thresholding:
                    iVal = inputExample[self.splitAttr]
                    nextNode = self.nodeDict[list(self.nodeDict.keys())[0]]
                    if nextNode.splitVal[0] == "<":
                        t = float(self.splitVal[1:])
                    else:
                        t = float(self.splitVal[2:])
                    if iVal < t:
                        return self.nodeDict[f"<{t}"].get_node_prediction(inputExample)
                    else:
                        return self.nodeDict[f">={t}"].get_node_prediction(inputExample)
                else:
                    return self.nodeDict[inputExample[self.splitAttr]].get_node_prediction(inputExample)
            except KeyError:
                # the node dictionary that stores the split does not recognize a value (for example, training
                # data does not have attr = 4, but we get an attr = 4 on test data).
                # In this case, since we return a result of 1 if and only if the number of 1 results on this node
                # is greater than half of the stored node, and 0 is not greater than 1/2 * 0, predict 0

                # Simulates all possible nodes with training set of 0 good 0 bad.
                return 0

    # Determine if this node is done splitting
    def check_and_set_end_cond(self):
        if len(self.data) == 0:
            self.finalized = True
            return
        testEx = self.data[0]
        # Base Case 1: All nodes same result
        if self.data.cond_len(lambda ex : ex.Result == testEx.Result) == len(self.data):
            self.finalized = True
            return
        # Base Case 2: All nodes same remaining attributes.
        if self.data.cond_len(lambda ex : testEx.equal_on_attr_set(self.attrs, ex)) == len(self.data):
            self.finalized = True
            return

    def str_helper(node, level = 0):
        s = f"Attribute: {'Root' if node.splitAttrSelf is None else node.splitAttrSelf}..Attribute Value: {'Thresh::' if node.thresholding else ''}{node.splitVal}..Bad|Good: {node.data.cond_len(lambda ex: ex.Result == 0)}|{node.data.cond_len(lambda ex: ex.Result == 1)}..Node Prediction: {node.get_node_prediction() if node.nodeDict is None else 'T'}"
        if node.nodeDict is not None:
            for n in node.nodeDict.values():
                s += "\n" + "\t" * (level + 1) + DecisionNode.str_helper(n, level + 1)
        return s
        
    
    def __str__(self):
        return DecisionNode.str_helper(self)
        
# Defines a Decision Tree class, that provides training and prediction functions
# Training functions directly modify the tree.

class DecisionTree():
    def __init__(self, trainData, splitSelectType="InfGainBucket", thresholdAttrs = []):
        if splitSelectType == "InfGainBucket":
            self.splitNode = self.InfGainSplitBucket
        elif splitSelectType == "InfGainThreshold":
            self.splitNode = self.InfGainSplitThreshold
        elif splitSelectType == "GiniBucket":
            self.splitNode = self.GiniSplitBucket
        elif splitSelectType == "GiniThreshold":
            self.splitNode = self.GiniSplitThreshold
        else:
            raise ValueError("Split Algorithm must be either InfGain or Gini")
        self.data = trainData
        self.thresholdAttrs = thresholdAttrs
        for attr in thresholdAttrs:
            self.data.updateNull(attr, 0)
        # Create a root node with no self-split attribute, with the full attribute list.
        # Make sure it should be split on.
        self.root = self.splitNode(None)
        self.root.check_and_set_end_cond()

    # Get a list of leaf nodes

    def get_leaves(node):
        leaves = []
        if node.nodeDict is None:
            return [node]
        for n in node.nodeDict.values():
            leaves.extend(DecisionTree.get_leaves(n))
        return leaves
        
    
    # Entropy functions for InfGain

    def entropy(data):
        # Only two possible Y values
        p0 = data.cond_len(lambda ex : ex.Result == 0) / len(data)
        p1 = 1 - p0

        return -p0*math.log(p0)-p1*math.log(p1)

    def cond_entropy(data, attr):
        entropy = 0
        for val in set([ex.Data[attr] for ex in data.data]):
            px = data.cond_len(lambda ex : ex.Data[attr] == val)/len(data)
            for j in range(2):
                try:
                    pyx = data.cond_len(lambda ex : ex.Result == j and ex.Data[attr] == val)/data.cond_len(lambda ex : ex.Data[attr] == val)
                    entropy -= px*pyx*math.log(pyx)
                except ValueError:
                    # pyx is 0, so entropy on this value is 0.
                    continue
        return entropy

    def cond_threshold_entropy(data, attr, t):
        entropy = 0
        pxl = data.cond_len(lambda ex : float(ex.Data[attr]) < t)/len(data)
        pxg = data.cond_len(lambda ex : float(ex.Data[attr]) >= t)/len(data)
        for j in range(2):
            try:
                pyxl = data.cond_len(lambda ex : ex.Result == j and float(ex.Data[attr]) < t)/data.cond_len(lambda ex : float(ex.Data[attr]) < t)
                entropy -= pxl*pyxl*math.log(pyxl)
            except ValueError:
                # pyxl is 0, so entropy on this value is 0.
                pass
            except ZeroDivisionError:
                # None here in this class
                pass
            try:
                pyxr = data.cond_len(lambda ex : ex.Result == j and float(ex.Data[attr]) >= t)/data.cond_len(lambda ex : float(ex.Data[attr]) >= t)
                entropy -= pxg*pyxr*math.log(pyxr)
            except ValueError:
                # pyxr is 0, so entropy on this value is 0.
                pass
            except ZeroDivisionError:
                # None here in this class
                pass
        return entropy
    
    def gini(data, attr):
        attrVals = list(set([ex.Data[attr] for ex in data.data]))
        pvals = [data.cond_len(lambda ex: ex.Data[attr] == val)/len(data) for val in attrVals]
        pclass0 = [data.cond_len(lambda ex: ex.Data[attr] == val and ex.Result == 0)/data.cond_len(lambda ex: ex.Data[attr] == val) for val in attrVals]
        pclass1 = [data.cond_len(lambda ex: ex.Data[attr] == val and ex.Result == 1)/data.cond_len(lambda ex: ex.Data[attr] == val) for val in attrVals]

        ginis = [1 - math.pow(class0p,2) - math.pow(class1p,2) for class0p, class1p in zip(pclass0, pclass1)]
        finalGini = 0
        for pv, gini in zip(pvals, ginis):
            finalGini += pv * gini
        return finalGini

    def gini_thresholded(data, attr, t):
        pvals = [data.cond_len(lambda ex: float(ex.Data[attr]) < t)/len(data), data.cond_len(lambda ex: float(ex.Data[attr]) >= t)/len(data)]
        pclass0 = [data.cond_len(lambda ex: float(ex.Data[attr]) < t and ex.Result == 0)/data.cond_len(lambda ex: float(ex.Data[attr]) < t), data.cond_len(lambda ex: float(ex.Data[attr]) >= t and ex.Result == 0)/data.cond_len(lambda ex: float(ex.Data[attr]) >= t)]
        pclass1 = [data.cond_len(lambda ex: float(ex.Data[attr]) < t and ex.Result == 1)/data.cond_len(lambda ex: float(ex.Data[attr]) < t), data.cond_len(lambda ex: float(ex.Data[attr]) >= t and ex.Result == 1)/data.cond_len(lambda ex: float(ex.Data[attr]) >= t)]

        ginis = [1 - math.pow(class0p,2) - math.pow(class1p,2) for class0p, class1p in zip(pclass0, pclass1)]
        finalGini = 0
        for pv, gini in zip(pvals, ginis):
            finalGini += pv * gini
        return finalGini

    # The split algorithms. InfGainSplit function splits using information gain, and
    # Gini uses the Gini index. Which is used is determined by what is passed
    # in __init__

    # They return 0 if a node is not split, and 1 if it is. This is used
    # to track when to stop running splits.

    def InfGainSplitBucket(self, node):
        if node is None:
            return DecisionNode(self.data, self.data.attrs)
        if node.finalized:
            return 0
        testAttrs = node.attrs
        IGs = {}
        for attr in testAttrs:
            IG = DecisionTree.entropy(node.data) - DecisionTree.cond_entropy(node.data, attr)
            IGs.update({IG: attr})
        splitAttr = IGs[max(list(IGs.keys()))]
        nodeDict = {}
        for val in set([ex.Data[splitAttr] for ex in node.data.data]):
            newAttrs = node.attrs.copy()
            newAttrs.remove(splitAttr)
            newNode = DecisionNode(node.data.filterData(lambda ex : ex.Data[splitAttr] == val), newAttrs, splitAttr)
            newNode.splitVal = val
            nodeDict.update({val: newNode})
            newNode.check_and_set_end_cond()
        node.set_node_as_split(nodeDict, splitAttr)
        return 1

    # Information Gain algorithm with thresholding binary tree
    # instead of bucketing. 

    def InfGainSplitThreshold(self, node):
        if node is None:
            return DecisionNode(self.data, self.data.attrs)

        if node.finalized:
            return 0
        testAttrs = node.attrs
        IGs = {}
        thresholds = {}
        for attr in testAttrs:
            # If attr is one we threshold on, perform the threshold
            # by searching for best t, and setting it.
            if attr in self.thresholdAttrs:
                consider = node.data.sortData(lambda ex: float(ex.Data[attr]))
                consider = list(set([float(ex.Data[attr]) for ex in consider.data]))
                consider.sort()
                ts = []
                for i in range(1,len(consider) - 1):
                    xi = consider[i]
                    xi1 = consider[i+1]
                    ts.append(xi + (xi1-xi)/2)
                maxtIG = None
                maxtIGt = None
                for t in ts:
                    IG = DecisionTree.entropy(node.data) - DecisionTree.cond_threshold_entropy(node.data, attr, t)
                    if maxtIG is None or IG > maxtIG:
                        maxtIG = IG
                        maxtIGt = t
                IG = maxtIG
                if IG is None:
                    # Assume no split. 
                    node.finalized = True
                    return 0
                IGs.update({IG: attr})
                thresholds.update({attr: maxtIGt})
            else:
                IG = DecisionTree.entropy(node.data) - DecisionTree.cond_entropy(node.data, attr)
                IGs.update({IG: attr})
        splitAttr = IGs[max(list(IGs.keys()))]
        nodeDict = {}
        # Create new nodes depending on thresholding. Thresholded 
        # attributes do not get removed from consideration.
        if splitAttr in self.thresholdAttrs:
            newAttrs = node.attrs.copy()
            t = thresholds[splitAttr]
            newNodeL = DecisionNode(node.data.filterData(lambda ex : float(ex.Data[splitAttr]) < t), newAttrs, splitAttr, thresholding = True)
            newNodeR = DecisionNode(node.data.filterData(lambda ex : float(ex.Data[splitAttr]) >= t), newAttrs, splitAttr, thresholding = True)
            newNodeL.splitVal = f"<{t}"
            newNodeR.splitVal = f">={t}"
            nodeDict.update({f"<{t}": newNodeL})
            nodeDict.update({f">={t}": newNodeR})
            newNodeL.check_and_set_end_cond()
            newNodeR.check_and_set_end_cond()
        else:
            for val in set([ex.Data[splitAttr] for ex in node.data.data]):
                newAttrs = node.attrs.copy()
                newAttrs.remove(splitAttr)
                newNode = DecisionNode(node.data.filterData(lambda ex : ex.Data[splitAttr] == val), newAttrs, splitAttr)
                newNode.splitVal = val
                nodeDict.update({val: newNode})
                newNode.check_and_set_end_cond()
        node.set_node_as_split(nodeDict, splitAttr)
        return 1

    def GiniSplitBucket(self, node):
        if node is None:
            return DecisionNode(self.data, self.data.attrs)
        if node.finalized:
            return 0
        testAttrs = node.attrs
        Ginis = {}
        for attr in testAttrs:
            Gini = DecisionTree.gini(node.data, attr) 
            Ginis.update({Gini: attr})
        splitAttr = Ginis[min(list(Ginis.keys()))]
        nodeDict = {}
        for val in set([ex.Data[splitAttr] for ex in node.data.data]):
            newAttrs = node.attrs.copy()
            newAttrs.remove(splitAttr)
            newNode = DecisionNode(node.data.filterData(lambda ex : ex.Data[splitAttr] == val), newAttrs, splitAttr)
            newNode.splitVal = val
            nodeDict.update({val: newNode})
            newNode.check_and_set_end_cond()
        node.set_node_as_split(nodeDict, splitAttr)
        return 1

    def GiniSplitThreshold(self, node):
        if node is None:
            return DecisionNode(self.data, self.data.attrs)
        if node.finalized:
            return 0
        testAttrs = node.attrs
        Ginis = {}
        thresholds = {}
        for attr in testAttrs:
            if attr in self.thresholdAttrs:
                consider = node.data.sortData(lambda ex: float(ex.Data[attr]))
                consider = list(set([float(ex.Data[attr]) for ex in consider.data]))
                consider.sort()
                ts = []
                for i in range(1,len(consider) - 1):
                    xi = consider[i]
                    xi1 = consider[i+1]
                    ts.append(xi + (xi1-xi)/2)
                mintGini = None
                mintGinit = None
                for t in ts:
                    Gini = DecisionTree.gini_thresholded(node.data, attr, t)
                    if mintGini is None or Gini < mintGini:
                        mintGini = Gini
                        mintGinit = t
                Gini = mintGini
                if Gini is None:
                    # Assume no split. 
                    node.finalized = True
                    return 0
                Ginis.update({Gini: attr})
                thresholds.update({attr: mintGinit})
            else:
                Gini = DecisionTree.gini(node.data, attr) 
                Ginis.update({Gini: attr})
        splitAttr = Ginis[min(list(Ginis.keys()))]
        nodeDict = {}
        if splitAttr in self.thresholdAttrs:
            newAttrs = node.attrs.copy()
            t = thresholds[splitAttr]
            newNodeL = DecisionNode(node.data.filterData(lambda ex : float(ex.Data[splitAttr]) < t), newAttrs, splitAttr, thresholding = True)
            newNodeR = DecisionNode(node.data.filterData(lambda ex : float(ex.Data[splitAttr]) >= t), newAttrs, splitAttr, thresholding = True)
            newNodeL.splitVal = f"<{t}"
            newNodeR.splitVal = f">={t}"
            nodeDict.update({f"<{t}": newNodeL})
            nodeDict.update({f">={t}": newNodeR})
            newNodeL.check_and_set_end_cond()
            newNodeR.check_and_set_end_cond()
        else:
            for val in set([ex.Data[splitAttr] for ex in node.data.data]):
                newAttrs = node.attrs.copy()
                newAttrs.remove(splitAttr)
                newNode = DecisionNode(node.data.filterData(lambda ex : ex.Data[splitAttr] == val), newAttrs, splitAttr)
                newNode.splitVal = val
                nodeDict.update({val: newNode})
                newNode.check_and_set_end_cond()
        node.set_node_as_split(nodeDict, splitAttr)
        return 1

    def train_tree(self):
        continue_training = False
        # Continue training as long as there is at least one leaf node that is not
        # done splitting (hasn't reached a base case)
        while True:
            for node in DecisionTree.get_leaves(self.root):
                if self.splitNode(node) == 1:
                    continue_training = True
            if len(DecisionTree.get_leaves(self.root)) == 0:
                break
            if not continue_training:
                break
            continue_training = False
        print(self.root)

    def predict(self, ex):
        return self.root.get_node_prediction(ex)

    def __str__(self):
        print(f"{self.root}")

def evaluate_tree(Tree, Data):
    right = 0
    wrong = 0
    for ex in Data.data:
        if Tree.predict(ex.Data) == ex.Result:
            right += 1
        else:
            wrong += 1
    return right / (right + wrong)