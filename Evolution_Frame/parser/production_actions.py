from .ast_nodes import *

# program -> block_dec
# stmt -> if_stmt
# stmt -> while_stmt
# stmt -> return_stmt
# stmt -> assignmetn
# return_value -> expression
# expression -> logic_or
# unary -> call
def action_1(node):
    node.ast = node.childs[0].get_ast()
    return node.ast


# block_dec -> fun_dec block_dec_
# block_dec -> var_dec block_dec_
# block_dec -> stmt block_dec_
def action_2(node):
    node.childs[1].l_attribute = [node.childs[0].get_ast()]
    node.ast = BlockDec(node.childs[1].get_ast())
    return node.ast


# block_dec -> eps
def action_3(node):
    node.ast = BlockDec([])
    return node.ast


# block_dec_ -> fun_dec block_dec_
# block_dec_ -> var_dec block_dec_
# block_dec_ -> stmt block_dec_
def action_4(node):
    node.l_attribute.append(node.childs[0].get_ast())
    node.childs[1].l_attribute = node.l_attribute
    node.ast = node.childs[1].get_ast()
    return node.ast


# block_dec_ -> eps
# param_list_ -> eps
# logic_or_ -> eps
# logic_and_ -> eps
# equality_ -> eps
# logic_or_ -> eps
# arg_list_ -> eps
# call__ -> eps
def action_5(node):
    return node.l_attribute


# fun_dec -> fun type ID ( param_list ) { block_dec }
def action_6(node):
    node.ast = FunDec(
        node.childs[1].get_ast(),
        node.childs[2].lexeme,
        node.childs[4].get_ast(),
        node.childs[7].get_ast(),
    )
    return node.ast


# var_dec -> type ID = var_dec_ ;
def action_7(node):
    node.ast = VarDec(
        node.childs[0].get_ast(), node.childs[1].lexeme, node.childs[3].get_ast()
    )
    return node.ast


# type -> number
def action_8(node):
    node.ast = LType(node.childs[0].lexeme)
    return node.ast


# type -> str
def action_9(node):
    node.ast = LType(node.childs[0].lexeme)
    return node.ast


# type -> nil
def action_10(node):
    node.ast = Nil(node.childs[0].lexeme)
    return node.ast


# type -> bool
def action_11(node):
    node.ast = LType(node.childs[0].lexeme)
    return node.ast


# var_dec_ -> expression
def action_12(node):
    node.ast = node.childs[0].get_ast()
    return node.ast


# var_dec_ -> eps
# return_value -> eps
def action_13(node):
    node.ast = Nil()
    return node.ast


# param_list -> type ID param_list_
def action_14(node):
    node.childs[2].l_attribute = [
        Param(node.childs[0].get_ast(), node.childs[1].lexeme)
    ]
    node.ast = node.childs[2].get_ast()
    return node.ast


# param_list -> eps
def action_15(node):
    node.ast = []
    return node.ast


# param_list_ -> , type ID param_list_
def action_16(node):
    node.l_attribute.append(Param(node.childs[1].get_ast(), node.childs[2].lexeme))
    node.childs[3].l_attribute = node.l_attribute
    node.ast = node.childs[3].get_ast()
    return node.ast


# if_stmt -> if ( exp ) { block_dec } else_stmt
def action_17(node):
    node.childs[7].l_attribute = [node.childs[2].get_ast(), node.childs[5].get_ast()]
    node.ast = node.childs[7].get_ast()
    return node.ast


# else_stmt -> else { block_dec }
def action_18(node):
    node.ast = IfElse(node.l_attribute[0], node.l_attribute[1].node.childs[2].get_ast())
    return node.ast


# else_stmt -> eps
def action_19(node):
    node.ast = If(node.l_attribute[0], node.l_attribute[1])
    return node.ast


# while_stmt -> while ( exp ) { block_dec }
def action_20(node):
    node.ast = While(node.childs[2].get_ast(), node.childs[5].get_ast())
    return node.ast


# return_stmt -> return return_value ;
def action_21(node):
    node.ast = Return(node.childs[1].get_ast())
    return node.ast


# assignment -> ID assignment_ ;
def action_22(node):
    node.childs[1].l_attribute = node.childs[0].lexeme
    node.ast = node.childs[1].get_ast()
    return node.ast


