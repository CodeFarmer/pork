#! /usr/bin/env python

class Op(object):
    
    # FIXME args to be a bit more expressive in terms of type?
    def __init__(self, name, opcode, args = 0):
        
        assert isinstance(name, basestring)
        assert isinstance(opcode, int)
        assert isinstance(args, int)
        
        self.name = name.lower()
        self.opcode = opcode
        self.args   = args

class UnknownOperation(Exception):

    def __init__(self, name):
        assert isinstance(name, basestring)
        self.name = name

    def __str__(self):
        return self.name


OPERATIONS = {}


def addOperation(op):

    assert isinstance(op, Op)
    OPERATIONS[op.name] = op


def getOperation(name):

    assert isinstance(name, basestring)
    name = name.lower()
    if (not OPERATIONS.has_key(name)):
        raise UnknownOperation(name)

    return OPERATIONS[name]

# addOperation(Op('ret',    0xa9, 1))
addOperation(Op('return', 0xb1, 0)) # return void

