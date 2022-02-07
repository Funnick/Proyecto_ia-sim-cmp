class DefineContext:
    def __init__(self) -> None:
        self.context = set([])

    def declare_var(self, id):
        if id not in self.context:
            self.context.add(id)
            return True
        return False

    def exist_var(self, id):
        return id in self.context


class Context:
    def __init__(self) -> None:
        self.father = None
        self.id_value = {}
        self.infered_id_type = {}

    def set_id_value(self, id, value):
        self.id_value[id] = value

    def get_id_value(self, id):
        if self.id_value.get(id) != None:
            return self.id_value[id]
        return self.father.get_id_value(id)

    def exist_id_value(self, id):
        if self.id_value.get(id) != None:
            return True
        if self.father == None:
            return False
        return self.father.exist_id_value(id)

    def set_infered_id_type(self, id, type):
        self.infered_id_type[id] = type

    def get_infered_id_type(self, id):
        if self.infered_id_type.get(id):
            return self.infered_id_type[id]
        return self.father.get_infered_id_type(id)

    def exist_id_type(self, id):
        if self.infered_id_type.get(id) != None:
            return True
        if self.father == None:
            return False
        return self.father.exist_id_type(id)

    def create_child_context(self):
        context_child = Context()
        context_child.father = self
        return context_child