# logic_or -> logic_and logic_or_
# logic_and -> equality logic_and_
# equality -> cmp equality_
# cmp -> term cmp_
# term -> factor term_
# factor -> unary factor_
# call -> primary call_
def action_23(node):
    node.childs[1].l_attribute = node.childs[0].get_ast()
    node.ast = node.childs[1].get_ast()
    return node.ast


# logic_or_ -> or logic_and logic_or_
def action_24(node):
    node.childs[2].l_attribute = Or(node.l_attribute, node.childs[1].get_ast())
    node.ast = node.childs[2].get_ast()
    return node.ast


# logic_and_ -> and equality logic_and
def action_25(node):
    node.childs[2].l_attribute = And(node.l_attribute, node.childs[1].get_ast())
    node.ast = node.childs[2].get_ast()
    return node.ast


# equality_ -> == cmp
def action_26(node):
    node.ast = EqualEqual(node.l_attribute, node.childs[1].get_ast())
    return node.ast


# equality_ -> != cmp
def action_27(node):
    node.ast = NotEqual(node.l_attribute, node.childs[1].get_ast())
    return node.ast


# cmp_ -> > term
def action_28(node):
    node.ast = Greater(node.l_attribute, node.childs[1].get_ast())
    return node.ast


# cmp_ -> >= term
def action_29(node):
    node.ast = GreaterEqual(node.l_attribute, node.childs[1].get_ast())
    return node.ast


# cmp_ -> < term
def action_30(node):
    node.ast = LessEqual(node.l_attribute, node.childs[1].get_ast())
    return node.ast


# cmp_ -> > term
def action_31(node):
    node.ast = LessEqual(node.l_attribute, node.childs[1].get_ast())
    return node.ast


# term_ -> + factor term_
def action_32(node):
    node.childs[2].l_attribute = Plus(node.l_attribute, node.childs[1].get_ast())
    node.ast = node.childs[2].get_ast()
    return node.ast


# term_ -> - factor term_
def action_33(node):
    node.childs[2].l_attribute = Sub(node.l_attribute, node.childs[1].get_ast())
    node.ast = node.childs[2].get_ast()
    return node.ast


# factor_ -> * unary factor_
def action_34(node):
    node.childs[2].l_attribute = Star(node.l_attribute, node.childs[1].get_ast())
    node.ast = node.childs[2].get_ast()
    return node.ast


# factor_ -> / unary factor_
def action_35(node):
    node.childs[2].l_attribute = Div(node.l_attribute, node.childs[1].get_ast())
    node.ast = node.childs[2].get_ast()
    return node.ast


# unary -> not unary
def action_36(node):
    node.ast = Not(node.childs[1].get_ast())
    return node.ast


# call_ -> ( arg_list )
def action_37(node):
    node.ast = Call(node.l_attribute, node.childs[1].get_ast())
    return node.ast


# arg_list -> exp arg_list_
def action_38(node):
    node.childs[1].l_attribute = [node.childs[0].get_ast()]
    node.ast = node.childs[1].get_ast()
    return node.ast


# arg_list -> eps
def action_39(node):
    return []


# arg_list_ -> , exp arg_list_
def action_40(node):
    node.l_attribute.append(node.childs[1].get_ast())
    node.childs[2].l_attribute = node.l_attribute
    node.ast = node.childs[2].get_ast()
    return node.ast


# primary -> True
# primary -> False
def action_41(node):
    node.ast = Bool(node.childs[0].lexeme)
    return node.ast


# primary -> Nil
def action_42(node):
    node.ast = Nil()
    return node.ast


# primary -> Number
def action_43(node):
    node.ast = Number(node.childs[0].lexeme)
    return node.ast


# primary -> Str
def action_44(node):
    node.ast = String(node.childs[0].lexeme)
    return node.ast


# primary -> ID
def action_45(node):
    node.ast = ID(node.childs[0].lexeme)
    return node.ast


# assignment_ -> = exp
def action_46(node):
    node.ast = Assignment(node.l_attribute, node.childs[1].get_ast())
    return node.ast


# assignment_ -> ( arg_list )
def action_47(node):
    node.ast = Call(ID(node.l_attribute), node.childs[1].get_ast())
    return node.ast


# type -> simulator
def action_48(node):
    node.ast = LType(node.childs[0].lexeme)
    return node.ast
