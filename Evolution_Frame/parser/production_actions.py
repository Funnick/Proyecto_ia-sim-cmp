from .ast_nodes import *
#from .ast_nodes import built_in_fun

# program -> Program { block_stmt }
def action_1(node):
    node.ast = node.childs[2].get_ast()
    return node.ast


# block_stmt -> stmt block_stmt'
def action_2(node):
    node.childs[1].l_attribute = [node.childs[0].get_ast()]
    node.ast = BlockStmt(node.childs[1].get_ast())
    return node.ast


# block_stmt' -> stmt block_stmt'
def action_3(node):
    node.l_attribute.append(node.childs[0].get_ast())
    node.childs[1].l_attribute = node.l_attribute
    node.ast = node.childs[1].get_ast()
    return node.ast


# block_stmt' -> eps
def action_22(node):
    return node.l_attribute


# declaration -> var_declaration
# declaration -> stmt
# stmt -> expression_stmt
# stmt -> return_stmt
# stmt -> if_stmt
# stmt -> print_stmt
# expression_stmt -> expression ;
# expression -> assigment
# assigment -> logic_or
# assigment -> equality
# unary -> primary
def action_4(node):
    node.ast = node.childs[0].get_ast()
    return node.ast


# logic_or -> logic_and logic_or'
# logic_and -> equality logic_and'
# equality -> cmp equality'
# cmp -> term cmp'
# term -> factor term'
# factor -> unary factor'
def action_5(node):
    node.childs[1].l_attribute = node.childs[0].get_ast()
    node.ast = node.childs[1].get_ast()
    return node.ast


# equality' -> != cmp
def action_6(node):
    node.ast = NotEqual(node.l_attribute, node.childs[1].get_ast())
    return node.ast


# equality' -> == cmp
def action_7(node):
    node.ast = EqualEqual(node.l_attribute, node.childs[1].get_ast())
    return node.ast


# asg_list' -> eps
# logic_or' -> eps
# logic_and' -> eps
# equality' -> eps
# cmp' -> eps
# term' -> eps
# factor' -> eps
# call -> eps
# arg_expression -> eps
def action_8(node):
    node.ast = node.l_attribute
    return node.ast


# cmp' -> > term
def action_9(node):
    node.ast = Greater(node.l_attribute, node.childs[1].get_ast())
    return node.ast


# cmp' -> >= term
def action_10(node):
    node.ast = GreaterEqual(node.l_attribute, node.childs[1].get_ast())
    return node.ast


# cmp' -> < term
def action_11(node):
    node.ast = Less(node.l_attribute, node.childs[1].get_ast())
    return node.ast


# cmp' -> <= term
def action_12(node):
    node.ast = LessEqual(node.l_attribute, node.childs[1].get_ast())
    return node.ast


# term' -> + factor term'
def action_13(node):
    node.childs[2].l_attribute = Sum(
        node.l_attribute, node.childs[1].get_ast()
    )
    node.ast = node.childs[2].get_ast()
    return node.ast


# term' -> - factor term'
def action_14(node):
    node.childs[2].l_attribute = Sub(
        node.l_attribute, node.childs[1].get_ast()
    )
    node.ast = node.childs[2].get_ast()
    return node.ast


# factor' -> * unary factor'
def action_15(node):
    node.childs[2].l_attribute = Mult(
        node.l_attribute, node.childs[1].get_ast()
    )
    node.ast = node.childs[2].get_ast()
    return node.ast


# factor' -> / unary factor'
def action_16(node):
    node.childs[2].l_attribute = Div(
        node.l_attribute, node.childs[1].get_ast()
    )
    node.ast = node.childs[2].get_ast()
    return node.ast


# unary -> - unary
def action_17(node):
    node.ast = Minus(node.childs[1].get_ast())
    return node.ast


# unary -> ! unary
def action_23(node):
    node.ast = Not(node.childs[1].get_ast())
    return node.ast


# primary -> Number
def action_18(node):
    node.ast = Number(node.childs[0].lexeme)
    return node.ast


# primary -> String
def action_19(node):
    node.ast = String(node.childs[0].lexeme)
    return node.ast


# primary -> Bool
def action_24(node):
    node.ast = Bool(node.childs[0].lexeme)
    return node.ast


# primary -> Nil
def action_20(node):
    node.ast = Nil()
    return node.ast


# primary -> ( expression )
def action_21(node):
    node.ast = node.childs[1].get_ast()
    return node.ast


