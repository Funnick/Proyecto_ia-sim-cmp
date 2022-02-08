from .object_base import Food, Tree
from .aux_meth import manhattan, mean

class Behavior:
    """
    Clase que se encargará de agrupar las diferentes reglas
    y estaods de comportamiento de los agentes.
    """
    def __init__(self, rules = [], states = []):
        """
        Recibe un conjunto de reglas y estados que definirán un
        comportamiento y crean diccionarios en los que quedarán estos.
        :param rules: reglas por las que se regirá el agente
        :type rules: list
        :param states: conjunto de estados por los que pasarán los agentes
        :type rules: list
        
        :rtype: Behavior
        """
        self.build_states(states=states)
        self.build_rules(rules=rules)
    
    def build_rules(self, rules = []):
        """
        Pone las reglas predeterminadas, y sustituye o agrega
        las reglas que sean pasadas por el agente.
        :param rules: conjunto de reglas a agregar
        :type rules: list
        
        :rtype: None
        """
        self.rules = {
            str('food'): EatRule(),
            str('tree'): TreeRule(),
            str('enemies'): EnemiesRule(),
            str('couples'): CouplesRule(),
            str('edges'): EdgeRule(),
            str('elevation'): ElevationRule(),
            str('footprint'): FootprintRule(),
            str('visited'): VisitedRule()
        }
        for rule in rules:
            self.rules[rule.name] = rule
    
    def set_rule(self, rule):
        """
        Guarda una nueva regla en el diccionario de reglas.
        :param rule: regla a agregar
        :type rule: Rule
        
        :rtype: None
        """
        self.rules[rule.name] = rule
    
    def del_rule(self, rule):
        """
        Elimina una regla del diccionario de reglas.
        :param rule: regla a eliminar
        :type rule: Rule
        
        :rtype: None
        """
        del self.rules[rule]
        
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
       
    def build_states(self, states = []):
        """
        Método que define los estados con los que contará
        este comportamiento.
        :param states: lista de funciones de estado pasadas por el usuario
        :type states: list
        
        :rtype: None
        """
        def state_starve(agent):
            if agent.food_eat_today == 0:
                return True
            
        def state_half(agent):
            if agent.food_eat_today == 1:
                return True
        
        def state_full(agent):
            if agent.food_eat_today > 1:
                return True
        
        def state_pregnant(agent):
            if agent.pregnant == 1:
                return True
        
        def state_low_energy(agent):
            if agent.current_energy < agent.max_energy / 2:
                return True
            
        self.states = {
            'starve':State('starve', state_starve),
            'half':State('half', state_half),
            'full':State('full', state_full),
            'pregnant':State('pregnant', state_pregnant),
            'low_energy':State('low_energy', state_low_energy)
        }
        for state in states:
            self.states[state.name] = state
             
class Rule:
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
    def __init__(self,
                 name = 'unnamed',
                 to_see = None,
                 to_move = None,
                 to_relevance = lambda agent:0):
        self.name = name
        self.to_see = to_see
        self.to_move = to_move
        self.to_relevance = to_relevance
        self.elements = []

class EatRule(Rule):
    """
    Regla para la alimentación.
    """
    def __init__(self, to_see = None, to_move = None, to_relevance = None):
        def see_food(agent, element):
            self_diet = agent.genetic_code.get_gene('diet').value
            self_size = agent.genetic_code.get_gene('size').value
            if (isinstance(element, Food) and
                (self_diet == 1 or self_diet == 3)):
                return True
            elif (not(element is agent) and isinstance(element, agent.__class__) and 
                  (self_size - 2 >= element.genetic_code.get_gene('size').value and self_diet > 1)):
                return True
            
        def move_food(cell = None, new_cell = None, world = None, path = None, elements = None):
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
            
        if not to_see:
            to_see = see_food
        if not to_move:
            to_move = move_food
        if not to_relevance:
            to_relevance = relevance_food
        Rule.__init__(self,
                      name = 'food',
                      to_see = to_see,
                      to_move = to_move,
                      to_relevance = to_relevance)
        
class TreeRule(Rule):
    """
    Regla para los árboles.
    """
    def __init__(self, to_see = None, to_move = None, to_relevance = None):
        def see_tree(agent, element):
            self_diet = agent.genetic_code.get_gene('diet').value
            if (isinstance(element, Tree) and 
                (self_diet == 1 or self_diet == 3)):
                return True
            
        def move_tree(cell = None, new_cell = None, world = None, path = None, elements = None):
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
            
        if not to_see:
            to_see = see_tree
        if not to_move:
            to_move = move_tree
        if not to_relevance:
            to_relevance = relevance_tree
        Rule.__init__(self,
                      name = 'tree',
                      to_see = to_see,
                      to_move = to_move,
                      to_relevance = to_relevance)
        
