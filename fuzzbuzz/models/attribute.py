#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Author: Tim Henderson
#Email: tim.tadh@hackthology.com
#For licensing see the LICENSE file in the top level directory.

from value import Value

class AttrChain(Value):

    def __init__(self, objs, lookup_chain):
        type = None                          ## TODO TYPES
        cobjs = objs
        cvalue = None
        for attr in lookup_chain:
            cvalue = attr(cobjs).value
            cobjs = cvalue.__dict__
        super(Attribute, self).__init__(objs, type, value)

class Attribute(Value):

    def __init__(self, objs, obj, call_chain=None):
        obj = obj(objs).value
        if call_chain is not None:
            assert hasattr(obj, '__call__')
            for call in call_chain(objs).value:
                print call
            value = None
            raise Exception
        else:
            value = obj
        type = None                          ## TODO TYPES
        super(Attribute, self).__init__(objs, type, value)

class FCall(Value):

    def __init__(self, objs, parameters):
        type = None                          ## TODO TYPES
        value = [param(objs).value for param in parameters]
        super(Object, self).__init__(objs, type, value)

class CallChain(Value):

    def __init__(self, objs, calls):
        type = None
        value = [call(objs).value for call in calls]
        super(Object, self).__init__(objs, type, value)

class Object(Value):

    def __init__(self, objs, name):
        type = None                          ## TODO TYPES
        value = objs[name]
        super(Object, self).__init__(objs, type, value)

class SymbolObject(Object):

    def __init__(self, objs, name, id):
        type = None                          ## TODO TYPES
        value = objs[(name, id)]
        super(SymbolObject, self).__init__(objs, type, value)
