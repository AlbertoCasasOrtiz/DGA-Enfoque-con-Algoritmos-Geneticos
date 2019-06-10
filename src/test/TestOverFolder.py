import cv2

from src.model.algorithm import GeneticAlgorithm
from src.model.algorithm.problem.deblurr_image.ProblemDeblurrImage import ProblemDeblurrImage
from src.model.configuration.Configuration import Configuration
import os

# Cargamos configuración inicial.
Configuration.load_configuration()

# Establecemos path con imágenes de prueba.
path = "images/dataset/"

# Cargamos path de imagenes.
files = []
for r, d, f in os.walk(path):
    for file in f:
        if '.png' in file:
            files.append(os.path.join(r, file))

# Crear carpeta que contendrá resultados
print("Creando carpeta de resultados...")
try:
    os.mkdir("res-test")
except FileExistsError:
    print("Carpeta", "res-test", "ya existe")

# Para cada path...
print("Procesando imágenes...")
for f in files:
    print("Image: " + str(str(f.split("/")[len(f.split("/")) - 1])))
    name = "res-test/" + str(str(f.split("/")[len(f.split("/")) - 1]).split('.')[0]) + "-res/"
    # Crea subcarpeta.
    try:
        os.mkdir(name)
    except FileExistsError:
        print("Carpeta", name, "ya existe")
    for i in range(0, 10):
        print("Iteration: " + str(i))
        # Nombre de subcarpeta
        iteration_name = name + str(i) + "/"
        # Crea una subcarpeta.
        try:
            os.mkdir(iteration_name)
        except FileExistsError:
            print("Carpeta", iteration_name, "ya existe")
        # Ponemos el nombre de la imagen en configuración.
        ProblemDeblurrImage.image_path = f
        ProblemDeblurrImage.image = cv2.imread(f)
        # Ponemos el nombre del directorio de salida en configuración.
        Configuration.path_results = iteration_name
        # Ejecuta el algoritmo.
        ga = GeneticAlgorithm.GeneticAlgorithm()
        ga.execute()
