import object_base
import action
from random import randint


class Agent(object_base.ObjectBase):
    def __init__(self, pos_x, pos_y, sense, max_energy):
        object_base.ObjectBase.__init__(self, pos_x, pos_y)
        self.perception_pos_x = -1
        self.perception_pos_y = -1
        self.sense = sense
        self.food_eat_today = 0
        self.max_energy = max_energy
        self.current_energy = max_energy

    def __str__(self):
        return "Agent"

    def get_random_move(self, perception):
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
        new_plan = [plan[cell[0] * dimension_y + cell[1]]]
        cell = pi[cell[0] * dimension_y + cell[1]]

        while cell != -1:
            new_plan.append(plan[cell[0] * dimension_y + cell[1]])
            cell = pi[cell[0] * dimension_y + cell[1]]

        return new_plan

    def look_for_food(self, perception):
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
        if self.current_energy == 0:
            return action.DoNothing()
        if self.food_eat_today == 0 or (
            self.food_eat_today == 1 and self.current_energy >= self.max_energy // 2
        ):
            return self.look_for_food(perception)[0]
        return self.go_to_edge(perception)[0]

    def see(self, world):
        left_corner_x = max(0, self.pos_x - self.sense)
        left_corner_y = max(0, self.pos_y - self.sense)
        right_corner_x = min(self.pos_x + self.sense, world.dimension_x - 1)
        right_corner_y = min(self.pos_y + self.sense, world.dimension_y - 1)

        self.perception_pos_x = min(self.pos_x, self.sense)
        self.perception_pos_y = min(self.pos_y, self.sense)

        return world.get_a_peek(
            left_corner_x,
            left_corner_y,
            right_corner_x,
            right_corner_y,
            right_corner_x - left_corner_x + 1,
            right_corner_y - left_corner_y + 1,
        )
