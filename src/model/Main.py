from src.model.algorithm import GeneticAlgorithm
from src.model.configuration import Configuration

# Inicializar configuración y lanzar algoritmo.
Configuration.Configuration.load_configuration()
ga = GeneticAlgorithm.GeneticAlgorithm()
ga.execute()
