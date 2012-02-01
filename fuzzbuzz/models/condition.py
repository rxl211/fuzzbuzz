#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Author: Tim Henderson
#Email: tim.tadh@hackthology.com
#For licensing see the LICENSE file in the top level directory.

from random import choice
import abc

from attr_types import Set

class Condition(object):

    def __init__(self, operation):
        self.operation = operation

    def flow(self, objs):
        self.operation.flow(objs)

    def generate_constraint(self, objs):
        return self.operation.generate_constraints(objs)

class Any(Condition):

    def __init__(self, *options):
        self.options = options

    def applies(self, objs):
        return all(opt.applies(objs) for opt in self.options)

    def evaluate(self, objs):
        return any(opt.evaluate(objs) for opt in self.options)
        
    def flow(self, objs):
        choices = list()
        for opt in self.options:
            #print opt.applies(objs),
            #if opt.applies(objs): print opt.evaluate(objs)
            #else: print
            if opt.applies(objs) and not opt.evaluate(objs): continue
            for choice in opt.flow(dict(objs)):
                choices.append(choice)
        return choices
    
    def generate_constraint(self, objs):
        constraints = list()
        for opt in self.options:
            constraint = opt.generate_constraint(objs)
            if constraint is None: continue
            constraints.append(constraint)
        return OrConstraint(constraints)

class All(Condition):

    def __init__(self, *requirements):
        self.requirements = requirements

    def applies(self, objs):
        return all(req.applies(objs) for req in self.requirements)
    
    def evaluate(self, objs):
        return all(req.evaluate(objs) for req in self.requirements)

    def flow(self, objs):
        choices = list()
        for req in self.requirements:
            for choice in req.flow(objs):
                choices.append(choice)
        return choices

    def generate_constraint(self, objs):
        constraints = list()
        for req in self.requirements:
            constraint = req.generate_constraint(objs)
            if constraint is None: continue
            constraints.append(constraint)
        return AndConstraint(constraints)
        
class BooleanOperator(Condition):

    def __init__(self, a, b):
        self.a = a
        self.b = b

class Is(BooleanOperator):

    def applies(self, objs):
        return self.a.has_value(objs) and self.b.has_value(objs)

    def evaluate(self, objs):
        return self.a.value(objs) == self.b.value(objs)

    def flow(self, objs):
        a_hasvalue = self.a.has_value(objs)
        b_hasvalue = self.b.has_value(objs)
        if a_hasvalue and b_hasvalue:
            assert self.a.value(objs) == self.b.value(objs)
        elif a_hasvalue:
            #print 'set b to', self.a.value(objs)
            self.b.set_value(objs, self.a.value(objs))
        elif b_hasvalue:
            #print 'set a to', self.b.value(objs)
            #print self.b.value(objs)
            self.a.set_value(objs, self.b.value(objs))
        else:
            #print self.b(objs).value
            #print 'no values'
            pass # nothing should need to be done here
        return [objs]

    def generate_constraint(self, objs):
        a_hasvalue = self.a.has_value(objs)
        b_hasvalue = self.b.has_value(objs)
        if a_hasvalue and b_hasvalue:
            if self.a.value(objs) == self.b.value(objs):
                return TrueConstraint()
            else:
                return FalseConstraint()
        elif a_hasvalue:
            return SingleValueConstraint(self.b, self.a.value(objs))
        elif b_hasvalue:
            return SingleValueConstraint(self.a, self.b.value(objs))
        else:
            return TrueConstraint()


class In(BooleanOperator):

    def applies(self, objs):
        return self.a.has_value(objs) and self.b.has_value(objs)

    def evaluate(self, objs):
        return self.a.value(objs) in self.b.value(objs)

    def flow(self, objs):
        a_hasvalue = self.a.has_value(objs)
        b_hasvalue = self.b.has_value(objs)
        if a_hasvalue and b_hasvalue:
            assert self.b.type(objs) == Set
            #print self.a.value(objs), self.b.value(objs)
            assert self.a.value(objs) in self.b.value(objs)
        elif a_hasvalue:
            raise Exception, 'Need to think about how to do this correctly'
        elif b_hasvalue:
            assert self.b.type(objs) == Set
            value = choice(tuple(self.b.value(objs)))
            print '----->', value
            self.a.set_value(objs, value)
        else:
            #print self.b(objs).value
            #print 'no values'
            pass # nothing should need to be done here
        return [objs]
    
    def generate_constraint(self, objs):
        a_hasvalue = self.a.has_value(objs)
        b_hasvalue = self.b.has_value(objs)
        if a_hasvalue and b_hasvalue:
            assert self.b.type(objs) == Set
            print self.a.value(objs), self.b.value(objs)
            if self.a.value(objs) in self.b.value(objs):
                return TrueConstraint()
            else:
                return FalseConstraint()
        elif a_hasvalue:
            raise Exception, 'Need to think about how to do this correctly'
            return None
        elif b_hasvalue:
            assert self.b.type(objs) == Set
            return MultiValueConstraint(self.a, tuple(self.b.value(objs)))
        else:
            return TrueConstraint()

class Constraint(object):

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def satisfiable(self, objs): pass

    @abc.abstractmethod
    def flow(self, objs): pass

class FalseConstraint(Constraint):

    def satisfiable(self, objs): return False

    def flow(self, objs): pass

class TrueConstraint(Constraint):

    def satisfiable(self, objs): return True

    def flow(self, objs): pass
    
class AndConstraint(Constraint):

    def __init__(self, constraints):
        self.constraints = constraints

    def satisfiable(self, objs):
        return all(con.satisfiable(objs) for con in self.constraints)

    def flow(self, objs):
        for con in self.constraints:
            con.flow(objs)

class OrConstraint(Constraint):

    def __init__(self, constraints):
        self.constraints = constraints

    def satisfiable(self, objs):
        return any(con.satisfiable(objs) for con in self.constraints)

    def flow(self, objs):
        satisfiable = [con for con in self.constraints if con.satisfiable(objs)]
        constraint = choice(satisfiable)
        constraint.flow(objs)

class SingleValueConstraint(Constraint):

    def __init__(self, obj, value):
        self.obj = obj
        self.value = value

    def satisfiable(self, objs):
        if self.obj.has_value(objs):
            return self.obj.value(objs) == self.value
        else:
            return True

    def flow(self, objs):
        if self.obj.has_value(objs):
            assert self.obj.value(objs) == self.value
        else:
            self.obj.set_value(objs, self.value)

class MultiValueConstraint(Constraint):

    def __init__(self, obj, values):
        self.obj = obj
        self.values = values

    def satisfiable(self, objs):
        if self.obj.has_value(objs):
            return self.obj.value(objs) in self.values
        else:
            return True

    def flow(self, objs):
        if self.obj.has_value(objs):
            assert self.obj.value(objs) == self.value
        else:
            self.obj.set_value(objs, choice(self.values))
