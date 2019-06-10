import cv2
import numpy as np
from numpy.lib.scimath import logn
from skimage.measure import compare_ssim as ssim

from src.model.algorithm.problem import Problem
from src.model.configuration import Configuration, ConfigParser
from src.model.image_functions import MeasureBlurr


class ProblemDeblurrImage (Problem.Problem):
    """
    Definición del problema de enfocar una imagen.
    """

    dim_x = 0
    dim_y = 0
    min_val = 0
    max_val = 0
    decimals = 0
    image_path = ""
    image = None
    measure_function = ""
    ground_truth = False

    def parse_line(self, s_line):
        """
        Método para interpretar una linea del archivo de configuración del problema.
        :param s_line: Linea que vamos a interpretar.
        :return: None.
        """
        split = s_line.split(": ")
        key = split[0]
        value = split[1]

        if key == "num_decimals":
            ProblemDeblurrImage.decimals = int(value)
        elif key == "dim_x":
            ProblemDeblurrImage.dim_x = int(value)
        elif key == "dim_y":
            ProblemDeblurrImage.dim_y = int(value)
        elif key == "min_val":
            ProblemDeblurrImage.min_val = float(value)
        elif key == "max_val":
            ProblemDeblurrImage.max_val = float(value)
        elif key == "image_path":
            ProblemDeblurrImage.image_path = value
            ProblemDeblurrImage.image = cv2.imread(value)
        elif key == "ground_truth":
            ProblemDeblurrImage.ground_truth = ConfigParser.ConfigParser.parse_bool(value)
        elif key == "treshold":
            ProblemDeblurrImage.treshold = int(value)
        elif key == "measure_function":
            ProblemDeblurrImage.measure_function = value

    def is_maximization(self):
        """
        Establecemos si estamos ante un problema de maximización o de minimización.
        :return: True
        """
        return True

    def function(self, params):
        """
        Función de evaluación de un genotipo.
        :param params: Genotipo.
        :return: Fitness del genotupo.
        """
        return self.blur_measure(params)

    def blur_measure(self, params):
        """
        Función usada para medir el desenfoque de una imagen.

        :param params: Gen que codifica el kernel.
        :return: Cantidad de desenfoque.
        """

        # Decodificamos el kernel.
        kernel = np.array(self.decode(params))

        # Aplicamos el kernel.
        applied_kernel = cv2.filter2D(ProblemDeblurrImage.image, -1, kernel)

        # Pasamos la imagen a escala de grises para poder medir desenfoque.
        gray = cv2.cvtColor(applied_kernel, cv2.COLOR_BGR2GRAY)
        blurr = MeasureBlurr.MeasureBlurr.measure(gray)

        return blurr

    def decode(self, genotype):
        """
        Decodificar el genotipo para obtener el kernel.
        :param genotype: Genotipo
        :return: Kernel
        """
        arity = Configuration.Configuration.alphabet.size()
        nary_to_dec = 0
        arr = []
        beginning = 0
        for i in range(0, self.dim_x):
            subarr = []
            for j in range(0, self.dim_y):
                for k in range(0, self.variable_size()):
                    nary_to_dec += int(genotype[k+beginning]) * pow(arity, k)
                # En alfabetos binarios, aplicamos código gray.
                if Configuration.Configuration.gray_code:
                    if arity == 2:
                        gray = 0
                        while nary_to_dec > 0:
                            gray ^= nary_to_dec
                            nary_to_dec >>= 1
                        nary_to_dec = gray
                    else:
                        print("Arity is not 2. Not using gray.")
                        pass
                fenotype = self.min_val + nary_to_dec * (self.max_val - self.min_val) / pow(arity, self.variable_size())
                subarr.append(fenotype)
                nary_to_dec = 0
                beginning += self.variable_size()
            arr.append(subarr.copy())
        return arr

    def genotype_size(self):
        """
        Obtener tamaño del genotipo que necesitamos.
        :return: Tamaño del genotipo que necesitamos.
        """
        size = 0
        for i in range(0, self.dim_x*self.dim_y):
            size += int(self.variable_size())
        return size

    def variable_size(self):
        """
        Obtener tamaño necesario para codificar una variable del fenotipo.
        :return: Tamaño necesario.
        """
        arity = Configuration.Configuration.alphabet.size()
        a = 1 + (self.max_val - self.min_val) * pow(10, self.decimals)
        size = int(logn(arity, a))
        return size

    @staticmethod
    def is_gray():
        """
        Obtener valor que determina si aplicamos código gray o no.
        :return: True or False.
        """
        return Configuration.Configuration.gray_code

    @staticmethod
    def ssim(image1, image2):
        """
        Obtener similaridad estructural de dos imágenes.
        :param image1: Imagen 1.
        :param image2: Imagen 2.
        :return: Medida de similaridad estructural.
        """
        return ssim(image1, image2)
