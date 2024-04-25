import numpy as np
from PIL import Image, ImageOps

def get_image(path, gray = False):
    image = Image.open(path)
    if gray:
        image = ImageOps.grayscale(image)
    return np.array(image)

def save_image(image_array, name):
    image = Image.fromarray(image_array)
    image.convert("RGB").save(name)
    return

def copy_image(image):
    return np.copy(image)

def to_array(PILimage):
    return np.array(PILimage)