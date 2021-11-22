import world
import agent
from action import DoNothing


class Simulator:
    def __init__(self):
        self.world = None
        self.agents = []

    def create_world(self, dimension_x, dimension_y):
        self.world = world.World(dimension_x, dimension_y)

    def create_agent(self, sense, max_energy):
        r, c = self.world.get_pos_random_edge()
        ag = agent.Agent(r, c, sense, max_energy)
        self.agents.append(ag)
        self.world.add_agent(r, c, ag)

    def simulate_one_agent_action(self):
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
        for ag in self.agents:
            if not (
                self.world.cell_is_edge(ag.pos_x, ag.pos_y) and ag.food_eat_today >= 1
            ):
                self.world.remove_agent(ag)
                self.agents.remove(ag)

    def replicate_agents(self):
        for ag in self.agents:
            if ag.food_eat_today == 2:
                self.create_agent(3, 10)

    def reset_agents_attributes(self):
        for ag in self.agents:
            ag.food_eat_today = 0
            ag.current_energy = ag.max_energy

    def simulate_one_round(self):
        while not self.simulate_one_agent_action():
            print(self.world)
            pass

        self.eliminate_poorly_positioned_hungry_agents()

        self.replicate_agents()

        self.reset_agents_attributes()
