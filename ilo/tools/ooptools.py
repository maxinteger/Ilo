# -*- coding: utf -*-

__author__ = ("Vadasz Laszlo", "Kay Schluehr")
__date__ = "2009.10.16. 12:13:39"

"""
public function and Object class source
from: http://code.activestate.com/recipes/496920/
by: Kay Schluehr
"""

def publicmethod(f):
    '''
    Decorator used to assign the attribute __public__ to methods.
    '''
    f.__public__ = True
    return f

class Object(object):
    '''
    Base class of all classes that want to hide protected attributes from
    public access.
    '''

    __public__ = []

    def __new__(cls, * args, ** kwd):
        obj = object.__new__(cls)
        cls.__init__(obj, * args, ** kwd)

        def __getattr__(self, name):
            attr = getattr(obj, name)
            if hasattr(attr, "__public__"):
                return attr
            elif hasattr(cls, "__public__"):
                if name in cls.__public__:
                    return attr
            raise AttributeError, "Attribute %s is not public." % name

        def __setattr__(self, name, value):
            attr = getattr(obj, name)
            cls.__setattr__(self, name, value)

        # Magic methods defined by cls must be copied to Proxy.
        # Delegation using __getattr__ is not possible.

        def is_own_magic(cls, name, without = []):
            return name not in without and\
                name.startswith("__") and name.endswith("__")

        Proxy = type("Protected(%s)" % cls.__name__, (), {})

        for name in dir(cls):
            if is_own_magic(cls, name, without = dir(Proxy)):
                try:
                    setattr(Proxy, name, getattr(obj, name))
                except TypeError:
                    pass


        Proxy.__getattr__ = __getattr__
        Proxy.__setattr__ = __setattr__
        return Proxy()
