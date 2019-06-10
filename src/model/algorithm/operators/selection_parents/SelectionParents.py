from abc import ABC, abstractmethod


class SelectionParents (ABC):
    """
    Definición de un método de selección de padres. Un nuevo método de selección de padres debe heredar de esta clase.
    """

    @abstractmethod
    def select(self, population):
        return population
