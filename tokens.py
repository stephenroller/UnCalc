#!/usr/bin/env
import ply.lex as lex
from units import make_unit_re

tokens = (
    'IN',
    'CONSTANT',
    'NUMBER',
    'LPAR', 'RPAR',
    'MINUS', 'PLUS',
    'TIMES', 'DIVIDE',
    'EXP',
    'UNIT',
)

t_ignore = ' \n\t'

t_CONSTANT = '(pi|e)'

t_IN = r'in'
t_NUMBER = r"\d+(\.\d*)?(e([+-]?\d+))?"
t_LPAR = r'\('
t_RPAR = r'\)'
t_MINUS = r'-'
t_PLUS = r'\+'
t_TIMES = r'\*'
t_DIVIDE = r'/|per'
t_EXP = r'\^|\*\*'
t_UNIT = make_unit_re()

def t_error(t):
    import sys
    sys.stdout.write("Illegal character '%s'\n" % t.value[0])
    t.lexer.skip(1)


lexer = lex.lex()

