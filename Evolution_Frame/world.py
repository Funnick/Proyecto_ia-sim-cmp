import object_base
from random import randint, random


class World:
    def __init__(self, dimension_x, dimension_y):
        self.dimension_x = dimension_x
        self.dimension_y = dimension_y
        self.map = [
            [[object_base.ObjectBase(i, j)] for i in range(dimension_y)]
            for j in range(dimension_x)
        ]
        self.add_edges()

    def add_edges(self):
        for i in range(self.dimension_y):
            self.map[0][i][0] = object_base.Edge(0, i)
            self.map[self.dimension_x - 1][i][0] = object_base.Edge(
                self.dimension_x - 1, i
            )
        for i in range(1, self.dimension_x - 1):
            self.map[i][0][0] = object_base.Edge(i, 0)
            self.map[i][self.dimension_y - 1][0] = object_base.Edge(
                i, self.dimension_y - 1
            )

    def __str__(self):
        m = ""
        for i in range(self.dimension_x):
            for j in range(self.dimension_y):
                m += str(self.map[i][j][-1]) + " "
            m += "\n"
        return m

    def add_food(self, food_amount):
        while food_amount > 0:
            u = randint(0, self.dimension_x * self.dimension_y - 1)
            pos_x, pos_y = u // self.dimension_y, u % self.dimension_y
            if not self.map[pos_x][pos_y][0].is_edge:
                self.map[pos_x][pos_y].append(object_base.Food(pos_x, pos_y))
                food_amount = food_amount - 1

    def get_a_peek(
        self,
        left_corner_x,
        left_corner_y,
        right_corner_x,
        right_corner_y,
        dimension_x,
        dimension_y,
    ):
        w = World(dimension_x, dimension_y)
        d_x, d_y = 0, 0
        for i in range(left_corner_x, right_corner_x + 1):
            for j in range(left_corner_y, right_corner_y + 1):
                w.map[d_x][d_y] = self.map[i][j]
                d_y = d_y + 1
            d_x = d_x + 1
            d_y = 0

        return w

    def cell_is_edge(self, pos_x, pos_y):
        for c in self.map[pos_x][pos_y]:
            if c.is_edge:
                return True
        return False

    def valid_cell_to_move(self, pos_x, pos_y):
        return (
            pos_x >= 0
            and pos_x < self.dimension_x
            and pos_y >= 0
            and pos_y < self.dimension_y
        )

    def cell_have_food(self, pos_x, pos_y):
        for c in self.map[pos_x][pos_y]:
            if c.is_food:
                return True
        return False

    def move_agent(self, agent, new_pos_x, new_pos_y):
        self.map[new_pos_x][new_pos_y].append(agent)
        self.map[agent.pos_x][agent.pos_y].remove(agent)

    def agent_eat_food(self, food_pos_x, food_pos_y):
        for c in self.map[food_pos_x][food_pos_y]:
            if c.is_food:
                self.map[food_pos_x][food_pos_y].remove(c)
                return True
        return False

    def get_pos_random_edge(self):
        r = randint(0, self.dimension_x - 1)
        if r == 0 or r == self.dimension_x - 1:
            c = randint(0, self.dimension_y - 1)
        elif random() <= 0.5:
            c = 0
        else:
            c = self.dimension_y - 1
        return r, c

    def add_agent(self, edge_pos_x, edge_pos_y, agent):
        self.map[edge_pos_x][edge_pos_y].append(agent)

    def remove_agent(self, agent):
        self.map[agent.pos_x][agent.pos_y].remove(agent)
