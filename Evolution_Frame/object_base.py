class Tile:
    """
    Clase que representa el objeto base\n
    del mapa. Todos los elementos\n
    del mundo heredan de él.
    """

    def __init__(self, pos_x, pos_y):
        """
        Se crea un objeto en la ubicación (pos_x, pos_y),
        se define por defecto que no es un borde ni comida.

        :param pos_x: coordenada x del objeto
        :type pos_x: int
        :param pos_y: coordenada y del objeto
        :type pos_y: int

        :rtype: Tile
        """
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.is_edge = False
        self.has_food = False
        self.has_tree = False
        self.has_agent = False
        self.can_pass = True
        self.footprints = []
        self.object_list = []
        self.height = 0

    def __str__(self):
        return "Nothing"

class Object_base():
    def __init__ (self):
        pass


class Food(Object_base):
    """
    Clase que representa la comida\n
    del mundo.
    """

    def __init__(self, pos_x, pos_y):
        Tile.__init__(self, pos_x, pos_y)
        self.is_food = True

    def __str__(self):
        return "Food"


class Tree(Object_base):
    """
    Clase que representa los árboles del mundo.
    """
    def __init__(self, pos_x, pos_y, max_life):
        Tile.__init__(self, pos_x, pos_y)
        self.max_life = max_life
        self.is_tree = True
        self.age = 0

    def __str__(self):
        return "Tree"
    
    def get_older(self):
        self.age += 1
