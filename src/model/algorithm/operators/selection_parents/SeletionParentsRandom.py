import random

from src.model.algorithm.individuals import IndividualSet
from src.model.algorithm.operators.selection_parents.SelectionParents import SelectionParents


class SelectionParentsRandom(SelectionParents):
    """
    Método de selección de padres de forma aleatoria. No recomendado porque no asegura convergencia del algoritmo.
    Usado para testing.
    """

    def select(self, population):
        """
        Selecciona individuos de forma aleatoria.
        :param population: Población
        :return: Individuos seleccionados.
        """
        selected = IndividualSet.IndividualSet()
        for i in range(0, population.size()):
            rand = random.randint(0, population.size()-1)
            selected.add_element(population.get_element(rand).copy())
        return selected