class EnemiesRule(Rule):
    """
    Regla para los enemigos.
    """
    def __init__(self, to_see = None, to_move = None, to_relevance = None):
        def see_enemies(agent, element):
            self_size = agent.genetic_code.get_gene('size').value
            if (not(element is agent) and isinstance(element, agent.__class__) and 
                (element.genetic_code.get_gene('size').value - 2 >= 
                 self_size and element.genetic_code.get_gene('diet').value > 1)):
                return True
            
        def move_enemies(cell = None, new_cell = None, world = None, path = None, elements = None):
            return mean([manhattan([new_cell[0], new_cell[1]], [i[0], i[1]])
                  for i in elements])
        
        def relevance_enemies(agent):
            return -1
        
        if not to_see:
            to_see = see_enemies
        if not to_move:
            to_move = move_enemies
        if not to_relevance:
            to_relevance = relevance_enemies
        Rule.__init__(self,
                      name = 'enemies',
                      to_see = to_see,
                      to_move = to_move,
                      to_relevance = to_relevance)
        
class CouplesRule(Rule):
    """
    Regla para las parejas.
    """
    def __init__(self, to_see = None, to_move = None, to_relevance = None):
        def see_couples(agent, element):
            self_sex = agent.genetic_code.get_gene('sex').value
            self_repr = agent.genetic_code.get_gene('reproduction').value
            if (not(element is agent) 
                and isinstance(element, agent.__class__) 
                and (self_repr == 2 and element.genetic_code.get_gene('reproduction').value == 2 
                     and element.genetic_code.get_gene('sex').value != self_sex)): 
                return True
            
        def move_couples(cell = None, new_cell=None, world = None, path = None, elements = None):
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
            
        if not to_see:
            to_see = see_couples
        if not to_move:
            to_move = move_couples
        if not to_relevance:
            to_relevance = relevance_couples
        Rule.__init__(self,
                      name = 'couples',
                      to_see = to_see,
                      to_move = to_move,
                      to_relevance = to_relevance)
        
class ElevationRule(Rule):
    """
    Regla para las diferencias de elevación.
    """
    def __init__(self):
        def move_elevation(cell ,new_cell, world = None, path = None, elements = None):
            return abs(world.map[new_cell[0]][new_cell[1]].height - 
                       world.map[cell[0]][cell[1]].height)
            
        def relevance_elevation(agent):
            return 0.1
        Rule.__init__(self,
                      name = 'elevation',
                      to_see = None,
                      to_move = move_elevation,
                      to_relevance = relevance_elevation)
        
class EdgeRule(Rule):
    """
    Regla para los bordes.
    """
    def __init__(self, to_see = None, to_move = None, to_relevance = None):
        def move_elevation(cell = None, new_cell = None, world = None, path = None, elements = None):
            return abs(world.map[new_cell[0]][new_cell[1]].height - 
                       world.map[cell[0]][cell[1]].height)
            
        def relevance_elevation(agent):
            return 0.1
        
        if not to_move:
            to_move = move_elevation
        if not to_relevance:
            to_relevance = relevance_elevation
        Rule.__init__(self,
                      name = 'elevation',
                      to_see = to_see,
                      to_move = to_move,
                      to_relevance = to_relevance)
        
class FootprintRule(Rule):
    """
    Regla para las marcas de las pisadas.
    """
    def __init__(self, to_see = None, to_move = None, to_relevance = None):
        def move_footprint(cell = None, new_cell = None, world = None, path = None, elements = None):
            return len(world.map[new_cell[0]][new_cell[1]].footprints)
            
        def relevance_footprint(agent):
            return 0.1
        
        if not to_move:
            to_move = move_footprint
        if not to_relevance:
            to_relevance = relevance_footprint
        Rule.__init__(self,
                      name = 'footprint',
                      to_see = to_see,
                      to_move = to_move,
                      to_relevance = to_relevance)
        
class VisitedRule(Rule):
    """
    Regla para las casillas ya visitadas.
    """
    def __init__(self, to_see = None, to_move = None, to_relevance = None):
        def move_edges(cell = None, new_cell = None, world = None, path = None, elements = None):
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
        
        if not to_move:
            to_move = move_edges
        if not to_relevance:
            to_relevance = relevance_edges
        Rule.__init__(self,
                      name = 'edges',
                      to_see = to_see,
                      to_move = to_move,
                      to_relevance = to_relevance)
     
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
