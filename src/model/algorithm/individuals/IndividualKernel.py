from src.model.algorithm.individuals.Individual import Individual
from src.model.configuration import Configuration


class IndividualKernel(Individual):
    """
    Individuo que representa un kernel. Usado en problemas de filtrado de imágenes.
    """

    def evaluate(self):
        """
        Evaluar como de apto es el individuo.
        :return: Aptitud o fitness del individuo.
        """
        self.fitness = Configuration.Configuration.problem.evaluate(self.genotype)

    def copy(self):
        """
        Realizamos una copia exacta de este individuo.
        :return: Copia del individup.
        """
        ind = IndividualKernel()
        ind.genotype = self.genotype.copy()
        ind.fitness = self.fitness
        ind.prob = self.prob
        ind.accum_prob = self.accum_prob
        return ind

    def initialize(self):
        """
        Inicializar el individuo de forma aleatoria.
        :return: None
        """
        size = Configuration.Configuration.problem.genotype_size()
        for i in range(0, size):
            self.genotype.append(Configuration.Configuration.alphabet.get_random())
