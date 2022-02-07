class CSTNode:
    pass


class NoTerminalNode(CSTNode):
    def __init__(self) -> None:
        self.ast = None
        self.l_attribute = None
        self.production = None
        self.childs = []

    def set_production(self, production):
        self.production = production

    def set_childs(self, childs):
        self.childs = childs

    def get_ast(self):
        ast = self.production.action(self)
        return ast


class TerminalNode(CSTNode):
    def __init__(self) -> None:
        self.lexeme = None

    def set_lexeme(self, lexeme):
        self.lexeme = lexeme
