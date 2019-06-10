from src.model.algorithm.individuals import IndividualFactory
from src.model.configuration import Configuration


class IndividualSet:
    """
    Clase que encapsula un conjunto de individuos y las funciones que operan sobre ellos.
    """

    def __init__(self):
        """
        Inicializar conjunto de individuos.
        """
        self.set = []
        self.average_fitness = 0
        self.best_individual = None
        self.worst_individual = None

    def size(self):
        """
        Obtener número de individuos en el conjunto.
        :return: Número de individuos en el conjunto.
        """
        return len(self.set)

    def initialize(self):
        """
        Inicializar conjunto de individuos metiendo individuos aleatorios.
        :return: None
        """

        # Construct Individuals and append to set.
        for i in range(0, Configuration.Configuration.population_size):
            self.set.append(IndividualFactory.IndividualFactory.factory_individual(Configuration.Configuration.problem))

        # Initialize individuals.
        for ind in self.set:
            ind.initialize()

        # Evaluate population.
        self.evaluate()

    def evaluate(self):
        """
        Evaluar todos los individuos del conjunto.
        :return: None
        """
        best_fitness = float("-inf")
        worst_fitness = float("inf")
        self.average_fitness = 0
        # Para cada individuo...
        for ind in self.set:
            # Lo evaluamos
            ind.evaluate()
            # Actualizamos mejor y peor individuo del set junto al fitness medio.
            self.average_fitness += ind.fitness
            if ind.fitness > best_fitness:
                self.best_individual = ind
                best_fitness = ind.fitness
            if ind.fitness < worst_fitness:
                self.worst_individual = ind
                worst_fitness = ind.fitness
        self.average_fitness /= self.size()

    def add_elements(self, individuals):
        """
        Añadimos una lista de individuos al conjunto.
        :param individuals: Lista con individuos
        :return: None
        """
        self.set.extend(individuals)

    def add_element(self, individual):
        """
        Añadimos un individuo al conjunto.
        :param individual: Individuo
        :return: None
        """
        self.set.append(individual)

    def clear(self):
        """
        Eliminamos todos los individuos del conjunto.
        :return: None
        """
        self.set.clear()
        self.average_fitness = float("-inf")
        self.best_individual = None
        self.worst_individual = None

    def increase_age(self):
        """
        Aumentamos la edad de todos los individuos del conjunto.
        :return: None
        """
        for ind in self.set:
            ind.increase_age()

    def get_element(self, pos):
        """
        Obtenemos el individuo en la posición pos.
        :param pos: Posición del individuo.
        :return: Individuo en la posición pos.
        """
        return self.set[pos]
