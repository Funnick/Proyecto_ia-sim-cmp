from abc import ABC, abstractmethod
from typing import List
from .automata import *


class Regex(ABC):
    @abstractmethod
    def create_automata(self, stack):
        pass


class RegexSymbol(Regex):
    def __init__(self, symbol: str) -> None:
        self._symbol: str = symbol

    def create_automata(self, stack) -> Automata:
        start_state = State()
        final_state = State()

        return Automata(
            [start_state, final_state],
            start_state,
            SYMBOL_TABLE,
            [final_state],
            TransitionFunction([Transition(start_state, self._symbol, final_state)]),
        )


class RegexOr(Regex):
    def create_automata(self, stack) -> Automata:
        rigth = stack.pop()
        rigth = rigth.create_automata(stack)
        left = stack.pop()
        left = left.create_automata(stack)

        return automata_union(left, rigth)


class RegexConcat(Regex):
    def create_automata(self, stack) -> Automata:
        rigth = stack.pop()
        rigth = rigth.create_automata(stack)
        left = stack.pop()
        left = left.create_automata(stack)

        return automata_concat(left, rigth)


class RegexClosure(Regex):
    def create_automata(self, stack) -> Automata:
        left = stack.pop()
        left = left.create_automata(stack)

        return automata_closure(left)


def fix_op_stack(stack, op_stack, item, lexema_item) -> None:
    if item == ")":
        ind = len(op_stack) - 1
        while op_stack[ind] != "(":
            stack.append(op_stack.pop())
            ind = ind - 1
        op_stack.pop()
    elif lexema_item == "cc":
        op_stack.append(item)
    else:
        if len(op_stack) > 0:
            ind = len(op_stack) - 1
            while ind >= 0 and isinstance(op_stack[ind], RegexConcat):
                stack.append(op_stack.pop())
                ind = ind - 1
        op_stack.append(item)


def convert_str_in_regex(string: str) -> List[Regex]:
    stack = []
    op_stack = []

    can_came_a_cc = False
    special = False

    for c in string:
        if c == "\\":
            special = True
        elif c == "(" and not special:
            if can_came_a_cc:
                fix_op_stack(stack, op_stack, RegexConcat(), "cc")
            op_stack.append("(")
            can_came_a_cc = False
        elif c == ")" and not special:
            fix_op_stack(stack, op_stack, ")", ")")
            can_came_a_cc = True
        elif c == "|" and not special:
            fix_op_stack(stack, op_stack, RegexOr(), "|")
            can_came_a_cc = False
        elif c == "*" and not special:
            stack.append(RegexClosure())
            can_came_a_cc = True
        else:
            special = False
            if can_came_a_cc:
                stack.append(RegexSymbol(c))
                fix_op_stack(stack, op_stack, RegexConcat(), "cc")
            else:
                stack.append(RegexSymbol(c))
                can_came_a_cc = True

    for i in range(len(op_stack)):
        stack.append(op_stack.pop())

    return stack


def convert_regex_in_automata(list_regex: List[Regex]) -> Automata:
    start = list_regex.pop()
    return start.create_automata(list_regex)
