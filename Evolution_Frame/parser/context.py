from .built_in_fun import built_in_functions, built_in_fun_type


class Context:
    def __init__(self) -> None:
        self.context = {}
        self.parent = None

    def declare_id(self, id, type_):
        self.context[id] = type_

    def is_built_in(self, id):
        if built_in_functions.get(id):
            return True
        return False

    def get_built_in_fun_type(self, id):
        return built_in_fun_type[id]

    def exist_id(self, id):
        if self.context.get(id):
            return True
        elif self.parent:
            return self.parent.exist_id(id)
        return False

    def exist_id_in_this_context(self, id):
        if self.context.get(id):
            return True
        return False

    def get_id_type(self, id):
        if not (self.context.get(id) is None):
            return self.context[id]
        else:
            return self.parent.get_id_type(id)

    def get_child(self):
        child_context = Context()
        child_context.parent = self
        return child_context


class ExecuteContext:
    def __init__(self) -> None:
        self.var_type = {}
        self.var_context = {}
        self.fun_context = {}
        self.fun_params = {}
        self.parent = None

    def define_var(self, id, type, value):
        self.var_type[id] = type
        self.var_context[(id, type)] = value

    def assigment_var(self, id, value):
        if self.var_context.get((id, self.get_var_type(id))) != None:
            self.var_context[(id, self.get_var_type(id))] = value
        else:
            self.parent.assigment_var(id, value)

    def define_fun(self, id, type, param_list, body):
        self.var_type[id] = type
        self.fun_params[(id, type)] = param_list
        self.fun_context[(id, type)] = body

    def id_is_built_in(self, id):
        if built_in_functions.get(id):
            return True
        return False

    def is_var(self, id):
        if self.var_context.get((id, self.get_var_type(id))) != None:
            return True
        elif self.parent:
            return self.parent.is_var(id)
        return False

    def get_built_in_fun(self, id):
        return built_in_functions[id]

    def get_fun(self, id):
        if self.fun_context.get((id, self.get_var_type(id))) != None:
            return self.fun_context[(id, self.get_var_type(id))]
        return self.parent.get_fun(id)

    def get_fun_param(self, id):
        if self.fun_params.get((id, self.get_var_type(id))) != None:
            return self.fun_params[(id, self.get_var_type(id))]
        else:
            return self.parent.get_fun_param(id)

    def get_var_type(self, id):
        if self.var_type.get(id):
            return self.var_type[id]
        else:
            return self.parent.get_var_type(id)

    def get_var_value(self, id):
        if self.var_context.get((id, self.get_var_type(id))) != None:
            return self.var_context[(id, self.get_var_type(id))]
        return self.parent.get_var_value(id)

    def get_child(self):
        child_context = ExecuteContext()
        child_context.parent = self
        return child_context
