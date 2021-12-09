import object_base
import action
from random import randint


class Agent(object_base.ObjectBase):
    """
    Clase que reprenseta a los agentes de la simulación.
    """

    def __init__(self, pos_x, pos_y, max_energy, sense_gene, speed_gene):
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
        self.perception_pos_x = -1
        self.perception_pos_y = -1
        self.food_eat_today = 0
        self.max_energy = max_energy
        self.current_energy = max_energy
        self.sense_gene = sense_gene
        self.speed_gene = speed_gene
        self.energy_lost_fun = lambda sense, speed: sense + speed

    def __str__(self):
        return "Agent"

    def reduce_energy_to_perform_an_action(self):
        """
        Devuelve verdadero en caso de que se pueda consumir energía
        para realizar una acción, falso en otro caso.

        :rtype: bool
        :return: self.current_energy >= self.sense_gene.value
        """
        elf = self.energy_lost_fun(self.sense_gene.value, self.speed_gene.value)
        if self.current_energy >= elf:
            self.current_energy = self.current_energy - elf
            return True
        return False

    def replicate(self):
        """
        Devuelve un nuevo agente que puede tener características mutadas,
        es el resultado de una reproducción asexual.

        :rtype: Agent
        :return: Agent(...)
        """
        return Agent(
            -1, -1, self.max_energy, self.sense_gene.mutate(), self.speed_gene.mutate()
        )

    def get_random_move(self, perception):
        """
        Devuelve una acción que mueve al agente en una dirección.

        :param perception: parte del mundo que es percibida por el agente
        :type perception: World

        :rtype: Action
        :return: [moves[randint(0, len(moves) - 1)]]
        """
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        directions_actions = [
            action.MoveNorth(),
            action.MoveSouth(),
            action.MoveWest(),
            action.MoveEast(),
        ]
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

    def look_for_food(self, perception):
        """
        Devuelve una lista de acciones que se deben realizar para conseguir comida.
        En caso de no haber una acción clara en la percepción se devuelve una
        acción de moverse aleatoria.

        :param perception: parte del mundo que es percibida por el agente
        :type perception: World

        :rtype: Action list
        """
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        directions_actions = [
            action.MoveNorth(),
            action.MoveSouth(),
            action.MoveWest(),
            action.MoveEast(),
        ]

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
            if perception.cell_have_food(cell[0], cell[1]):
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
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        directions_actions = [
            action.MoveNorth(),
            action.MoveSouth(),
            action.MoveWest(),
            action.MoveEast(),
        ]

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
        if self.current_energy < self.energy_lost_fun(
            self.sense_gene.value, self.speed_gene.value
        ):
            return [action.DoNothing()]
        if self.food_eat_today == 0 or (
            self.food_eat_today == 1 and self.current_energy >= self.max_energy // 2
        ):
            l = self.look_for_food(perception)[: self.speed_gene.value]
            return l
        return self.go_to_edge(perception)[: self.speed_gene.value]

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
        left_corner_x = max(0, self.pos_x - self.sense_gene.value)
        left_corner_y = max(0, self.pos_y - self.sense_gene.value)
        right_corner_x = min(self.pos_x + self.sense_gene.value, world.dimension_x - 1)
        right_corner_y = min(self.pos_y + self.sense_gene.value, world.dimension_y - 1)

        self.perception_pos_x = min(self.pos_x, self.sense_gene.value)
        self.perception_pos_y = min(self.pos_y, self.sense_gene.value)

        return world.get_a_peek(
            left_corner_x,
            left_corner_y,
            right_corner_x,
            right_corner_y,
            right_corner_x - left_corner_x + 1,
            right_corner_y - left_corner_y + 1,
        )
