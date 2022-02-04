from world import World
from action import DoNothing
from random import shuffle
from matplotlib import pyplot as plt


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
        self.restrictions = True
        self.food_function = None

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
        
        # Función predeterminada de adición de alimentos (10% del mapa)
        self.food_function = (dimension_x * dimension_y * 10) / 100

    def set_food_function(self, func):
        """
        Agrega una nueva función de distribución de comida.
        :param func: función de distribución.
        :type func: function
        
        :rtype: None
        """
        self.food_function = func
    
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
        else: 
            r,c = pos[0],pos[1]
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
                    for child in ag.pregnant:
                        self.add_agent_to_simulation(child,(ag.pos_x,ag.pos_y))

    def reset_agents_attributes(self):
        """
        Reinicia los atributos de todos los agentes de la simulación
        """
        for ag in self.agents:
            ag.get_older()
            ag.food_eat_today = 0
            ag.current_energy = ag.max_energy
            ag.pregnant = []

    def clean_map(self):
        """
        Limpia o actualiza la simulación de todos los 
        objetos presentes que deben ser retirados.
        
        :rtype: None
        """
        self.world.remove_food()
        self.world.remove_tree()
        self.world.remove_footprints()
    
    def simulate(self, rounds = 1, food_function = None, maping = [], plot = 0):
        """
        Corre una cantidad n de días de la simulación.
        
        :param rounds: cantidad de rondas o días que se desean correr.
        :type rounds: int
        :param food_function: función de distibución de la alimentación.

        :rtype: None
        """
        agents = []
        if food_function:
            self.set_food_function(food_function)
            
        for r in range(rounds):
            if not self.restrictions:
                break
            self.world.add_food(self.food_function(self))
            self.simulate_one_round()
            agents.append(self.get_number_of_agents())
            for func in maping:
                func.elements.append(len(self.get_agents_that(func.func)))
                
        if plot:
            for func in maping:
                plt.plot([i for i in range(len(func.elements))], func.elements, '-', alpha=1.00, label=func.name)
                plt.fill_between([i for i in range(len(func.elements))], func.elements, alpha=.25)
            leg = plt.legend(loc=9,ncol=2, mode="expand", shadow=True, fancybox=True)
            leg.get_frame().set_alpha(0.5)
            plt.grid()
            plt.xlabel('days')
            plt.ylabel('agents')
            plt.show()
        self.end_simulation()
        return agents
                   
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
    
    def end_simulation(self):
        """
        Mensaje de que la simulación llegó a su fin.
        Además imprime en consola las estadísticas.
        
        :rtype: None
        """
        print('La simulación ha terminado.')
        self.get_statistics()
    
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
    
class MapFunction:
    """
    Clase para crear funciones de mapeo, que filtren los
    agentes según el comportamiento de una variable.
    """
    def __init__(self, name='unnamed', func = None):
        """
        Se crea una nueva función de mapeo.
        
        :param name: nombre que recibirá la función de mapeo
        :type name: str
        :param func: función de mapeo, que recibe un agente y retorna
        True || False
        :type func: function
        
        :rtype: MapFunction
        """
        self.name = name
        self.func = func
        self.elements = []
        
class SimulatorMaster:
    """
    Clase que permitirá correr varias simulaciones con las
    mismas características para evaluar el comportamiento
    promedio de una configuración.
    """
    def __init__(self, 
                 dimensions = (50,50), 
                 rounds = 30, 
                 days = 100,
                 food_distribution = None, 
                 agents_distribution = None):
        """
        Se crea una nueva instancia de una simulación maestra.
        
        :param dimensions: tupla que contiene las dimensiones del mapa
        :type dimensions: Tuple[int, int]
        :param rounds: cantidad de simulaciones que vas a ser ejecutadas
        :type rounds: int
        :param days: cantidad de días que van a transcurrir en cada simulación
        :type days: int
        :param food_distribution: función que describe cómo se va a distribuir
        la comida en el mapa
        :type food_distribution: function
        :param agents_distribution: función que retorna un conjunto de agentes
        :type agents_distribution: function
        
        :rtype: SimulatorMaster
        """
        self.dimensions = dimensions
        self.rounds = rounds
        self.days = days
        self.food_distribution = food_distribution
        self.agents_distribution = agents_distribution
        self.rounds = rounds
        
    def run(self, plot = 0):
        """
        Corre n simulaciones con las mismas características.
        :param plot: define si se desea graficar los resultados obtenidos
        :type plot: int
        
        :rtype: list
        :return: total_agents_by_simulation
        """
        total_agents_by_simulation = []
        for r in range(self.rounds):
            print("Comenzando la simulación:", r+1)
            s = Simulator()
            s.create_world(self.dimensions[0], self.dimensions[1])
            for a in self.agents_distribution():
                s.add_agent_to_simulation(a)
            agents=(s.simulate(self.days, 
                                     self.food_distribution, 
                                     maping=[], 
                                     plot=0))
            plt.plot([i for i in range(len(agents))], agents, 'b-', alpha=0.25)
            total_agents_by_simulation.append(agents)
        
        mean_agents = []
        for d in range(self.days):
            total = 0
            for s in total_agents_by_simulation:
                total += s[d]
            total /= len(total_agents_by_simulation) if len(total_agents_by_simulation)!=0 else 0
            mean_agents.append(total)
        plt.plot([i for i in range(len(mean_agents))], mean_agents, 'r-', alpha=1)
        plt.grid()
        plt.xlabel('days')
        plt.ylabel('agents')
        plt.show()
        return total_agents_by_simulation
        