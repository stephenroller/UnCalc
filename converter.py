#!/usr/bin/env python

from operator import add, mul, div
from parser import parse, OpConstants
from units import units, constants
from unitvalue import UnitValue

def number(arg):
    try:
        return UnitValue(value=int(arg))
    except ValueError:
        return UnitValue(value=float(arg))

def constant(arg):
    return constants[arg]

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
