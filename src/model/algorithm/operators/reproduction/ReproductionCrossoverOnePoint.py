import random

from src.model.algorithm.individuals import IndividualSet
from src.model.algorithm.individuals import IndividualFactory
from src.model.algorithm.operators.reproduction.Reproduction import Reproduction
from src.model.configuration import Configuration


class ReproductionCrossoverOnePoint(Reproduction):
    """
    Método de reproducción de cruce por un punto.
    """

    def reproduce(self, parents):
        """
        Reproducimos individuos de un conjunto de individuos.
        :param parents: Conjunto de individuos.
        :return: Descendencia.
        """
        offspring = IndividualSet.IndividualSet()
        # Mientras no tengamos suficiente descendencia...
        while offspring.size() < parents.size():
            # Elegimos dos padres al azar.
            ind1 = random.randint(0, parents.size()-1)
            ind2 = random.randint(0, parents.size()-1)
            # Si la probabilidad de reproducción lo permite, los cruzamos.
            if Configuration.Configuration.p_reproduction >= random.uniform(0, 1):
                offspring.add_elements(self.crossover(parents.set[ind1], parents.set[ind2]))
            # Si no, los padres pasan a la generación.
            else:
                offspring.add_elements([parents.set[ind1].copy(), parents.set[ind2].copy()])
        return offspring

    @staticmethod
    def crossover(ind1, ind2):
        """
        Método de cruce por un punto.
        :param ind1: Individuo padre 1.
        :param ind2: Individuo padre 2.
        :return: Descendencia.
        """

        # Inicializamos la descendencia.
        offspring1 = IndividualFactory.IndividualFactory.factory_individual(Configuration.Configuration.problem)
        offspring2 = IndividualFactory.IndividualFactory.factory_individual(Configuration.Configuration.problem)

        # Elegimos un punto al azar.
        point = random.randint(0, ind1.size()-1)

        # Creamos el primer descendiente.
        offspring1.genotype.extend(ind1.genotype[0:point])
        offspring1.genotype.extend(ind2.genotype[point:ind2.size()])

        # Creamos el segundo descendiente.
        offspring2.genotype.extend(ind2.genotype[0:point])
        offspring2.genotype.extend(ind1.genotype[point:ind1.size()])

        return [offspring1, offspring2]
