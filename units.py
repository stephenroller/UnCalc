#!/usr/bin/env python
from unitvalue import UnitValue

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

constants = {
    'pi': UnitValue(3.14159265),
    'e': UnitValue(2.71828183),
}

