from lib2to3.pgen2.grammar import Grammar
from unittest.mock import sentinel
from grammar import (
    Terminal,
    NoTerminal,
    ContextFreeProductionDict,
    ContextFreeGrammar,
    SentenceForm,
    Production,
)
from token_ import TokenType
from production_actions import *

# Start Symbol
program = NoTerminal("program")
# No Terminals
block_stmt = NoTerminal("block_stmt")
block_stmt_ = NoTerminal("block_stmt_")
declaration = NoTerminal("declaration")
fun_declaration = NoTerminal("fun_declaration")
function = NoTerminal("function")
arg_list = NoTerminal("arg_list")
arg_list_ = NoTerminal("arg_list_")
var_declaration = NoTerminal("var_declaration")
var_declaration_ = NoTerminal("var_declaration_")
stmt = NoTerminal("stmt")
return_stmt = NoTerminal("return_stmt")
return_value = NoTerminal("return_value")
if_stmt = NoTerminal("if_stmt")
while_stmt = NoTerminal("while_stmt")
else_stmt = NoTerminal("else_stmt")
print_stmt = NoTerminal("print_stmt")
expression_stmt = NoTerminal("expression_stmt")
expression = NoTerminal("expression")
assigment = NoTerminal("assigment")
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
call = NoTerminal("call")
arg_exps = NoTerminal("arg_exps")
arg_exps_ = NoTerminal("arg_exps_")
predicate = NoTerminal("predicate")
expr_pred = NoTerminal("expr_pred")
no_terminals_list = [
    program,
    block_stmt,
    block_stmt_,
    declaration,
    fun_declaration,
    function,
    arg_list,
    arg_list_,
    var_declaration,
    var_declaration_,
    stmt,
    return_stmt,
    return_value,
    if_stmt,
    while_stmt,
    else_stmt,
    print_stmt,
    expression_stmt,
    expression,
    assigment,
    logic_or,
    logic_and,
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
    call,
    arg_exps,
    arg_exps_,
    predicate,
]
# Terminals
program_terminal = Terminal("Program", TokenType.PROGRAM)
left_key = Terminal("{", TokenType.LEFT_KEY)
right_key = Terminal("}", TokenType.RIGHT_KEY)
eps = Terminal("eps", TokenType.EPS)
fun = Terminal("fun", TokenType.FUN)
var = Terminal("var", TokenType.VAR)
return_terminal = Terminal("return", TokenType.RETURN)
if_terminal = Terminal("if", TokenType.IF)
while_terminal = Terminal("while", TokenType.WHILE)
else_terminal = Terminal("else", TokenType.ELSE)
redefine = Terminal("redefine", TokenType.REDEFINE)
equal = Terminal("=", TokenType.EQUAL)
print_terminal = Terminal("print", TokenType.PRINT)
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
not_terminal = Terminal("!", TokenType.NOT)
id_terminal = Terminal("id", TokenType.ID)
number_terminal = Terminal("number", TokenType.NUMBER)
string_terminal = Terminal("str", TokenType.STRING)
true_terminal = Terminal("True", TokenType.TRUE)
false_terminal = Terminal("False", TokenType.FALSE)
nil = Terminal("nil", TokenType.NIL)
left_paren = Terminal("(", TokenType.LEFT_PAREN)
right_paren = Terminal(")", TokenType.RIGHT_PAREN)
agent_predicate = Terminal("AgentPredicate", TokenType.AGENT_PREDICATE)
empty_predicate = Terminal("EmptyPredicate", TokenType.EMPTY_PREDICATE)
terminals_list = [
    program_terminal,
    left_key,
    right_key,
    fun,
    var,
    equal,
    redefine,
    eps,
    return_terminal,
    if_terminal,
    while_terminal,
    else_terminal,
    print_terminal,
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
    number_terminal,
    string_terminal,
    true_terminal,
    false_terminal,
    nil,
    left_paren,
    right_paren,
    agent_predicate,
    empty_predicate,
]
# Productions
# program
program_productions = [
    Production(
        program,
        SentenceForm([program_terminal, left_key, block_stmt, right_key]),
        action_1,
    )
]
# block_stmt
block_stmt_productions = [
    Production(block_stmt, SentenceForm([declaration, block_stmt_]), action_2)
]
# block_stmt_
block_stmt__productions = [
    Production(block_stmt_, SentenceForm([declaration, block_stmt_]), action_3),
    Production(block_stmt_, SentenceForm([eps]), action_22),
]
# declaration
declaration_productions = [
    Production(declaration, SentenceForm([fun_declaration]), action_4),
    Production(declaration, SentenceForm([var_declaration]), action_4),
    Production(declaration, SentenceForm([stmt]), action_4),
]
# fun_declaration
fun_declaration_productions = [
    Production(fun_declaration, SentenceForm([fun, function]), action_38)
]
# function
function_productions = [
    Production(
        function,
        SentenceForm(
            [
                id_terminal,
                left_paren,
                arg_list,
                right_paren,
                left_key,
                block_stmt,
                right_key,
            ]
        ),
        action_39,
    )
]
# arg_list
arg_list_productions = [
    Production(arg_list, SentenceForm([id_terminal, arg_list_]), action_40),
    Production(arg_list, SentenceForm([eps]), action_41),
]
# arg_list'
arg_list__productions = [
    Production(arg_list_, SentenceForm([coma, id_terminal, arg_list_]), action_42),
    Production(arg_list_, SentenceForm([eps]), action_8),
]
# var_declaration
var_declaration_productions = [
    Production(
        var_declaration,
        SentenceForm([var, id_terminal, var_declaration_, dot_coma]),
        action_27,
    )
]
# var_declaration_
var_declaration__productions = [
    Production(var_declaration_, SentenceForm([equal, expression]), action_28),
    Production(var_declaration_, SentenceForm([eps]), action_29),
]
# stmt
stmt_productions = [
    Production(stmt, SentenceForm([expression_stmt]), action_4),
    Production(stmt, SentenceForm([print_stmt]), action_4),
    Production(stmt, SentenceForm([if_stmt]), action_4),
    Production(stmt, SentenceForm([return_stmt]), action_4),
    Production(stmt, SentenceForm([while_stmt]), action_4),
]
# return_stmt
return_stmt_productions = [
    Production(
        return_stmt, SentenceForm([return_terminal, return_value, dot_coma]), action_47
    )
]
# return_value
return_value_productions = [
    Production(return_value, SentenceForm([expression]), action_48),
    Production(return_value, SentenceForm([eps]), action_49),
]
# if_stmt
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
                block_stmt,
                right_key,
                else_stmt,
            ]
        ),
        action_32,
    ),
]
# else_stmt
else_stmt_productions = [
    Production(
        else_stmt,
        SentenceForm([else_terminal, left_key, block_stmt, right_key]),
        action_33,
    ),
    Production(else_stmt, SentenceForm([eps]), action_34),
]
# while_stmt
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
                block_stmt,
                right_key,
            ]
        ),
        action_37,
    )
]
# print_stmt
print_stmt_productions = [
    Production(
        print_stmt, SentenceForm([print_terminal, expression, dot_coma]), action_26
    )
]
# expression_stmt
expression_stmt_productions = [
    Production(expression_stmt, SentenceForm([expression, dot_coma]), action_4)
]
# expression
expression_productions = [Production(expression, SentenceForm([assigment]), action_4)]
# assigment
assigment_productions = [
    Production(
        assigment, SentenceForm([redefine, id_terminal, equal, logic_or]), action_31
    ),
    Production(assigment, SentenceForm([logic_or]), action_4),
]
# logic_or
logic_or_productions = [
    Production(logic_or, SentenceForm([logic_and, logic_or_]), action_5)
]
# logic_or_
logic_or__productions = [
    Production(logic_or_, SentenceForm([or_terminal, logic_and, logic_or_]), action_35),
    Production(logic_or_, SentenceForm([eps]), action_8),
]
# logic_and
logic_and_productions = [
    Production(logic_and, SentenceForm([equality, logic_and_]), action_5)
]
# logic_and_
logic_and__productions = [
    Production(
        logic_and_, SentenceForm([and_terminal, equality, logic_and_]), action_36
    ),
    Production(logic_and_, SentenceForm([eps]), action_8),
]
# equality
equality_productions = [Production(equality, SentenceForm([cmp, equality_]), action_5)]
# equality_
equality__productions = [
    Production(equality_, SentenceForm([not_equal, cmp]), action_6),
    Production(equality_, SentenceForm([equal_equal, cmp]), action_7),
    Production(equality_, SentenceForm([eps]), action_8),
]
# cmp
cmp_productions = [Production(cmp, SentenceForm([term, cmp_]), action_5)]
# cmp_
cmp__productions = [
    Production(cmp_, SentenceForm([greater, term]), action_9),
    Production(cmp_, SentenceForm([greater_equal, term]), action_10),
    Production(cmp_, SentenceForm([less, term]), action_11),
    Production(cmp_, SentenceForm([less_equal, term]), action_12),
    Production(cmp_, SentenceForm([eps]), action_8),
]
# term
term_productions = [Production(term, SentenceForm([factor, term_]), action_5)]
# term_
term__productions = [
    Production(term_, SentenceForm([plus, factor, term_]), action_13),
    Production(term_, SentenceForm([sub, factor, term_]), action_14),
    Production(term_, SentenceForm([eps]), action_8),
]
# factor
factor_productions = [Production(factor, SentenceForm([unary, factor_]), action_5)]
# factor_
factor__productions = [
    Production(factor_, SentenceForm([star, unary, factor_]), action_15),
    Production(factor_, SentenceForm([div, unary, factor_]), action_16),
    Production(factor_, SentenceForm([eps]), action_8),
]
# unary
unary_productions = [
    Production(unary, SentenceForm([sub, unary]), action_17),
    Production(unary, SentenceForm([not_terminal, unary]), action_23),
    Production(unary, SentenceForm([primary]), action_4),
]
# primary
primary_producitons = [
    Production(primary, SentenceForm([number_terminal]), action_18),
    Production(primary, SentenceForm([string_terminal]), action_19),
    Production(primary, SentenceForm([true_terminal]), action_24),
    Production(primary, SentenceForm([false_terminal]), action_24),
    Production(primary, SentenceForm([nil]), action_20),
    Production(primary, SentenceForm([left_paren, expression, right_paren]), action_21),
    Production(primary, SentenceForm([id_terminal, call]), action_30),
]
call_productions = [
    Production(call, SentenceForm([left_paren, arg_exps, right_paren]), action_43),
    Production(call, SentenceForm([eps]), action_46),
]
arg_exps_productions = [
    Production(arg_exps, SentenceForm([expr_pred, arg_exps_]), action_44),
    Production(arg_exps, SentenceForm([eps]), action_41),
]
arg_exps__productions = [
    Production(arg_exps_, SentenceForm([coma, expr_pred, arg_exps_]), action_45),
    Production(arg_exps_, SentenceForm([eps]), action_8),
]
expr_pred_productions = [
    Production(expr_pred, SentenceForm([expression]), action_50),
    Production(expr_pred, SentenceForm([predicate]), action_50),
]
predicate_productions = [
    Production(predicate, SentenceForm([agent_predicate, id_terminal]), action_51),
    Production(predicate, SentenceForm([empty_predicate, id_terminal]), action_51),
]
# context free productions
productions_dict = {
    program: program_productions,
    block_stmt: block_stmt_productions,
    block_stmt_: block_stmt__productions,
    declaration: declaration_productions,
    fun_declaration: fun_declaration_productions,
    function: function_productions,
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
    print_stmt: print_stmt_productions,
    expression_stmt: expression_stmt_productions,
    expression: expression_productions,
    assigment: assigment_productions,
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
    primary: primary_producitons,
    call: call_productions,
    arg_exps: arg_exps_productions,
    arg_exps_: arg_exps__productions,
    expr_pred: expr_pred_productions,
    predicate: predicate_productions,
}
gr = ContextFreeGrammar(
    program,
    no_terminals_list,
    terminals_list,
    ContextFreeProductionDict(productions_dict),
)
