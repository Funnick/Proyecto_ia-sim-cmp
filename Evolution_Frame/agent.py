from object_base import *
from action import *
from aux_meth import manhattan, mean
from random import randint
from gene import GeneticCode

directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
directions_actions = [
    MoveNorth(),
    MoveSouth(),
    MoveWest(),
    MoveEast()
]
class Agent(Object_base):
    """
    Clase que reprensenta a los agentes de la simulación.
    """

    def __init__(self, pos_x = -1, pos_y = -1, genes = [], behavior = None, states = None):
        """
        Inicializa un agente en la posición (pos_x, pos_y) con una energía máxima (max_energy).

        :param pos_x: coordenada x del agente
        :type pos_x: int
        :param pos_y: coordenada y del agente
        :type pos_y: int
        :param genes: lista de genes que serán pasados al agente

        :rtype: Agent
        """
        Object_base.__init__(self, pos_x, pos_y)
        self.is_alive = True
        self.food_eat_today = 0
        self.pregnant = []
        self.age = 0
        self.set_genetic(genes)
        self.max_energy = self.genetic_code.get_gene('stamina').value
        self.current_energy = self.max_energy
        self.life_span = self.genetic_code.get_gene('life').value
        self.energy_lost_fun = lambda sense, speed, size: (
            self.genetic_code.get_gene('sense').value +
            self.genetic_code.get_gene('speed').value*2 + 
            self.genetic_code.get_gene('size').value*3)

        self.actual_state = []
        self.states = states
        if not states:
            self.states = {}
            self.set_default_states()
        self.behavior = behavior
        if not behavior:
            self.behavior = Behavior(self)
            self.set_default_behavior()
        
        
    def __str__(self):
        return "Agent"

    # Genética -------------------------------------------------------------
    def set_genetic(self, genes = []):
        """
        Agrega un código genético al agente con los valores predeterminados,
        o genes diseñados por el usuario.
        
        :rtype: None
        """
        genetic = GeneticCode(genes = genes)
        self.genetic_code = genetic
    
    def set_gen(self, gene):
        """
        Sustituye un gen del agente por otro del mismo tipo.
        
        :param gene: nuevo gen que reemplazará al anterior.
        :type gene: Gene
        
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
        
    def sexual_reproduction(self, other_agent):
        """
        Realiza la reproducción sexual entre dos agentes,
        combinando su genética.
        
        :param other_agent: agente con el cual se realizará la reproducción
        :type other_agent: Agent
        
        :rtype: Agent
        :return: childs
        """
        childs = []
        for child in range(self.genetic_code.get_gene('fertility').value):    
            if randint(0, 1):
                behavior = other_agent.behavior
                states = other_agent.states
            else:
                behavior = self.behavior
                states = self.states
            child_agent = Agent(-1, -1, behavior=behavior, states=states)
            child_agent.genetic_code = self.genetic_code + other_agent.genetic_code
            childs.append(child_agent)
            
        return childs
    
    def asexual_reproduction(self):
        """
        Devuelve un nuevo agente que puede tener características mutadas,
        es el resultado de una reproducción asexual.

        :rtype: Agent
        :return: child_agent
        """
        child_agent = Agent(-1, -1, behavior=self.behavior, states=self.states)
        child_agent.genetic_code = self.mutate()
        return child_agent
    
    def mutate(self):
        """
        Hace mutar todos los genes que posee el agente.

        :rtype: GeneticCode
        :return: child_genetic_code
        """
        child_genetic_code = self.genetic_code.mutate
        return child_genetic_code
    # -----------------------------------------------------------------------
    
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
       
    def reduce_energy_to_perform_an_action(self, coeficent = 0):
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
        ) + coeficent
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

        :rtype: Action list
        """
        global directions
        global directions_actions
        if self.current_energy < self.energy_lost_fun(
            self.genetic_code.get_gene('sense').value, 
            self.genetic_code.get_gene('speed').value, 
            self.genetic_code.get_gene('size').value):
            return [DoNothing()]
        
        world = perception[0]
        limits = perception[1]
        plan = []
        path = []
        self.update_state()
        queue = [(self.pos_x, self.pos_y)]
        steps = 0
        max_steps = self.genetic_code.get_gene('speed').value
        while (steps < max_steps):
            cell = queue.pop(0)
            path.append(cell)
            best_move = [10000,-1,None]
            
            for move in range(4):
                new_cell = (cell[0] + directions[move][0], cell[1] + directions[move][1])
                if (self.in_limits((new_cell[0], new_cell[1]), limits)):
                    if (world.cell_is_edge(new_cell[0], new_cell[1]) and 
                        self.food_eat_today == 0):
                        continue
                    
                    best_move_probability = 0
                    for rule in self.behavior.rules.values():
                        if rule.to_move:
                            if rule.to_relevance:
                                best_move_probability += (rule.to_relevance(self) * 
                                                          rule.to_move(cell, new_cell, world, path, rule.elements))
                    
                    if best_move_probability < best_move[0]:
                        best_move[0] = best_move_probability
                        best_move[1] = move
                        best_move[2] = new_cell
                        
            queue.append(best_move[2])
            plan.append(directions_actions[best_move[1]])
            if self.food_eat_today > 0 and world.map[best_move[2][0]][best_move[2][1]].is_edge:
                plan.append(DoNothing())
                break
            if not self.pregnant and (best_move[2][0], best_move[2][1]) in self.behavior.rules['couples'].elements:
                plan.append(HaveSex())
                self.behavior.rules['couples'].elements.remove(best_move[2])
            if ((best_move[2][0],best_move[2][1]) in self.behavior.rules['food'].elements):
                plan.append(Eat())
                self.behavior.rules['food'].elements.remove(best_move[2])
            steps += 1
            
        # Reiniciar elementos relevantes vistos
        for rule in self.behavior.rules.values():
            rule.elements = []
        return plan
    
    def see_around(self, world):
        """
        Devuelve la percepción del mundo que tiene el agente.
        La percepción son los límites del campo de visión del agente,
        de tamaño dimension_x * dimension_y. La parte que
        es copiada es el cuadrado que tiene esquina superior izquierda
        (left_corner_x y left_corner_y) y esquina inferior derecha
        (right_corner_x y right_corner_y). Además, revisa cada uno de los
        predicados del agente y verifica qué elementos le son relevantes.

        :param left_corner_x: coordenada x, esquina superior izquierda
        :type left_corner_x: int
        :param left_corner_y: coordenada y, esquina superior izquierda
        :type left_corner_y: int
        :param right_corner_x: coordenada x, esquina inferior derecha
        :type right_corner_x: int
        :param right_corner_y: coordenada y, esquina inferior derecha
        :type right_corner_y: int

        :rtype: World
        :return:(world, 
                 (left_corner_x,
                  right_corner_x,
                  left_corner_y,
                  right_corner_y))
        """
        self_sense = self.genetic_code.get_gene('sense').value
        
        left_corner_x = max(0, self.pos_x - self_sense)
        left_corner_y = max(0, self.pos_y - self_sense)
        right_corner_x = min(self.pos_x + self_sense, world.dimension_x - 1)
        right_corner_y = min(self.pos_y + self_sense, world.dimension_y - 1)
        
        for i in range(left_corner_x, right_corner_x + 1):
            for j in range(left_corner_y, right_corner_y + 1):
                current_tile = world.map[i][j]
                for element in current_tile.object_list:
                    for rule in self.behavior.rules.values():
                        if rule.to_see and rule.to_see(self, element):
                            rule.elements.append((i,j))
                        
        return (world,
                (left_corner_x,
                 right_corner_x,
                 left_corner_y,
                 right_corner_y))
    
    def set_default_behavior(self):
        """
        Agrega al agente un comportamiento predeterminado,
        con las reglas establecidas por nosostros.
        
        :rtype: None
        """
        
        # Configuración de la alimentación -------------------------------------------------
        def see_food(agent, element):
            self_diet = agent.genetic_code.get_gene('diet').value
            self_size = agent.genetic_code.get_gene('size').value
            if (isinstance(element, Food) and
                (self_diet == 1 or self_diet == 3)):
                return True
            elif (not(element is agent) and isinstance(element, agent.__class__) and 
                  (self_size - 2 >= element.genetic_code.get_gene('size').value and self_diet > 1)):
                return True
            
        def move_food(cell, new_cell, world = None, path = None, elements = None):
            return mean([manhattan([new_cell[0], new_cell[1]], [i[0], i[1]])
                  for i in elements])
        
        def relevance_food(agent):
            if 'starve' in agent.actual_state:
                return 1
            elif 'half' in agent.actual_state:
                if 'low_energy' in agent.actual_state:
                    return 0
                else:
                    return 0.5
            else:
                return 0
        
        self.behavior.set_rule(Rule('food', see_food, move_food, relevance_food))
        # ----------------------------------------------------------------------------------    
        
        # Configuración para los árboles ---------------------------------------------------
        def see_tree(agent, element):
            self_diet = agent.genetic_code.get_gene('diet').value
            if (isinstance(element, Tree) and 
                (self_diet == 1 or self_diet == 3)):
                return True
            
        def move_tree(cell, new_cell, world = None, path = None, elements = None):
            return mean([manhattan([new_cell[0], new_cell[1]], [i[0], i[1]])
                  for i in elements])
        
        def relevance_tree(agent):
            if 'starve' in agent.actual_state:
                return 0.30
            elif 'half' in agent.actual_state:
                if 'low_energy' in agent.actual_state:
                    return 0.10
                else:
                    return 0.15
            else:
                return 0.10
            
        self.behavior.set_rule(Rule('tree', see_tree, move_tree, relevance_tree))
        # ----------------------------------------------------------------------------------
        
        # Configuración para los enemigos --------------------------------------------------
        def see_enemies(agent, element):
            self_size = self.genetic_code.get_gene('size').value
            if (not(element is agent) and isinstance(element, agent.__class__) and 
                (element.genetic_code.get_gene('size').value - 2 >= 
                 self_size and element.genetic_code.get_gene('diet').value > 1)):
                return True
            
        def move_enemies(cell, new_cell, world = None, path = None, elements = None):
            return mean([manhattan([new_cell[0], new_cell[1]], [i[0], i[1]])
                  for i in elements])
        
        def relevance_enemies(agent):
            return -1
        
        self.behavior.set_rule(Rule('enemies', see_enemies, move_enemies, relevance_enemies))
        # ----------------------------------------------------------------------------------
        
        # Configuración para las posibles parejas ------------------------------------------
        def see_couples(agent, element):
            self_sex = agent.genetic_code.get_gene('sex').value
            self_repr = agent.genetic_code.get_gene('reproduction').value
            if (not(element is agent) 
                and isinstance(element, agent.__class__) 
                and (self_repr == 2 and element.genetic_code.get_gene('reproduction').value == 2 
                     and element.genetic_code.get_gene('sex').value != self_sex)): 
                return True
            
        def move_couples(cell, new_cell, world = None, path = None, elements = None):
            return mean([manhattan([new_cell[0], new_cell[1]], [i[0], i[1]])
                  for i in elements])
            
        def relevance_couples(agent):
            if 'pregnant' in agent.actual_state:
                return 0
            if 'starve' in agent.actual_state:
                return 0.20
            elif 'half' in agent.actual_state:
                if 'low_energy' in agent.actual_state:
                    return 0.10
                else:
                    return 0.15
            else:
                return 0.30
                
        self.behavior.set_rule(Rule('couples', see_couples, move_couples, relevance_couples))
        # -----------------------------------------------------------------------------------
        
        # Configuración para las elevaciones en el terreno ----------------------------------
        def move_elevation(cell ,new_cell, world = None, path = None, elements = None):
            return abs(world.map[new_cell[0]][new_cell[1]].height - 
                       world.map[cell[0]][cell[1]].height)
            
        def relevance_elevation(agent):
            return -0.1
        
        self.behavior.set_rule(Rule('elevation', to_move = move_elevation, to_relevance = relevance_elevation))
        # -----------------------------------------------------------------------------------
        
        # Configuración para las pisadas en el suelo ----------------------------------------
        def move_footprint(cell, new_cell, world = None, path = None, elements = None):
            return len(world.map[new_cell[0]][new_cell[1]].footprints)
            
        def relevance_footprint(agent):
            return 0.1
        
        self.behavior.set_rule(Rule('footprint', to_move = move_footprint, to_relevance = relevance_footprint))
        # ------------------------------------------------------------------------------------
        
        # Configuración para el camino ya visto ----------------------------------------------
        def move_visited(cell, new_cell, world = None, path = None, elements = None):
            return 1 if new_cell in path else 0
        
        def relevance_visited(agent):
            return 8
        
        self.behavior.set_rule(Rule('visited', to_move = move_visited, to_relevance = relevance_visited))
        # ------------------------------------------------------------------------------------
        
        # Configuración para la relevancia de los bordes -------------------------------------
        def move_edges(cell, new_cell, world = None, path = None, elements = None):
            edges = [abs(new_cell[0] - (world.dimension_x -1)), 
                     abs(new_cell[1] - (world.dimension_y -1)),
                     new_cell[0],
                     new_cell[1]]
                    
            return mean(edges)
        
        def relevance_edges(agent):
            if 'starve' in agent.actual_state:
                return 0
            elif 'half' in agent.actual_state:
                if 'low_energy' in agent.actual_state:
                    return 1
                else:
                    return 0.5
            else:
                return 1
        
        self.behavior.set_rule(Rule('edges', to_move = move_edges, to_relevance = relevance_edges))
        # ------------------------------------------------------------------------------------
    
    def set_state(self, state):
        """
        Agrega un nuevo estado al agente.
        
        :param state: estado a agregar
        :type state: State
        
        :rtype: None
        """
        self.states[state.name] = state
        
    def del_state(self, state):
        """
        Elimina un estado del agente.
        
        :param state: nombre del estado que será eliminado.
        :type state: str
        
        :rtype: None
        """
        del self.states[state.name]
    
    def get_states(self):
        """
        Retorna una lista con los nombres de todos los estados.
        
        :rtype: List[str,str,...,str]
        :return: [state for state in self.states.keys()]
        """
        return [state for state in self.states.keys()]
      
    def update_state(self):
        """
        Actualiza el estado actual del agente.
        
        :rtype: None
        """
        self.actual_state = []
        for state in self.states.keys():
            if self.states[state].func(self):
                self.actual_state.append(state)
        
    def set_default_states(self):
        """
        Define los estados por los que puede pasar el agente.
        
        :rtype: None
        """
        def state_starve(agent):
            if agent.food_eat_today == 0:
                return True
        self.set_state(State('starve', state_starve))
            
        def state_half(agent):
            if agent.food_eat_today == 1:
                return True
        self.set_state(State('half', state_half))
        
        def state_full(agent):
            if agent.food_eat_today > 1:
                return True
        self.set_state(State('full', state_full))
        
        def state_pregant(agent):
            if agent.pregnant == 1:
                return True
        self.set_state(State('pregnant', state_pregant))
        
        def state_low_energy(agent):
            if agent.current_energy < agent.max_energy / 2:
                return True
        self.set_state(State('low_energy', state_low_energy))
    
    def set_footprint(self, world):
        """
        Método para ubicar una pisada del agente en una casilla
        """
        tile = world.map[self.pos_x][self.pos_y]
        if not tile.is_edge:
            tile.footprints.append(Footprint())
        
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

