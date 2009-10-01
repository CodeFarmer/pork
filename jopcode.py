#! /usr/bin/env python

from bytes import u1

import logging as log

class Op(object):
    
    # FIXME args to be a bit more expressive in terms of type?
    def __init__(self, name, opcode, operands = 0, stackdelta = 0):
        
        assert isinstance(name, basestring)
        assert isinstance(opcode, int)
        assert isinstance(operands, int)
        
        self.name = name.lower()
        self.opcode = opcode
        self.operands = operands
        self.stackdelta = 0

        addOperation(self)


class UnknownOperation(Exception):

    def __init__(self, name):
        assert isinstance(name, basestring)
        self.name = name

    def __str__(self):
        return self.name

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


OPERATIONS = {}
OPCODES = {}

def addOperation(op):

    assert isinstance(op, Op)
    OPERATIONS[op.name] = op

    assert(not OPCODES.has_key(op.opcode))
    OPCODES[op.opcode]  = op


def getOperation(name):

    assert isinstance(name, basestring)
    name = name.lower()
    if (not OPERATIONS.has_key(name)):
        raise UnknownOperation(name)

    return OPERATIONS[name]


def byteString(name, args):

    # log.debug('byteString(' + name + ', ' + `args` + ')')
    
    op = getOperation(name)

    if not len(args) == op.operands:
        raise ArgumentException(name, args, 'expected ' + `op.operands` + ' operands, got ' + `len(args)`)

    ret = u1(op.opcode)
    for arg in args:
        ret += u1(arg)

    return ret


Op('aaload',          0x32, 0, -1)
Op('aastore',         0x53, 0, -3)
Op('aconst_null',     0x01, 0,  1)
# aload can't be used to load returnAddress
Op('aload',           0x19, 1,  1)
Op('aload_0',         0x2a, 0,  1)
Op('aload_1',         0x2b, 0,  1)
Op('aload_2',         0x2c, 0,  1)
Op('aload_3',         0x2d, 0,  1)
Op('anewarray',       0xbd, 2,  0)
Op('areturn',         0xb0, 0, -1)
Op('arraylength',     0xbe, 0,  0)
# astore is used to write returnAddress as well as reference
Op('astore',          0x3a, 1, -1)
Op('astore_0',        0x4b, 0, -1)
Op('astore_1',        0x4c, 0, -1)
Op('astore_2',        0x4d, 0, -1)
Op('astore_3',        0x4e, 0, -1)
Op('athrow',          0xbf, 0,  0)

Op('baload',          0x33, 0, -1)
Op('bastore',         0x54, 0, -3)
Op('bipush',          0x10, 1,  1)

Op('caload',          0x34, 0, -1)
Op('castore',         0x55, 0, -3)
Op('checkcast',       0xc0, 2,  0)

Op('d2f',             0x90, 0, -1) # shrinkage
Op('d2i',             0x8e, 0, -1)
Op('d2l',             0x8f, 0,  0)
Op('dadd',            0x63, 0, -2)
Op('daload',          0x31, 0,  0) # two one-word args -> one two-word
Op('dastore',         0x52, 0, -4)
Op('dcmpg',           0x98, 0, -3) # vice versa
Op('dcmpl',           0x97, 0, -3)
Op('dconst_0',        0x0e, 0,  2)
Op('dconst_1',        0x0f, 0,  2)
Op('ddiv',            0x6f, 0, -2)
Op('dload',           0x18, 1,  2)
Op('dload_0',         0x26, 0,  2)
Op('dload_1',         0x27, 0,  2)
Op('dload_2',         0x28, 0,  2)
Op('dload_3',         0x29, 0,  2)
Op('dmul',            0x6b, 0, -2)
Op('dneg',            0x77, 0,  0)
Op('drem',            0x73, 0, -2)
Op('dreturn',         0xaf, 0, -2) # TODO sort out how to describe returns
Op('dstore',          0x39, 1, -2)
Op('dstore_0',        0x47, 0, -2)
Op('dstore_1',        0x48, 0, -2)
Op('dstore_2',        0x49, 0, -2)
Op('dstore_3',        0x4a, 0, -2)
Op('dsub',            0x67, 0, -2)
Op('dup',             0x59, 0,  1)
Op('dup_x1',          0x5a, 0,  1)
Op('dup_x2',          0x5b, 0,  1) # beware type categories
Op('dup2',            0x5c, 0,  2) #
Op('dup2_x1',         0x5d, 0,  2) # 
Op('dup2_x2',         0x5e, 0,  2) #

