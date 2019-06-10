from src.model.algorithm.operators.selection_survivors.SelectionSurvivors import SelectionSurvivors


class SelectionSurvivorsGenerational(SelectionSurvivors):
    """
    Método de selección de supervivientes generacional. Los supervivientes elegidos serán los que formen la
    descendencia.
    """

    def select(self, parents, offspring):
        """
        Método de selección de supervivientes generacional.
        :param parents: Padres seleccionados para generar la descendencia.
        :param offspring: Descendencia generada.
        :return: Individuos supervivientes.
        """
        return offspring