class Behavior:
    """
    Clase que se encargará de agrupar las diferentes reglas
    de comportamiento de los agentes.
    """
    def __init__(self, agent):
        """
        Recibe el agente del cual constituirá su definición
        de comportamiento y crea un diccionario en el que
        quedarán las reglas.
        :param agent: agente asigando
        :type agent: Agent
        
        :rtype: Behavior
        """
        self.agent = agent
        self.rules = {}
        
    def set_rule(self, rule):
        """
        Guarda una nueva regla en el diccionario de reglas.
        
        :rtype: None
        """
        self.rules[rule.name] = rule
    
    def del_rule(self, rule):
        """
        Elimina regla del diccionario de reglas.
        
        :rtype: None
        """
        del self.rules[rule]
       
class Rule:
    """
    Define una regla por la que se regirá el agente.
    """
    def __init__(self,
                 name = 'unnamed',
                 to_see = None,
                 to_move = None,
                 to_relevance = lambda agent:0):
        
        """
        Se crea una nueva regla por la que se regirá el
        agente para comportarse.
        
        :param name: nombre de la regla.
        :type name: str
        :param to_see: es la función que define el comportamiento
        del agente a la hora de observar el mundo. Debe recibir un
        agente y un objeto, y retornar True || False
        :type to_see: function
        :param to_move: función que define cómo el agente valora una
        posición a la hora de moverse. Debe recibir una celda actual,
        una celda a la que nos moveremos, un mundo, un lista de las
        casillas ya vistas y una lista de elementos relevantes. Retorna
        un valor numérico.
        :type to_move: function
        :param to_relevance: esta función indica cuán relevante es una
        regla en dependencia del estado actual del agente. Debe retornar 
        un valor entre 0 y 1.
        :type to_relevance: function
        
        :rtype: Rule
        """
        self.name = name
        self.to_see = to_see
        self.to_move = to_move
        self.to_relevance = to_relevance
        self.elements = []
        
class State:
    """
    Define un estado por el que puede pasar el agente.
    """
    def __init__(self,
                 name = 'unnamed',
                 func = None):
        """
        Se crea un nuevo estado.
        :param name: nombre del estado
        :type name: str
        :param func: función que inidica si me encuentro en este estado.
        
        :rtype: State
        """
        self.name = name
        self.func = func