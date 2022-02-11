from lexer.lexical_analyzer import tokenize
from parser.project_grammar import gr, program, TokenType
from parser.LL_parse import build_parse_table, LL_parse
from parser.context import Context, ExecuteContext

import sys, pickle

if __name__ == "__main__":
    c = Context()
    program  = sys.argv[1]
    if program[len(program)-4:] != '.evo':
        print("not supported file")
    else:
        tokens = tokenize(program)
        try:
            with open('./parser/parse_table','rb') as f:
                parse_table = pickle.load(f)
                f.close()
        except:
            parse_table = build_parse_table(gr)
            with open('./parser/parse_table', 'wb') as f:
                pickle.dump(parse_table, f)
                f.close()
        cst = LL_parse(tokens, parse_table, gr)
        ast = cst.get_ast()
        if ast.check_semantics(c):
            ast.execute(ExecuteContext())
        else:
            print("semantic error")