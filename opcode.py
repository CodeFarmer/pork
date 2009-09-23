#! /usr/bin/env python

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


class UnknownOperation(Exception):

    def __init__(self, name):
        assert isinstance(name, basestring)
        self.name = name

    def __str__(self):
        return self.name


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


addOperation(Op('aaload',          0x32, 0, -1))
addOperation(Op('aastore',         0x53, 0, -3))
addOperation(Op('aconst_null',     0x01, 0,  1))
# aload can't be used to load returnAddress
addOperation(Op('aload',           0x19, 1,  1))
addOperation(Op('aload_0',         0x2a, 0,  1))
addOperation(Op('aload_1',         0x2b, 0,  1))
addOperation(Op('aload_2',         0x2c, 0,  1))
addOperation(Op('aload_3',         0x2d, 0,  1))
addOperation(Op('anewarray',       0xbd, 2,  0))
addOperation(Op('areturn',         0xb0, 0, -1))
addOperation(Op('arraylength',     0xbe, 0,  0))
# astore is used to write returnAddress as well as reference
addOperation(Op('astore',          0x3a, 1, -1))
addOperation(Op('astore_0',        0x4b, 0, -1))
addOperation(Op('astore_1',        0x4c, 0, -1))
addOperation(Op('astore_2',        0x4d, 0, -1))
addOperation(Op('astore_3',        0x4e, 0, -1))
addOperation(Op('athrow',          0xbf, 0,  0))

addOperation(Op('baload',          0x33, 0, -1))
addOperation(Op('bastore',         0x54, 0, -3))
addOperation(Op('bipush',          0x10, 1,  1))

addOperation(Op('caload',          0x34, 0, -1))
addOperation(Op('castore',         0x55, 0, -3))
addOperation(Op('checkcast',       0xc0, 2,  0))

addOperation(Op('d2f',             0x90, 0,  0))
addOperation(Op('d2i',             0x8e, 0,  0))
addOperation(Op('d2l',             0x8f, 0,  0))
addOperation(Op('dadd',            0x63, 0, -1))
addOperation(Op('daload',          0x31, 0, -1))
addOperation(Op('dastore',         0x52, 0, -3))
addOperation(Op('dcmpg',           0x98, 0, -1))
addOperation(Op('dcmpl',           0x97, 0, -1))
addOperation(Op('dconst_0',        0x0e, 0,  1))
addOperation(Op('dconst_1',        0x0f, 0,  1))
addOperation(Op('ddiv',            0x6f, 0, -1))
addOperation(Op('dload',           0x18, 1,  1))
addOperation(Op('dload_0',         0x26, 0,  1))
addOperation(Op('dload_1',         0x27, 0,  1))
addOperation(Op('dload_2',         0x28, 0,  1))
addOperation(Op('dload_3',         0x29, 0,  1))
addOperation(Op('dmul',            0x6b, 0, -1))
addOperation(Op('dneg',            0x77, 0,  0))
addOperation(Op('drem',            0x73, 0, -1))
addOperation(Op('dreturn',         0xaf, 0, -1))
addOperation(Op('dstore',          0x39, 1, -1))
addOperation(Op('dstore_0',        0x47, 0, -1))
addOperation(Op('dstore_1',        0x48, 0, -1))
addOperation(Op('dstore_2',        0x49, 0, -1))
addOperation(Op('dstore_3',        0x4a, 0, -1))
addOperation(Op('dsub',            0x67, 0, -1))
addOperation(Op('dup',             0x59, 0,  1))
addOperation(Op('dup_x1',          0x5a, 0,  1))
addOperation(Op('dup_x2',          0x5b, 0,  1)) # beware type categories
addOperation(Op('dup2',            0x5c, 0,  2)) #
addOperation(Op('dup2_x1',         0x5d, 0,  2)) # 
addOperation(Op('dup2_x2',         0x5e, 0,  2)) #