Op('f2d',             0x8d, 0,  1)
Op('f2i',             0x8b, 0,  0)
Op('f2l',             0x8c, 0,  1)
Op('fadd',            0x62, 0, -1)
Op('faload',          0x30, 0, -1)
Op('fastore',         0x51, 0, -3)
Op('fcmpg',           0x96, 0, -1)
Op('fcmpl',           0x95, 0, -1)
Op('fconst_0',        0x0b, 0,  1)
Op('fconst_1',        0x0c, 0,  1)
Op('fconst_2',        0x0d, 0,  1)
Op('fdiv',            0x6e, 0, -1)
Op('fload',           0x17, 1,  1)
Op('fload_0',         0x22, 0,  1)
Op('fload_1',         0x23, 0,  1)
Op('fload_2',         0x24, 0,  1)
Op('fload_3',         0x25, 0,  1)
Op('fmul',            0x6a, 0, -1)
Op('fneg',            0x76, 0,  0)
Op('frem',            0x72, 0, -1)
Op('freturn',         0xae, 0, -1)
Op('fstore',          0x38, 1, -1)
Op('fstore_0',        0x43, 0, -1)
Op('fstore_1',        0x44, 0, -1)
Op('fstore_2',        0x45, 0, -1)
Op('fstore_3',        0x46, 0, -1)
Op('fsub',            0x66, 0, -1)

Op('getfield',        0xb4, 2,  1) # delta actually 0 or 1
Op('getstatic',       0xb2, 2,  2) # 1 or 2
Op('goto',            0xa7, 2,  0)
Op('goto_w',          0xc8, 4,  0)

Op('i2b',             0x91, 0,  0)
Op('i2c',             0x92, 0,  0)
Op('i2d',             0x87, 0,  1)
Op('i2f',             0x86, 0,  0)
Op('i2l',             0x85, 0,  1)
Op('i2s',             0x93, 0,  0)
Op('iadd',            0x60, 0, -1)
Op('iaload',          0x2e, 0, -1)
Op('iand',            0x7e, 0, -1)
Op('iastore',         0x4f, 0, -3)
# bipush <i>
Op('iconst_m1',       0x02, 0,  1)
Op('iconst_0',        0x03, 0,  1)
Op('iconst_1',        0x04, 0,  1)
Op('iconst_2',        0x05, 0,  1)
Op('iconst_3',        0x06, 0,  1)
Op('iconst_4',        0x07, 0,  1)
Op('iconst_5',        0x08, 0,  1)
Op('idiv',            0x6c, 0, -1)
Op('if_acmpeq',       0xa5, 2, -2)
Op('if_acmpne',       0xa6, 2, -2)
# integer comparison
Op('if_icmpeq',       0x9f, 2, -2)
Op('if_icmpne',       0xa0, 2, -2)
Op('if_icmplt',       0xa1, 2, -2)
Op('if_icmpge',       0xa2, 2, -2)
Op('if_icmpgt',       0xa3, 2, -2)
Op('if_icmple',       0xa4, 2, -2)
# integer comparison with zero
Op('ifeq',            0x99, 2, -1)
Op('ifge',            0x9c, 2, -1)
Op('ifgt',            0x9d, 2, -1)
Op('ifle',            0x9e, 2, -1)
Op('iflt',            0x9b, 2, -1)
Op('ifne',            0x9a, 2, -1)
Op('ifnonnull',       0xc7, 2, -1)
Op('ifnull',          0xc6, 2, -1)
Op('iinc',            0x84, 2,  0)
# iload
Op('iload',           0x15, 1,  1) # wide allowed
Op('iload_0',         0x1a, 0,  1) # wide allowed
Op('iload_1',         0x1b, 0,  1) # wide allowed
Op('iload_2',         0x1c, 0,  1) # wide allowed
Op('iload_3',         0x1d, 0,  1) # wide allowed
Op('imul',            0x68, 0, -1)
Op('ineg',            0x74, 0,  0)
Op('instanceof',      0xc1, 2,  0)
# FIXME stack pop count for args, also rule that operand 3 must be zero?
Op('invokeinterface', 0xb9, 4,  None)
# FIXME stack pop count for args
Op('invokespecial',   0xb7, 2,  None)
# FIXME stack pop count for args
Op('invokestatic',    0xb8, 2,  None)
# FIXME stack pop count for args
Op('invokevirtual',   0xb6, 2,  None)
Op('ior',             0x80, 0, -1)
Op('irem',            0x70, 0, -1)
# What happens if there's a float on the stack instead? Find out.
Op('ireturn',         0xac, 0, -1) # return int
Op('ishl',            0x78, 0, -1)
Op('ishr',            0x7a, 0, -1)
# istore
Op('istore',          0x36, 1, -1)
Op('istore_0',        0x3b, 0, -1)
Op('istore_1',        0x3c, 0, -1)
Op('istore_2',        0x3d, 0, -1)
Op('istore_3',        0x3e, 0, -1)
Op('isub',            0x64, 0, -1)
Op('iushr',           0x7c, 0, -1)
Op('ixor',            0x82, 0, -1)

