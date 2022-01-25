import world
import agent
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
        self.agents = []
        self.day = 0
        self.cycle = 0

    def create_world(self, dimension_x, dimension_y):
        """
        Inicializa el mundo de la simulación con tamaño dimension_x * dimension_y.

        :param dimension_x: largo del mundo
        :type dimension_x: int
        :param dimension_y: ancho del mundo
        :type dimension_y: int

        :rtype: None
        """
        self.world = world.World(dimension_x, dimension_y)

    def add_agent_to_simulation(self, agent):
        """
        Añade un nuevo agente a la simulación.

        :param agent: instancia de un agente
        :type agent: Agent

        :rtype: None
        """
        r, c = self.world.get_pos_random_edge()
        agent.pos_x = r
        agent.pos_y = c
        self.agents.append(agent)
        self.world.add_agent(r, c, agent)

    def simulate_one_agent_action(self):
        """
        Ejecuta una acción por cada agente.

        :rtype: None
        """

        all_do_nothing_actions = True
        shuffle(self.agents)
        for ag in self.agents:
            for act in ag.play(ag.see(self.world)):
                if not (act.__class__ is DoNothing):
                    act.execute(self.world, ag)
                    all_do_nothing_actions = False

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

    def replicate_agents(self):
        """
        Reproduce los agentes que cumplieron la condición de reproducción.

        :rtype: None
        """
        for ag in self.agents:
            if ag.food_eat_today == 2:
                self.add_agent_to_simulation(ag.replicate())

    def reset_agents_attributes(self):
        for ag in self.agents:
            ag.food_eat_today = 0
            ag.current_energy = ag.max_energy

    def remove_food(self):
        self.world.remove_food()

    def simulate_one_round(self):
        """
        Corre un día completo de la simulación.

        :rtype: None
        """
        self.cycle = self.cycle + 1

        while not self.simulate_one_agent_action():
            pass

        if self.is_day():
            self.eliminate_poorly_positioned_hungry_agents()

            self.replicate_agents()

            self.reset_agents_attributes()

            self.remove_food()
            
        else:
            self.day = self.day + 1

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
        print("Día ->", self.get_simulation_day()," "+self.get_day_night)
        print("Número de agentes ->", self.get_number_of_agents())
        
    def print_world(self,world):
        m = ""
        for i in range(world.dimension_x):
            for j in range(world.dimension_y):
                m += self.world_dict[str(world.map[i][j][-1])]
            m += "\n"
        print(m) 
        
    def print_altitude(self,world):
        m = ""
        for i in range(world.dimension_x):
            for j in range(world.dimension_y):
                val = world.map[i][j][0].height
                m += str(val) + "  " if val >= 0 else str(val) + " "
            m += "\n"
        print(m) 

    world_dict ={
        "Food":"f",
        "Edge":".",
        "Agent":"a",
        "Nothing":" "
        }