#!/usr/bin/env python

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

def make_unit_re():
    unit_list = []
    for distance, conversions in units:
        for multiplier, base, names in conversions:
            unit_list += names
    
    return "(%s)" % ')|('.join(unit_list)