addOperation(Op('i2b',             0x91, 0,  0))
addOperation(Op('i2c',             0x92, 0,  0))
addOperation(Op('i2d',             0x87, 0,  0))
addOperation(Op('i2f',             0x86, 0,  0))
addOperation(Op('i2l',             0x85, 0,  0))
addOperation(Op('i2s',             0x93, 0,  0))
addOperation(Op('iadd',            0x60, 0, -1))
addOperation(Op('iaload',          0x2e, 0, -1))
addOperation(Op('iand',            0x7e, 0, -1))
addOperation(Op('iastore',         0x4f, 0, -3))
# bipush <i>
addOperation(Op('iconst_m1',       0x02, 0,  1))
addOperation(Op('iconst_0',        0x03, 0,  1))
addOperation(Op('iconst_1',        0x04, 0,  1))
addOperation(Op('iconst_2',        0x05, 0,  1))
addOperation(Op('iconst_3',        0x06, 0,  1))
addOperation(Op('iconst_4',        0x07, 0,  1))
addOperation(Op('iconst_5',        0x08, 0,  1))
addOperation(Op('idiv',            0x6c, 0, -1))
addOperation(Op('if_acmpeq',       0xa5, 2, -2))
addOperation(Op('if_acmpne',       0xa6, 2, -2))
# integer comparison
addOperation(Op('if_icmpeq',       0x9f, 2, -2))
addOperation(Op('if_icmpne',       0xa0, 2, -2))
addOperation(Op('if_icmplt',       0xa1, 2, -2))
addOperation(Op('if_icmpge',       0xa2, 2, -2))
addOperation(Op('if_icmpgt',       0xa3, 2, -2))
addOperation(Op('if_icmple',       0xa4, 2, -2))
# integer comparison with zero
addOperation(Op('ifeq',            0x99, 2, -1))
addOperation(Op('ifge',            0x9c, 2, -1))
addOperation(Op('ifgt',            0x9d, 2, -1))
addOperation(Op('ifle',            0x9e, 2, -1))
addOperation(Op('iflt',            0x9b, 2, -1))
addOperation(Op('ifne',            0x9a, 2, -1))
addOperation(Op('ifnonnull',       0xc7, 2, -1))
addOperation(Op('ifnull',          0xc6, 2, -1))
addOperation(Op('iinc',            0x84, 2,  0))
# iload
addOperation(Op('iload',           0x15, 1,  1)) # wide allowed
addOperation(Op('iload_0',         0x1a, 0,  1)) # wide allowed
addOperation(Op('iload_1',         0x1b, 0,  1)) # wide allowed
addOperation(Op('iload_2',         0x1c, 0,  1)) # wide allowed
addOperation(Op('iload_3',         0x1d, 0,  1)) # wide allowed
addOperation(Op('imul',            0x68, 0, -1))
addOperation(Op('ineg',            0x74, 0,  0))
addOperation(Op('instanceof',      0xc1, 2,  0))
# FIXME stack pop count for args, also rule that operand 3 must be zero?
addOperation(Op('invokeinterface', 0xb9, 4,  None))
# FIXME stack pop count for args
addOperation(Op('invokespecial',   0xb7, 2,  None))
# FIXME stack pop count for args
addOperation(Op('invokestatic',    0xb8, 2,  None))
# FIXME stack pop count for args
addOperation(Op('invokevirtual',   0xb6, 2,  None))
addOperation(Op('ior',             0x80, 0, -1))
addOperation(Op('irem',            0x70, 0, -1))
# What happens if there's a float on the stack instead? Find out.
addOperation(Op('ireturn',         0xac, 0, -1)) # return int
addOperation(Op('ishl',            0x78, 0, -1))
addOperation(Op('ishr',            0x7a, 0, -1))
# istore
addOperation(Op('istore',          0x36, 1, -1))
addOperation(Op('istore_0',        0x3b, 0, -1))
addOperation(Op('istore_1',        0x3c, 0, -1))
addOperation(Op('istore_2',        0x3d, 0, -1))
addOperation(Op('istore_3',        0x3e, 0, -1))
addOperation(Op('isub',            0x64, 0, -1))
addOperation(Op('iushr',           0x7c, 0, -1))
addOperation(Op('ixor',            0x82, 0, -1))

addOperation(Op('return',          0xb1, 0,  0)) # return void


