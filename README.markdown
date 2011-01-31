# UnCalc

UnCalc is a Unit Calculator, much like
[Google Calculator](http://www.google.com/intl/en/help/features.html#calculator).
It is written in Python.

UnCalc was hacked together in a few hours as a proof-of-concept. It requires 
substantial work before it should ever be used seriously.

## Usage

    $ python calculator.py '10 miles per hour in m / s'
    4.470 m/s
    
    $ python calculator.py '8 * 2'
    16.000

## Current Limitations

UnCalc has several large limitations keeping it from being a seriously
useful tool.

  * UnCalc has a very limited list of supported units and constants. See 
    units.py for a complete list.
  * UnCalc has no trigonometry functions, e.g. cos, sin..
  * UnCalc will die ungracefully if given an invalid conversion.
  * UnCalc is unaware of plurality, e.g. 1 days and 3 day are both valid 
    outputs.

[hbar]: http://en.wikipedia.org/wiki/Planck_constant "Planck constant"

## Dependencies

UnCalc depends on [ply](http://www.dabeaz.com/ply/).
