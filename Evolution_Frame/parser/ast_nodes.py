from abc import ABC, abstractmethod
from .utils import ReturnException


class Node(ABC):
    @abstractmethod
    def execute(self, context):
        pass

    @abstractmethod
    def check_semantics(self, context):
        pass


class BlockDec(Node):
    def __init__(self, dec_list) -> None:
        self.dec_list = dec_list

    def execute(self, context):
        for dec in self.dec_list:
            dec.execute(context)

    def check_semantics(self, context):
        for dec in self.dec_list:
            if not dec.check_semantics(context):
                return False
        return True


class FunDec(Node):
    def __init__(self, type_, id, param_list, body) -> None:
        self.type_ = type_
        self.id = id
        self.param_list = param_list
        self.body = body

    def execute(self, context):
        context.define_fun(self.id, self.type, self.param_list, self)

    def check_semantics(self, context):
        if context.exist_id(self.id):
            return False

        self.type = "fun_" + self.type_.type
        context.declare_id(self.id, self.type)
        child_context = context.get_child()
        for p in self.param_list:
            if not p.check_semantics(child_context):
                return False

        if self.body.check_semantics(child_context):
            return True
        return False


class VarDec(Node):
    def __init__(self, type_, id, exp) -> None:
        self.type_ = type_
        self.id = id
        self.exp = exp

    def execute(self, context):
        context.define_var(self.id, self.type_.type, self.exp.execute(context))

    def check_semantics(self, context):
        if context.exist_id(self.id):
            return False

        if (
            self.type_.check_semantics(context)
            and self.exp.check_semantics(context)
            and self.type_.type == self.exp.type
        ):
            context.declare_id(self.id, self.exp.type)
        return True


class Param(Node):
    def __init__(self, type_, id) -> None:
        self.type = type_
        self.id = id

    def execute(self, context):
        pass

    def check_semantics(self, context):
        if context.exist_id_in_this_context(self.id) and not self.type.check_semantics(
            context
        ):
            return False
        context.declare_id(self.id, self.type.type)
        return True


class LType(Node):
    def __init__(self, type) -> None:
        self.type = type

    def execute(self, context):
        pass

    def check_semantics(self, context):
        return True


class Number(Node):
    def __init__(self, value) -> None:
        self.value = value

    def execute(self, context):
        return self.value

    def check_semantics(self, context):
        if "." in self.value:
            self.value = float(self.value)
        else:
            self.value = int(self.value)
        self.type = "number"
        return True


class String(Node):
    def __init__(self, value) -> None:
        self.value = value

    def execute(self, context):
        return self.value

    def check_semantics(self, context):
        self.value = str(self.value[1:-1])
        self.type = "string"
        return True


class Bool(Node):
    def __init__(self, value) -> None:
        self.value = value

    def execute(self, context):
        return self.value

    def check_semantics(self, context):
        if self.value == "True":
            self.value = True
        elif self.value == "False":
            self.value = False
        else:
            return False
        self.type = "bool"
        return True


class Nil(Node):
    def __init__(self) -> None:
        self.value = "Nil"

    def execute(self, context):
        return None

    def check_semantics(self, context):
        self.value = None
        self.type = "nil"
        return True


class ID(Node):
    def __init__(self, value) -> None:
        self.value = str(value)

    def execute(self, context):
        if context.is_var(self.value):
            return context.get_var_value(self.value)
        elif context.id_is_built_in(self.value):
            return context.get_built_in_fun(self.value)
        return context.get_fun(self.value)

    def check_semantics(self, context):
        if not context.exist_id(self.value):
            return False
        self.type = context.get_id_type(self.value)
        return True


class If(Node):
    def __init__(self, exp, block_dec) -> None:
        self.exp = exp
        self.block_dec = block_dec

    def execute(self, context):
        if self.exp.execute(context):
            self.block_dec.execute(context.get_child())

    def check_semantics(self, context):
        if (
            self.exp.check_semantics(context)
            and self.exp.type == "bool"
            and self.block_dec.check_semantics(context)
        ):
            return True
        return False


class IfElse(Node):
    def __init__(self, exp, block_dec_1, block_dec_2) -> None:
        self.exp = exp
        self.block_dec_1 = block_dec_1
        self.block_dec_2 = block_dec_2

    def execute(self, context):
        if self.exp.execute(context):
            self.block_dec_1.execute(context.get_child())
        else:
            self.block_dec_2.execute(context.get_child())

    def check_semantics(self, context):
        if (
            self.exp.check_semantics(context)
            and self.exp.type == "bool"
            and self.block_dec_1.check_semantics(context)
            and self.block_dec_2.check_semantics(context)
        ):
            return True
        return False


