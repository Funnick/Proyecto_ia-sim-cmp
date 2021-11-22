class Action:
    def execute(self, world, agent):
        agent.current_energy = agent.current_energy - 1
        pass


class DoNothing(Action):
    def execute(self, world, agent):
        pass


class MoveNorth(Action):
    def execute(self, world, agent):
        Action.execute(self, world, agent)
        world.move_agent(agent, agent.pos_x - 1, agent.pos_y)
        agent.pos_x = agent.pos_x - 1


class MoveSouth(Action):
    def execute(self, world, agent):
        Action.execute(self, world, agent)
        world.move_agent(agent, agent.pos_x + 1, agent.pos_y)
        agent.pos_x = agent.pos_x + 1


class MoveEast(Action):
    def execute(self, world, agent):
        Action.execute(self, world, agent)
        world.move_agent(agent, agent.pos_x, agent.pos_y + 1)
        agent.pos_y = agent.pos_y + 1


class MoveWest(Action):
    def execute(self, world, agent):
        Action.execute(self, world, agent)
        world.move_agent(agent, agent.pos_x, agent.pos_y - 1)
        agent.pos_y = agent.pos_y - 1


class Eat(Action):
    def execute(self, world, agent):
        Action.execute(self, world, agent)
        if world.agent_eat_food(agent.pos_x, agent.pos_y):
            agent.food_eat_today = agent.food_eat_today + 1

    def __str__(self):
        return "ActionEat"
