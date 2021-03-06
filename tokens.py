#!/usr/bin/env
import ply.lex as lex
from units import units, constants, compound_units

def make_unit_re():
    unit_list = []
    for measurement, conversions in units:
        for base, multiplier, names in conversions:
            unit_list += names
    
    unit_list += compound_units.keys()
    
    unit_list.sort(key=len, reverse=True)
    return "(%s)" % ')|('.join(unit_list)

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

t_CONSTANT = '(' + '|'.join(k for k in constants.iterkeys()) + ')'

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

