# Source: https://www.pyimagesearch.com/2015/09/07/blur-detection-with-opencv/
# Source: https://github.com/vismantic-ohtuprojekti/qualipy/blob/master/qualipy/utils/focus_measure.py

import cv2
import numpy as np

from src.model.configuration import Configuration


class MeasureBlurr:
    """
    Clase con métodos de medir desenfoque.
    """

    @staticmethod
    def measure(image):
        """
        Obtener medida de desenfoque según la especificada en configuración.
        :param image: Imagen que queremos medir.
        :return: Medida de desenfoque.
        """
        if Configuration.Configuration.problem.measure_function == "Variance of Laplacian":
            return MeasureBlurr.variance_of_laplacian(image)
        elif Configuration.Configuration.problem.measure_function == "Modified Laplacian":
            return MeasureBlurr.modified_laplacian(image)
        elif Configuration.Configuration.problem.measure_function == "Tenengrad":
            return MeasureBlurr.tenengrad(image)

    @staticmethod
    def variance_of_laplacian(image):
        """
        Método de medida de desenfoque basado en la varianza de laplace.
        :param image: Imagen que queremos medir.
        :return: Varianza de Laplace.
        """
        return cv2.Laplacian(image, cv2.CV_64F).var()

    @staticmethod
    def modified_laplacian(image):
        """
        Método de medida de desenfoque basado en una modificación de Laplace.
        :param image: Imagen que queremos medir.
        :return: Valor de la modificación de Laplace.
        """
        kernel = np.array([-1, 2, -1])
        laplacian_x = np.abs(cv2.filter2D(image, -1, kernel))
        laplacian_y = np.abs(cv2.filter2D(image, -1, kernel.T))
        return np.mean(laplacian_x + laplacian_y)

    @staticmethod
    def tenengrad(image):
        """
        Método de medida de desenfoque basado en Tenengrad.
        :param image: Imagen que queremos medir.
        :return: Medida de desenfoque.
        """
        gaussian_x = cv2.Sobel(image, cv2.CV_64F, 1, 0)
        gaussian_y = cv2.Sobel(image, cv2.CV_64F, 1, 0)
        return np.mean(gaussian_x * gaussian_x + gaussian_y * gaussian_y)
