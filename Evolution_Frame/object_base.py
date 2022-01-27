class ObjectBase:
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

        :rtype: ObjectBase
        """
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.is_edge = False
        self.is_food = False
        self.is_tree = False
        self.is_soil = False
        self.can_pass = True
        self.smell = []
        self.height = 0

    def __str__(self):
        return "Nothing"


class Edge(ObjectBase):
    """
    Clase que representa el borde del mundo.
    """

    def __init__(self, pos_x, pos_y):
        ObjectBase.__init__(self, pos_x, pos_y)
        self.is_edge = True

    def __str__(self):
        return "Edge"


class Food(ObjectBase):
    """
    Clase que representa la comida\n
    del mundo.
    """

    def __init__(self, pos_x, pos_y):
        ObjectBase.__init__(self, pos_x, pos_y)
        self.is_food = True

    def __str__(self):
        return "Food"


class Tree(ObjectBase):
    """
    Clase que representa los árboles del mundo.
    """
    def __init__(self, pos_x, pos_y, max_life):
        ObjectBase.__init__(self, pos_x, pos_y)
        self.is_tree = True
        self.max_life = max_life
        self.age = 0

    def __str__(self):
        return "Tree"
    
    def get_older(self):
        self.age += 1
