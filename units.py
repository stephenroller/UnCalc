#!/usr/bin/env python

from graph import Graph

units = [
    ('distance', [
        # multiplier    from   [to and aliases]
        # e.g. 1 m = 6.213e-4 miles
        #      1 m = 39.370 inches, etc
        
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
    

def make_unit_re():
    unit_list = []
    for measurement, conversions in units:
        for multiplier, base, names in conversions:
            unit_list += names
    
    unit_list.sort(key=len, reverse=True)
    return "(%s)" % ')|('.join(unit_list)
