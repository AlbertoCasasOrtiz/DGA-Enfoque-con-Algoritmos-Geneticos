import numpy as np

from skimage.measure import compare_ssim as ssim

def mse(x, y):
    return np.linalg.norm(x - y)

