from enum import Enum, auto


class TokenType(Enum):
    # Program
    LEFT_KEY = auto()
    RIGHT_KEY = auto()

    # VarDeclaration
    FUN = auto()
    EQUAL = auto()

    # Stmt
    DOT_COMA = auto()
    COMA = auto()

    # IfStmt
    RETURN = auto()
    IF = auto()
    WHILE = auto()
    ELSE = auto()

    # LogicOr LogicAnd
    OR = auto()
    AND = auto()

    # Equality
    NOT_EQUAL = auto()
    EQUAL_EQUAL = auto()

    # Comparison
    GREATER = auto()
    GREATER_EQUAL = auto()
    LESS = auto()
    LESS_EQUAL = auto()

    # Term
    PLUS = auto()
    MINUS = auto()

    # Factor
    STAR = auto()
    SLASH = auto()

    # Unary
    NOT = auto()

    # Primary
    MASTER_SIMULATOR = auto()
    LIST = auto()
    AGENT = auto()
    SIMULATOR = auto()
    NUMBERTYPE = auto()
    STRINGTYPE = auto()
    ID = auto()
    NUMBER = auto()
    STRING = auto()
    BOOL = auto()
    TRUE = auto()
    FALSE = auto()
    LEFT_PAREN = auto()
    RIGHT_PAREN = auto()
    NIL = auto()

    # Eps
    EPS = auto()
    # Endmarker
    ENDMARK = auto()


class Token:
    def __init__(
        self, token_type: TokenType, lexeme: str, line: int, column: int
    ) -> None:
        self._token_type: TokenType = token_type
        self._lexeme: str = lexeme
        self._line: int = line
        self._column: int = column

    def __str__(self) -> str:
        return f"Token(token_type: {self._token_type}, lexeme: {self._lexeme}, line: {self._line}, column: {self._column})"

    def __repr__(self) -> str:
        return self.__str__()

    @property
    def token_type(self):
        return self._token_type


class TokenMatch:
    def __init__(self, lexeme: str, token_type: TokenType) -> None:
        self._lexeme = lexeme
        self._token_type: TokenType = token_type

    def get_token_type(self) -> TokenType:
        return self._token_type

    def get_lexeme(self) -> str:
        return self._lexeme