# print_stmt -> print expression ;
def action_26(node):
    node.ast = PrintStmt(node.childs[1].get_ast())
    return node.ast


# var_declaration -> var ID var_declaration_ ;
def action_27(node):
    node.childs[2].l_attribute = node.childs[1].lexeme
    node.ast = node.childs[2].get_ast()
    return node.ast


# var_declaration_ -> = expression
def action_28(node):
    node.ast = VarDeclaration(node.l_attribute, node.childs[1].get_ast())
    return node.ast


# var_declaration_ -> eps
def action_29(node):
    node.ast = VarDeclaration(node.l_attribute)
    return node.ast


# primary -> ID call
def action_30(node):
    node.childs[1].l_attribute = node.childs[0].lexeme
    node.ast = node.childs[1].get_ast()
    return node.ast


# assigment -> redefine ID = assigment
def action_31(node):
    node.ast = Redefine(node.childs[1].lexeme, node.childs[3].get_ast())
    return node.ast


# if_stmt -> if ( expression ) { block_stmt } else_stmt
def action_32(node):
    node.childs[7].l_attribute = [
        node.childs[2].get_ast(),
        node.childs[5].get_ast(),
    ]
    node.ast = node.childs[7].get_ast()
    return node.ast


# else_stmt -> else { block_stmt }
def action_33(node):
    node.ast = IfElse(
        node.l_attribute[0],
        node.l_attribute[1],
        node.childs[2].get_ast(),
    )
    return node.ast


# else_stmt -> eps
def action_34(node):
    node.ast = If(node.l_attribute[0], node.l_attribute[1])
    return node.ast


# logic_or' -> or logic_and logic_or'
def action_35(node):
    node.childs[2].l_attribute = Or(
        node.l_attribute, node.childs[1].get_ast()
    )
    node.ast = node.childs[2].get_ast()
    return node.ast


# logic_and' -> and equality logic_and'
def action_36(node):
    node.childs[2].l_attribute = And(
        node.l_attribute, node.childs[1].get_ast()
    )
    node.ast = node.childs[2].get_ast()
    return node.ast


# while_stmt -> while ( expression ) { block_stmt }
def action_37(node):
    node.ast = While(node.childs[2].get_ast(), node.childs[5].get_ast())
    return node.ast


# function_declaration -> fun function
def action_38(node):
    node.ast = node.childs[1].get_ast()
    return node.ast


# function -> ID ( arg_list ) { block_stmt }
def action_39(node):
    node.ast = FuntionDeclaration(
        node.childs[0].lexeme, node.childs[2].get_ast(), node.childs[5].get_ast()
    )
    return node.ast


# arg_list -> ID arg_list'
def action_40(node):
    node.childs[1].l_attribute = [node.childs[0].lexeme]
    node.ast = node.childs[1].get_ast()
    return node.ast


# arg_list -> eps
def action_41(node):
    node.ast = []
    return node.ast


# arg_list' -> , ID arg_list'
def action_42(node):
    node.l_attribute.append(node.childs[1].lexeme)
    node.childs[2].l_attribute = node.l_attribute
    node.ast = node.childs[2].get_ast()
    return node.ast


# call -> ( arg_expression )
def action_43(node):
    node.ast = Call(node.l_attribute, node.childs[1].get_ast())
    return node.ast


# arg_expression -> expression arg_expression_
def action_44(node):
    node.childs[1].l_attribute = [node.childs[0].get_ast()]
    node.ast = node.childs[1].get_ast()
    return node.ast


# arg_expression_ -> , expression arg_expression_
def action_45(node):
    node.l_attribute.append(node.childs[1].get_ast())
    node.childs[2].l_attribute = node.l_attribute
    node.ast = node.childs[2].get_ast()
    return node.ast


# call -> eps
def action_46(node):
    node.ast = Call(node.l_attribute, [])
    return node.ast


# return_stmt -> return return_value ;
def action_47(node):
    node.ast = node.childs[1].get_ast()
    return node.ast


# return_value -> expression
def action_48(node):
    node.ast = Return(node.childs[0].get_ast())
    return node.ast


# return_value -> eps
def action_49(node):
    node.ast = Return()
    return node.ast


# expr_pred -> *
def action_50(node):
    node.ast = node.childs[0].get_ast()
    return node.ast


# predicate -> AgentPredicate ID
def action_51(node):
    node.ast = AgentPredicate(node.childs[1].lexeme)
    return node.ast


## 51
