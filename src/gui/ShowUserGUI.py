from tkinter import *
from tkinter import filedialog

import cv2
import numpy as np
from PIL import Image
from PIL import ImageTk

from src.model.algorithm.GeneticAlgorithm import GeneticAlgorithm
from src.model.algorithm.problem.deblurr_image.ProblemDeblurrImage import ProblemDeblurrImage
from src.model.configuration.Configuration import Configuration
from src.model.image_functions.MeasureBlurr import MeasureBlurr


class ShowUserGUI:
    """
    Muestra interfaz gráfica.
    """

    panel = None
    root = None
    root_selection = None
    panels_selection = []
    checkbox = []
    indexes = []
    ga = GeneticAlgorithm()
    end = False
    p_mutation_input = None
    p_reproduction_input = None

    @staticmethod
    def show_chooser(root):
        """
        Mostrar selector de imagen.

        :param root:  Root de tkinter.
        :return: None
        """
        ShowUserGUI.root = root

        btn = Button(root, text="Start", command=ShowUserGUI.start_algorithm)
        btn.pack(side="bottom", fill="both", expand="yes", padx="10", pady="10")

        btn2 = Button(root, text="Select an image", command=ShowUserGUI.select_image)
        btn2.pack(side="bottom", fill="both", expand="yes", padx="10", pady="10")

    @staticmethod
    def select_image():
        """
        Selecciona la imagen.

        :return: None
        """
        # Abrir dialog para pedir archivo
        path = filedialog.askopenfilename()

        if len(path) > 0:
            Configuration.load_configuration()

            # Cargar imagen
            ProblemDeblurrImage.image_path = path
            ProblemDeblurrImage.image = cv2.imread(path)

            # Pasar imagen a RGB
            image_rgb = cv2.cvtColor(Configuration.problem.image, cv2.COLOR_BGR2RGB)

            # Pasar imagen a imagen de PIL
            image_rgb = Image.fromarray(image_rgb)

            # Redimensionar imagen para mostrarla
            image_rgb = ShowUserGUI.resize(300, image_rgb)

            # Convertir imagen a Tkinter
            image_rgb = ImageTk.PhotoImage(image_rgb)

            # Inicializar panel
            if ShowUserGUI.panel is None:
                ShowUserGUI.panel = Label(image=image_rgb)
                ShowUserGUI.panel.image = image_rgb
                ShowUserGUI.panel.pack(padx=10, pady=10)

            # Update panel si ya estaba
            else:
                ShowUserGUI.panel.configure(image=image_rgb)
                ShowUserGUI.panel.image = image_rgb

    @staticmethod
    def start_algorithm():
        """
        Inicia el algoritmo.

        :return: None
        """

        # Inicializa algoritmo genético
        ShowUserGUI.ga.initialize()

        # Sekección de indices iniciales
        ShowUserGUI.ga.iteration_interactive([0, 1, 2, 3, 4, 5, 6, 7])

        # Mostrar población a usuario
        ShowUserGUI.selection_window()

    @staticmethod
    def selection_window():
        """
        Muestra la ventana de selección de individuos.

        :return: None
        """

        # Crear nueva ventana
        ShowUserGUI.root_selection = Toplevel(ShowUserGUI.root)

        # Mostrar población
        ShowUserGUI.show_iteration()

        # Show label of p. mutation
        p_mutation_label = Label(ShowUserGUI.root_selection, text="P. Mutation", fg="black")
        p_mutation_label.grid(row=0, column=0)

        # Show input of p. mutation
        if ShowUserGUI.p_mutation_input is None:
            ShowUserGUI.p_mutation_input = Entry(ShowUserGUI.root_selection)
            ShowUserGUI.p_mutation_input.grid(row=0, column=1)
            ShowUserGUI.p_mutation_input.delete(0, END)
            ShowUserGUI.p_mutation_input.insert(0, Configuration.p_mutation)
        else:
            print(float(ShowUserGUI.p_mutation_input.get()))
            Configuration.p_mutation = float(ShowUserGUI.p_mutation_input.get())

        # Show label of p. reproduction
        p_reproduction_label = Label(ShowUserGUI.root_selection, text="P. Reproduction", fg="black")
        p_reproduction_label.grid(row=0, column=2)

        # Show input of p. mutation
        if ShowUserGUI.p_reproduction_input is None:
            ShowUserGUI.p_reproduction_input = Entry(ShowUserGUI.root_selection)
            ShowUserGUI.p_reproduction_input.grid(row=0, column=3)
            ShowUserGUI.p_reproduction_input.delete(0, END)
            ShowUserGUI.p_reproduction_input.insert(0, Configuration.p_reproduction)
        else:
            Configuration.p_mutation = float(ShowUserGUI.p_reproduction_input.get())

        # Definir boton para iterar
        button = Button(ShowUserGUI.root_selection, text="Next", command=ShowUserGUI.make_iteration)
        button.grid(row=5, column=3)

        # Definir boton para guardar
        button = Button(ShowUserGUI.root_selection, text="Save", command=ShowUserGUI.save_image)
        button.grid(row=5, column=0)

    @staticmethod
    def make_iteration():
        """
        Realiza una iteración del algoritmo.

        :return: None
        """

        # Cogemos los individuos seleccionados.
        for i in range(0, len(ShowUserGUI.checkbox)):
            if ShowUserGUI.checkbox[i].get():
                ShowUserGUI.indexes.append(i)
                print(i)

        # Cogemos probabilidad de mutación de la GUI y la metemos en configuración.
        if ShowUserGUI.p_mutation_input is not None:
            Configuration.p_mutation = float(ShowUserGUI.p_mutation_input.get())

        # Cogemos probabilidad de reproducción de la GUI y la metemos en configuración.
        if ShowUserGUI.p_reproduction_input is not None:
            Configuration.p_reproduction = float(ShowUserGUI.p_reproduction_input.get())

        # Pedimos al algoritmo que haga la iteración.
        ShowUserGUI.ga.iteration_interactive(ShowUserGUI.indexes)

        # Ponemos los índices elegidos en la iteración anterior a cero.
        ShowUserGUI.indexes.clear()

        # Mostramos resultados de la iteración.
        ShowUserGUI.show_iteration()

    @staticmethod
    def show_iteration():
        """
        Mostrar resultados de una iteración.

        :return: None
        """
        i = 1
        j = 0
        count = 0
        ShowUserGUI.checkbox.clear()

        # Procesamos y mostramos cada individuo
        for ind in ShowUserGUI.ga.population.set:
            # Obtener kernel
            kernel = np.array(Configuration.problem.decode(ind.genotype))

            # Obtener imagen kernelizada
            applied_kernel = cv2.filter2D(ProblemDeblurrImage.image, -1, kernel)
            image_rgb = cv2.cvtColor(applied_kernel, cv2.COLOR_BGR2RGB)
            image_rgb = Image.fromarray(image_rgb)
            image_rgb = ShowUserGUI.resize(250, image_rgb)
            image_rgb = ImageTk.PhotoImage(image_rgb)

            # Mostrar imagen kernelizada en GUI
            display = Label(ShowUserGUI.root_selection, image=image_rgb)
            display.image = image_rgb
            display.grid(row=i, column=j)
            ShowUserGUI.panels_selection.append(display)

            # Mostrar chechbox en GUI
            ShowUserGUI.checkbox.append(BooleanVar())
            c = Checkbutton(ShowUserGUI.root_selection, text=str(count), variable=ShowUserGUI.checkbox[count])
            c.grid(row=i + 1, column=j)

            # Actualizar contadores
            count += 1
            if j == 3:
                i += 2
                j = 0
            else:
                j += 1

    @staticmethod
    def save_image():
        """
        Guardar imagen elegida junto a su kernel y la media entre la imagen elegida y la original.

        :return: None
        """
        # Para cada imagen elegida
        for i in range(0, len(ShowUserGUI.checkbox)):
            if ShowUserGUI.checkbox[i].get():
                print(i)

                # Calculamos imagen kernelizada, y media de original y kernelizada
                kernel = np.array(Configuration.problem.decode(ShowUserGUI.ga.population.get_element(i).genotype))
                applied_kernel = cv2.filter2D(ProblemDeblurrImage.image, -1, kernel)
                mean = cv2.addWeighted(ProblemDeblurrImage.image, 0.5, applied_kernel, 0.5, 0)

                # Guardamos imagen kernelizada, media y kernel
                cv2.imwrite('kernelized.jpg', applied_kernel, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
                cv2.imwrite('mean.jpg', mean, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
                cv2.imwrite('kernel.jpg', kernel, [int(cv2.IMWRITE_JPEG_QUALITY), 100])

                # Imprimimos kernel
                print(kernel)

                # Redimensionamos imagenes para mostrarlas
                applied_kernel_resized = ShowUserGUI.resize2(500, applied_kernel)
                original_image_resized = ShowUserGUI.resize2(500, Configuration.problem.image)
                mean_resized = ShowUserGUI.resize2(500, mean)

                # Mostramos imágenes
                cv2.imshow("kernelized", applied_kernel_resized)
                cv2.imshow("original", original_image_resized)
                cv2.imshow("mean", mean_resized)

                cv2.waitKey(0)
                cv2.destroyAllWindows()
                print(MeasureBlurr.measure(applied_kernel))

    @staticmethod
    def resize(new_width, img):
        """
        Redimensiona una imagen de PIL

        :param new_width: Nueva anchura.
        :param img: Imagen de PIL
        :return: Imagen redimensionada.
        """
        new_height = int(new_width * img.height / img.width)
        return img.resize((new_width, new_height), Image.ANTIALIAS)

    @staticmethod
    def resize2(new_width, img):
        """
        Redimensiona una imagen de OpenCV.

        :param new_width: Nueva anchura.
        :param img: Imagen de PIL
        :return: Imagen redimensionada.
        """
        new_height = int(new_width * img.shape[0] / img.shape[1])
        return cv2.resize(img, dsize=(new_width, new_height), interpolation=cv2.INTER_CUBIC)
