#! /usr/bin/env python

import logging
from logging import DEBUG, INFO, ERROR

from bytes import u1
from jopcode import getOperation

log = logging.getLogger('compiler')
log.setLevel(INFO)


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


class UnknownSymbol(Exception):

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return name

class UnknownLabel(UnknownSymbol):
    def __init__(self, name):
        UnknownSymbol.__init__(self, name)


class Symbol(object):
    def __init__(self, name):
        self.name = name

class Label(Symbol):
    def __init__(self, name):
        Symbol.__init__(self, name)


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
                    raise UnknownLabel(arg)

                ret += u1(labelTable[arg])

            elif isinstance(arg, Symbol):

                name = arg.name
                if not symbolTable.has_key(name):
                    
                    if log.getEffectiveLevel() <= ERROR:
                        log.error('Unknown symbol ' + name + ': ' + `symbolTable`)
                    raise UnknownSymbol(name)

                if log.getEffectiveLevel() <= DEBUG:
                    log.debug('resolving symbol $' + name + ' to ' + `symbolTable[name]` + '(' + `symbolTable` + ')')

                for b in symbolTable[name]: # list of bytes
                    ret += u1(b)
                
            else:
                ret += u1(arg) # arg is an integer

        return ret

# This is crude; FIXME
def calculateLabelOffset(name, instructionsSoFar):

    offset = reduce(lambda x, y: x + y.op.operands + 1, instructionsSoFar, 0)

    if log.getEffectiveLevel() <= DEBUG:
        log.debug('Resolving label ' + `name` + ' to ' + `offset`)

    return offset;
   


def buildMethodBody(instructions, symbols, labels):

    ret = ''
    pc = 0

    for instruction in instructions:

        # first, convert symbol references to byte groups

        args = instruction.args
        newargs = []
        for arg in args:

            if isinstance(arg, Label):

                name = arg.name

                if not labels.has_key(name):

                    if log.getEffectiveLevel() <= ERROR:
                        log.error('Unknown label ' + `name` + ': ' + `labels`)

                    raise UnknownLabel(name)

                branchOffset = labels[name] - pc


                if branchOffset < 0:
                    
                    # agh, nail down two's compliment signed 16-bit
                    # TODO find out if there's a better way in Python?
                    branchOffset = ((~(-branchOffset)) + 1) & 0xffff

                newargs.append((branchOffset >> 8) & 0xff)
                newargs.append(branchOffset      & 0xff)

 
            elif isinstance(arg, Symbol):

                name = arg.name
                if not symbols.has_key(name):

                    if log.getEffectiveLevel() <= ERROR:
                        log.error('Unknown symbol ' + name + ': ' + `symbols`)

                    raise UnknownSymbol(name)

                newargs += symbols[name]

            else: # it's a byte literal

                newargs.append(arg)
                
        # check lengths

        op = instruction.op

        pc += 1 ;
        pc += op.operands ;

        if not len(newargs) == op.operands:
            message = op.name + ' expected ' + `op.operands` + ' operands, got '  + `len(newargs)`

            if log.getEffectiveLevel() <= ERROR:
                log.error(message)

            raise ArgumentException(op.name, newargs, message)

        # add bytes
        instruction.args = newargs
        ret += instruction.byteString()

    return ret

