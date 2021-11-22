class ObjectBase:
    def __init__(self, pos_x, pos_y):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.is_edge = False
        self.is_food = False

    def __str__(self):
        return "Nothing"


class Edge(ObjectBase):
    def __init__(self, pos_x, pos_y):
        ObjectBase.__init__(self, pos_x, pos_y)
        self.is_edge = True

    def __str__(self):
        return "Edge"


class Food(ObjectBase):
    def __init__(self, pos_x, pos_y):
        ObjectBase.__init__(self, pos_x, pos_y)
        self.is_food = True

    def __str__(self):
        return "Food"
