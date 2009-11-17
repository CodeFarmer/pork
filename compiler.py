#! /usr/bin/env python

import logging
from logging import DEBUG, INFO, ERROR

from bytes import u1

from classfile import Code_attribute, ExceptionTableEntry, LineNumberTable_attribute

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

class InternalCompilerError(Exception):

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return name

class UnknownSymbol(Exception):

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return name

class UnknownLabel(UnknownSymbol):
    def __init__(self, name):
        UnknownSymbol.__init__(self, name)


class Symbol(object):
    def __init__(self, owningClass):
        self.owningClass = owningClass

# Now Symbols must be actually dereferenced to trigger creation of constant
# entries in the classfile - therefore they need to be typed. When
# dereferenced, they return the bytes appropriate to their index into the
# constant pool.

class ConstantSymbol(Symbol):

    def __init__(self, owningClass, value):
        Symbol.__init__(self, owningClass)
        self.value = value

class StringSymbol(ConstantSymbol):

    def get(self):
        return [self.owningClass.stringConstant(self.value) & 0xff]


class ClassSymbol(ConstantSymbol):

    def get(self):
        const = self.owningClass.classConstant(self.value)
        return [const >> 8 & 0xff, const & 0xff]

class IntegerSymbol(ConstantSymbol):

    def get(self):
        return [self.owningClass.integerConstant(self.value) & 0xff]

class FloatSymbol(ConstantSymbol):

    def get(self):
        return [self.owningClass.floatConstant(self.value) & 0xff]

# value is the method signature (or field desc)!
class FieldSymbol(ConstantSymbol):

    def __init__(self, owningClass, targetClassName, fieldName, typeDesc):
        ConstantSymbol.__init__(self, owningClass, typeDesc)
        self.fieldName = fieldName
        self.targetClassName = targetClassName

    def get(self):
        const = self.owningClass.fieldConstant(self.targetClassName, self.fieldName, self.value)
        return [const >> 8 & 0xff, const & 0xff] ;

class MethodSymbol(FieldSymbol):

    def get(self):
        const = self.owningClass.methodConstant(self.targetClassName, self.fieldName, self.value)
        return [const >> 8 & 0xff, const & 0xff] ;

class SymbolRef(object):
    def __init__(self, name):
        self.name = name

class LabelRef(SymbolRef):
    None


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
            if isinstance(arg, LabelRef):

                if not labelTable.has_key(arg):
                    raise UnknownLabel(arg)

                ret += u1(labelTable[arg])

            elif isinstance(arg, SymbolRef):

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

# shut up

def getAbsoluteOrLabelOffset(labels, offset):

    if isinstance(offset, int):
        return offset
    elif isinstance(offset, basestring):
        if not labels.has_key(offset):
            raise UnknownLabel(offset)
        return labels[offset]

    else:
        raise InternalCompilerError('The compiler attempted to create an offset that was neither a label or an integer')

class ExceptionDef(object):
    
    def __init__(self, owningClass, startThing, endThing, throwableClass, target):

        if log.getEffectiveLevel() <= DEBUG:
            log.debug('ExceptionDef(' + `owningClass` + ', ' + `startThing` + ', ' + `endThing` + ', ' + `throwableClass` + ', ' + `target` + ')') 
        
        self.owningClass = owningClass
        self.startThing = startThing
        self.endThing = endThing
        self.throwableClass = throwableClass
        self.target = target

    def getExceptionTableEntry(self, labels):

        return ExceptionTableEntry(self.owningClass,
                                   getAbsoluteOrLabelOffset(labels, self.startThing),
                                   getAbsoluteOrLabelOffset(labels, self.endThing),
                                   self.throwableClass,
                                   getAbsoluteOrLabelOffset(labels, self.target))

# This is crude; FIXME
def calculateLabelOffset(name, instructionsSoFar):

    offset = reduce(lambda x, y: x + y.op.operands + 1, instructionsSoFar, 0)

    if log.getEffectiveLevel() <= DEBUG:
        log.debug('Resolving label ' + `name` + ' to ' + `offset`)

    return offset;
   

def buildExceptionTable(defs, labels):

    return map(lambda x: x.getExceptionTableEntry(labels), defs)


def buildMethodBody(instructions, symbols, labels):

    ret = ''
    pc = 0

    for instruction in instructions:

        # first, convert symbol references to byte groups

        args = instruction.args
        newargs = []
        for arg in args:

            if isinstance(arg, LabelRef):

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

 
            elif isinstance(arg, SymbolRef):

                name = arg.name
                if not symbols.has_key(name):

                    if log.getEffectiveLevel() <= ERROR:
                        log.error('Unknown symbol ' + name + ': ' + `symbols`)

                    raise UnknownSymbol(name)

                newargs += symbols[name].get()

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

def buildMethod(owningClass, methodName, methodDesc, accessMask, stackSize, localSize, operations, symbols, labels, exceptionDefs, lineNumberTable, compileLineNumbers):

    exceptionTable = buildExceptionTable(exceptionDefs, labels)
    methodBody     = buildMethodBody(operations, symbols, labels)

    codeAttributeAttributes = []

    if compileLineNumbers:
        lineNumberPairs = []
        for key in lineNumberTable.keys():
            lineNumberPairs.append((lineNumberTable[key], key))

        codeAttributeAttributes = [LineNumberTable_attribute(owningClass, lineNumberPairs)]

    meth = owningClass.method(methodName, 
                              methodDesc,
                              accessMask,
                              [Code_attribute(owningClass, stackSize, localSize, methodBody, exceptionTable, codeAttributeAttributes)]) ;
       
    symbols[methodName] = MethodSymbol(owningClass, owningClass.name, methodName, methodDesc);

    return meth

