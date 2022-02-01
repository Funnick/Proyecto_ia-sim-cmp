from object_base import *
import gene
import action
from random import randint
from math import sqrt

directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
directions_actions = [
    action.MoveNorth(),
    action.MoveSouth(),
    action.MoveWest(),
    action.MoveEast()
]
class Agent(Object_base):
    """
    Clase que reprenseta a los agentes de la simulación.
    """

    def __init__(self, pos_x, pos_y, max_energy = 100):
        """
        Inicializa un agente en la posición (pos_x, pos_y) con una energía máxima (max_energy).

        :param pos_x: coordenada x del agente
        :type pos_x: int
        :param pos_y: coordenada y del agente
        :type pos_y: int
        :param max_energy: energía máxima del agente
        :type max_energy: int

        :rtype: Agent
        """
        Object_base.__init__(self, pos_x, pos_y)
        self.is_alive = True
        self.food_eat_today = 0
        self.max_energy = max_energy
        self.current_energy = max_energy
        self.life_span = 10
        self.pregnant = False
        self.age = 0
        self.genetic_code = gene.GeneticCode()
        self.energy_lost_fun = lambda sense, speed, size: (
            self.genetic_code.get_gene('sense').value *
            self.genetic_code.get_gene('speed').value + 
            self.genetic_code.get_gene('size').value)

    def __str__(self):
        return "Agent"

    def set_random_genetic(self):
        for gene in range(randint(3)):
            self.genetic_code
        
    def sexual_reproduction(self, other_agent):
        """
        Realiza la reproducción sexual entre dos agentes,
        combinando su genética.
        
        :param other_agent: agente con el cual se realizará la reproducción
        :type other_agent: Agent
        
        :rtype: Agent
        :return: child_agent
        """
        child_max_energy = (self.max_energy + other_agent.max_energy)/2
        child_agent = Agent(-1, -1, child_max_energy)
        child_agent.genetic_code = self.genetic_code + other_agent.genetic_code
        return child_agent
    
    def asexual_reproduction(self):
        """
        Devuelve un nuevo agente que puede tener características mutadas,
        es el resultado de una reproducción asexual.

        :rtype: Agent
        :return: child_agent
        """
        child_agent = Agent(-1, -1, self.max_energy)
        child_agent.genetic_code = self.mutate()
        return child_agent
    
    def add_gene(self, gene):
        """
        Agrega un gen al agente.
        :param gene: gen que se va a agregar

        :rtype: None
        """
        self.genetic_code.add_gene(gene)
        
    def have_gene(self, gene):
        """
        Comprueba si el agente posee un gen.
        :param gene: gen a comprobar si el agente lo posee

        :rtype: bool
        ::return: True || False
        """
        if self.genetic_code.have_gene(gene):
            return True
        else:
            return False
        
    def mutate(self):
        """
        Hace mutar todos los genes que posee el agente.

        :rtype: GeneticCode
        :return: child_genetic_code
        """
        child_genetic_code = self.genetic_code.mutate()
        return child_genetic_code
    
    def get_older(self):
        """
        Envejece al agente en un punto.\n
        Retorna la edad del agente.
        
        :rtype: int
        
        """
        self.age += 1
        if self.life_span == self.age:
            self.is_alive = False
        return self.age
       
    def reduce_energy_to_perform_an_action(self):
        """
        Devuelve verdadero en caso de que se pueda consumir energía
        para realizar una acción, falso en otro caso.

        :rtype: bool
        :return: self.current_energy >= self.sense_gene.value
        """
        elf = self.energy_lost_fun(
            self.genetic_code.get_gene('sense').value,
            self.genetic_code.get_gene('speed').value,
            self.genetic_code.get_gene('size').value
        )
        if self.current_energy >= elf:
            self.current_energy = self.current_energy - elf
            return True
        return False
    
    def in_limits(self, pos, perception):
        """
        Recibe una posición y verifica si se encuentra en los
        límites establecidos.
        
        :param pos: coordenadas de la posición
        :type pos: Tuple[int, int]
        :param perception: coordenadas de los límites
        :param perception: Tuple[int, int, int, int]
        """
        if (pos[0] >= perception[0] and
            pos[0] <= perception[1] and
            pos[1] >= perception[2] and
            pos[1] <= perception[3]):
            return True
        else:
            return False
               
    def move(self, perception):
        """
        Retorna una lista de acciones que debe realizar el agente\n
        para acercarce lo más posible a conseguir alimento y sobrevivir\n
        en el día.

        :param perception.Item1: Mundo en el que se encuentra el agente
        :type perception.Item1: World
        :param perception.Item2: Límites de visión del agente
        :type perception.Item2: Tuple[int,int,int,int]
        :param perception.Item3: Lista de alimentos vistos por el agente
        :type perception.Item3: List
        :param perception.Item4: Lista de árboles vistos por el agente
        :type perception.Item4: List
        :param perception.Item5: Lista de enemigos vistos por el agente
        :type perception.Item5: List
        :param perception.Item6: Lista de posibles parejas vistas por el agente
        :type perception.Item6: List

        :rtype: Action list
        """
        global directions
        global directions_actions
        if self.current_energy < self.energy_lost_fun(
            self.genetic_code.get_gene('sense').value, 
            self.genetic_code.get_gene('speed').value, 
            self.genetic_code.get_gene('size').value):
            return [action.DoNothing()]
        
        world = perception[0]
        limits = perception[1]
        foods = perception[2]
        trees = perception[3]
        enemies = perception[4]
        couples = perception[5]
        plan = []
        path = []

        queue = [(self.pos_x, self.pos_y)]
        steps = 0
        max_steps = self.genetic_code.get_gene('speed').value
        current_food = 0
        while (steps < max_steps):
            cell = queue.pop(0)
            path.append(cell)
            best_move = [10000,-1,None]
            
            # Reglas ----------------------------------
            if self.food_eat_today == 0:
                eat_coeficent = 1
                tree_coeficent = 0.30
                edge_coeficent = 0
                sex_coeficent = 0.10
            elif self.food_eat_today == 1:
                if self.current_energy < self.max_energy / 2:
                    eat_coeficent = 0
                    tree_coeficent = 0.10
                    edge_coeficent = 1
                    sex_coeficent = 0.2
                else: 
                    eat_coeficent = 0.5
                    tree_coeficent = 0.15
                    edge_coeficent = 0.1
                    sex_coeficent = 0.15
            else:
                eat_coeficent = 0
                tree_coeficent = 0.10
                edge_coeficent = 1
                sex_coeficent = 0.2
            if self.pregnant:
                sex_coeficent = 0
            # --------------------------------------------
            for i in range(4):
                new_cell = (cell[0] + directions[i][0], cell[1] + directions[i][1])
                if (self.in_limits((new_cell[0], new_cell[1]), limits)):
                    
                    if (world.cell_is_edge(new_cell[0], new_cell[1]) and 
                        self.food_eat_today == 0):
                        continue
                        
                    footprints = 0.1 * len(world.map[new_cell[0]][new_cell[1]].footprints)
                    
                    foods_nearby = eat_coeficent * mean([manhattan([new_cell[0], new_cell[1]], [i[0], i[1]])
                                for i in foods])
                    
                    trees_nearby = tree_coeficent * mean([manhattan([new_cell[0], new_cell[1]], [i[0], i[1]])
                                for i in trees])
                    
                    couples_nearby = sex_coeficent * mean([manhattan([new_cell[0], new_cell[1]], [i[0], i[1]])
                                for i in couples])
                    
                    enemies_nearby = mean([manhattan([new_cell[0], new_cell[1]], [i[0], i[1]])
                                for i in enemies])
                    
                    elevation_diff = 0.1 * abs(world.map[new_cell[0]][new_cell[1]].height -
                                world.map[cell[0]][cell[1]].height)
                    
                    cells_visited = 8 if new_cell in path else 0
                    
                    edges = [abs(new_cell[0] - (world.dimension_x -1)),
                             abs(new_cell[1] - (world.dimension_y -1)),
                             new_cell[0], new_cell[1]]
                    
                    edges_nearbys = edge_coeficent * mean(edges)
                    
                    total = (footprints +
                             foods_nearby +
                             trees_nearby -
                             enemies_nearby -
                             elevation_diff +
                             cells_visited +
                             edges_nearbys +
                             couples_nearby)
                    
                    if total < best_move[0]:
                        best_move[0] = total
                        best_move[1] = i
                        best_move[2] = new_cell
                        
            queue.append(best_move[2])
            plan.append(directions_actions[best_move[1]])
            if not self.pregnant and (best_move[2][0],best_move[2][1]) in couples:
                plan.append(action.HaveSex())
            if self.food_eat_today > 0 and world.map[best_move[2][0]][best_move[2][1]].is_edge:
                plan.append(action.DoNothing())
                break
            if ((best_move[2][0],best_move[2][1]) in foods and 
                self.food_eat_today + current_food <= 2):
                current_food += 1
                plan.append(action.Eat())
                foods.remove(best_move[2])
            steps += 1
        return plan
    
    def see_around(self, world):
        """
        Devuelve la percepción del mundo que tiene el agente.
        La percepción son los límites del campo de visión del agente,
        de tamaño dimension_x * dimension_y. La parte que
        es copiada es el cuadrado que tiene esquina superior izquierda
        (left_corner_x y left_corner_y) y esquina inferior derecha
        (right_corner_x y right_corner_y). Además, hay listas de
        elementos relevantes vistos por el agente, como comida, árboles y
        enemigos.

        :param left_corner_x: coordenada x, esquina superior izquierda
        :type left_corner_x: int
        :param left_corner_y: coordenada y, esquina superior izquierda
        :type left_corner_y: int
        :param right_corner_x: coordenada x, esquina inferior derecha
        :type right_corner_x: int
        :param right_corner_y: coordenada y, esquina inferior derecha
        :type right_corner_y: int
        :param foods: coordenadas de las comidas vistas por el agente
        :type foods: list
        :param trees: coordenadas de los árboles vistos por el agente
        :type trees: list
        :param enemies: coordenadas de los enemigos vistos por el agente
        :type enemies: list
        :param couples: coordenadas de las posibles parejas vistas por el agente
        :type couples: list

        :rtype: World
        :return:(world, 
                 (left_corner_x,
                  right_corner_x,
                  left_corner_y,
                  right_corner_y),
                 foods,
                 trees,
                 enemies,
                 couples)
        """
        left_corner_x = max(0, self.pos_x - self.genetic_code.get_gene('sense').value)
        left_corner_y = max(0, self.pos_y - self.genetic_code.get_gene('sense').value)
        right_corner_x = min(self.pos_x + self.genetic_code.get_gene('sense').value,
                             world.dimension_x - 1)
        right_corner_y = min(self.pos_y + self.genetic_code.get_gene('sense').value,
                             world.dimension_y - 1)
        foods = []
        trees = []
        enemies = []
        couples = []
        
        for i in range(left_corner_x, right_corner_x + 1):
            for j in range(left_corner_y, right_corner_y + 1):
                current_tile = world.map[i][j]
                for element in current_tile.object_list:
                    if isinstance(element, Food):
                        foods.append((i,j))
                    elif isinstance(element, Tree):
                        trees.append((i,j))
                    elif not(element is self) and isinstance(element, self.__class__):
                        agent = element
                        if (agent.genetic_code.get_gene('size').value - 2 >=
                            self.genetic_code.get_gene('size').value):
                            enemies.append((i,j))
                        elif (self.genetic_code.get_gene('size').value - 2 >=
                            agent.genetic_code.get_gene('size').value):
                            foods.append((i,j))
                        elif (self.genetic_code.get_gene('reproduction').value == 2 and
                            agent.genetic_code.get_gene('reproduction').value == 2): 
                            couples.append((i,j))
                        
        return (world,
                (left_corner_x,
                 right_corner_x,
                 left_corner_y,
                 right_corner_y),
                foods,
                trees,
                enemies,
                couples)
    
    def set_footprint(self, world):
        """
        Método para ubicar una pisada del agente en una casilla
        """
        world.map[self.pos_x][self.pos_y].footprints.append(Footprint())
        
