import object_base
import gene
import action
from random import randint
from math import sqrt

directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
directions_actions = [
    action.MoveNorth(),
    action.MoveSouth(),
    action.MoveWest(),
    action.MoveEast(),  
]
class Agent(object_base.ObjectBase):
    """
    Clase que reprenseta a los agentes de la simulación.
    """

    def __init__(self, pos_x, pos_y, max_energy = 100):
        """
        Inicializa un agente en la posición (pos_x, pos_y) con una energía máxima (max_energy).

        :param pos_x: coordenada x del agente
        :type pos_x: int
        :param pos_y: coordenada y del agente
        :type pos_y: int
        :param max_energy: energía máxima del agente
        :type max_energy: int

        :rtype: Agent
        """
        object_base.ObjectBase.__init__(self, pos_x, pos_y)
        self.is_alive = True
        self.perception_pos_x = -1
        self.perception_pos_y = -1
        self.food_eat_today = 0
        self.max_energy = max_energy
        self.current_energy = max_energy
        self.sex = 0
        self.age = 0
        self.memory = [[],[],[]]
        self.genetic_code = gene.GeneticCode()
        self.energy_lost_fun = lambda sense, speed, size: (
            self.genetic_code.get_gene('sense').value + 
            self.genetic_code.get_gene('speed').value + 
            self.genetic_code.get_gene('size').value)

    def __str__(self):
        return "Agent"

    def set_random_genetic(self):
        for gene in range(randint(3)):
            self.genetic_code
        
    def sexual_reproduction(self, other_agent):
        son_max_energy = (self.max_energy + other_agent.max_energy)/2
        son_agent = Agent(-1, -1, son_max_energy)
        son_agent.genetic_code = self.genetic_code + other_agent.genetic_code
        return son_agent
    
    def memory(self, pos, type):
        if type == 'Tree':
            self.memory[0].append(pos)
        elif type == 'Agent':
            self.memory[1].append(pos)
        elif type == 'Food':
            self.memory[2].append(pos)
    
    def get_older(self):
        """
        Envejece al agente en un punto.\n
        Retorna la edad del agente.
        
        :rtype: int
        
        """
        self.age += 1
        return self.age
    
    def add_gene(self, gene):
        """
        Agrega un gen al agente.
        :param gene: gen que se va a agregar

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
    
    def mutate(self):
        """
        Hace mutar todos los genes que posee el agente.

        :rtype: GeneticCode
        :return: child_genetic_code
        """
        child_genetic_code = self.genetic_code.mutate()
        return child_genetic_code
    
    def reduce_energy_to_perform_an_action(self):
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
        )
        if self.current_energy >= elf:
            self.current_energy = self.current_energy - elf
            return True
        return False

    def asexual_reproduction(self):
        """
        Devuelve un nuevo agente que puede tener características mutadas,
        es el resultado de una reproducción asexual.

        :rtype: Agent
        :return: agent
        """
        agent = Agent(-1, -1, self.max_energy)
        agent.genetic_code = self.mutate()
        return agent

    def get_random_move(self, perception):
        """
        Devuelve una acción que mueve al agente en una dirección.

        :param perception: parte del mundo que es percibida por el agente
        :type perception: World

        :rtype: Action
        :return: [moves[randint(0, len(moves) - 1)]]
        """
        global directions
        global directions_actions
        
        moves = []

        for i in range(4):
            if perception.valid_cell_to_move(
                self.perception_pos_x + directions[i][0],
                self.perception_pos_y + directions[i][1],
            ):
                moves.append(directions_actions[i])

        return [moves[randint(0, len(moves) - 1)]]

    def make_plan(self, cell, pi, plan, dimension_y):
        """
        Devuelve una lista de acciones que consituye el plan del agente.

        :param cell: última casilla vista en el BFS
        :type cell: (int, int)
        :param pi: arreglo pi del BFS
        :type pi: (int, int) list
        :param plan: lista de acciones que se debe tomar en la casilla i-ésima
        :type plan: Action list
        :param dimension_y: ancho del mundo para poder cambiar las dimensiones de pi y plan.
        :type dimension_y: int

        :rtype: Action list
        :return: new_plan
        """
        new_plan = [plan[cell[0] * dimension_y + cell[1]]]
        cell = pi[cell[0] * dimension_y + cell[1]]

        while cell != -1:
            new_plan.append(plan[cell[0] * dimension_y + cell[1]])
            cell = pi[cell[0] * dimension_y + cell[1]]

        return new_plan


    def go_to_edge(self, perception):
        """
        Devuelve una lista de acciones que se deben realizar para conseguir llegar al borde.
        En caso de no haber una acción clara en la percepción se devuelve una
        acción de moverse aleatoria.

        :param perception: parte del mundo que es percibida por el agente
        :type perception: World

        :rtype: Action list
        """
        
        matrix = [
            [False for i in range(perception.dimension_y)]
            for j in range(perception.dimension_x)
        ]
        matrix[self.perception_pos_x][self.perception_pos_y] = True

        pi = []
        plan = []
        for i in range(perception.dimension_x * perception.dimension_y):
            pi.append(-1)
            plan.append(action.DoNothing())

        queue = [(self.perception_pos_x, self.perception_pos_y)]
        while len(queue) > 0:
            cell = queue.pop(0)
            if perception.cell_is_edge(cell[0], cell[1]):
                return self.make_plan(cell, pi, plan, perception.dimension_y)

            for i in range(4):
                new_cell = (cell[0] + directions[i][0], cell[1] + directions[i][1])

                if (
                    perception.valid_cell_to_move(new_cell[0], new_cell[1])
                    and not matrix[new_cell[0]][new_cell[1]]
                ):
                    queue.append(new_cell)
                    matrix[new_cell[0]][new_cell[1]] = True
                    pi[new_cell[0] * perception.dimension_y + new_cell[1]] = cell
                    plan[
                        new_cell[0] * perception.dimension_y + new_cell[1]
                    ] = directions_actions[i]

        return self.get_random_move(perception)
    
    def look_for_food(self, perception):
        """
        Devuelve una lista de acciones que se deben realizar para conseguir comida.
        En caso de no haber una acción clara en la percepción se devuelve una
        acción de moverse aleatoria.

        :param perception: parte del mundo que es percibida por el agente
        :type perception: World

        :rtype: Action list
        """
        global directions
        global directions_actions
        
        matrix = [
            [False for i in range(perception.dimension_y)]
            for j in range(perception.dimension_x)
        ]
        matrix[self.perception_pos_x][self.perception_pos_y] = True
        
        pi = []
        plan = []
        for i in range(perception.dimension_x * perception.dimension_y):
            pi.append(-1)
            plan.append(action.Eat())

        queue = [(self.perception_pos_x, self.perception_pos_y)]
        while len(queue) > 0:
            cell = queue.pop(0)
            if perception.cell_have_food(cell[0], cell[1], self):
                return self.make_plan(cell, pi, plan, perception.dimension_y)

            for i in range(4):
                new_cell = (cell[0] + directions[i][0], cell[1] + directions[i][1])

                if (
                    perception.valid_cell_to_move(new_cell[0], new_cell[1])
                    and not matrix[new_cell[0]][new_cell[1]]
                ):
                    queue.append(new_cell)
                    matrix[new_cell[0]][new_cell[1]] = True
                    pi[new_cell[0] * perception.dimension_y + new_cell[1]] = cell
                    plan[
                        new_cell[0] * perception.dimension_y + new_cell[1]
                    ] = directions_actions[i]

        return self.get_random_move(perception)

    def go_to_edge(self, perception):
        """
        Devuelve una lista de acciones que se deben realizar para conseguir llegar al borde.
        En caso de no haber una acción clara en la percepción se devuelve una
        acción de moverse aleatoria.

        :param perception: parte del mundo que es percibida por el agente
        :type perception: World

        :rtype: Action list
        """
        
        matrix = [
            [False for i in range(perception.dimension_y)]
            for j in range(perception.dimension_x)
        ]
        matrix[self.perception_pos_x][self.perception_pos_y] = True

        pi = []
        plan = []
        for i in range(perception.dimension_x * perception.dimension_y):
            pi.append(-1)
            plan.append(action.DoNothing())

        queue = [(self.perception_pos_x, self.perception_pos_y)]
        while len(queue) > 0:
            cell = queue.pop(0)
            if perception.cell_is_edge(cell[0], cell[1]):
                return self.make_plan(cell, pi, plan, perception.dimension_y)

            for i in range(4):
                new_cell = (cell[0] + directions[i][0], cell[1] + directions[i][1])

                if (
                    perception.valid_cell_to_move(new_cell[0], new_cell[1])
                    and not matrix[new_cell[0]][new_cell[1]]
                ):
                    queue.append(new_cell)
                    matrix[new_cell[0]][new_cell[1]] = True
                    pi[new_cell[0] * perception.dimension_y + new_cell[1]] = cell
                    plan[
                        new_cell[0] * perception.dimension_y + new_cell[1]
                    ] = directions_actions[i]

        return self.get_random_move(perception)

    def play(self, perception):
        """
        Devuelve las acciones que se deben realizar para conseguir algún objetivo.

        :param perception: parte del mundo que es percibida por el agente
        :type perception: World

        :rtype: Action
        """
        if not self.is_alive:
            return []
        if self.current_energy < self.energy_lost_fun(
            self.genetic_code.get_gene('sense').value, 
            self.genetic_code.get_gene('speed').value, 
            self.genetic_code.get_gene('size').value
        ):
            return [action.DoNothing()]
        if self.food_eat_today == 0 or (
            self.food_eat_today == 1 and self.current_energy >= self.max_energy // 2
        ):
            l = self.look_for_food(perception)[: self.genetic_code.get_gene('speed').value]
            return l
        return self.go_to_edge(perception)[: self.genetic_code.get_gene('speed').value]

    def see(self, world):
        """
        Devuelve la percepción del mundo que tiene el agente.
        La percepción es nuevo mundo, de tamaño dimension_x * dimension_y,
        que es una copia de un lugar del mundo original. La parte que
        es copiada es el cuadrado que tiene esquina superior izqueda
        (left_corner_x y left_corner_y) y esquina inferior derecha
        (right_corner_x y right_corner_y).

        :param left_corner_x: coordenada x, esquina superior izquierda
        :type left_corner_x: int
        :param left_corner_y: coordenada y, esquina superior izquierda
        :type left_corner_y: int
        :param right_corner_x: coordenada x, esquina inferior derecha
        :type right_corner_x: int
        :param right_corner_y: coordenada y, esquina inferior derecha
        :type right_corner_y: int
        :param dimension_x: largo de la copia
        :type dimension_x: int
        :param dimension_y: ancho de la copia
        :type dimension_y: int

        :rtype: World
        :return: world.get_a_peek(
            left_corner_x,
            left_corner_y,
            right_corner_x,
            right_corner_y,
            right_corner_x - left_corner_x + 1,
            right_corner_y - left_corner_y + 1,
        )
        """
        left_corner_x = max(0, self.pos_x - self.genetic_code.get_gene('sense').value)
        left_corner_y = max(0, self.pos_y - self.genetic_code.get_gene('sense').value)
        right_corner_x = min(self.pos_x + self.genetic_code.get_gene('sense').value, world.dimension_x - 1)
        right_corner_y = min(self.pos_y + self.genetic_code.get_gene('sense').value, world.dimension_y - 1)

        self.perception_pos_x = min(self.pos_x, self.genetic_code.get_gene('sense').value)
        self.perception_pos_y = min(self.pos_y, self.genetic_code.get_gene('sense').value)

        return world.get_a_peek(left_corner_x,
                left_corner_y,
                right_corner_x,
                right_corner_y,
                right_corner_x - left_corner_x + 1,
                right_corner_y - left_corner_y + 1)

    def set_feromone(self, world):
        world.map[self.pos_x][self.pos_y].add_feromone(Pheromone())
        
class Pheromone:
    def __init__(self, value = 1):
        self.value = value
        self.time = 2
    
    def evaporate(self):
        self.time -= 1