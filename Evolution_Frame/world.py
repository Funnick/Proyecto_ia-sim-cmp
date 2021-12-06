import object_base
from random import randint, random


class World:
    """
    Clase que representa el mundo de la simulación,\n
    contiene un mapa con los agentes y comida.\n
    """

    def __init__(self, dimension_x, dimension_y):
        """
        Crea un nuevo mundo de tamaño dimension_x * dimension_y, también se
        añaden los bordes.

        :param dimension_x: largo del mundo
        :type dimension_x: int
        :param dimension_y: ancho del mundo
        :type dimension_y: int

        :rtype: World
        """
        self.dimension_x = dimension_x
        self.dimension_y = dimension_y
        self.map = [
            [[object_base.ObjectBase(i, j)] for i in range(dimension_y)]
            for j in range(dimension_x)
        ]
        self.add_edges()

    def add_edges(self):
        """
        Añade los bordes al mundo. Esta función es llamada en el constructor.

        :rtype: None
        """
        for i in range(self.dimension_y):
            self.map[0][i][0] = object_base.Edge(0, i)
            self.map[self.dimension_x - 1][i][0] = object_base.Edge(
                self.dimension_x - 1, i
            )
        for i in range(1, self.dimension_x - 1):
            self.map[i][0][0] = object_base.Edge(i, 0)
            self.map[i][self.dimension_y - 1][0] = object_base.Edge(
                i, self.dimension_y - 1
            )

    def __str__(self):
        m = ""
        for i in range(self.dimension_x):
            for j in range(self.dimension_y):
                m += str(self.map[i][j][-1]) + " "
            m += "\n"
        return m

    def add_food(self, food_amount):
        """
        Añade comida al mundo. No añade comida en los bordes.

        :param food_amount: cantidad de comida que se quiere añadir
        :type food_amount: int

        :rtype: None
        """
        while food_amount > 0:
            u = randint(0, self.dimension_x * self.dimension_y - 1)
            pos_x, pos_y = u // self.dimension_y, u % self.dimension_y
            if not self.map[pos_x][pos_y][0].is_edge:
                self.map[pos_x][pos_y].append(object_base.Food(pos_x, pos_y))
                food_amount = food_amount - 1

    def get_a_peek(
        self,
        left_corner_x,
        left_corner_y,
        right_corner_x,
        right_corner_y,
        dimension_x,
        dimension_y,
    ):
        """
        Devuelve un nuevo mundo, de tamaño dimension_x * dimension_y,
        que es una copia de un lugar del mundo original. La parte que
        es copiada es el cuadrado que tiene esquina superior izqueda
        (left_corner_x y left_corner_y) y esquina inferior derecha
        (right_corner_x y right_corner_y).

        :param left_corner_x: coordenada x, esquina superior izquierda
        :type left_corner_x: int
        :param left_corner_y: coordenada y, esquina superior izquierda
        :type left_corner_y: int
        :param right_corner_x: coordenada x, esquina inferior derecha
        :type right_corner_x: int
        :param right_corner_y: coordenada y, esquina inferior derecha
        :type right_corner_y: int
        :param dimension_x: largo de la copia
        :type dimension_x: int
        :param dimension_y: ancho de la copia
        :type dimension_y: int

        :rtype: World
        :return: w
        """
        w = World(dimension_x, dimension_y)
        d_x, d_y = 0, 0
        for i in range(left_corner_x, right_corner_x + 1):
            for j in range(left_corner_y, right_corner_y + 1):
                w.map[d_x][d_y] = self.map[i][j]
                d_y = d_y + 1
            d_x = d_x + 1
            d_y = 0

        return w

    def cell_is_edge(self, pos_x, pos_y):
        """
        Determina si una casilla del mapa es un borde.

        :param pos_x: coordenada x de la casilla
        :type pos_x: int
        :param pos_y: coordenada y de la casilla
        :type pos_y: int

        :rtype: bool
        :return: True || False
        """
        for c in self.map[pos_x][pos_y]:
            if c.is_edge:
                return True
        return False

    def valid_cell_to_move(self, pos_x, pos_y):
        """
        Determina si la posición (pos_x, pos_y) del mapa es una casilla válida para moverse.

        :param pos_x: coordenada x del mapa
        :type pos_x: int
        :param pos_y: coordenada y del mapa
        :type pos_y: int

        :rtype: bool
        :return: return (pos_x >= 0 and pos_x < self.dimension_x and pos_y >= 0 and pos_y < self.dimension_y)
        """
        return (
            pos_x >= 0
            and pos_x < self.dimension_x
            and pos_y >= 0
            and pos_y < self.dimension_y
        )

    def cell_have_food(self, pos_x, pos_y):
        """
        Determina si existe comida en la casilla (pos_x, pos_y)

        :param pos_x: coordenada x de la casilla
        :type pos_x: int
        :param pos_y: coordenada y de la casilla
        :type pos_y: int

        :rtype: bool
        :return: True || False
        """
        for c in self.map[pos_x][pos_y]:
            if c.is_food:
                return True
        return False

    def move_agent(self, agent, new_pos_x, new_pos_y):
        """
        Reubica un agente en el mapa a la casilla (new_pos_x, new_pos_y)

        :param agent: la intancia de un agente de la simulación
        :type agent: Agent
        :param new_pos_x: coordenada x de la nueva ubicación
        :type new_pos_x: int
        :param new_pos_y: coordenada y de la nueva ubicación
        :type new_pos_y: int

        :rtype: None
        """
        self.map[new_pos_x][new_pos_y].append(agent)
        self.map[agent.pos_x][agent.pos_y].remove(agent)

    def agent_eat_food(self, food_pos_x, food_pos_y):
        """
        Comprueba si existe comida en la casilla (food_pos_x, food_pos_y), de existir
        la remueve y devuelve verdadero, devuelve falso en otro caso.

        :param food_pos_x: coordenada x de la casilla
        :type food_pos_x: int
        :param food_pos_y: coordenada y de la casilla
        :type food_pos_y: int

        :rtype: bool
        :return: True || False
        """
        for c in self.map[food_pos_x][food_pos_y]:
            if c.is_food:
                self.map[food_pos_x][food_pos_y].remove(c)
                return True
        return False

    def get_pos_random_edge(self):
        """
        Devulve las coordenadas de fila y columna de algún borde. El borde
        se elige de manera aleatoria.

        :rtype: int, int
        :return: r, c
        """
        r = randint(0, self.dimension_x - 1)
        if r == 0 or r == self.dimension_x - 1:
            c = randint(0, self.dimension_y - 1)
        elif random() <= 0.5:
            c = 0
        else:
            c = self.dimension_y - 1
        return r, c

    def add_agent(self, edge_pos_x, edge_pos_y, agent):
        """
        Añade al mundo un agente en el borde (edge_pos_x, edge_pos_y).

        :param edge_pos_x: coordenada x del borde
        :type edge_pos_x: int
        :param edge_pos_y: coordenada y del borde
        :type edge_pos_y: int
        :param agent: instancia del agente
        :type agent: Agent

        :rtype: None
        """
        self.map[edge_pos_x][edge_pos_y].append(agent)

    def remove_agent(self, agent):
        """
        Elimina un agente del mundo.

        :param agent: instancia del agente
        :type agent: Agent

        :rtype: None
        """
        self.map[agent.pos_x][agent.pos_y].remove(agent)
