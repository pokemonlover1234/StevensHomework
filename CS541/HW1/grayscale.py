#matrix manipulation - convert color image to grayscale
#do not make changes in the function names
#do not use any inbuilt libraries and/or packages to convert image to grayscale, implement the code yourself


from matplotlib.image import imread
from matplotlib import pyplot as plt
import numpy as np

Rc = 0.2989
Gc = 0.587
Bc = 0.114

def to_grayscale(image):
    #Start your code implementation from here
    gr = np.zeros(image.shape[:2])
    for r in range(image.shape[0]): 
        for c in range(image.shape[1]):
            R, G, B = image[r, c]
            gr[r, c] = Rc * R + Gc * G + Bc * B
    return gr

def main():
    #use the already given image only for submission
    #Load the colored image here
    #save the grayscale image as grayscale_image in same folder
    im = imread("colorImage.jpg")
    gr_im = to_grayscale(im)
    image_gray = plt.imsave('grayscale_image.jpg', gr_im/255, cmap="gray")

if __name__ == "__main__":
    main()
