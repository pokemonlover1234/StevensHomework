# Considered features by index:
# 0: Page Popularity/likes: defines popularity
# 1: Page Checkins: number of visits
# 2: Page talking about: daily interest
# 29: CC1: total comments before base date/time
# 30: CC2: number of comments last 24 hours, relative to base date/time
# 31: CC3: number of comments last 48 to last 24 horus relative to base date/time
# 32: CC4: number of comments first 24 hours after posting
# 34: Base time:  selected time for scenario simulation
# 35: Post length: length of post in characters
# 36: post share count: counts number of post shares
# 37: post promotion status: whether post is promoted or not
# 38: H local: number of h hrs, for which we have the target variable received
# 39-45: binary indicating weekday post was published. 
# 46-52: binary indicating weekday on selected base date/time
# 53: Actual value, not included in training but included in dataset dict for loss function.

def add_csv_to_dataset(filename, dataset):
    datasetcopy = dataset.copy()
    with open(filename, "r") as datasetpart:
        lines = datasetpart.readlines()
        for line in lines:
            feature = []
            data = line.split(",")
            feature.append(float(data[0]))
            feature.append(float(data[1]))
            feature.append(float(data[2]))
            feature.append(float(data[29]))
            feature.append(float(data[30]))
            feature.append(float(data[31]))
            feature.append(float(data[32]))
            feature.append(float(data[34]))
            feature.append(float(data[35]))
            feature.append(float(data[36]))
            feature.append(float(data[37]))
            feature.append(float(data[38]))
            feature.extend([float(data[39]),float(data[40]),float(data[41]),float(data[42]),float(data[43]),float(data[44]),float(data[45])])
            feature.extend([float(data[46]),float(data[47]),float(data[48]),float(data[49]),float(data[50]),float(data[51]),float(data[52])])
            #.strip() required to get rid of newline character.
            feature.append(float(data[53].strip()))
            datasetcopy.append(feature)
    return datasetcopy


def get_full_dataset():
    #dataset variable keeps arrays of feature values linked to name of feature
    #will help with later output.
    print("Loading dataset...")
    dataset = []
    for i in range(1,6):
        dataset = add_csv_to_dataset(f"../Dataset/Training/Features_Variant_{i}.csv",dataset)
    return dataset