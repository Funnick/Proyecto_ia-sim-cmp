from world import World
from action import DoNothing
from random import shuffle


class Simulator:
    """
    Clase principal para representar la simulación. Contiene el mundo y los agentes.
    """

    def __init__(self):
        """
        Crea una entidad de simulación sin mundo ni agentes
        y con 0 días de simulaciones pasadas.

        :rtype: Simulator
        """
        self.world = None
        self.restrictions = None
        self.agents = []
        self.active_agents = []
        self.day = 0
        self.cycle = 0

    def create_world(self, dimension_x, dimension_y, trees = 0):
        """
        Inicializa el mundo de la simulación con tamaño dimension_x * dimension_y.

        :param dimension_x: largo del mundo
        :type dimension_x: int
        :param dimension_y: ancho del mundo
        :type dimension_y: int

        :rtype: None
        """
        self.world = World(dimension_x, dimension_y, trees)

    def add_restrictions(self, func):
        """
        Agrega restricciones a la simulación.
        
        :param func: función que revisa las restricciones
        :type func: function
        
        :rtype: None
        """
        self.restrictions = func

    def add_agent_to_simulation(self, agent, pos = (-1,-1)):
        """
        Añade un nuevo agente a la simulación.

        :param agent: instancia de un agente
        :type agent: Agent

        :rtype: None
        """
        if pos == (-1,-1):
            r, c = self.world.get_pos_random_edge()
        else: r,c = pos[0],pos[1]
        agent.pos_x = r
        agent.pos_y = c
        self.agents.append(agent)
        self.world.add_agent(r, c, agent)

    def add_agents_to_simulation(self, agents):
        """
        Añade a partir de una lista un grupo de agentes a la
        simulación.
        
        :param agents: lista de agentes
        :type agents: list
        
        :rtype: None
        """
        for agent in agents:
            self.add_agent_to_simulation(agent)
    
    def simulate_one_agent_action(self):
        """
        Ejecuta una acción por cada agente.

        :rtype: None
        """

        all_do_nothing_actions = True
        shuffle(self.active_agents)
        for ag in self.active_agents:
            if ag.is_alive:
                for act in ag.move(ag.see_around(self.world)):
                    if not (act.__class__ is DoNothing):
                        act.execute(self.world, ag)
                        all_do_nothing_actions = False
                    else:
                        self.active_agents.remove(ag)
            else:
                self.active_agents.remove(ag)

        return all_do_nothing_actions

    def eliminate_poorly_positioned_hungry_agents(self):
        """
        Elimina de la simulación a los agentes que no sobrevivieron al día.

        :rtype: None
        """
        for i in range(len(self.agents) - 1, -1, -1):
            if not (
                self.world.cell_is_edge(self.agents[i].pos_x, self.agents[i].pos_y)
                and self.agents[i].food_eat_today >= 1
                and self.agents[i].is_alive
            ):
                self.world.remove_agent(self.agents[i])
                self.agents.pop(i)

    def reproduction_agents(self):
        """
        Reproduce los agentes que cumplieron la condición de reproducción.

        :rtype: None
        """
        for ag in self.agents:
            if ag.food_eat_today >= 2:
                reproduction = ag.genetic_code.get_gene('reproduction').value
                if reproduction == 1:
                    self.add_agent_to_simulation(ag.asexual_reproduction(),(ag.pos_x,ag.pos_y))
                elif reproduction == 2 and ag.pregnant:
                    self.add_agent_to_simulation(ag.pregnant,(ag.pos_x,ag.pos_y))

    def reset_agents_attributes(self):
        """
        Reinicia los atributos de todos los agentes de la simulación
        """
        for ag in self.agents:
            ag.get_older()
            ag.food_eat_today = 0
            ag.current_energy = ag.max_energy
            ag.pregnant = None

    def clean_map(self):
        """
        Limpia o actualiza la simulación de todos los 
        objetos presentes que deben ser retirados.
        
        :rtype: None
        """
        self.world.remove_food()
        self.world.remove_tree()
        self.world.remove_footprints()
        
    def simulate_one_round(self):
        """
        Corre un día completo de la simulación.

        :rtype: None
        """
        self.day = self.day + 1
        self.active_agents = [a for a in self.agents if a.is_alive]
        while not self.simulate_one_agent_action():
            pass
        
        self.eliminate_poorly_positioned_hungry_agents()
        self.clean_map()
        self.reproduction_agents()
        self.reset_agents_attributes()
        
    def get_agents_that(self, func):
        """
        Retorna los agentes que cumplen con cierto predicado.
        :param func: Función que devuelve True or False
        :type func: Func
        
        :rtype: list
        :return: agents_list
        """
        agents_list = []
        for ag in self.agents:
            if ag.is_alive and func(ag):
                agents_list.append(ag)
        return agents_list

    def get_simulation_day(self):
        """
        Devuelve el día actual de la simulación.

        :rtype: int
        :return: self.day
        """
        return self.day
    
    def is_day(self):
        return self.cycle%2==0
    
    def get_day_night(self):
        return "dia" if self.is_day() else "noche"

    def get_number_of_agents(self):
        """
        Devuelve la cantidad de agentes que hay en la simulación.

        :rtype: int
        :return: len(self.agents)
        """
        return len(self.agents)
    
    def get_statistics(self):
        print("Día ->", self.get_simulation_day())
        print("Número de agentes ->", self.get_number_of_agents())
    
    def get_species(self):
        pass   
    #TODO: cambiar el diccionario agregando que revise la lista.
    def print_world(self,world):
        m = ""
        for i in range(world.dimension_x):
            for j in range(world.dimension_y):
                if len(self.world.map[i][j].object_list) > 0:
                    m+= self.world_dict[str(world.map[i][j].object_list[-1])]
                elif self.world.map[i][j].is_edge:
                    m+= self.world_dict['Edge']
                else :
                    m+= self.world_dict['Nothing']
                # m += self.world_dict[str(world.map[i][j])]
            m += "\n"
        print(m) 
        
    def print_footprints(self,world):
        m = ""
        for i in range(world.dimension_x):
            for j in range(world.dimension_y):
                val = len(world.map[i][j].footprints)
                m += str(val) + "  " if val >= 0 else str(val) + " "
            m += "\n"
        print(m) 
        
    def print_altitude(self,world):
        m = ""
        for i in range(world.dimension_x):
            for j in range(world.dimension_y):
                val = world.map[i][j].height
                m += str(val) + "  " if val >= 0 else str(val) + " "
            m += "\n"
        print(m) 

    world_dict ={
        "Food":"o",
        "Edge":"#",
        "Agent":"A",
        "Nothing":" ",
        "Tree": "T"
        }