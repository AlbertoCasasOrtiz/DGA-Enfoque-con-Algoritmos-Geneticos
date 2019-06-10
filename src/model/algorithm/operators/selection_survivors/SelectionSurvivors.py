from abc import ABC, abstractmethod


class SelectionSurvivors (ABC):
    """
    Definición de un método de selección de supervivientes. Un nuevo método de selección de supervivientes debe heredar
    de esta clase.
    """
    @abstractmethod
    def select(self, parents, offspring):
        pass
