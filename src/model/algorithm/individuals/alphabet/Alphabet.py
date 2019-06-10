import random


class Alphabet:
    """
    Definimos un alfabeto para representar el genotipo de los individuos. Puede ser de cualquier aridad.
    """

    def __init__(self, path_alphabet):
        """
        Inicializamos el alfabeto desde el archivo de definición.

        :param path_alphabet: Path del archivo de definición.
        """
        self.alphabet = []
        if path_alphabet != "":
            self.read_alphabet(path_alphabet)

    def size(self):
        """
        Aridad del alfabeto.
        :return: Aridad del alfabeto.
        """
        return len(self.alphabet)

    def read_alphabet(self, path_alphabet):
        """
        Leer alfabeto del archivo de definición.
        :param path_alphabet: Path del archivo de definición.
        :return: None
        """
        file = open(path_alphabet, "r")
        lines = file.read().splitlines()
        num = 0
        for line in lines:
            if not line.startswith("#"):
                self.alphabet.append(line)
            num += 1
        file.close()

    def get_random(self):
        """
        Obtenemos un elemento del alfabeto al azar.
        :return: Elemento del alfabeto al azar.
        """
        return random.choice(self.alphabet)