class Footprint:
    """
    Clase utilizada para describir la marca dejada por un agente
    al pisar sobre una casilla.
    """
    def __init__(self, value = 1, time = 2):
        """
        :param value: valor de relevancia de la pisada
        :type value: int
        :param time: tiempo de duración de la pisada
        :type time: int
        
        rtype: Footprint
        """
        self.value = value
        self.time = 2
    
    def disappear(self):
        """
        Método para disminuir el tiempo de existencia
        de una marca de pisada.
        
        :rtype: None
        """
        self.time -= 1
    
def mean(array):
    """
    Función para calcular la media, dando relevancia a los
    valores más pequeños.
    
    :param array: lista de elementos a hallarle la media
    :type array: list
    
    :rtype: float
    :return: mean
    """
    total = len(array)
    sum_elem = 0
    for elem in array:
        sum_elem = sum_elem + 1/elem if elem != 0 else sum_elem + 1
    mean = total/sum_elem if len(array) or sum_elem!=0 else 0
    return mean

def manhattan(pos1, pos2):
    """
    Función para calcular la distancia manhattan entre
    dos coordenas de una matriz
    
    :param pos1: primera coordenada
    :type pos1: Tuple[int, int]
    :param pos2: segunda coordenada
    :type pos2: Tuple[int, int]
    
    :rtype: int
    :return: distance
    """
    distance = int(abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1]))
    return distance
