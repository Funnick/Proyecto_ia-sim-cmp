from .grammar import (
    Terminal,
    NoTerminal,
    ContextFreeProductionDict,
    ContextFreeGrammar,
    SentenceForm,
    Production,
)
from .token_ import TokenType
from .production_actions import *


# Start Symbol
program = NoTerminal("program")
# No Terminals
block_dec = NoTerminal("block_dec")
block_dec_ = NoTerminal("block_dec_")
fun_declaration = NoTerminal("fun_declaration")
var_declaration = NoTerminal("var_declaration")
var_declaration_ = NoTerminal("var_declaration_")
stmt = NoTerminal("stmt")
type_ = NoTerminal("type_")
param_list = NoTerminal("param_list")
param_list_ = NoTerminal("param_list_")
if_stmt = NoTerminal("if_stmt")
else_stmt = NoTerminal("else_stmt")
while_stmt = NoTerminal("while_stmt")
return_stmt = NoTerminal("return_stmt")
return_value = NoTerminal("return_value")
assignment = NoTerminal("assignment")
assignment_ = NoTerminal("assignment_")
expression = NoTerminal("expression")
logic_or = NoTerminal("logic_or")
logic_or_ = NoTerminal("logic_or_")
logic_and = NoTerminal("logic_and")
logic_and_ = NoTerminal("logic_and_")
equality = NoTerminal("equality")
equality_ = NoTerminal("equality_")
cmp = NoTerminal("cmp")
cmp_ = NoTerminal("cmp_")
term = NoTerminal("term")
term_ = NoTerminal("term_")
factor = NoTerminal("factor")
factor_ = NoTerminal("factor_")
unary = NoTerminal("unary")
primary = NoTerminal("primary")
call_ = NoTerminal("call")
call__ = NoTerminal("call_")
arg_list = NoTerminal("arg_list")
arg_list_ = NoTerminal("arg_list_")
# NoTerminalsList
no_terminals_list = [
    program,
    block_dec,
    block_dec_,
    fun_declaration,
    var_declaration,
    var_declaration_,
    stmt,
    type_,
    param_list,
    param_list_,
    return_stmt,
    return_value,
    if_stmt,
    while_stmt,
    else_stmt,
    expression,
    assignment,
    assignment_,
    logic_or,
    logic_or_,
    logic_and,
    logic_and_,
    equality,
    equality_,
    cmp,
    cmp_,
    term,
    term_,
    factor,
    factor_,
    unary,
    primary,
    call_,
    call__,
    arg_list,
    arg_list_,
]
# Terminals
left_key = Terminal("{", TokenType.LEFT_KEY)
right_key = Terminal("}", TokenType.RIGHT_KEY)
eps = Terminal("eps", TokenType.EPS)
fun = Terminal("fun", TokenType.FUN)
return_terminal = Terminal("return", TokenType.RETURN)
if_terminal = Terminal("if", TokenType.IF)
while_terminal = Terminal("while", TokenType.WHILE)
else_terminal = Terminal("else", TokenType.ELSE)
equal = Terminal("=", TokenType.EQUAL)
dot_coma = Terminal(";", TokenType.DOT_COMA)
coma = Terminal(",", TokenType.COMA)
or_terminal = Terminal("or", TokenType.OR)
and_terminal = Terminal("and", TokenType.AND)
not_equal = Terminal("!=", TokenType.NOT_EQUAL)
equal_equal = Terminal("==", TokenType.EQUAL_EQUAL)
greater = Terminal(">", TokenType.GREATER)
greater_equal = Terminal(">=", TokenType.GREATER_EQUAL)
less = Terminal("<", TokenType.LESS)
less_equal = Terminal("<=", TokenType.LESS_EQUAL)
plus = Terminal("+", TokenType.PLUS)
sub = Terminal("-", TokenType.MINUS)
star = Terminal("*", TokenType.STAR)
div = Terminal("/", TokenType.SLASH)
not_terminal = Terminal("not", TokenType.NOT)
id_terminal = Terminal("id", TokenType.ID)
list_terminal = Terminal("list", TokenType.LIST)
agent = Terminal("agent", TokenType.AGENT)
simulator = Terminal("simulator", TokenType.SIMULATOR)
master_simulator = Terminal("master_simulator", TokenType.MASTER_SIMULATOR)
type_number_terminal = Terminal("type_number", TokenType.NUMBERTYPE)
type_string_terminal = Terminal("type_string", TokenType.STRINGTYPE)
number_terminal = Terminal("number", TokenType.NUMBER)
string_terminal = Terminal("str", TokenType.STRING)
bool_terminal = Terminal("bool", TokenType.BOOL)
true_terminal = Terminal("True", TokenType.TRUE)
false_terminal = Terminal("False", TokenType.FALSE)
nil = Terminal("Nil", TokenType.NIL)
left_paren = Terminal("(", TokenType.LEFT_PAREN)
right_paren = Terminal(")", TokenType.RIGHT_PAREN)
# Terminals List
terminals_list = [
    left_key,
    right_key,
    fun,
    equal,
    eps,
    return_terminal,
    if_terminal,
    while_terminal,
    else_terminal,
    dot_coma,
    coma,
    or_terminal,
    and_terminal,
    not_equal,
    equal_equal,
    greater,
    greater_equal,
    less,
    less_equal,
    plus,
    sub,
    star,
    div,
    not_terminal,
    simulator,
    master_simulator,
    agent,
    list_terminal,
    number_terminal,
    type_number_terminal,
    bool_terminal,
    string_terminal,
    type_string_terminal,
    true_terminal,
    false_terminal,
    nil,
    left_paren,
    right_paren,
]
program_productions = [
    Production(
        program,
        SentenceForm([block_dec]),
        action_1,
    )
]
block_dec_productions = [
    Production(
        block_dec,
        SentenceForm([fun_declaration, block_dec_]),
        action_2,
    ),
    Production(
        block_dec,
        SentenceForm([var_declaration, block_dec_]),
        action_2,
    ),
    Production(
        block_dec,
        SentenceForm([stmt, block_dec_]),
        action_2,
    ),
    Production(
        block_dec,
        SentenceForm([eps]),
        action_3,
    ),
]
block_dec__productions = [
    Production(
        block_dec_,
        SentenceForm([fun_declaration, block_dec_]),
        action_4,
    ),
    Production(
        block_dec_,
        SentenceForm([var_declaration, block_dec_]),
        action_4,
    ),
    Production(
        block_dec_,
        SentenceForm([stmt, block_dec_]),
        action_4,
    ),
    Production(
        block_dec_,
        SentenceForm([eps]),
        action_5,
    ),
]
fun_declaration_productions = [
    Production(
        fun_declaration,
        SentenceForm(
            [
                fun,
                type_,
                id_terminal,
                left_paren,
                param_list,
                right_paren,
                left_key,
                block_dec,
                right_key,
            ]
        ),
        action_6,
    ),
]
var_declaration_productions = [
    Production(
        var_declaration,
        SentenceForm([type_, id_terminal, equal, var_declaration_, dot_coma]),
        action_7,
    ),
]
type__productions = [
    Production(
        type_,
        SentenceForm([type_number_terminal]),
        action_8,
    ),
    Production(
        type_,
        SentenceForm([type_string_terminal]),
        action_9,
    ),
    Production(
        type_,
        SentenceForm([nil]),
        action_10,
    ),
    Production(
        type_,
        SentenceForm([bool_terminal]),
        action_11,
    ),
    Production(
        type_,
        SentenceForm([simulator]),
        action_48,
    ),
    Production(
        type_,
        SentenceForm([agent]),
        action_48,
    ),
    Production(
        type_,
        SentenceForm([list_terminal]),
        action_48,
    ),
    Production(
        type_,
        SentenceForm([master_simulator]),
        action_48,
    ),
]
var_declaration__productions = [
    Production(
        var_declaration_,
        SentenceForm([expression]),
        action_12,
    ),
    Production(
        var_declaration_,
        SentenceForm([eps]),
        action_13,
    ),
]
param_list_productions = [
    Production(
        param_list,
        SentenceForm([type_, id_terminal, param_list_]),
        action_14,
    ),
    Production(
        param_list,
        SentenceForm([eps]),
        action_15,
    ),
]
param_list__productions = [
    Production(
        param_list_,
        SentenceForm([coma, type_, id_terminal, param_list_]),
        action_16,
    ),
    Production(
        param_list_,
        SentenceForm([eps]),
        action_5,
    ),
]
stmt_productions = [
    Production(
        stmt,
        SentenceForm([if_stmt]),
        action_1,
    ),
    Production(
        stmt,
        SentenceForm([while_stmt]),
        action_1,
    ),
    Production(
        stmt,
        SentenceForm([return_stmt]),
        action_1,
    ),
    Production(
        stmt,
        SentenceForm([assignment]),
        action_1,
    ),
]
if_stmt_productions = [
    Production(
        if_stmt,
        SentenceForm(
            [
                if_terminal,
                left_paren,
                expression,
                right_paren,
                left_key,
                block_dec,
                right_key,
                else_stmt,
            ]
        ),
        action_17,
    ),
]
else_stmt_productions = [
    Production(
        else_stmt,
        SentenceForm([else_terminal, left_key, block_dec, right_key]),
        action_18,
    ),
    Production(
        else_stmt,
        SentenceForm([eps]),
        action_19,
    ),
]
while_stmt_productions = [
    Production(
        while_stmt,
        SentenceForm(
            [
                while_terminal,
                left_paren,
                expression,
                right_paren,
                left_key,
                block_dec,
                right_key,
            ]
        ),
        action_20,
    ),
]
return_stmt_productions = [
    Production(
        return_stmt, SentenceForm([return_terminal, return_value, dot_coma]), action_21
    )
]
return_value_productions = [
    Production(return_value, SentenceForm([expression]), action_1),
    Production(return_value, SentenceForm([eps]), action_13),
]
assignment_productions = [
    Production(
        assignment, SentenceForm([id_terminal, assignment_, dot_coma]), action_22
    ),
]
assignment__productions = [
    Production(assignment_, SentenceForm([equal, expression]), action_46),
    Production(
        assignment_, SentenceForm([left_paren, arg_list, right_paren]), action_47
    ),
]
expression_productions = [Production(expression, SentenceForm([logic_or]), action_1)]
logic_or_productions = [
    Production(logic_or, SentenceForm([logic_and, logic_or_]), action_23)
]
logic_or__productions = [
    Production(logic_or_, SentenceForm([or_terminal, logic_and, logic_or_]), action_24),
    Production(logic_or_, SentenceForm([eps]), action_5),
]
logic_and_productions = [
    Production(logic_and, SentenceForm([equality, logic_and_]), action_23)
]
logic_and__productions = [
    Production(
        logic_and_, SentenceForm([and_terminal, equality, logic_and_]), action_25
    ),
    Production(logic_and_, SentenceForm([eps]), action_5),
]
equality_productions = [
    Production(equality, SentenceForm([cmp, equality_]), action_23),
]
equality__productions = [
    Production(equality_, SentenceForm([equal_equal, cmp]), action_26),
    Production(equality_, SentenceForm([not_equal, cmp]), action_27),
    Production(equality_, SentenceForm([eps]), action_5),
]
cmp_productions = [Production(cmp, SentenceForm([term, cmp_]), action_23)]
cmp__productions = [
    Production(cmp_, SentenceForm([greater, term]), action_28),
    Production(cmp_, SentenceForm([greater_equal, term]), action_29),
    Production(cmp_, SentenceForm([less, term]), action_30),
    Production(cmp_, SentenceForm([less_equal, term]), action_31),
    Production(cmp_, SentenceForm([eps]), action_5),
]
term_productions = [
    Production(term, SentenceForm([factor, term_]), action_23),
]
term__productions = [
    Production(term_, SentenceForm([plus, factor, term_]), action_32),
    Production(term_, SentenceForm([sub, factor, term_]), action_33),
    Production(term_, SentenceForm([eps]), action_5),
]
factor_productions = [
    Production(factor, SentenceForm([unary, factor_]), action_23),
]
factor__productions = [
    Production(factor_, SentenceForm([star, unary, factor_]), action_34),
    Production(factor_, SentenceForm([div, unary, factor_]), action_35),
    Production(factor_, SentenceForm([eps]), action_5),
]
unary_productions = [
    Production(unary, SentenceForm([not_terminal, unary]), action_36),
    Production(unary, SentenceForm([call_]), action_1),
]
call__productions = [Production(call_, SentenceForm([primary, call__]), action_23)]
call___productions = [
    Production(call__, SentenceForm([left_paren, arg_list, right_paren]), action_37),
    Production(call__, SentenceForm([eps]), action_5),
]
arg_list_productions = [
    Production(arg_list, SentenceForm([expression, arg_list_]), action_38),
    Production(arg_list, SentenceForm([eps]), action_39),
]
arg_list__productions = [
    Production(arg_list_, SentenceForm([coma, expression, arg_list_]), action_40),
    Production(arg_list_, SentenceForm([eps]), action_5),
]
primary_productions = [
    Production(primary, SentenceForm([true_terminal]), action_41),
    Production(primary, SentenceForm([false_terminal]), action_41),
    Production(primary, SentenceForm([nil]), action_42),
    Production(primary, SentenceForm([number_terminal]), action_43),
    Production(primary, SentenceForm([string_terminal]), action_44),
    Production(primary, SentenceForm([id_terminal]), action_45),
]
# Productions_dict
productions_dict = {
    program: program_productions,
    block_dec: block_dec_productions,
    block_dec_: block_dec__productions,
    fun_declaration: fun_declaration_productions,
    type_: type__productions,
    arg_list: arg_list_productions,
    arg_list_: arg_list__productions,
    var_declaration: var_declaration_productions,
    var_declaration_: var_declaration__productions,
    stmt: stmt_productions,
    return_stmt: return_stmt_productions,
    return_value: return_value_productions,
    if_stmt: if_stmt_productions,
    while_stmt: while_stmt_productions,
    else_stmt: else_stmt_productions,
    expression: expression_productions,
    assignment: assignment_productions,
    assignment_: assignment__productions,
    logic_or: logic_or_productions,
    logic_or_: logic_or__productions,
    logic_and: logic_and_productions,
    logic_and_: logic_and__productions,
    equality: equality_productions,
    equality_: equality__productions,
    cmp: cmp_productions,
    cmp_: cmp__productions,
    term: term_productions,
    term_: term__productions,
    factor: factor_productions,
    factor_: factor__productions,
    unary: unary_productions,
    primary: primary_productions,
    call_: call__productions,
    call__: call___productions,
    param_list: param_list_productions,
    param_list_: param_list__productions,
}
gr = ContextFreeGrammar(
    program,
    no_terminals_list,
    terminals_list,
    ContextFreeProductionDict(productions_dict),
)