class While(Node):
    def __init__(self, exp, block_dec) -> None:
        self.exp = exp
        self.block_dec = block_dec

    def execute(self, context):
        while self.exp.execute(context):
            self.block_dec.execute(context.get_child())

    def check_semantics(self, context):
        if (
            self.exp.check_semantics(context)
            and self.exp.type == "bool"
            and self.block_dec.check_semantics(context)
        ):
            return True
        return False


class Return(Node):
    def __init__(self, exp) -> None:
        self.exp = exp

    def execute(self, context):
        if self.exp is None:
            raise ReturnException(None, "Nil")
        raise ReturnException(self.exp.execute(context), self.exp.type)

    def check_semantics(self, context):
        if self.exp is None:
            return True
        else:
            if self.exp.check_semantics(context):
                return True
        return False


class Assignment(Node):
    def __init__(self, id, exp) -> None:
        self.id = id
        self.exp = exp

    def execute(self, context):
        context.assigment_var(self.id, self.exp.execute(context))

    def check_semantics(self, context):
        if not context.exist_id(self.id):
            return False

        id_type = context.get_id_type(self.id)
        if self.exp.check_semantics(context) and self.exp.type == id_type:
            return True
        return False


class BinaryExpression(Node):
    def __init__(self, left_child, right_child) -> None:
        self.left_child = left_child
        self.right_child = right_child

    def check_semantics(self, context):
        if self.left_child.check_semantics(
            context
        ) and self.right_child.check_semantics(context):
            return True


class Or(BinaryExpression):
    def __init__(self, left_child, right_child) -> None:
        super().__init__(left_child, right_child)

    def execute(self, context):
        left = self.left_child.execute(context)
        right = self.right_child.execute(context)
        return left or right

    def check_semantics(self, context):
        if not super().check_semantics(context):
            return False

        if (
            self.left_child.type == self.right_child.type
            and self.left_child.type == "bool"
        ):
            self.type = "bool"
            return True
        return False


class And(BinaryExpression):
    def __init__(self, left_child, right_child) -> None:
        super().__init__(left_child, right_child)

    def execute(self, context):
        left = self.left_child.execute(context)
        right = self.right_child.execute(context)
        return left and right

    def check_semantics(self, context):
        if not super().check_semantics(context):
            return False

        if (
            self.left_child.type == self.right_child.type
            and self.left_child.type == "bool"
        ):
            self.type = "bool"
            return True
        return False


class EqualEqual(BinaryExpression):
    def __init__(self, left_child, right_child) -> None:
        super().__init__(left_child, right_child)

    def execute(self, context):
        left = self.left_child.execute(context)
        right = self.right_child.execute(context)
        return left == right

    def check_semantics(self, context):
        if not super().check_semantics(context):
            return False

        if self.left_child.type == self.right_child.type:
            self.type = "bool"
            return True
        return False


class NotEqual(BinaryExpression):
    def __init__(self, left_child, right_child) -> None:
        super().__init__(left_child, right_child)

    def execute(self, context):
        left = self.left_child.execute(context)
        right = self.right_child.execute(context)
        return left != right

    def check_semantics(self, context):
        if not super().check_semantics(context):
            return False

        if self.left_child.type == self.right_child.type:
            self.type = "bool"
            return True
        return False


class Greater(BinaryExpression):
    def __init__(self, left_child, right_child) -> None:
        super().__init__(left_child, right_child)

    def execute(self, context):
        left = self.left_child.execute(context)
        right = self.right_child.execute(context)
        return left > right

    def check_semantics(self, context):
        if not super().check_semantics(context):
            return False

        if (
            self.left_child.type == self.right_child.type
            and self.left_child.type == "number"
        ):
            self.type = "bool"
            return True
        return False


class GreaterEqual(BinaryExpression):
    def __init__(self, left_child, right_child) -> None:
        super().__init__(left_child, right_child)

    def execute(self, context):
        left = self.left_child.execute(context)
        right = self.right_child.execute(context)
        return left >= right

    def check_semantics(self, context):
        if not super().check_semantics(context):
            return False

        if (
            self.left_child.type == self.right_child.type
            and self.left_child.type == "number"
        ):
            self.type = "bool"
            return True
        return False


