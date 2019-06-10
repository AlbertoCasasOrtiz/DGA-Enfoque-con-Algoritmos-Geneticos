from src.model.algorithm.operators.mutation.MutationBasic import MutationBasic
from src.model.algorithm.operators.reproduction.ReproductionCrossoverOnePoint import ReproductionCrossoverOnePoint
from src.model.algorithm.operators.selection_parents.SelectionParentsRoulette import SelectionParentsRoulette
from src.model.algorithm.operators.selection_parents.SeletionParentsRandom import SelectionParentsRandom
from src.model.algorithm.operators.selection_survivors.SelectionSurvivorsGenerational import \
    SelectionSurvivorsGenerational
from src.model.algorithm.problem.deblurr_image.ProblemDeblurrImage import ProblemDeblurrImage


class ConfigParser:
    """
    Clase con métodos para interpretar diferentes opciones de configuración.
    """

    @staticmethod
    def parse_problem(value):
        """
        Interpretar problema a abordar.
        :param value: Texto del problema.
        :return: Problema a abordar.
        """
        if value == "Deblurr Image":
            return ProblemDeblurrImage()

    @staticmethod
    def parse_selection_parents(value):
        """
        Interpretar método de selección de padres.
        :param value: Texto del método de selección.
        :return: Método de selección de padres.
        """
        if value == "Random":
            return SelectionParentsRandom()
        elif value == "Roulette":
            return SelectionParentsRoulette()

    @staticmethod
    def parse_reproduction(value):
        """
        Interpretar método de reproducción.
        :param value: Texto del método de reproducción.
        :return: Método de reproducción.
        """
        if value == "Crossover - Points 1":
            return ReproductionCrossoverOnePoint()

    @staticmethod
    def parse_mutation(value):
        """
        Interpretar método de mutación.
        :param value: Texto del método de mutación.
        :return: Método de mutación.
        """
        if value == "Basic":
            return MutationBasic()

    @staticmethod
    def parse_selection_survivors(value):
        """
        Interpretar método de selección de supervivientes.
        :param value: Texto del método de supervivientes.
        :return: Método de selección de supervivientes.
        """
        if value == "Generational":
            return SelectionSurvivorsGenerational()

    @staticmethod
    def parse_list_int(value):
        """
        Interpretar una lista de enteros.
        :param value: Texto con la lista.
        :return: Lista de enteros.
        """
        split = value.split(", ")
        res = []
        for val in split:
            res.append(int(val))
        return res

    @staticmethod
    def parse_bool(value):
        """
        Interpretar un valor booleano.
        :param value: Texto del booleano.
        :return: Boolean.
        """
        if value == "True":
            return True
        elif value == "False":
            return False
