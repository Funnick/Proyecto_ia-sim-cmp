from abc import ABC, abstractmethod

from .context import DefineContext
from .project_context import built_in_fun, built_in_fun_type
from .utils import ReturnException

define_context = DefineContext()
define_context.context = set(built_in_fun.keys())


class Node(ABC):
    @abstractmethod
    def execute(self, project_context):
        pass

    @abstractmethod
    def check_semantics(self):
        pass


class BlockStmt(Node):
    def __init__(self, childs) -> None:
        self.childs = childs

    def execute(self, project_context):
        for child in self.childs:
            child.execute(project_context)

    def check_semantics(self):
        for child in self.childs:
            if not child.check_semantics():
                return False

        return True


class Expression(Node):
    def __init__(self) -> None:
        self.type = None


class Leaf(Expression):
    def execute(self, project_context):
        return self.value


class Number(Leaf):
    def __init__(self, value) -> None:
        super().__init__()
        self.value = int(value)

    def check_semantics(self):
        self.type = "Number"
        return True


class String(Leaf):
    def __init__(self, value) -> None:
        super().__init__()
        self.value = str(value[1:-1])

    def check_semantics(self):
        self.type = "Str"
        return True


class Bool(Leaf):
    def __init__(self, value) -> None:
        if value == "True":
            self.value = True
        else:
            self.value = False

    def check_semantics(self):
        self.type = "Bool"
        return True


class Nil(Leaf):
    def __init__(self) -> None:
        self.value = None

    def check_semantics(self):
        self.type = "Nil"
        return True


class BinaryExpression(Expression):
    def __init__(self, left_child, right_child) -> None:
        super().__init__()
        self.left_child = left_child
        self.right_child = right_child
        self.left_value = None
        self.right_value = None

    def execute(self, project_context):
        self.left_value = self.left_child.execute(project_context)
        self.right_value = self.right_child.execute(project_context)

    def get_left_value(self, project_context):
        return self.left_child.execute(project_context)

    def get_right_value(self, project_context):
        return self.right_child.execute(project_context)

    def check_semantics(self):
        csl = self.left_child.check_semantics()
        csr = self.right_child.check_semantics()
        return csl and csr


class Or(BinaryExpression):
    def __init__(self, left_child, right_child) -> None:
        super().__init__(left_child, right_child)

    def execute(self, project_context):
        self.type = "Bool"
        return self.get_left_value(project_context) or self.get_right_value(
            project_context
        )

    def check_semantics(self):
        return super().check_semantics()


class And(BinaryExpression):
    def __init__(self, left_child, right_child) -> None:
        super().__init__(left_child, right_child)

    def execute(self, project_context):
        self.type = "Bool"
        return self.get_left_value(project_context) and self.get_right_value(
            project_context
        )

    def check_semantics(self):
        return super().check_semantics()


class NotEqual(BinaryExpression):
    def execute(self, project_context):
        self.type = "Bool"
        return self.get_left_value(project_context) != self.get_right_value(
            project_context
        )

    def check_semantics(self):
        if not super().check_semantics():
            return False
        if self.left_child.type == self.right_child.type:
            self.type = "Bool"
            return True
        return False


class EqualEqual(BinaryExpression):
    def execute(self, project_context):
        self.type = "Bool"
        return self.get_left_value(project_context) == self.get_right_value(
            project_context
        )

    def check_semantics(self):
        return super().check_semantics()


class Greater(BinaryExpression):
    def execute(self, project_context):
        self.type = "Bool"
        return self.get_left_value(project_context) > self.get_right_value(
            project_context
        )

    def check_semantics(self):
        return super().check_semantics()


class GreaterEqual(BinaryExpression):
    def execute(self, project_context):
        self.type = "Bool"
        return self.get_left_value(project_context) >= self.get_right_value(
            project_context
        )

    def check_semantics(self):
        return super().check_semantics()


class Less(BinaryExpression):
    def execute(self, project_context):
        self.type = "Bool"
        return self.get_left_value(project_context) < self.get_right_value(
            project_context
        )

    def check_semantics(self):
        return super().check_semantics()


class LessEqual(BinaryExpression):
    def execute(self, project_context):
        self.type = "Bool"
        return self.get_left_value(project_context) <= self.get_right_value(
            project_context
        )

    def check_semantics(self):
        return super().check_semantics()


class Sum(BinaryExpression):
    def execute(self, project_context):
        self.type = "Number"
        return self.get_left_value(project_context) + self.get_right_value(
            project_context
        )

    def check_semantics(self):
        return super().check_semantics()


class Sub(BinaryExpression):
    def execute(self, project_context):
        self.type = "Number"
        return self.get_left_value(project_context) - self.get_right_value(
            project_context
        )

    def check_semantics(self):
        return super().check_semantics()


class Mult(BinaryExpression):
    def execute(self, project_context):
        self.type = "Number"
        return self.get_left_value(project_context) * self.get_right_value(
            project_context
        )

    def check_semantics(self):
        return super().check_semantics()


class Div(BinaryExpression):
    def execute(self, project_context):
        self.type = "Number"
        return self.get_left_value(project_context) / self.get_right_value(
            project_context
        )

    def check_semantics(self):
        return super().check_semantics()


class UnaryExpression(Expression):
    def __init__(self, child) -> None:
        super().__init__()
        self.child = child

    def get_value(self, project_context):
        return self.child.execute(project_context)

    def execute(self, project_context):
        self.child_value = self.child.execute(project_context)

    def check_semantics(self):
        return self.child.check_semantics()


class Minus(UnaryExpression):
    def execute(self, project_context):
        self.type = "Number"
        return -self.get_value(project_context)

    def check_semantics(self):
        return super().check_semantics()


