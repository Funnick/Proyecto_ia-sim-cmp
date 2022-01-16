from random import random


class Gene:
    """
    Clase base de los genes
    """

    def __init__(self, value, chance_to_mutate, chance_to_go_up) -> None:
        """
        Devuelve un nuevo gen. min_level (1) y max_level (10)
        representan los niveles mínimos y máximos en que puede mutar un gen

        :param value: nivel de la característica
        :type value: int
        :param chance_to_mutate: probabilidad de mutar
        :type chance_to_mutate: float [0, 1]
        :param chance_to_go_up: probabilidad de aumentar en 1 si muta
        :type chance_to_go_up: float [0, 1]

        :rtype: Gene
        """
        self.min_level = 1
        self.max_level = 10
        self.value = value
        self.chance_to_mutate = chance_to_mutate
        self.chance_to_go_up = chance_to_go_up

    def mutate(self):
        """
        Devuelve un gen mutado con probabilidad chance_to_mutate y
        uno idéntico con probabilidad 1 - chance_to_mutate. En caso
        de un gen mutado su valor es +1 con probabilidad chance_to_go_up,
        -1 con el complemento de chance_to_go_up.
        """
        if random() <= self.chance_to_mutate:
            if random() > self.chance_to_go_up and self.value > self.min_level:
                return Gene(self.value - 1, self.chance_to_mutate, self.chance_to_go_up)
            elif self.value < self.max_level:
                return Gene(self.value + 1, self.chance_to_mutate, self.chance_to_go_up)
        return Gene(self.value, self.chance_to_mutate, self.chance_to_go_up)
