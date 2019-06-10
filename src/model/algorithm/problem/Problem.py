from abc import ABC, abstractmethod

from src.model.configuration import Configuration


class Problem (ABC):
    """
    Definición de un problema del algoritmo.
    """

    def __init__(self):
        """
        Inicializar problema.
        """
        self.load_configuration()

    def evaluate(self, params):
        """
        Evaluar el genotipo de un individuo.
        :param params: Genotipo de un individuo.
        :return: Valor fitness obtenido.
        """
        if self.is_maximization():
            return self.function(params)
        else:
            return -self.function(params)

    def load_configuration(self):
        """
        Cargamos la configuración del problema.
        :return: None
        """
        file = open(Configuration.Configuration.path_config_problem, "r")
        lines = file.read().splitlines()
        num = 0
        for line in lines:
            if not line.startswith("#") or not line.strip():
                self.parse_line(line)
            num += 1
        file.close()

    @abstractmethod
    def parse_line(self, line):
        pass

    @abstractmethod
    def is_maximization(self):
        pass

    @abstractmethod
    def function(self, params):
        pass

    @abstractmethod
    def decode(self, genotype):
        pass
