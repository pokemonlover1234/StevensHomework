import numpy as np
import math
from tqdm import trange, tqdm

#Euclidean squared distance of 2 RGB-space triples.
def rgb_dst(rgb1, rgb2):
    a, b, c = (rgb1 - rgb2) ** 2
    return a + b + c

#Transforms rgb_triplets to the form [(r,g,b,ci),...] where
#ci is the index of the assigned centroid in the centroids array.
#-1 if multiple minimums.
def assign_centroids(rgb_triplets, centroids, train_adjustment=False, train_triplets=None, train_mode=0):
    assignments = np.zeros((rgb_triplets.shape[0], 4))
    dists = np.zeros((centroids.shape[0]))
    for i in trange(rgb_triplets.shape[0], desc="Assigning triples to nearest centroid", leave=False):
        if(train_adjustment and train_mode == 0 and np.array_equal(train_triplets[i], [255,255,255])):
            assignments[i] = [0,0,0,-1]
            continue
        elif(train_adjustment and train_mode == 1 and not np.array_equal(train_triplets[i], [255,255,255])):
            assignments[i] = [0,0,0,-1]
            continue
        for j in range(centroids.shape[0]):
            dists[j] = rgb_dst(rgb_triplets[i], centroids[j])
        assignments[i] = [rgb_triplets[i][0], rgb_triplets[i][1], rgb_triplets[i][2], np.argmin(dists)]    
    return assignments

def get_new_centroids(assignments, k):
    new_centroids = np.zeros((k, 3))
    sum_count_accumulator = np.zeros((k, 4))
    for triplet in tqdm(assignments, desc="Calculating updated centroids", leave=False):
        if triplet[3] == -1:
            continue
        sum_count_accumulator[int(triplet[3]),:3] += triplet[:3]
        sum_count_accumulator[int(triplet[3]), 3] += 1
    for i in range(k):
        if sum_count_accumulator[i,3] > 0:
            new_centroids[i] = np.floor(sum_count_accumulator[i,:3]/sum_count_accumulator[i,3])
    return new_centroids

#Performs kmeans over the RGB distance space.
def kmeans_rgb(image, k):
    #An image is just a bunch of RGB-space triples. We are
    #not considering xy position in this K-means implementation,
    #so just get k random entries.
    cfile = open("kmeans-convergence-log.txt","w+", buffering=1)
    #Use a fixed seed for consistent results
    rand = np.random.default_rng(490750240578)
    bounds = image.shape
    rgb_triplets = np.copy(np.asarray(image, dtype=np.int32))
    #Reshape image to list of rgb triplets to simplify random selection
    rgb_triplets.shape = (bounds[0] * bounds[1], 3)
    centroids = rgb_triplets[rand.choice(rgb_triplets.shape[0], k, replace=False)]
    cfile.write("Generation 1 (Initial choice): " + str(centroids) + "\n\n") 
    #Run to convergence
    i = 2
    while True:
        assignments = assign_centroids(rgb_triplets, centroids)
        new_centroids = get_new_centroids(assignments, k)
        if(np.array_equal(centroids, new_centroids)):
            break
        centroids = new_centroids
        cfile.write(f"Generation {i}: " + str(centroids) + "\n\n")
        i += 1
    assignments.shape = (bounds[0], bounds[1], 4)
    result = np.zeros(image.shape)
    for r in trange(assignments.shape[0],desc = "Constructing segmented image"):
        for c in range(assignments.shape[1]):
            result[r,c] = centroids[int(assignments[r,c,3])]
    cfile.close()
    return np.asarray(result,dtype=(np.uint8))

def split_kmeans(train_labeled, train_unlabeled, k):
    #Use a fixed seed for consistent results
    rand = np.random.default_rng(490750240578)
    bounds = train_unlabeled.shape
    centroids_sky = np.zeros((0,3))
    centroids_nonsky = np.zeros((0,3))
    rgb_triplets = np.copy(np.asarray(train_unlabeled, dtype=np.int32))
    rgb_triplets.shape = (bounds[0] * bounds[1], 3)
    train_triplets = np.copy(np.asarray(train_labeled, dtype=np.int32))
    train_triplets.shape = (bounds[0] * bounds[1], 3)
    
    while len(centroids_sky) < k:
        y = rand.choice(range(bounds[0]))
        x = rand.choice(range(bounds[1]))
        if (train_unlabeled[y,x] == centroids_sky).all(1).any() or not np.array_equal(train_labeled[y,x], [255,255,255]) :
            continue
        centroids_sky = np.append(centroids_sky, [train_unlabeled[y,x]], axis=0)
    while len(centroids_nonsky) < k:
        y = rand.choice(range(bounds[0]))
        x = rand.choice(range(bounds[1]))
        if (train_unlabeled[y,x] == centroids_nonsky).all(1).any() or np.array_equal(train_labeled[y,x], [255,255,255]) :
            continue
        centroids_nonsky = np.append(centroids_nonsky, [train_unlabeled[y,x]], axis=0)
        
    #Run to convergence
    i = 2
    converged_sky = False
    converged_nonsky = False
    while True:
        if not converged_sky:
            assignments_sky = assign_centroids(rgb_triplets, centroids_sky, train_adjustment=True, train_triplets=train_triplets, train_mode=1)
            new_centroids_sky = get_new_centroids(assignments_sky, k)
            if(np.array_equal(centroids_sky, new_centroids_sky)):
                converged_sky = True
            else:
                centroids_sky = new_centroids_sky
        if not converged_nonsky:
            assignments_nonsky = assign_centroids(rgb_triplets, centroids_nonsky, train_adjustment=True, train_triplets=train_triplets, train_mode=0)
            new_centroids_nonsky = get_new_centroids(assignments_nonsky, k)        
            if(np.array_equal(centroids_nonsky, new_centroids_nonsky)):
                converged_nonsky = True
            else:
                centroids_nonsky = new_centroids_nonsky
        if(converged_nonsky and converged_sky):
            break
        
        i += 1
    return (centroids_nonsky, centroids_sky)