class Not(UnaryExpression):
    def execute(self, project_context):
        self.type = "Bool"
        return not self.get_value(project_context)

    def check_semantics(self):
        return super().check_semantics()


class PrintStmt(Node):
    def __init__(self, child) -> None:
        self.child = child
        self.child_value = None

    def execute(self, project_context):
        self.child_value = self.child.execute(project_context)
        print(self.child_value)

    def check_semantics(self):
        return self.child.check_semantics()


class Call(Node):
    def __init__(self, id, args) -> None:
        self.id = id
        self.args = args

    def execute(self, project_context):
        new_context = project_context.create_child_context()
        if built_in_fun.get(self.id) is not None:
            self.type = built_in_fun_type[self.id]
            return built_in_fun[self.id](new_context, self.args)
        calleable_type = project_context.get_infered_id_type(self.id)
        funct = project_context.get_id_value(self.id)
        if calleable_type != "Fun":
            self.type = calleable_type
            return funct
        for i, a in enumerate(funct.args):
            new_context.set_id_value(a, self.args[i].execute(project_context))
            new_context.set_infered_id_type(a, self.args[i].type)
        try:
            funct.block_stmt.execute(new_context)
        except ReturnException as r:
            self.type = r.type
            return r.value
        self.type = "Nil"
        return None

    def check_semantics(self):
        for arg in self.args:
            if not arg.check_semantics():
                return False
        return define_context.exist_var(self.id)


class Return(Node):
    def __init__(self, expression=None) -> None:
        self.expression = expression

    def execute(self, project_context):
        if self.expression is None:
            raise ReturnException(None)
        raise ReturnException(
            self.expression.execute(project_context), self.expression.type
        )

    def check_semantics(self):
        if self.expression == None:
            return True
        return self.expression.check_semantics()


class FuntionDeclaration(Node):
    def __init__(self, id, args, block_stmt) -> None:
        self.id = id
        self.args = args
        self.block_stmt = block_stmt

    def execute(self, project_context):
        project_context.set_id_value(self.id, self)
        project_context.set_infered_id_type(self.id, "Fun")

    def check_semantics(self):
        for arg in self.args:
            if not define_context.declare_var(arg):
                return False
        return define_context.declare_var(self.id) and self.block_stmt.check_semantics()


class VarDeclaration(Node):
    def __init__(self, id, expr=None) -> None:
        self.id = id
        self.expr = expr

    def execute(self, project_context):
        if self.expr == None:
            project_context.set_infered_id_type(self.id, "Nil")
            project_context.set_id_value(self.id, "Nil")
        else:
            project_context.set_id_value(self.id, self.expr.execute(project_context))
            project_context.set_infered_id_type(self.id, self.expr.type)

    def check_semantics(self):
        if self.expr == None:
            return define_context.declare_var(self.id)
        expr_sem = self.expr.check_semantics()
        return expr_sem and define_context.declare_var(self.id)


class VarCall(Expression):
    def __init__(self, id) -> None:
        super().__init__()
        self.id = id

    def execute(self, project_context):
        self.type = project_context.get_infered_id_type(self.id)
        return project_context.get_id_value(self.id)

    def check_semantics(self):
        return define_context.exist_var(self.id)


class Redefine(Expression):
    def __init__(self, id, expr) -> None:
        super().__init__()
        self.id = id
        self.expr = expr

    def execute(self, project_context):
        self.type = self.expr.type
        project_context.set_id_value(self.id, self.expr.execute(project_context))
        return project_context.get_id_value(self.id)

    def check_semantics(self):
        return define_context.exist_var(self.id) and self.expr.check_semantics()


class VarAssigment(Expression):
    def __init__(self, id, expr) -> None:
        super().__init__()
        self.id = id
        self.expr = expr

    def execute(self, project_context):
        self.type = self.expr.type
        project_context.set_id_value(self.id, self.expr.execute(project_context))
        project_context.set_infered_id_type(self.id, self.type)
        return project_context.get_id_value(self.id)

    def check_semantics(self):
        return define_context.exist_var(self.id) and self.expr.check_semantics()


class If(Node):
    def __init__(self, expr, stmt) -> None:
        self.expr = expr
        self.stmt = stmt

    def execute(self, project_context):
        if self.expr.execute(project_context):
            self.stmt.execute(project_context)

    def check_semantics(self):
        expr_sem = self.expr.check_semantics()
        stmt_sem = self.stmt.check_semantics()

        return expr_sem and stmt_sem


class IfElse(Node):
    def __init__(self, expr, stmt, else_stmt) -> None:
        self.expr = expr
        self.stmt = stmt
        self.else_stmt = else_stmt

    def execute(self, project_context):
        if self.expr.execute(project_context):
            self.stmt.execute(project_context)
        else:
            self.else_stmt.execute()

    def check_semantics(self):
        expr_sem = self.expr.check_semantics()
        stmt_sem = self.stmt.check_semantics()
        else_stmt_sem = self.else_stmt.check_semantics()

        return expr_sem and stmt_sem and else_stmt_sem


class While(Node):
    def __init__(self, expr, block_stmt) -> None:
        self.expr = expr
        self.block_stmt = block_stmt

    def execute(self, project_context):
        while self.expr.execute(project_context):
            self.block_stmt.execute(project_context)

    def check_semantics(self):
        return self.expr.check_semantics() and self.block_stmt.check_semantics()


class AgentPredicate(Node):
    def __init__(self, id) -> None:
        self.id = id

    def execute(self, project_context):
        return project_context.get_id_value(self.id)

    def check_semantics(self):
        return define_context.exist_var(self.id)
