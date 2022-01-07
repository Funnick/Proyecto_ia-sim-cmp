import world
import agent
from action import DoNothing


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

    def create_agent(self, max_energy, sense):
        """
        Añade un nuevo agente a la simulación.

        :param agent: instancia de un agente
        :type agent: Agent

        :rtype: None
        """
        r, c = self.world.get_pos_random_edge()
        ag = agent.Agent(r, c, max_energy, sense)
        self.agents.append(ag)
        self.world.add_agent(r, c, ag)

    def simulate_one_agent_action(self):
        """
        Ejecuta una acción por cada agente.

        :rtype: None
        """
        actions = []
        for ag in self.agents:
            actions.append(ag.play(ag.see(self.world)))

        all_do_nothing_actions = True
        for i in range(len(actions)):
            if not (actions[i].__class__ is DoNothing):
                actions[i].execute(self.world, self.agents[i])
                all_do_nothing_actions = False

        return all_do_nothing_actions

    def eliminate_poorly_positioned_hungry_agents(self):
        """
        Elimina de la simulación a los agentes que no sobrevivieron al día.

        :rtype: None
        """
        for ag in self.agents:
            if not (
                self.world.cell_is_edge(ag.pos_x, ag.pos_y) and ag.food_eat_today >= 1
            ):
                self.world.remove_agent(ag)
                self.agents.remove(ag)

    def replicate_agents(self):
        """
        Reproduce los agentes que cumplieron la condición de reproducción.

        :rtype: None
        """
        for ag in self.agents:
            if ag.food_eat_today == 2:
                self.create_agent(3, 10)

    def reset_agents_attributes(self):
        for ag in self.agents:
            ag.food_eat_today = 0
            ag.current_energy = ag.max_energy

    def simulate_one_round(self):
        """
        Corre un día completo de la simulación.

        :rtype: None
        """
        self.day = self.day + 1

        while not self.simulate_one_agent_action():
            pass

        self.eliminate_poorly_positioned_hungry_agents()

        self.replicate_agents()

        self.reset_agents_attributes()

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
