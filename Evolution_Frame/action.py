class Action:
    """
    Clase base de todas la acciones.
    """

    def execute(self, world, agent):
        """
        Ejecuta una acción cambiando el estado del mundo y agente

        :param world: instancia del mundo
        :type world: World
        :param agent: instancia del agente
        :type agent: Agent

        :rtype: None
        """
        agent.current_energy = agent.current_energy - 1
        pass


class DoNothing(Action):
    """
    Acción de no hacer nada
    """

    def execute(self, world, agent):
        pass


class MoveNorth(Action):
    """
    Mueve al agente en dirección norte
    """

    def execute(self, world, agent):
        Action.execute(self, world, agent)
        world.move_agent(agent, agent.pos_x - 1, agent.pos_y)
        agent.pos_x = agent.pos_x - 1


class MoveSouth(Action):
    """
    Mueve al agente en dirección sur
    """

    def execute(self, world, agent):
        Action.execute(self, world, agent)
        world.move_agent(agent, agent.pos_x + 1, agent.pos_y)
        agent.pos_x = agent.pos_x + 1


class MoveEast(Action):
    """
    Mueve al agente en dirección este
    """

    def execute(self, world, agent):
        Action.execute(self, world, agent)
        world.move_agent(agent, agent.pos_x, agent.pos_y + 1)
        agent.pos_y = agent.pos_y + 1


class MoveWest(Action):
    """
    Mueve al agente en dirección oeste
    """

    def execute(self, world, agent):
        Action.execute(self, world, agent)
        world.move_agent(agent, agent.pos_x, agent.pos_y - 1)
        agent.pos_y = agent.pos_y - 1


class Eat(Action):
    """
    Acción de comer
    """

    def execute(self, world, agent):
        Action.execute(self, world, agent)
        if world.agent_eat_food(agent.pos_x, agent.pos_y):
            agent.food_eat_today = agent.food_eat_today + 1

    def __str__(self):
        return "ActionEat"
