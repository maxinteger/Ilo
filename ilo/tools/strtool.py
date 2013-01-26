# -*- coding: utf -*-

__author__="Vadasz Laszlo"
__date__ ="2009.07.22. 12:58:21"

import re

"""
Szöveg változók manipulálásra szólgáló függvény gyűjtemény
"""

__string_strip__ = re.compile('\s*')

def fullstrip(str_in, in_list=False):
    """
    A megadott szövegből eltávolítja az összes szóköz és tabulátor karaktert

    @param  str_in: Feldolgozandó szöveg
    @type   str_in: C{string}

    @return:    Szóköz és tabulátor mentes szöveg
    @rtype:     C{string}
    """
    data = __string_strip__.split(str_in.strip())
    return data if in_list else " ".join(data)


if __name__ == "__main__":
    print "fullstr_inip test";
    print "'' ->", fullstrip("")
    print "'  ' ->", fullstrip("  ")
    print "'   a  ' ->", fullstrip("  a  ")
    print "'   ab   ' ->", fullstrip("  ab  ")
    print "'  ds   dsd sd ds  fdf  ' ->", fullstrip("  ds   dsd sd ds  fdf  ")