from typing import Iterable, List, Set, Optional

from token_ import TokenType


class Symbol:
    def __init__(self, symbol) -> None:
        self._symbol = symbol
        self._is_terminal = False

    def __str__(self) -> str:
        return f"Symbol -> {self.symbol}"

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, __o: object) -> bool:
        return self.symbol == __o.symbol

    def __hash__(self) -> int:
        return hash(self._symbol)

    @property
    def symbol(self):
        return self._symbol

    @property
    def is_terminal(self):
        return self._is_terminal


class Terminal(Symbol):
    def __init__(self, symbol, token_type) -> None:
        super().__init__(symbol)
        self._is_terminal = True
        self._token_type = token_type

    def __str__(self) -> str:
        return f"Terminal -> {self.symbol}, TokenType -> {self.token_type}"

    def __repr__(self) -> str:
        return self.__str__()

    def __hash__(self) -> int:
        return super().__hash__()

    def __eq__(self, __o: object) -> bool:
        return super().__eq__(__o) and self.token_type == __o.token_type

    @property
    def token_type(self):
        return self._token_type


class NoTerminal(Symbol):
    def __init__(self, symbol) -> None:
        super().__init__(symbol)
        self.ast = None
        self.l_attribute = None

    def __str__(self) -> str:
        return f"NoTerminal -> {self.symbol}"

    def __repr__(self) -> str:
        return self.__str__()

    def __hash__(self) -> int:
        return super().__hash__()


class SentenceForm:
    def __init__(self, symbols: List[Symbol]) -> None:
        self._symbols: List[Symbol] = symbols
        self._symbols_len: int = len(symbols)

    def __str__(self) -> str:
        symb = []
        for s in self.symbols:
            symb.append(s.__str__())
        return "Sentence Form " + " ".join(symb)

    def __repr__(self) -> str:
        return self.__str__()

    @property
    def symbols_len(self) -> int:
        return self._symbols_len

    @property
    def symbols(self) -> List[Symbol]:
        return self._symbols

    def contain(self, symbol: Symbol) -> bool:
        for s in self.symbols:
            if s.__eq__(symbol):
                return True
        return False


class Production:
    def __init__(self, head: NoTerminal, body: SentenceForm, action) -> None:
        self._head = head
        self._body = body
        self._action = action

    def __str__(self) -> str:
        return f"{self._head} -> {self._body}"

    def __repr__(self) -> str:
        return self.__str__()

    @property
    def head(self):
        return self._head

    @property
    def body(self):
        return self._body

    @property
    def action(self):
        return self._action


class ContextFreeProductionDict:
    def __init__(self, productions) -> None:
        self._productions = productions

    def get_production_of(self, A: NoTerminal) -> Optional[List[Production]]:
        if self._productions.get(A):
            return self._productions[A]
        return None

    @property
    def items(self):
        return self._productions.items()

    @property
    def heads(self) -> Iterable[NoTerminal]:
        return self._productions.keys()

    @property
    def bodys(self) -> Iterable[Production]:
        return self._productions.values()


class ContextFreeGrammar:
    def __init__(
        self,
        start_symbol: NoTerminal,
        no_terminals: List[NoTerminal],
        terminals: List[Terminal],
        productions: ContextFreeProductionDict,
    ) -> None:
        self._start_symbol: NoTerminal = start_symbol
        self._no_terminals: List[NoTerminal] = no_terminals
        self._terminals: List[Terminal] = terminals
        self._productions: ContextFreeProductionDict = productions

    @property
    def start_symbol(self) -> NoTerminal:
        return self._start_symbol

    @property
    def no_terminals(self) -> List[NoTerminal]:
        return self._no_terminals

    @property
    def terminals(self) -> List[Terminal]:
        return self._terminals

    @property
    def productions(self) -> ContextFreeProductionDict:
        return self._productions

    def first(self, alpha: SentenceForm) -> Set[Terminal]:
        super_set = set([])
        eps = Terminal("eps", TokenType.EPS)

        for symbol in alpha.symbols:
            new_set = self.first_aux(symbol)
            if eps not in new_set:
                super_set = super_set.union(new_set)
                break
            new_set.remove(eps)
            super_set = super_set.union(new_set)
        else:
            super_set.add(eps)

        return super_set

    def first_aux(self, X: Symbol) -> Set[Terminal]:
        super_set = set([])

        if X.is_terminal:
            super_set.add(X)
            return super_set

        productions_of_X = self.productions.get_production_of(X)
        for production in productions_of_X:
            super_set = super_set.union(self.first(production.body))

        return super_set

    def follow(self, A: NoTerminal) -> Set[Terminal]:
        super_set = set([])
        eps = Terminal("eps", TokenType.EPS)

        if A.__eq__(self.start_symbol):
            super_set.add(Terminal("$", TokenType.ENDMARK))

        for item in self.productions.items:
            for production in item[1]:
                for i, s in enumerate(production.body.symbols):
                    if s.__eq__(A):
                        if i == production.body.symbols_len - 1:
                            if not item[0].__eq__(A):
                                super_set = super_set.union(self.follow(item[0]))
                        else:
                            first_B = self.first(
                                SentenceForm(production.body.symbols[i + 1 :])
                            )

                            if eps in first_B:
                                first_B.remove(eps)
                                super_set = super_set.union(first_B)
                                if not item[0].__eq__(A):
                                    super_set = super_set.union(self.follow(item[0]))
                            else:
                                super_set = super_set.union(first_B)

        return super_set
