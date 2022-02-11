from typing import Dict, Tuple, List
from .cst import NoTerminalNode, TerminalNode
from .grammar import (
    ContextFreeGrammar,
    NoTerminal,
    Production,
    Symbol,
    Terminal,
    SentenceForm,
)
from .token_ import TokenType, Token


def build_parse_table(
    g: ContextFreeGrammar,
) -> Dict[Tuple[NoTerminal, TokenType], Production]:
    parse_table = {}
    eps = Terminal("eps", TokenType.EPS)

    for prod in g.productions.items:
        for production in prod[1]:
            for a in g.first(production.body):
                if a.__eq__(eps):
                    for b in g.follow(prod[0]):
                        parse_table[(prod[0], b.token_type)] = production
                else:
                    parse_table[(prod[0], a.token_type)] = production

    return parse_table


def eq_symbol_token(symbol: Symbol, token: Token) -> bool:
    if symbol.is_terminal and symbol.token_type == token.token_type:
        return True
    return False


def LL_parse(
    tokens_string: List[Token],
    parse_table: Dict[Tuple[NoTerminal, TokenType], Production],
    g: ContextFreeGrammar,
):
    tokens_string.append(Token(TokenType.ENDMARK, "$", -1, -1))
    parse_stack = [g.start_symbol]
    root_tree = NoTerminalNode()
    concret_syntax_tree = [root_tree]
    leaf_tree = []
    eps = Terminal("eps", TokenType.EPS)

    token_index = 0

    while len(parse_stack) > 0:
        A = parse_stack[0]
        a = tokens_string[token_index]
        if A.is_terminal:
            if A.token_type == a.token_type:
                terminal_node = leaf_tree.pop(0)
                terminal_node.lexeme = a._lexeme
                parse_stack.pop(0)
                token_index = token_index + 1
            else:
                return None
        else:
            prod = parse_table.get((A, a.token_type))
            if prod == None:
                return None

            no_terminal_node = concret_syntax_tree.pop(0)
            no_terminal_node.set_production(prod)

            child_nodes = []

            parse_stack.pop(0)
            symbols = prod.body.symbols
            if prod.body.symbols_len == 1 and eps in symbols:

                continue
            for i in range(prod.body.symbols_len - 1, -1, -1):
                parse_stack.insert(0, symbols[i])
                child = None
                if symbols[i].is_terminal:
                    child = TerminalNode()
                    leaf_tree.insert(0, child)
                else:
                    child = NoTerminalNode()
                    concret_syntax_tree.insert(0, child)
                child_nodes.insert(0, child)

            no_terminal_node.set_childs(child_nodes)

    return root_tree
