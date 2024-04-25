# Creates a dict for each class linking words to their class probabilities.

import math
from tqdm import tqdm


def p_c_word(ClassData):
    # Get all unique words
    import nltk
    try:
        nltk.data.find('corpora/stopwords.zip')
    except LookupError:
        nltk.download('stopwords')
    from nltk.corpus import stopwords
    stops = set(stopwords.words('english'))
    words = set(ClassData)
    return {word: (ClassData.count(word)+1)/len(ClassData) for word in tqdm(words, desc="Building word probabilities") if word not in stops}

def prob_class(ClassProbs, xx):
    prob = 1
    for word in xx:
        if not (word in ClassProbs.keys()):
            # Ignore word if not in training data
            continue
        prob *= ClassProbs[word]
    return math.log(prob)

def sample_class(C1Probs, C2Probs, sample):
    c1prob = prob_class(C1Probs, sample)
    c2prob = prob_class(C2Probs, sample)
    return 1 if c1prob >= c2prob else 2

# test_set = [[sample, class={1,2}], [sample, class={1,2}],...]

def evaluate_model(C1_tset, C2_tset, test_set):
    C1Probs = p_c_word(C1_tset)
    C2Probs = p_c_word(C2_tset)
    right = 0
    wrong = 0
    for sample in tqdm(test_set, desc="Evaluating Model"):
        prediction = sample_class(C1Probs, C2Probs, sample[0])
        if prediction == sample[1]:
            right+=1
        else:
            wrong+=1
    return right/(right+wrong)
