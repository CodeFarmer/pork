#! /usr/bin/env python


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


def Symbol(object):
    def __init__(name):
        self.name = name

def Label(Symbol):
    def __init__(name):
        Symbol(self, name)


class Instruction(object):

    # (Operation, list of integer literals, symbols or labels)
    def __init__(op, args):

        op = getOperation(name)

        if not len(args) == op.operands:
            message = name + ' expected ' + `op.operands` + ' operands, got '  + `len(args)`
            log.warn(message)
            raise ArgumentException(name, args, message)


    def byteString(self, symbolTable, labelTable):

        # log.debug('byteString(' + name + ', ' + `args` + ')')
    
        ret = u1(op.opcode)
        for arg in args:

            # TODO reconsider this, maybe just have local and global symbol tables
            if isinstance(arg, Label):

                if not labelTable.has_key(arg):
                    raise new UnkownLabel(arg)

                ret += u1(labelTable[arg])

            elif isinstance(arg, Symbol):

                if not symbolTable.has_key(arg):
                    raise new UnkownSymbol(arg)

                ret += u1(symbolTable[arg])
                
            else:
                ret += u1(arg)

        return ret

