import random

from src.model.algorithm.individuals import IndividualSet
from src.model.algorithm.operators.selection_parents.SelectionParents import SelectionParents


class SelectionParentsRoulette(SelectionParents):
    """
    Método de selección de padres por ruleta. Se le asignan probabilidades a los individuos de manera proporcional
    a su fitness y luego se seleccionan en función de esas probabilidades de forma aleatoria.
    """

    def select(self, population):
        """
        Seleccionar individuos por el método de ruleta.
        :param population: Población del algoritmo.
        :return: Individuos seleccionados.
        """
        # Asignar probabilidades
        self.assign_probabilites(population)

        # Seleccionar por ruleta
        selected = IndividualSet.IndividualSet()
        for i in range(0, len(population.set)):
            rand = random.uniform(0, 1)
            cont = 0
            found = False
            while not found:
                ind = population.set[cont+1]
                if rand < ind.accum_prob:
                    selected.set.append(ind)
                    found = True
                else:
                    cont += 1
        return selected

    @staticmethod
    def assign_probabilites(population):
        """
        Asignar probabilidades a los individuos de una población.
        :param population: Población
        :return: None
        """
        # Ordenamos de mayor a menor
        population.set.sort(key=lambda x: x.fitness, reverse=True)

        # Calculamos fitness total
        total_fitness = 0
        for ind in population.set:
            total_fitness += ind.fitness

        # Asignamos probabilidad a cada individuo
        accumulated = 0
        for ind in population.set:
            ind.prob = ind.fitness/total_fitness
            accumulated += ind.prob
            ind.accum_prob += accumulated
