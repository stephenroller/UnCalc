#!/usr/bin/env python
import ply.yacc as yacc
from tokens import tokens
from units import convert_many

precedence = (
    ('left', 'IN'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('left', 'EXP'),
    ('right', 'UMINUS'),
)

class UnitValue(object):
    def __init__(self, value=None, numer=None, denom=None):
        self.value = value or 1
        self.numer = numer or []
        self.denom = denom or []
    
    def __mul__(self, other):
        assert isinstance(other, UnitValue)
        return UnitValue(value=self.value * other.value,
                         numer=self.numer + other.numer,
                         denom=self.denom + other.denom)
    
    def __div__(self, other):
        assert isinstance(other, UnitValue)
        return UnitValue(value = self.value / other.value,
                         numer=self.numer + other.denom,
                         denom=self.denom + other.numer)
    
    def __repr__(self):
        out = ""
        if self.value != 1:
            out += "%.3f" % self.value
        if self.numer:
            if out:
                out += " "
            out += "*".join(self.numer)
        if self.denom:
            out += "/" + "*".join(self.denom)
        
        return out
    
    def __neg__(self):
        return UnitValue(value=-self.value,
                         numer=self.numer,
                         denom=self.denom)
    
    def __pow__(self, x):
        assert not x.numer and not x.denom
        x = x.value
        if x >= 0:
            return UnitValue(value=self.value ** x, 
                             numer=self.numer * x,
                             denom=self.denom * x)
        else:
            return UnitValue(value=self.value ** x,
                             numer=self.denom * -x,
                             denom=self.numer * -x)
    
    def __add__(self, other):
        return UnitValue(self.value + other.convert_to(self).value,
                         self.numer,
                         self.denom)
    
    def __sub__(self, other):
        return self + - other
    
    def convert_to(self, goal):
        value = self.value
        value *= convert_many(self.numer, goal.numer)
        value /= convert_many(self.denom, goal.denom)
        
        return UnitValue(value=value,
                         numer=goal.numer,
                         denom=goal.denom)
        

def p_eval_expr(p):
    '''eval-expr : conversion
                 | unit-expr
    '''
    p[0] = p[1]

def p_conversion(p):
    '''conversion : unit-expr IN unit-expr %prec IN
    '''
    p[0] = p[1].convert_to(p[3])

def p_expr_unary(p):
    '''unit-expr : MINUS unit-expr          %prec UMINUS'''
    p[0] = - p[2]

def p_expr_paren(p):
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
        p[0] = p[1] + p[3]
    elif op == '-':
        p[0] = p[1] - p[3]
    elif op == '*':
        p[0] = p[1] * p[3]
    elif op == '/':
        p[0] = p[1] / p[3]
    elif op == '^':
        p[0] = p[1] ** p[3]
    else:
        raise ValueError, "'%s' is not an operator." % op

def p_unit_expr(p):
    '''unit-expr : expr units
    '''
    p[0] = p[1] * p[2]

def p_unit_expr_one(p):
    '''unit-expr : units
                 | expr
    '''
    p[0] = p[1]

def p_expr_literal(p):
    '''expr : NUMBER
    '''
    try:
        p[0] = UnitValue(value=int(p[1]))
    except ValueError:
        p[0] = UnitValue(value=float(p[1]))

def p_units_units(p):
    '''units : UNIT units'''
    p[0] = UnitValue(numer=[p[1]]) * p[2]

def p_units_unit(p):
    '''units : UNIT'''
    p[0] = UnitValue(numer=[p[1]])

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

if __name__ == '__main__':
    print parse("9.8 m / s + 10 miles / hours in ft / week")