Op('jsr',             0xa8, 2,  1)
Op('jsr_w',           0xc9, 4,  1)

Op('l2d',             0x8a, 0,  0)
Op('l2f',             0x89, 0, -1) # shrinker
Op('l2i',             0x88, 0, -1) # 
Op('ladd',            0x61, 0, -2)
Op('laload',          0x2f, 0,  0)
Op('land',            0x7f, 0, -2)
Op('lastore',         0x50, 0, -4)
Op('lcmp',            0x94, 0, -3)
Op('lconst_0',        0x09, 0,  2)
Op('lconst_1',        0x0a, 0,  2)
Op('ldc',             0x12, 1,  1)
Op('ldc_w',           0x13, 2,  1)
Op('ldc2_w',          0x14, 2,  2)
Op('ldiv',            0x6d, 0, -2)
Op('lload',           0x16, 1,  2)
Op('lload_0',         0x1e, 0,  2)
Op('lload_1',         0x1f, 0,  2)
Op('lload_2',         0x20, 0,  2)
Op('lload_3',         0x21, 0,  2)
Op('lmul',            0x69, 0, -2)
Op('lneg',            0x75, 0,  0)
# TODO figure out how to implement lookupswitch.
# Op('lookupswitch', 0xab, None, -1)
Op('lor',             0x81, 0, -2)
Op('lrem',            0x71, 0, -2)
# TODO returns clear stack, ignore their deltas or..?
Op('lreturn',         0xad, 0, -2)
Op('lshl',            0x79, 0, -1)
Op('lshr',            0x7b, 0, -1)
Op('lstore',          0x37, 1, -2)
Op('lstore_0',        0x3f, 0, -2)
Op('lstore_1',        0x40, 0, -2)
Op('lstore_2',        0x41, 0, -2)
Op('lstore_3',        0x42, 0, -2)
Op('lsub',            0x65, 0, -2)
Op('lushr',           0x7d, 0, -1)
Op('lxor',            0x83, 0, -1)

Op('monitorenter',    0xc2, 0, -1)
Op('monitorexit',     0xc3, 0, -1)
Op('multinewarray',   0xc5, 3,  None) # stack pop count from dimensions?

Op('new',             0xbb, 2,  1)
Op('newarray',        0xbc, 1,  0)
Op('nop',             0x00, 0,  0)

Op('pop',             0x57, 0, -1)
Op('pop2',            0x58, 0, -2)
Op('putfield',        0xb5, 2, -2)
Op('putstatic',       0xb3, 2, -1)

Op('ret',             0xa9, 1,  0)
Op('return',          0xb1, 0,  0) # return void

Op('saload',          0x35, 0, -1)
Op('sastore',         0x56, 0, -3)
Op('sipush',          0x11, 2,  1)
Op('swap',            0x5f, 0,  0) # note lack of swap2

# TODO figure out how to implement tableswitch
# Op('tableswitch',     0xaa, None, -1)

# TODO figure out how to implement wide
# Op('wide',            0xc4, None, None)

# arguments to newarray
T_BOOLEAN =  4
T_CHAR    =  5
T_FLOAT   =  6
T_DOUBLE  =  7
T_BYTE    =  8
T_SHORT   =  9
T_INT     = 10
T_LONG    = 11

