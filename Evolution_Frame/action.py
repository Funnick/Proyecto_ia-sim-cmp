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
        self.aux_execute(world, agent)

    def aux_execute(self, world, agent):
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

    def aux_execute(self, world, agent):
        world.move_agent(agent, agent.pos_x - 1, agent.pos_y)
        agent.pos_x = agent.pos_x - 1
        agent.set_footprint(world)


class MoveSouth(Action):
    """
    Mueve al agente en dirección sur
    """

    def aux_execute(self, world, agent):
        world.move_agent(agent, agent.pos_x + 1, agent.pos_y)
        agent.pos_x = agent.pos_x + 1
        agent.set_footprint(world)


class MoveEast(Action):
    """
    Mueve al agente en dirección este
    """

    def aux_execute(self, world, agent):
        world.move_agent(agent, agent.pos_x, agent.pos_y + 1)
        agent.pos_y = agent.pos_y + 1
        agent.set_footprint(world)


class MoveWest(Action):
    """
    Mueve al agente en dirección oeste
    """

    def aux_execute(self, world, agent):
        world.move_agent(agent, agent.pos_x, agent.pos_y - 1)
        agent.pos_y = agent.pos_y - 1
        agent.set_footprint(world)


class Eat(Action):
    """
    Acción de comer
    """

    def aux_execute(self, world, agent):
        agent_eat, _type, food = world.agent_eat_food(agent.pos_x, agent.pos_y, agent)
        if agent_eat:
            agent.food_eat_today = agent.food_eat_today + 1
            if _type:
                world.map[agent.pos_x][ agent.pos_y].object_list.remove(food)
                if not world.cell_have_food(agent.pos_x,  agent.pos_y):
                    world.map[agent.pos_x][ agent.pos_y].has_food = False
            else:
                food.is_alive = False
                

    def __str__(self):
        return "ActionEat"

class HaveSex(Action):
    """
    Mueve al agente en dirección oeste
    """
    def aux_execute(self, world, agent):
        agent_have_sex, other_agent = world.agents_have_sex(agent.pos_x, agent.pos_y, agent)
        if agent_have_sex:
            agent.pregnant = agent.sexual_reproduction(other_agent)