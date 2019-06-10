from abc import ABC, abstractmethod


class Mutation(ABC):
    """
    Definición de un método de mutación. Un nuevo método de mutación debe heredar de esta clase.
    """

    @abstractmethod
    def mutate(self, offspring):
        pass
