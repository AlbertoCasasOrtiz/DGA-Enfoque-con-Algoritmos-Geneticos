from abc import ABC, abstractmethod


class Reproduction (ABC):
    """
    Definición de un método de reproducción. Un nuevo método de reproducción debe heredar de esta clase.
    """

    @abstractmethod
    def reproduce(self, parents):
        pass
