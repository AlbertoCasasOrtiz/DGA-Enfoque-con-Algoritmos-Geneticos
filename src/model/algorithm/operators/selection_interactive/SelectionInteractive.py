import random

from src.model.algorithm.individuals.IndividualSet import IndividualSet


class SelectionInteractive:
    """
    Método de selección interactiva.
    """

    @staticmethod
    def select(population, indexes):
        """
        Seleccionamos los individuos según el criterio del usuario.
        :param population: Población completa.
        :param indexes: Selecciones del usuario.
        :return:
        """
        new_population = IndividualSet()
        # Seleccionamos individuos elegidos por el usuario al azar hasta llenar población.
        while new_population.size() < population.size():
            rand = random.randint(0, len(indexes)-1)
            new_population.add_element(population.set[indexes[rand]])
        return new_population