class Less(BinaryExpression):
    def __init__(self, left_child, right_child) -> None:
        super().__init__(left_child, right_child)

    def execute(self, context):
        left = self.left_child.execute(context)
        right = self.right_child.execute(context)
        return left < right

    def check_semantics(self, context):
        if not super().check_semantics(context):
            return False

        if (
            self.left_child.type == self.right_child.type
            and self.left_child.type == "number"
        ):
            self.type = "bool"
            return True
        return False


class LessEqual(BinaryExpression):
    def __init__(self, left_child, right_child) -> None:
        super().__init__(left_child, right_child)

    def execute(self, context):
        left = self.left_child.execute(context)
        right = self.right_child.execute(context)
        return left <= right

    def check_semantics(self, context):
        if not super().check_semantics(context):
            return False

        if (
            self.left_child.type == self.right_child.type
            and self.left_child.type == "number"
        ):
            self.type = "bool"
            return True
        return False


class Plus(BinaryExpression):
    def __init__(self, left_child, right_child) -> None:
        super().__init__(left_child, right_child)

    def execute(self, context):
        left = self.left_child.execute(context)
        right = self.right_child.execute(context)
        return left + right

    def check_semantics(self, context):
        if not super().check_semantics(context):
            return False

        if (
            self.left_child.type == self.right_child.type
            and self.left_child.type == "number"
        ):
            self.type = "number"
            return True
        return False


class Sub(BinaryExpression):
    def __init__(self, left_child, right_child) -> None:
        super().__init__(left_child, right_child)

    def execute(self, context):
        left = self.left_child.execute(context)
        right = self.right_child.execute(context)
        return left - right

    def check_semantics(self, context):
        if not super().check_semantics(context):
            return False

        if (
            self.left_child.type == self.right_child.type
            and self.left_child.type == "number"
        ):
            self.type = "number"
            return True
        return False


class Star(BinaryExpression):
    def __init__(self, left_child, right_child) -> None:
        super().__init__(left_child, right_child)

    def execute(self, context):
        left = self.left_child.execute(context)
        right = self.right_child.execute(context)
        return left * right

    def check_semantics(self, context):
        if not super().check_semantics(context):
            return False

        if (
            self.left_child.type == self.right_child.type
            and self.left_child.type == "number"
        ):
            self.type = "number"
            return True
        return False


class Div(BinaryExpression):
    def __init__(self, left_child, right_child) -> None:
        super().__init__(left_child, right_child)

    def execute(self, context):
        left = self.left_child.execute(context)
        right = self.right_child.execute(context)
        return left / right

    def check_semantics(self, context):
        if not super().check_semantics(context):
            return False

        if (
            self.left_child.type == self.right_child.type
            and self.left_child.type == "number"
        ):
            self.type = "number"
            return True
        return False


class UnaryExpression(Node):
    def __init__(self, child) -> None:
        self.child = child

    def check_semantics(self, context):
        if self.child.check_semantics(context):
            return True


class Not(UnaryExpression):
    def __init__(self, child) -> None:
        super().__init__(child)

    def execute(self, context):
        return not self.child.execute(context)

    def check_semantics(self, context):
        if not super().check_semantics(context):
            return False

        if self.child.type == "bool":
            self.type = "bool"
            return True
        return False


class Call(Node):
    def __init__(self, id, arg_list) -> None:
        self.id = id
        self.arg_list = arg_list

    def execute(self, context):
        if context.id_is_built_in(self.id.value):
            fun = context.get_built_in_fun(self.id.value)
            return fun(context, self.arg_list)

        new_context = context.get_child()
        fun = context.get_fun(self.id.value)
        fun_param = context.get_fun_param(self.id.value)
        for i, arg in enumerate(self.arg_list):
            val = arg.execute(context)
            new_context.define_var(fun_param[i].id, arg.type, val)
        try:
            fun.body.execute(new_context)
        except ReturnException as r:
            return r.value
        return None

    def check_semantics(self, context):
        if context.is_built_in(self.id.value):
            self.type = context.get_built_in_fun_type(self.id.value)
            for arg in self.arg_list:
                if not arg.check_semantics(context):
                    return False
            return True
        if not context.exist_id(self.id.value):
            return False
        for arg in self.arg_list:
            if not arg.check_semantics(context):
                return False
        self.type = context.get_id_type(self.id.value)[4:]
        return True
