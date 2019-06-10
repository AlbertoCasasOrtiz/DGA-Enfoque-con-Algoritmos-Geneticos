from src.model.algorithm.individuals.IndividualKernel import IndividualKernel
from src.model.algorithm.problem.deblurr_image.ProblemDeblurrImage import ProblemDeblurrImage


class IndividualFactory:
    """
    Patrón factoría para obtener individuos según el problema que abordemos.
    """

    @staticmethod
    def factory_individual(problem):
        """
        Obtenemos un individuo dependiendo del problema que vamos a abordar.
        :param problem:  Problema que vamos a abordar.
        :return: Individuo del tipo pedido.
        """
        if isinstance(problem, ProblemDeblurrImage):
            return IndividualKernel()
