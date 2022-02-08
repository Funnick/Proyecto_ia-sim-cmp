from lexer.lexical_analyzer import tokenize
from parser.project_grammar import gr
from parser.LL_parse import build_parse_table, LL_parse
from parser.project_context import pc

tokens = tokenize("program1.txt")
parse_table = build_parse_table(gr)
cst = LL_parse(tokens, parse_table, gr)
ast = cst.get_ast()
if ast.check_semantics():
    ast.execute(pc)
else:
    print("semantic error")
