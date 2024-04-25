import numpy as np
from PIL import ImageDraw, Image
from tqdm import tqdm
import Harris
import Image as Im
import math
#Implementation of NCC. Use w by w patches centered on 
#feature, return a triple with top left x,y and patch
def get_template_from_coords(image,x,y,w):
    s = math.floor(w/2)
    arr = np.matrix(image[y-s:y+s+1,x-s:x+s+1])
    fif = np.zeros((w,w))
    b = np.shape(arr)
    fif[0:b[0],0:b[1]] = arr
    return fif
def ncc_func(template, patch):
    mean_norm_temp = template - np.average(template)
    mean_norm_patch = patch - np.average(patch)
    num = np.sum(np.multiply(mean_norm_temp, mean_norm_patch))
    den1 = np.sum(np.multiply(mean_norm_temp, mean_norm_temp))
    den2 = np.sum(np.multiply(mean_norm_patch, mean_norm_patch))
    den = math.sqrt(den1 * den2)
    return num/den

def ncc(image1, image2, harris1, harris2):
    h = []
    for feat1 in tqdm(harris1, desc="Performing NCC"):
        for feat2 in harris2:
            template = get_template_from_coords(image1, feat1[0], feat1[1], 51)
            image_patch = get_template_from_coords(image2, feat2[0], feat2[1], 51)
            h.append((feat1, feat2, ncc_func(template, image_patch)))
    h = sorted(h, key = lambda x : x[2], reverse = True)
    y1,x1 = np.shape(image1)
    y2,x2 = np.shape(image2)
    x,y = (x1+x2,max(y1,y2))
    resim = np.zeros((y,x))
    resim[0:y1,0:x1] = image1
    resim[0:y2,x1:x+1] = image2
    resim = Image.fromarray(resim)
    draw = ImageDraw.Draw(resim)
    for i in range(20):
        draw.line(((h[i][0][0],h[i][0][1]),(h[i][1][0]+x1,h[i][1][1])),width=3, fill="Black")
    r = np.random.default_rng()
    if len(h) <= 50:
        return (Im.to_array(resim),h)
    hres = h[0:20]
    ivals = r.choice([i for i in range(21,len(h))], size = (30), replace=False)
    for i in ivals:
        hres.append(h[i])
    return (Im.to_array(resim),hres)