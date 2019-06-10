import os

import cv2
import numpy as np

from src.model.algorithm.individuals.IndividualSet import IndividualSet
from src.model.algorithm.operators.selection_interactive.SelectionInteractive import SelectionInteractive
from src.model.algorithm.problem.deblurr_image.ProblemDeblurrImage import ProblemDeblurrImage
from src.model.image_functions.MeasureBlurr import MeasureBlurr
from src.model.configuration.Configuration import Configuration
import matplotlib.pyplot as plt


class GeneticAlgorithm:
    """
    Implementación del algoritmo genético.
    """

    def __init__(self):
        """
        Inicialización del algoritmo genético.
        """
        self.population = IndividualSet()
        self.generations = 0
        self.elite = IndividualSet()
        self.progress = 0
        self.current_generation = 0
        self.best_fitness_array = []
        self.worst_fitness_array = []
        self.average_fitness_array = []

    def initialize(self):
        """
        Reinicialización de un algoritmo genético ya instanciado.
        :return: None
        """
        self.population.clear()
        self.population.initialize()
        self.elite.clear()
        self.select_elite()

    def execute(self):
        """
        Ejecución del algoritmo genético.
        :return: None
        """
        self.initialize()
        while self.current_generation < Configuration.total_generations:
            self.select_elite()
            parents = Configuration.selection_parents.select(self.population)
            offspring = Configuration.reproduction.reproduce(parents)
            offspring = Configuration.mutation.mutate(offspring)
            offspring.evaluate()
            self.population = Configuration.selection_survivors.select(parents, offspring)
            self.population.evaluate()
            self.add_elite()
            self.elite.clear()
            self.current_generation += 1
            # Mostrar progreso.
            print(".", end='')
            self.best_fitness_array.append(self.population.best_individual.fitness)
            self.worst_fitness_array.append(self.population.worst_individual.fitness)
            self.average_fitness_array.append(self.population.average_fitness)
        print("")
        self.show_results(self.population.best_individual.genotype)

    def iteration_interactive(self, indexes):
        """
        Iteración del algoritmo genético en modo interactivo.
        :param indexes: Índices de la población elegidos por el usuario.
        :return: Población.
        """
        parents = SelectionInteractive.select(self.population, indexes)
        offspring = Configuration.reproduction.reproduce(parents)
        offspring = Configuration.mutation.mutate(offspring)
        self.population = Configuration.selection_survivors.select(parents, offspring)
        self.population.evaluate()
        self.current_generation += 1
        return self.population

    def select_elite(self):
        """
        Seleccionar élite.
        :return: None
        """
        if Configuration.elitism:
            for ind in self.population.set:
                if self.elite.size() < Configuration.num_elitism:
                    self.elite.add_element(ind.copy())
                    self.elite.evaluate()
                elif self.elite.best_individual.fitness < ind.fitness:
                    self.elite.set.insert(self.elite.set.index(self.elite.worst_individual), ind.copy())
                    self.elite.evaluate()
            self.elite.increase_age()

    def add_elite(self):
        """
        Añadir élite a la población. Sustituye los peores individuos.
        :return:
        """
        if Configuration.elitism:
            for ind in self.elite.set:
                self.population.set[self.population.set.index(self.population.worst_individual)] = ind.copy()
                self.population.evaluate()

    def show_results(self, params):
        """
        Mostrar resultados.
        :param params: Genotipo del mejor individuo.
        :return: None
        """
        # Obtener kernel, aplicarlo a la imagen, y obtener imagen media.
        kernel = np.array(Configuration.problem.decode(params))
        applied_kernel = cv2.filter2D(ProblemDeblurrImage.image, -1, kernel)
        mean = cv2.addWeighted(ProblemDeblurrImage.image, 0.5, applied_kernel, 0.5, 0)

        # Si no existe, creamos directorio de resultados.
        try:
            os.mkdir(Configuration.path_results)
        except FileExistsError:
            print("Carpeta", Configuration.path_results, "ya existe")

        # Guardamos imagen kernelizada, media y kernel en disco.
        if Configuration.save_images:
            try:
                os.mkdir(Configuration.path_results + "images/")
            except FileExistsError:
                print("Carpeta", Configuration.path_results + "images/", "ya existe")
            cv2.imwrite(Configuration.path_results + 'images/kernelized-image.jpg', applied_kernel, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
            cv2.imwrite(Configuration.path_results + 'images/mean-image.jpg', mean, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
            cv2.imwrite(Configuration.path_results + 'images/original-image.jpg', ProblemDeblurrImage.image, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
            cv2.imwrite(Configuration.path_results + 'images/kernel.jpg', kernel, [int(cv2.IMWRITE_JPEG_QUALITY), 100])

        # Escribimos kernel y medidas en fichero.
        if Configuration.write_kernel_measure:
            f = open(Configuration.path_results + "results.txt", "w+")
            f.write("Kernel:\n")
            f.write(str(kernel)+"\n")
            f.write("\n")
            f.write("Measure original:\n")
            f.write(str(MeasureBlurr.measure(ProblemDeblurrImage.image))+"\n")
            f.write("Measure mean:\n")
            f.write(str(MeasureBlurr.measure(mean))+"\n")
            f.write("Measure kernelized:\n")
            f.write(str(MeasureBlurr.measure(applied_kernel))+"\n")
            f.close()

        # Mostramos gráfica de evolución del mejor fitness y guardamos en disco.
        plt.plot(self.best_fitness_array, label='Best Fitness')
        plt.plot(self.worst_fitness_array, label='Worst Fitness')
        plt.plot(self.average_fitness_array, label='Average Fitness')
        plt.ylabel('sharpness')
        plt.xlabel('generations')
        plt.legend()
        if Configuration.show_graphic:
            plt.show()
        if Configuration.save_graphic:
            plt.savefig(Configuration.path_results + 'graphic.png')
        plt.cla()

        # Mostramos imágenes al usuario.
        if Configuration.show_images:
            cv2.imshow("kernelized", applied_kernel)
            cv2.imshow("original", Configuration.problem.image)
            cv2.imshow("mean", mean)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
