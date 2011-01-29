#!/usr/bin/env python

from operator import add, mul, div
from parser import parse, OpConstants
from units import units, constants
from graph import Graph

# number of decimals to print
DECIMALS_OUT = 5

class UnitValue(object):
    def __init__(self, value=1, numer=None, denom=None):
        self.value = value
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
        value = round(self.value, DECIMALS_OUT)
        if value == int(value):
            out += str(int(self.value))
        else:
            out += ("%." + str(DECIMALS_OUT) + "f") % self.value
            
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
    
    def __sub____(self, other):
        return UnitValue(value=self.value + other.convert_to(self).value,
                         numer=self.numer,
                         denom=self.denom)
    
    def __sub__(self, other):
        return self + (- other)
    
    def convert_to(self, goal):
        value = self.value
        value *= convert_many(self.numer, goal.numer)
        value /= convert_many(self.denom, goal.denom)
        
        return UnitValue(value=value,
                         numer=goal.numer,
                         denom=goal.denom)



def number(arg):
    try:
        return UnitValue(value=int(arg))
    except ValueError:
        return UnitValue(value=float(arg))

def constant(arg):
    return UnitValue(value=constants[arg])

def sub(*args):
    if len(args) == 1:
        return - args[0]
    elif len(args) == 2:
        return args[0] - args[1]
    else:
        raise Exception, "sub takes one or two arguments."

def unit(arg):
    return UnitValue(numer=[arg])

functions = dict([
    (OpConstants.PLUS, add),
    (OpConstants.MINUS, sub),
    (OpConstants.TIMES, mul),
    (OpConstants.DIVIDE, div),
    (OpConstants.EXP, pow),
    (OpConstants.NUMBER, number),
    (OpConstants.CONSTANT, constant),
    (OpConstants.CONVERT, UnitValue.convert_to),
    (OpConstants.UNIT, unit)
])

def eval_expr(tree):
    if isinstance(tree, list):
        fn = functions[tree[0]]
        args = map(eval_expr, tree[1:])
        return fn(*args)
    else:
        return tree

# create the measurements dictionary
unit_types = dict(
    (name, measurement)
    for measurement, conversions in units
    for base, multiplier, names in conversions
    for name in names
)

unit_graphs = dict()

for measurement, conversions in units:
    vertices = []
    edges = []
    for base, multiplier, names in conversions:
        vertices += names
        edges.append((base, names[0], multiplier))
        for name in names[1:]:
            edges.append((names[0], name, 1))

    unit_graphs[measurement] = Graph(vertices, edges)

def convert_one(from_unit, to_unit):
    assert unit_types[from_unit] == unit_types[to_unit]

def convert_many(from_units, to_units):
    assert len(from_units) == len(to_units), "Invalid conversion."
    # copies so we can mess with them freely
    from_units = list(from_units)
    to_units = list(to_units)

    value = 1.0

    while from_units:
        from_unit = from_units.pop(0)
        unit_type = unit_types[from_unit]
        possible_goals = [unit2 for unit2 in to_units if unit_types[unit2] == unit_type]
        assert possible_goals, "Invalid conversion."
        to_unit = possible_goals[0]
        to_units.remove(to_unit)
        mult, path = unit_graphs[unit_type].path(from_unit, to_unit)
        value *= mult

    assert not to_units, "Invalid conversion."

    return value