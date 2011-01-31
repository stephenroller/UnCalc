#!/usr/bin/env python
import ply.yacc as yacc
from tokens import tokens

class OpConstants:
    CONVERT = 'CONVERT'
    CONSTANT = 'CONSTANT'
    UNIT = 'UNIT'
    MINUS = '-'
    PLUS = '+'
    TIMES = '*'
    DIVIDE = '/'
    EXP = '^'
    NUMBER = 'NUMBER'


precedence = (
    ('left', 'IN'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('left', 'EXP'),
    ('right', 'UMINUS'),
)


def p_eval_expr(p):
    '''eval-expr : conversion
                 | unit-expr
    '''
    p[0] = p[1]

def p_conversion(p):
    '''conversion : unit-expr IN unit-expr %prec IN
    '''
    p[0] = [OpConstants.CONVERT, p[1], p[3]]

def p_expr_unary(p):
    '''unit-expr : MINUS unit-expr          %prec UMINUS'''
    p[0] = [OpConstants.MINUS, p[2]]

def p_expr_paren(p):
    '''expr : LPAR expr RPAR
    '''
    p[0] = p[2]

def p_unit_expr_paren(p):
    '''unit-expr : LPAR unit-expr RPAR
    '''
    p[0] = p[2]

def p_expr_binop(p):
    '''unit-expr : unit-expr PLUS unit-expr       %prec PLUS
                 | unit-expr MINUS unit-expr      %prec MINUS
                 | unit-expr TIMES unit-expr      %prec TIMES
                 | unit-expr DIVIDE unit-expr     %prec DIVIDE
                 | unit-expr EXP unit-expr        %prec EXP
    '''
    op = p[2]
    if op == '+':
        p[0] = [OpConstants.PLUS, p[1], p[3]]
    elif op == '-':
        p[0] = [OpConstants.MINUS, p[1], p[3]]
    elif op == '*':
        p[0] = [OpConstants.TIMES, p[1], p[3]]
    elif op == '/' or op == 'per':
        p[0] = [OpConstants.DIVIDE, p[1], p[3]]
    elif op == '^' or op == '**':
        p[0] = [OpConstants.EXP, p[1], p[3]]
    else:
        raise ValueError, "'%s' is not an operator." % op

def p_unit_expr(p):
    '''unit-expr : unit-expr units
    '''
    p[0] = [OpConstants.TIMES, p[1], p[2]]

def p_unit_expr_one(p):
    '''unit-expr : expr
                 | units
    '''
    p[0] = p[1]

def p_expr_constant(p):
    '''expr : CONSTANT
    '''
    p[0] = [OpConstants.CONSTANT, p[1]]

def p_expr_literal(p):
    '''expr : NUMBER
    '''
    p[0] = [OpConstants.NUMBER, p[1]]
    return

def p_units_units(p):
    '''units : UNIT units'''
    p[0] = [OpConstants.TIMES, p[1], p[2]]

def p_units_unit(p):
    '''units : UNIT'''
    p[0] = [OpConstants.UNIT, p[1]]

def p_error(p):
    import sys
    if p is None:
        sys.stdout.write("Unexpected end of file.\n")
    else:
        sys.stdout.write("Syntax error at '%s' on line %d.\n" % (p.value, p.lineno))
    sys.exit(1)

def parse(string):
    parser = yacc.yacc()
    return parser.parse(string)
