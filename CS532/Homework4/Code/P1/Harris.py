# Harris corner detection
import P1.Filter as Filter
import numpy as np

from tqdm import tqdm

def harris(image):
    prog = tqdm(total=13, desc="Applying Filters")
    # Compute derivatives
    Ix = Filter.filter_im(image, Filter.Ix)
    prog.update()
    Iy = Filter.filter_im(image, Filter.Iy)
    prog.update()
    Ix2 = Filter.filter_im(Ix, Filter.Ix)
    prog.update()
    Iy2 = Filter.filter_im(Iy, Filter.Iy)
    prog.update()
    Ixy = Filter.filter_im(Ix, Filter.Iy)
    prog.update()
    # Apply gaussians
    Ix = Filter.filter_im(Ix, Filter.gaussian)
    prog.update()
    Iy = Filter.filter_im(Iy, Filter.gaussian)
    prog.update()
    Ix2 = Filter.filter_im(Ix2, Filter.gaussian)
    prog.update()
    Iy2 = Filter.filter_im(Iy2, Filter.gaussian)
    prog.update()
    Ixy = Filter.filter_im(Ixy, Filter.gaussian)
    prog.update()
    # Reduce sizes to smallest to get same shapes
    Ix = Filter.crop_to(Ix, Ixy)
    prog.update()
    Iy = Filter.crop_to(Iy, Ixy)
    prog.update()
    im = image.copy()
    im = Filter.crop_to(im, Ixy)
    prog.update()
    # Because the gaussians are already applied, 
    # The second moment matrices are embedded in 
    # the variables.
    R = np.zeros(im.shape)
    for y in range(im.shape[0]):
        for x in range(im.shape[1]):
            M = np.matrix([
                [Ix2[y, x], Ixy[y ,x]],
                [Ixy[y, x], Iy2[y, x]]
            ])
            R[y, x] = np.linalg.det(M) - 0.05 * (np.trace(M) ** 2)
            # Threshold
            R[y, x] = R[y, x] if R[y, x] > 10 else 0
    return R