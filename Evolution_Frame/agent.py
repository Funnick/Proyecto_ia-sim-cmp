from object_base import Object_base
from action import MoveNorth, MoveSouth, MoveWest, MoveEast, Eat, HaveSex, DoNothing
from random import randint
from gene import Genetic_code
from behavior import Behavior

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

    def __init__(self, pos_x = -1, pos_y = -1, genes = [], behavior = None, rules = [], states = []):
        """
        Inicializa un agente en la posición (pos_x, pos_y) con una energía máxima (max_energy).

        :param pos_x: coordenada x del agente
        :type pos_x: int
        :param pos_y: coordenada y del agente
        :type pos_y: int
        :param genes: lista de genes que serán pasados al agente
        :param behavior: comportamiento que será pasado al agente 
        :param rules: conjunto de reglas que será pasado al agente
        :param states: estados del agente

        :rtype: Agent
        """
        Object_base.__init__(self, pos_x, pos_y)
        self.is_alive = True
        self.is_agent = True
        self.age = 0
        self.food_eat_today = 0
        self.pregnant = []
        self.set_genetic(genes)
        self.max_energy = self.genetic_code.get_gene('stamina').value
        self.current_energy = self.max_energy
        self.life_span = self.genetic_code.get_gene('life').value
        
        self.energy_lost_fun = lambda sense, speed, size: (
            self.genetic_code.get_gene('sense').value +
            self.genetic_code.get_gene('speed').value*2 + 
            self.genetic_code.get_gene('size').value*3)

        self.actual_state = []
        if not behavior:
            self.behavior = Behavior(rules=rules, states=[])
        else: 
            self.behavior = behavior
        
    def __str__(self):
        return "Agent"

    # Genética -------------------------------------------------------------
    def set_genetic(self, genes = []):
        """
        Agrega un código genético al agente con los valores predeterminados,
        o genes diseñados por el usuario.
        
        :rtype: None
        """
        genetic = Genetic_code(genes = genes)
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
        
        :rtype: list
        :return: childs
        """
        childs = []
        for child in range(self.genetic_code.get_gene('fertility').value):    
            if randint(0, 1):
                behavior = other_agent.behavior
            else:
                behavior = self.behavior
            child_agent = Agent(behavior=behavior)
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
        child_agent = Agent(-1, -1, behavior=self.behavior)
        child_agent.genetic_code = self.mutate
        return child_agent
    
    @property
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
        # Actualiza el estado actual del agente
        self.update_state()
        
        world = perception[0]
        limits = perception[1]
        plan = []
        path = []
        steps = 0
        queue = [(self.pos_x, self.pos_y)]
        max_steps = self.genetic_code.get_gene('speed').value
        while (steps < max_steps):
            cell = queue.pop(0)
            path.append(cell)
            best_move = [10000,-1,None]
            # Por cada posible movimiento que puedo hacer desde la casilla casilla actual
            for move in range(4):
                new_cell = (cell[0] + directions[move][0], cell[1] + directions[move][1])
                
                # Si el movimiento está en los límites de la visión
                if (self.in_limits((new_cell[0], new_cell[1]), limits)):
                    # Si la celda es un borde y no he comido, ve hacia la siguiente
                    if (world.cell_is_edge(new_cell[0], new_cell[1]) and 
                        self.food_eat_today == 0):
                        continue
                    
                    best_move_probability = 0
                    # Por cada regla en el comportamiento del agente
                    for rule in self.behavior.rules.values():
                        # Si existen funciones para el movimiento y para la relevancia
                        # calcula la probabilidad de que sea el mejor movimiento
                        if rule.to_move and rule.to_relevance:
                            best_move_probability += (rule.to_relevance(self) * 
                                                      rule.to_move(cell, 
                                                                   new_cell, 
                                                                   world, 
                                                                   path, 
                                                                   rule.elements))
                    # Si este movimiento es el mejor hasta ahora, actualiza el mejor movimiento
                    if best_move_probability < best_move[0]:
                        best_move[0] = best_move_probability
                        best_move[1] = move
                        best_move[2] = new_cell
            # Agrega el nuevo movimiento a la lista de movimientos
            queue.append(best_move[2])
            # Agrega al plan la acción de moverse en la dirección indicada
            plan.append(directions_actions[best_move[1]])
            # Si ya el agente comió, y está parado sobre un borde, que se quede ahí y no haga nada
            if self.food_eat_today > 0 and world.map[best_move[2][0]][best_move[2][1]].is_edge:
                plan.append(DoNothing())
                break
            # Si el agente no está embarazado, y en el nuevo movimiento vi una posible pareja
            # agrega la acción de tener sexo
            if not self.pregnant and best_move[2] in self.behavior.rules['couples'].elements:
                plan.append(HaveSex())
                self.behavior.rules['couples'].elements.remove(best_move[2])
            # Si el nuevo movimiento me lleva a un lugar donde vi comida, agrega al plan la
            # acción de comer
            if (best_move[2] in self.behavior.rules['food'].elements):
                plan.append(Eat())
                self.behavior.rules['food'].elements.remove(best_move[2])
                
            # Aumenta en uno los pasos dados hasta ahora
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
        (right_corner_x y right_corner_y). Además, revisa cada uno de las
        reglas del agente y verifica qué elementos le son relevantes.

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
    
    def get_states(self):
        """
        Retorna una lista con los nombres de todos los estados.
        
        :rtype: List[str,str,...,str]
        :return: [state for state in self.behavior.states.keys()]
        """
        return [state for state in self.behavior.states.keys()]
      
    def update_state(self):
        """
        Actualiza el estado actual del agente.
        
        :rtype: None
        """
        self.actual_state = []
        for state in self.behavior.states.keys():
            if self.behavior.states[state].func(self):
                self.actual_state.append(state)
    
    def set_footprint(self, world):
        """
        Método para ubicar una pisada del agente en una casilla
        :param world: mundo en el cual será ubicada la pisada
        :type world: World
        
        :rtype: None
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
