#! /usr/bin/env python

import logging as log 

from bytes import u1
from jopcode import getOperation


class ArgumentException(Exception):

    def __init__(self, name, args, mess=None):

        assert isinstance(name, basestring)
        self.name = name
        self.args = args
        self.mess = mess

    # FIXME this doesn't appear to be working correctly
    def __str__(self):

        ret = self.name + ' ( '
        for arg in self.args:
            ret += arg
            ret += ' '

        ret += ')'

        if self.mess:

            ret += ' : '
            ret += self.mess

        return ret


class UnkownSymbol(Exception):

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return name

class UnknownLabel(UnkownSymbol):
    def __init__(self, name):
        UnknownSymbol(self, name)


class Symbol(object):
    def __init__(self, name):
        self.name = name

class Label(Symbol):
    def __init__(self, name):
        Symbol(self, name)


class Instruction(object):

    # (Operation, list of integer literals, symbols or labels)
    def __init__(self, opName, args):

        op = getOperation(opName)

        # operand checking no longer happens here, as symbol resolution
        # can change the number of argument slots
        self.op = op
        self.args = args


    def byteString(self):

        ret = u1(self.op.opcode)
        for arg in self.args:

            # TODO reconsider this, maybe just have local and global symbol tables
            if isinstance(arg, Label):

                if not labelTable.has_key(arg):
                    raise UnkownLabel(arg)

                ret += u1(labelTable[arg])

            elif isinstance(arg, Symbol):

                name = arg.name
                if not symbolTable.has_key(name):
                    log.warn('Unknown symbol ' + name + ': ' + `symbolTable`)
                    raise UnkownSymbol(name)

                log.debug('resolving symbol $' + name + ' to ' + `symbolTable[name]` + '(' + `symbolTable` + ')')
                for b in symbolTable[name]: # list of bytes
                    ret += u1(b)
                
            else:
                ret += u1(arg) # arg is an integer

        return ret


def buildMethodBody(instructions, symbols, labels):

    ret = ''
    for instruction in instructions:

        # first, convert symbol references to byte groups

        args = instruction.args
        newargs = []
        for arg in args:

            if isinstance(arg, Label):

                name = arg.name

                if not labels.has_key(name):
                    raise UnkownLabel(name)

                newargs += labels[name]

            elif isinstance(arg, Symbol):

                name = arg.name
                if not symbols.has_key(name):
                    log.warn('Unknown symbol ' + name + ': ' + `symbols`)
                    raise UnkownSymbol(name)

                log.debug('resolving symbol $' + name + ' to ' + `symbols[name]`)
                newargs += symbols[name]

            else: # it's a byte literal

                newargs.append(arg)
                
        # check lengths

        op = instruction.op

        if not len(newargs) == op.operands:
            message = op.name + ' expected ' + `op.operands` + ' operands, got '  + `len(newargs)`
            log.warn(message)
            raise ArgumentException(op.name, newargs, message)

        # add bytes
        instruction.args = newargs
        ret += instruction.byteString()

    return ret

