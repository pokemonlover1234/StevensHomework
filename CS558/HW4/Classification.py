import numpy as np
from KMeans import split_kmeans, rgb_dst
from tqdm import trange

BRIGHT_PINK = [228, 97, 237]

def do_classification(train_labeled, train_unlabeled, input_images):
    non_sky_classes, sky_classes = split_kmeans(train_labeled, train_unlabeled, 10)
    output_images = []
    for image in input_images:
        output_images.append(np.zeros(image.shape))
    for i in trange(len(input_images), desc="Generating Output"):
        for j in trange(input_images[i].shape[0], desc=f"Image {i+1} of {len(input_images)}", leave=False):
            for k in range(input_images[i].shape[1]):
                dsts_sky = []
                dsts_nonsky = []
                for c in sky_classes:
                    dsts_sky.append(rgb_dst(input_images[i][j,k],c))
                for c in non_sky_classes:
                    dsts_nonsky.append(rgb_dst(input_images[i][j,k],c))
                if min(dsts_sky) < min(dsts_nonsky):
                    output_images[i][j,k] = BRIGHT_PINK
                else:
                    output_images[i][j,k] = input_images[i][j,k]
    return output_images