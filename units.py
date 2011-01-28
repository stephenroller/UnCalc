#!/usr/bin/env python

from graph import Graph

units = [
    ('distance', [
        # from  multiplier     [to and aliases]
        # e.g. 1 m = 6.213e-4 miles
        #      1 m = 39.370 inches, etc
        
        ('m',   6.21371192e-4, ['mi', 'mile', 'miles']),
        ('m',   1.0,           ['m', 'meter', 'meters']),
        ('m',   39.3700787,    ['inch', 'inches']),
        ('m',   3.2808399,     ['ft', 'foot', 'feet']),
    ]),
    ('time', [
        ('min', 60,            ['s', 'second', 'seconds']),
        ('h',   60,            ['min', 'minute', 'minutes']),
        ('d',   24,            ['h', 'hr', 'hour', 'hours']),
        ('y',   365.25,        ['d', 'day', 'days']),
        ('y',   1.0,           ['y', 'yr', 'year', 'years']),
        ('d',   0.142857143,   ['w', 'wk', 'week', 'weeks'])
    ]),
]

_add = lambda x,y: x+y

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
    

def make_unit_re():
    unit_list = []
    for measurement, conversions in units:
        for base, multiplier, names in conversions:
            unit_list += names
    
    unit_list.sort(key=len, reverse=True)
    return "(%s)" % ')|('.join(unit_list)
