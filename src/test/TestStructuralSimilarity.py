import cv2
import os
import pandas as pd
import logging
import numpy as np

from skimage.measure import compare_ssim as ssim


def mean_squared_error(sharp_image, generated_image):
    return np.linalg.norm(sharp_image - generated_image)


def variance_of_laplacian(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return cv2.Laplacian(gray, cv2.CV_64F).var()


SCRIPT_DIR = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
path_blurred_images = "res/blurred/"
path_generated_images = "res/generadas/"
path_sharp_images = "res/sharp/"
name = "GA"
logging.basicConfig(format='%(asctime)s.%(msecs)03d  %(message)s', datefmt='%d/%m/%Y %H:%M:%S', level=logging.INFO)
logger = logging.getLogger('blur_detector')

logger.info('Running from {0}'.format(SCRIPT_DIR))

df = pd.DataFrame(columns=['File', 'Arquitecture', 'Sharp - Variance of Laplacian', 'Blurred - Variance of Laplacian',
                           'Generated - Variance Of Laplacian', 'Mean Squared Error', 'Structural Similarity'])


blurred_images = os.listdir(path_blurred_images)
generated_images = os.listdir(path_generated_images)
sharp_images = os.listdir(path_sharp_images)
for i in range(0, len(blurred_images)):
    # Leemos imagen actual.
    blurred = cv2.imread(path_blurred_images + blurred_images[i])
    generated = cv2.imread(path_generated_images + generated_images[i])
    sharp = cv2.imread(path_sharp_images + sharp_images[i])

    file = blurred_images[i]
    arch = name
    variance_laplacian_sharp = variance_of_laplacian(sharp)
    variance_laplacian_blurred = variance_of_laplacian(blurred)
    variance_laplacian_generated = variance_of_laplacian(generated)
    mse = mean_squared_error(sharp, generated)
    structural_similarity = ssim(sharp, generated, data_range=generated.max() - generated.min(), multichannel=True)

    df = df.append(pd.Series([file, arch, variance_laplacian_sharp, variance_laplacian_blurred,
                              variance_laplacian_generated, mse, structural_similarity],
                             index=df.columns), ignore_index=True)

    print("Image: " + file + " processed.")

df.to_csv(path_or_buf=os.path.join("res/", 'data.csv'), sep=';')
