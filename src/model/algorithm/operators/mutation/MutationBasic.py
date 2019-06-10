import random

from src.model.algorithm.operators.mutation.Mutation import Mutation
from src.model.configuration import Configuration


class MutationBasic(Mutation):
    """
    Método de mutación básico. Cambia el valor de un gen por otro aleatorio.
    """

    def mutate(self, offspring):
        """
        Mutar un conjunto de individuos.
        :param offspring: Conjunto de individuos
        :return: Conjunto de individuos mutados.
        """

        # Mutamos cada individuo por separado.
        for ind in offspring.set:
            self.mutate_ind(ind)
        return offspring

    @staticmethod
    def mutate_ind(ind):
        """
        Mutamos un individuo gen a gen.
        :param ind: Individuo.
        :return: None
        """

        # Para cada gen, realizamos la mutación si nos lo permite la probabilidad de mutación.
        for i in range(0, ind.size()):
            if Configuration.Configuration.p_mutation >= random.uniform(0, 1):
                ind.genotype[i] = Configuration.Configuration.alphabet.get_random()
