#!/usr/bin/env python

from graph import Graph

# METRIC_PREFIXES = r"(k(ilo)?|c(enti)?|m(illi)?)?"

units = [
    ('distance', [
        (6.21371192e-4, 'm',   ['mi', 'mile', 'miles']),
        (1.0,           'm',   ['m', 'meter', 'meters']),
        (39.3700787,    'm',   ['inch', 'inches']),
        (3.2808399,     'm',   ['ft', 'foot', 'feet']),
    ]),
    ('time', [
        (60,            'min', ['s', 'second', 'seconds']),
        (60,            'h',   ['min', 'minute', 'minutes']),
        (24,            'd',   ['h', 'hr', 'hour', 'hours']),
        (365.25,        'y',   ['d', 'day', 'days']),
        (1.0,           'y',   ['y', 'yr', 'year', 'years']),
        (0.142857143,   'd',   ['w', 'wk', 'week', 'weeks'])
    ]),
]

_add = lambda x,y: x+y

# create the measurements dictionary
unit_types = dict(
    (name, measurement)
    for measurement, conversions in units
    for multiplier, base, names in conversions
    for name in names
)

unit_graphs = dict()

for measurement, conversions in units:
    vertices = []
    edges = []
    for multiplier, base, names in conversions:
        vertices += names
        edges.append((base, names[0], multiplier))
        for name in names[1:]:
            edges.append((names[0], name, 1))
    
    unit_graphs[measurement] = Graph(vertices, edges)

def convert_one(from_unit, to_unit):
    assert unit_types[from_unit] == unit_types[to_unit]

def make_unit_re():
    unit_list = []
    for measurement, conversions in units:
        for multiplier, base, names in conversions:
            unit_list += names
    
    return "(%s)" % ')|('.join(unit_list)
