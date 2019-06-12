import cv2
import sys
import os
import logging
import pandas as pd

from skimage.measure import compare_ssim as ssim


logging.basicConfig(format='%(asctime)s.%(msecs)03d  %(message)s', datefmt='%d/%m/%Y %H:%M:%S', level=logging.INFO)
logger = logging.getLogger('blur_detector')

SCRIPT_DIR		 = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
ORIGINAL_SHARP	 = os.path.join(SCRIPT_DIR, 'Original_sharp')
ORIGINAL_BLURRED = os.path.join(SCRIPT_DIR, 'Original_blurred')
CNN_IMAGES		 = os.path.join(SCRIPT_DIR, 'CNN')
RNN_IMAGES		 = os.path.join(SCRIPT_DIR, 'RNN')


def laplacian(image_path):
	image = cv2.imread(image_path)
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	return cv2.Laplacian(gray, cv2.CV_64F).var()

def get_score_list(images_path):

	logger.info('Getting scores from {0}'.format(images_path))
	score_list = []

	for file in sorted(os.listdir(images_path)):
		score_list.append(laplacian(os.path.join(images_path, file)))

	return score_list

def get_similarities(images_path):

	logger.info('Getting similarities from {0}'.format(images_path))
	similarities = []

	for o_img, g_img in zip(sorted(os.listdir(ORIGINAL_SHARP)), sorted(os.listdir(images_path))):
		original  = cv2.imread(os.path.join(ORIGINAL_SHARP, o_img))
		generated = cv2.imread(os.path.join(images_path, g_img))
		similarities.append(ssim(original, generated, data_range=(generated.max() - generated.min()), multichannel=True))

	return similarities


logger.info('Running from {0}'.format(SCRIPT_DIR))

original_sharp_scores   = get_score_list(ORIGINAL_SHARP)
original_blurred_scores = get_score_list(ORIGINAL_BLURRED)
cnn_scores 				= get_score_list(CNN_IMAGES)
rnn_scores 				= get_score_list(RNN_IMAGES)

cnn_similarities		= get_similarities(CNN_IMAGES)
rnn_similarities		= get_similarities(RNN_IMAGES)

filenames 				= ['{0}.png'.format(i) for i in range(1,101)]

cnn_dict = {
		'File': 		filenames,
		'Architecture': 'CNN',
		'LS Sharp': 	original_sharp_scores,
		'LS Blurred': 	original_blurred_scores,
		'LS Generated': cnn_scores,
		'SE': 			cnn_similarities
}

rnn_dict = {
		'File': 		filenames,
		'Architecture': 'RNN',
		'LS Sharp': 	original_sharp_scores,
		'LS Blurred': 	original_blurred_scores,
		'LS Generated': rnn_scores,
		'SE': 			rnn_similarities
}

cnn_df = pd.DataFrame(cnn_dict)
rnn_df = pd.DataFrame(rnn_dict)

cnn_df.to_csv(path_or_buf=os.path.join(SCRIPT_DIR, 'cnn.csv'))
rnn_df.to_csv(path_or_buf=os.path.join(SCRIPT_DIR, 'rnn.csv'))
