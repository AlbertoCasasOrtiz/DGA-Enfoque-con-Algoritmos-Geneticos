from abc import ABC, abstractmethod


class Individual(ABC):
    """
    Definición de un individuo. Un tipo de individuo debe heredar de esta clase.
    """

    def __init__(self):
        """
        Inicialización de individuuo.
        """
        self.genotype = []
        self.fitness = 0
        self.prob = 0
        self.accum_prob = 0
        self.age = 0

    def size(self):
        """
        Número de genes en el individuo.
        :return: Número de genes en el individuo.
        """
        return len(self.genotype)

    def increase_age(self):
        """
        Aumentar edad del individuo
        :return: None
        """
        self.age += 1

    @abstractmethod
    def initialize(self):
        pass

    @abstractmethod
    def evaluate(self):
        pass

    @abstractmethod
    def copy(self):
        pass
