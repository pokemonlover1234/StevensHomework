import numpy as np
import math
import Filter
import Hessian
from PIL import Image, ImageDraw
from tqdm import tqdm
#How much to discretize in the p direction. for example, this = 1 means p -> [0,1), [1,2), ...
#in vote accumulator
P_DISCRETIZATION = 0.8

def apply_hough(hessian, image):
    #Theta = 0-180
    #p = xcos(theta) + ysin(theta). Between cos(theta) and sin(theta) <= 1, p <= x + y
    #p = 0 - max(x+y)/PDISC = sum of bounds of image / discretization constant
    hessian = Filter.unbound_image(hessian, np.shape(image))
    hessian = Hessian.to_point_array(hessian)
    #Base algorithm
    H = np.zeros((181, math.floor(np.sum(np.shape(image))/P_DISCRETIZATION)))
    Hpt = [[[] for c in r] for r in H]
    for pt in tqdm(hessian, desc="Hough: Counting votes..."):
        x, y = pt
        for theta in range(181):
            t = math.radians(theta)
            p = float(x) * math.cos(t) + float(y) * math.sin(t)
            H[theta, math.floor(p/P_DISCRETIZATION)] += 1
            Hpt[theta][math.floor(p/P_DISCRETIZATION)].append(pt)
    im = Image.fromarray(image)
    draw = ImageDraw.Draw(im)
    #Local maxima
    maxima = Filter.nms(H)
    Hpt = np.array(Hpt, dtype=object)
    #Find and draw lines with most votes
    for _ in range(4):
        #Weirdness with np.array conversions here due to how np.unravel_index returns.
        theta, p = np.array(np.array(np.unravel_index(np.argmax(maxima),np.shape(maxima))).flat)
        t = math.radians(theta)
        #Now generate a function we can use to get y values for specific x values so we
        #can plot the line with whatever extreme points voted for it.
        def thisline(x, pt):
            #p = xcos(t) + ysin(t). Solve for y.
            #p - xcos(t) = ysin(t)
            #y = (p - xcos(t))/sin(t)
            if math.sin(t) == 0:
                return pt[1]
            return (p * P_DISCRETIZATION - x * math.cos(t))/math.sin(t)
        #Get sorted points that voted.
        pts = sorted(Hpt[theta,p], key = lambda x: x[0])
        #Draw
        draw.line([pts[0][0], thisline(pts[0][0], pts[0]), pts[-1][0], thisline(pts[-1][0],pts[-1])])
        for pt in pts:
            bounds = [pt[0] - 1, pt[1] - 1, pt[0] + 2, pt[1] + 2]
            draw.rectangle(bounds, width = 1)
        # Remove this vote so it isn't double counted
        maxima[theta, p] = 0
    return im
