from src.model.algorithm.individuals.alphabet.Alphabet import Alphabet
from src.model.configuration.ConfigParser import ConfigParser


class Configuration:
    """
    Clase que contiene todos los parámetros de configuración del algoritmo.
    """
    path_config = "cfg/config.cfg"
    path_alphabet = ""
    alphabet = Alphabet("")
    path_config_problem = ""
    gray_code = False
    population_size = 0
    total_generations = 0
    ranking_s = 0
    p_reproduction = 0
    p_mutation = 0
    elitism = False
    num_elitism = 0
    problem = None
    selection_parents = None
    reproduction = None
    mutation = None
    selection_survivors = None
    type_individual = None
    save_images = False
    write_kernel_measure = False
    show_images = False
    show_graphic = False
    save_graphic = False
    path_results = ""

    @staticmethod
    def load_configuration():
        """
        Cargar configuración desde el archivo de configuración.
        :return: None
        """
        file = open(Configuration.path_config, "r")
        lines = file.read().splitlines()
        for line in lines:
            if not line.startswith("#") or not line.strip():
                Configuration.parse_line(line)
        file.close()

    @staticmethod
    def parse_line(s_line):
        """
        Interpretar una línea del archivo de configuración.
        :param s_line: Línea con el parámetro de configuración.
        :return: None
        """
        split = s_line.split(": ")
        key = split[0]
        value = split[1]

        if key == "alphabet":
            Configuration.path_alphabet = value
            Configuration.alphabet = Alphabet(value)
        elif key == "path_config_problem":
            Configuration.path_config_problem = value
        elif key == "gray_code":
            Configuration.gray_code = ConfigParser.parse_bool(value)
        elif key == "problem":
            Configuration.problem = ConfigParser.parse_problem(value)
        elif key == "population_size":
            Configuration.population_size = int(value)
        elif key == "total_generations":
            Configuration.total_generations = int(value)
        elif key == "selection_parents":
            Configuration.selection_parents = ConfigParser.parse_selection_parents(value)
        elif key == "reproduction":
            Configuration.reproduction = ConfigParser.parse_reproduction(value)
        elif key == "p_reproduction":
            Configuration.p_reproduction = float(value)
        elif key == "mutation":
            Configuration.mutation = ConfigParser.parse_mutation(value)
        elif key == "p_mutation":
            Configuration.p_mutation = float(value)
        elif key == "selection_survivors":
            Configuration.selection_survivors = ConfigParser.parse_selection_survivors(value)
        elif key == "elitism":
            Configuration.elitism = ConfigParser.parse_bool(value)
        elif key == "num_elitism":
            Configuration.num_elitism = int(value)
        elif key == "save_images":
            Configuration.save_images = ConfigParser.parse_bool(value)
        elif key == "write_kernel_measure":
            Configuration.write_kernel_measure = ConfigParser.parse_bool(value)
        elif key == "show_images":
            Configuration.show_images = ConfigParser.parse_bool(value)
        elif key == "show_graphic":
            Configuration.show_graphic = ConfigParser.parse_bool(value)
        elif key == "save_graphic":
            Configuration.save_graphic = ConfigParser.parse_bool(value)
        elif key == "path_results":
            Configuration.path_results = value
