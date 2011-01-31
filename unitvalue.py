#!/usr/bin/env python

# number of decimals to print
DECIMALS_OUT = 5

unit_types = dict()
unit_graphs = dict()

def _groups(lst):
    grouped = []
    
    while lst:
        item = lst.pop(0)
        if not grouped or item == grouped[0]:
            grouped.append(item)
        else:
            yield grouped
            grouped = [item]
    
    if grouped:
        yield grouped
    
    raise StopIteration

class UnitValue(object):
    def __init__(self, value=1, numer=None, denom=None):
        self.value = value
        self.numer = numer or []
        self.denom = denom or []
        
        self._simplify()
    
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
    
    def _group_like_units(self, unitslist):
        unitslist = sorted(unitslist)
        output = []
        for group in _groups(unitslist):
            if len(group) == 1:
                output.append(group[0])
            else:
                output.append("%s^%d" % (group[0], len(group)))
        return output
    
    def __repr__(self):
        from math import log10
        
        out = ""
        rounded_value = round(self.value, DECIMALS_OUT)
        
        fits_decimals = abs(log10(abs(self.value))) < DECIMALS_OUT
        
        if fits_decimals and rounded_value == int(rounded_value):
            out += str(int(self.value))
        elif fits_decimals:
            out += ("%." + str(DECIMALS_OUT) + "f") % self.value
        else:
            out += ("%." + str(DECIMALS_OUT) + "e") % self.value
            
        if self.numer:
            if out:
                out += " "
            out += "*".join(self._group_like_units(self.numer))
        if self.denom:
            out += "/" + "*".join(self._group_like_units(self.denom))
        
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
    
    def _simplify(self):
        global unit_types
        if not unit_types:
            initialize_converter()
        
        for n in list(self.numer):
            ntyp = unit_types[n]
            for d in list(self.denom):
                dtyp = unit_types[d]
                if ntyp == dtyp:
                    self.value *= convert_many([n], [d])
                    self.numer.remove(n)
                    self.denom.remove(d)
                    break
        
        self.numer.sort()
        self.denom.sort()
    
    def convert_to(self, goal):
        value = self.value
        value *= convert_many(self.numer, goal.numer)
        value /= convert_many(self.denom, goal.denom)
        
        return UnitValue(value=value,
                         numer=goal.numer,
                         denom=goal.denom)


def initialize_converter():
    # create the measurements dictionary
    global unit_types, unit_graphs
    from units import units
    from graph import Graph
    
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

def convert_many(from_units, to_units):
    if not unit_graphs or not unit_types:
        initialize_converter()
    
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
