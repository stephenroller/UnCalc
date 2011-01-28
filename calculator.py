#!/usr/bin/env

import sys
from parser import parse

EXAMPLE = '10 miles / hour in ft / s'

def help():
    progname = sys.argv[0]
    
    sys.stdout.write("\n".join([
        "Usage: python %s conversion" % progname,
        "",
        "Example: ",
        "   $ python %s '10 m / s in mi/hr'" % progname,
        "   4.470 m/s",
    ]) + "\n")

if __name__ == '__main__':
    if len(sys.argv) <= 1:
        help()
        sys.exit(2)
    
    inpt = sys.argv[1]
    try:
        print parse(inpt)
    except Exception, msg:
        sys.stdout.write("Error: %s\n" % msg)
        sys.exit(1)

    