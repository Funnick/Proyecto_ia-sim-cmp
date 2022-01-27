import object_base
from random import randint, random


class World:
    """
    Clase que representa el mundo de la simulación,\n
    contiene un mapa con los agentes y comida.\n
    """

    def __init__(self, dimension_x, dimension_y, trees = 0):
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
        self.init_map(dimension_x, dimension_y)
        
        self.trees = []
        self.add_tree(trees)

    def __str__(self):
        m = ""
        for i in range(self.dimension_x):
            for j in range(self.dimension_y):
                m += str(self.map[i][j][-1]) + " "
            m += "\n"
        return m

    def init_map(self, dimension_x, dimension_y):
        """
        Crea un mapa inicial, con suelo en todo el terreno y\n
        añade bordes. Esta función es llamada en el constructor.
        :param dimension_x: largo del mundo
        :type: int
        :param dimension_y: ancho del mundo
        :type: int
        
        :rtype: None
        """
        for i in range(dimension_x):
            for j in range(dimension_y):
                if i == 0 or i == dimension_x - 1:
                    self.map[i][j].append(object_base.Edge(i, j))
                elif j == 0 or j == dimension_y - 1:
                    self.map[i][j].append(object_base.Edge(i, j))
                else: self.map[i][j].append(object_base.Soil(i, j))

    def add_soil(self, pos_x, pos_y, amount = 1):
        """
        Añade más nivel de suelo al mundo.
        :param pos_x: x de la coordenada para colocar más suelo en el mundo.
        :type pos_x: int
        :param pos_y: y de la coordenada para colocar más suelo en el mundo.
        
        :rtype: None
        """
        self.map[pos_x][pos_y][1].level_up(amount)
        
    def del_soil(self, pos_x, pos_y, amount = 1):
        """
        Elimina nivel de suelo al mundo.
        :param pos_x: x de la coordenada para retirar suelo del mundo.
        :type pos_x: int
        :param pos_y: y de la coordenada para retirar más suelo del mundo.
        
        :rtype: None
        """
        self.map[pos_x][pos_y][1].level_down(amount)
    
    def add_tree(self, count):
        """
        Añade árboles al mundo. No añade árboles en los bordes.

        :param count: cantidad de árboles que se quiere añadir
        :type count: int

        :rtype: None
        """
        while count > 0:
            u = randint(0, self.dimension_x * self.dimension_y - 1)
            pos_x, pos_y = u // self.dimension_y, u % self.dimension_y
            if not self.cell_is_edge(pos_x, pos_y) and not self.cell_have_tree(pos_x, pos_y):
                max_life = randint(1, 10)
                tree = object_base.Tree(pos_x, pos_y, max_life)
                self.trees.append(tree)
                self.map[pos_x][pos_y].append(tree)
                count = count - 1
    
    def add_trees_food(self, max_food):
        """
        Añada comida al mundo desde los árboles. No añade árboles\n
        en los bordes.

        :param max_food: cantidad de comida máxima que se quiere añadir por cada árbol
        :type max_food: int

        :rtype: int
        """
        used = 0
        for tree in self.trees:
            tree.get_older()
            food_amount = randint(0, max_food)
            while food_amount > 0:
                pos_x, pos_y = tree.pos_x + randint(-1, 1), tree.pos_y + randint(-1, 1)
                if (
                    not self.cell_is_edge(pos_x, pos_y)
                    and not self.cell_have_tree(pos_x, pos_y)
                    ):
                    self.map[pos_x][pos_y].append(object_base.Food(pos_x, pos_y))
                    food_amount = food_amount - 1
                    used = used + 1
        return used
        
    
    def add_food(self, food_amount):
        """
        Añade comida al mundo. No añade comida en los bordes.\n
        Algunas comidas aparecerán aleatoriamente por el mundo,\n
        otras se concentrarán alrededor de los árboles.

        :param food_amount: cantidad de comida que se quiere añadir
        :type food_amount: int

        :rtype: None
        """
        if len(self.trees):
            max_food = randint(0, int(food_amount/len(self.trees)))
            food_amount = food_amount - self.add_trees_food(max_food)
        while food_amount > 0:
            u = randint(0, self.dimension_x * self.dimension_y - 1)
            pos_x, pos_y = u // self.dimension_y, u % self.dimension_y
            if (
                not self.cell_is_edge(pos_x, pos_y)
                and not self.cell_have_tree(pos_x, pos_y)
                ):
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
        es copiada es el cuadrado que tiene esquina superior izquierda
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
            if isinstance(c, object_base.Edge):
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

    def cell_have_food(self, pos_x, pos_y, agent):
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
            if c.is_food or (
                c.__class__ == agent.__class__
                and hasattr(c, "size_gene")
                and agent.size_gene.value - 2 >= c.size_gene.value
                and c.is_alive
            ):
                return True
        return False

    def cell_have_tree(self, pos_x, pos_y):
        """
        Determina si existe un árbol en la casilla (pos_x, pos_y)

        :param pos_x: coordenada x de la casilla
        :type pos_x: int
        :param pos_y: coordenada y de la casilla
        :type pos_y: int

        :rtype: bool
        :return: True || False
        """
        for c in self.map[pos_x][pos_y]:
            if c.is_tree:
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

    def agent_eat_food(self, food_pos_x, food_pos_y, agent):
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
                return True, None
            if (
                c.__class__ == agent.__class__
                #and hasattr(c, "size_gene")
                and agent.genetic_code['size'].value - 2 >= c.genetic_code['size'].value
                and c.is_alive
            ):
                return True, c

        return False, None

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

    def remove_tree(self):        
        for r in range(1, self.dimension_x - 1):
            for c in range(1, self.dimension_y - 1):
                for k in range(len(self.map[r][c]) - 1, -1, -1):
                    if (
                        self.map[r][c][k].is_tree and 
                        self.map[r][c][k].max_life == self.map[r][c][k].age
                        ):
                        self.map[r][c].pop(k)
    
    def remove_food(self):
        for r in range(1, self.dimension_x - 1):
            for c in range(1, self.dimension_y - 1):
                for k in range(len(self.map[r][c]) - 1, -1, -1):
                    if self.map[r][c][k].is_food:
                        self.map[r][c].pop(k)
