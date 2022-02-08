from typing import List, Dict
from parser.token_ import Token, TokenMatch, TokenType
from .regex import convert_str_in_regex, convert_regex_in_automata
from .automata import (
    Automata,
    FiniteState,
    State,
    Transition,
    SYMBOL_TABLE,
    TransitionFunction,
    convert_NFA_in_DFA,
)
from .lexer import Lexer

matches = [
    # Program
    TokenMatch("Program", TokenType.PROGRAM),
    TokenMatch("{", TokenType.LEFT_KEY),
    TokenMatch("}", TokenType.RIGHT_KEY),
    # VarDeclaration
    TokenMatch("var", TokenType.VAR),
    TokenMatch("fun", TokenType.FUN),
    TokenMatch("=", TokenType.EQUAL),
    # Assigment
    TokenMatch("redefine", TokenType.REDEFINE),
    TokenMatch("AgentPredicate", TokenType.AGENT_PREDICATE),
    TokenMatch("EmptyPredicate", TokenType.EMPTY_PREDICATE),
    # Stmt
    TokenMatch(";", TokenType.DOT_COMA),
    TokenMatch(",", TokenType.COMA),
    # IfStmt
    TokenMatch("return", TokenType.RETURN),
    TokenMatch("if", TokenType.IF),
    TokenMatch("while", TokenType.WHILE),
    TokenMatch("else", TokenType.ELSE),
    # PrintStmt
    TokenMatch("print", TokenType.PRINT),
    # LogicOr
    TokenMatch("or", TokenType.OR),
    # LogicAnd
    TokenMatch("and", TokenType.AND),
    # Equality
    TokenMatch("!=", TokenType.NOT_EQUAL),
    TokenMatch("==", TokenType.EQUAL_EQUAL),
    # Comparison
    TokenMatch(">", TokenType.GREATER),
    TokenMatch(">=", TokenType.GREATER_EQUAL),
    TokenMatch("<", TokenType.LESS),
    TokenMatch("<=", TokenType.LESS_EQUAL),
    # Term
    TokenMatch("-", TokenType.MINUS),
    TokenMatch("+", TokenType.PLUS),
    # Factor
    TokenMatch("/", TokenType.SLASH),
    TokenMatch("\*", TokenType.STAR),
    # Unary
    TokenMatch("!", TokenType.NOT),
    # Primary
    TokenMatch("False", TokenType.FALSE),
    TokenMatch("Nil", TokenType.NIL),
    TokenMatch("True", TokenType.TRUE),
    TokenMatch("\(", TokenType.LEFT_PAREN),
    TokenMatch("\)", TokenType.RIGHT_PAREN),
    # Falta rellenar el string
    TokenMatch(
        '"(_| |a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z|A|B|C|D|E|F|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z|0|1|2|3|4|5|6|7|8|9)*"',
        TokenType.STRING,
    ),
    TokenMatch(
        "(1|2|3|4|5|6|7|8|9)(0|1|2|3|4|5|6|7|8|9)*|0",
        TokenType.NUMBER,
    ),
    TokenMatch(
        "(_|a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z)(_|a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z|0|1|2|3|4|5|6|7|8|9)*",
        TokenType.ID,
    ),
]


def create_NFA_for_matches() -> List[Automata]:
    automatas = []

    for match in matches:
        automatas.append(
            convert_regex_in_automata(convert_str_in_regex(match.get_lexeme()))
        )

    return automatas


def tag_automatas_final_state(
    finite_automata, automata_list: List[Automata]
) -> Dict[State, TokenType]:
    d = {}

    for final_state in finite_automata._final_states:
        for i, aut in enumerate(automata_list):
            if aut._final_states[0] in final_state._states_represented:
                d[final_state] = matches[i].get_token_type()
                break

    return d


def get_patern_matched(
    fnl_states_patterns: Dict[State, TokenType], sequence_states: List[FiniteState]
):

    for i in range(len(sequence_states) - 1, -1, -1):
        if sequence_states[i]._is_final:
            return fnl_states_patterns.get(sequence_states[i]), i

    return None, -1


def join_automatas(automata_list: List[Automata]) -> Automata:
    new_start_state = State()

    states = [new_start_state]
    initials_states = []
    finals_states = []
    new_transitions = []
    for automata in automata_list:
        states.extend(automata._states)
        initials_states.append(automata._initial_state)
        finals_states.append(automata._final_states[0])
        new_transitions.extend(automata._transition_function.transitions)
        new_transitions.append(
            Transition(new_start_state, "eps", automata._initial_state)
        )

    return Automata(
        states,
        new_start_state,
        SYMBOL_TABLE,
        finals_states,
        TransitionFunction(new_transitions),
    )


def tokenize(program: str):
    tokens = []

    automatas_pattern = create_NFA_for_matches()
    big_automata = convert_NFA_in_DFA(join_automatas(automatas_pattern))

    tags = tag_automatas_final_state(big_automata, automatas_pattern)

    lex = Lexer(program)

    lexeme = []
    while lex.move_next():
        char = lex.current
        lexeme.append(char)
        if (char == " " or char == "\n") and len(lexeme) == 1:
            lexeme = []
            continue
        if not big_automata.match_one_char(char) or lex.is_end():
            token_type, pos = get_patern_matched(tags, big_automata.sequence_states)
            if not token_type:
                print("Error")
                break
            lexeme = lexeme[:pos]
            lex.move_back(len(big_automata.sequence_states) - pos - 1)
            l, c = lex.get_line_column
            tokens.append(Token(token_type, "".join(lexeme), l, c - pos))
            lexeme = []
            big_automata.reset()

    #

    return tokens
