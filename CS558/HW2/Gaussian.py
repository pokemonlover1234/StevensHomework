import numpy as np
import math
#Get the value of the gaussian function for a given sigma, x, and y
#Splits the calculation into a few lines to make it easier to read.
def gaussian_function(sigma, x, y):
    partial1 = 1/(2*math.pi*math.pow(sigma,2))
    partial2 = -(math.pow(x,2)+math.pow(y,2))/(2*math.pow(sigma,2))
    partial2 = math.exp(partial2)
    return partial1*partial2

#Generate the gaussian filter with the given sigma
#Offsets x and y to center the maximum value.
def gaussian_filter(sigma):
    f = np.zeros((sigma*6+1,sigma*6+1))
    for x in range(-(sigma*3),sigma*3+1):
        for y in range(-(sigma*3),sigma*3+1):
            f[x+sigma*3][y+sigma*3] = gaussian_function(sigma, x, y)
    f = f * 1 / sum(sum(f))
    return f