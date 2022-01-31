from object_base import *
import perlin
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
        self.map = []
        elevation = perlin.generate_elevation_matrix(dimension_x,dimension_y)
        self.init_map(dimension_x, dimension_y, elevation)
        self.trees = []
        self.add_tree(trees)

    def __str__(self):
        m = ""
        for i in range(self.dimension_x):
            for j in range(self.dimension_y):
                m += str(self.map[i][j]) + " "
            m += "\n"
        return m

    def init_map(self, dimension_x, dimension_y, elevation):
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
            self.map.append([])
            for j in range(dimension_y):
                self.map[i].append([])
                base = Tile(i, j)
                base.height = elevation[i][j]
                self.map[i][j] = (base)
                if i == 0 or i == dimension_x - 1:
                    self.map[i][j].is_edge = True
                elif j == 0 or j == dimension_y - 1:
                    self.map[i][j].is_edge = True
    
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
                tree = Tree(pos_x, pos_y, max_life)
                self.trees.append(tree)
                self.map[pos_x][pos_y].object_list.append(tree)
                self.map[pos_x][pos_y].has_tree = True
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
            food_amount = randint(0, int(max_food/len(self.trees)))
            tries = 0
            while food_amount > 0 and tries < 10:
                pos_x, pos_y = tree.pos_x + randint(-1, 1), tree.pos_y + randint(-1, 1)
                if (
                    not self.cell_is_edge(pos_x, pos_y)
                    and not self.cell_have_tree(pos_x, pos_y)
                    ):
                    self.map[pos_x][pos_y].object_list.append(Food(pos_x, pos_y))
                    self.map[pos_x][pos_y].has_food = True
                    food_amount = food_amount - 1
                    used = used + 1
                tries += 1
                    
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
            food_amount -= self.add_trees_food(food_amount)
        while food_amount > 0:
            u = randint(0, self.dimension_x * self.dimension_y - 1)
            pos_x, pos_y = u // self.dimension_y, u % self.dimension_y
            if (
                not self.cell_is_edge(pos_x, pos_y)
                and not self.cell_have_tree(pos_x, pos_y)
                ):
                self.map[pos_x][pos_y].object_list.append(Food(pos_x, pos_y))
                self.map[pos_x][pos_y].has_food = True
                food_amount = food_amount - 1

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
        return self.map[pos_x][pos_y].is_edge

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
        if self.map[pos_x][pos_y].has_food:
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
        return self.map[pos_x][pos_y].has_tree
    
      
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
        self.map[new_pos_x][new_pos_y].object_list.append(agent)
        self.map[new_pos_x][new_pos_y].has_agent = True
        self.map[agent.pos_x][agent.pos_y].object_list.remove(agent)
        self.map[agent.pos_x][agent.pos_y].has_agent = False

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
        for c in self.map[food_pos_x][food_pos_y].object_list:
            if isinstance(c, Food):
                return True, True, c
            if (
                c.__class__ == agent.__class__
                and (agent.genetic_code.get_gene('size').value - 2 >=
                     c.genetic_code.get_gene('size').value)
                and c.is_alive
            ):
                return True, False, c

        return False, False, None
    
    def agents_have_sex(self, couple_x, couple_y, agent):
        """
        Comprueba si existe una posible pareja en la casilla (couple_x, couple_y),
        de existir, practican la reproducción sexual y devuelve verdadero,
        devuelve falso en otro caso.

        :param couple_x: coordenada x de la casilla
        :type couple_x: int
        :param couple_y: coordenada y de la casilla
        :type couple_y: int

        :rtype: bool
        :return: True || False
        """
        for c in self.map[food_pos_x][food_pos_y].object_list:
            if isinstance(c, Food):
                return True, True, c
            if (
                c.__class__ == agent.__class__
                and (agent.genetic_code.get_gene('size').value - 2 >=
                     c.genetic_code.get_gene('size').value)
                and c.is_alive
            ):
                return True, False, c

        return False, False, None

    def get_pos_random_edge(self):
        """
        Devulve las coordenadas de fila y columna de algún borde. El borde
        se elige de manera aleatoria.

        :rtype: int, int
        :return: r, c
        """
        r = randint(0, self.dimension_x - 1)
        if r == 0 or r == self.dimension_x - 1:
            c = randint(1, self.dimension_y - 2 )
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
        self.map[edge_pos_x][edge_pos_y].object_list.append(agent)

    def remove_agent(self, agent):
        """
        Elimina un agente del mundo.

        :param agent: instancia del agente
        :type agent: Agent

        :rtype: None
        """
        self.map[agent.pos_x][agent.pos_y].object_list.remove(agent)
        self.map[agent.pos_x][agent.pos_y].has_agent = False

    def remove_tree(self): 
        """
        Elimina los árboles que ya hayan envejecido\n
        demasiado de la simulación.
        
        :rtype: None
        """       
        for r in range(1, self.dimension_x - 1):
            for c in range(1, self.dimension_y - 1):
                for k in range(len(self.map[r][c].object_list) - 1, -1, -1):
                    if (isinstance(self.map[r][c].object_list[k], Tree)  and 
                        self.map[r][c].object_list[k].max_life == 
                        self.map[r][c].object_list[k].age):
                        self.map[r][c].object_list.pop(k)
                        self.map[r][c].has_tree = False
    
    def remove_footprints(self):
        """
        Evapora las feromonas, y si esta llega al\n
        tiempo máximo de existencia, la elimina
      
        :rtype: None
        """   
        for r in range(1, self.dimension_x - 1):
            for c in range(1, self.dimension_y - 1):
                footprints = self.map[r][c].footprints
                for f in footprints:
                    f.disappear()
                    if f.time == 0:
                        footprints.remove(f)
    
    def remove_food(self):
        """
        Remueve la comida de la simulación, y\n
        con una probabilidad muy pequeña, la transforma\n
        en un árbol.
        
        :rtype: None
        """   
        for r in range(1, self.dimension_x - 1):
            for c in range(1, self.dimension_y - 1):
                for k in range(len(self.map[r][c].object_list) - 1, -1, -1):
                    if self.map[r][c].has_food:
                        if not self.map[r][c].has_tree and random() < 0.02:
                            max_life = randint(1, 10)
                            tree = Tree(r, c, max_life)
                            self.map[r][c].object_list[k] = tree
                            self.trees.append(tree)
                            self.map[r][c].has_tree = True
                        else:
                            self.map[r][c].object_list.pop(k)
                self.map[r][c].has_food = False
                            
        
class Tile:
    """
    Clase que representa una casilla del mapa\n. 
    Todos los elementos del mundo se ubican sobre él.
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
        self.footprints = []
        self.object_list = []
        self.height = 0

    def __str__(self):
        return "Nothing"