import PIL
import numpy as np
from PIL import Image

def get_image(path):
    image = Image.open(path)
    return np.array(image)

def save_image(image_array, name):
    image = Image.fromarray(image_array)
    image.convert("RGB").save(name)
    return

def copy_image(image):
    return np.copy(image)

def to_array(PILimage):
    return np.array(PILimage)