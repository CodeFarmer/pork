#! /usr/bin/env python

from io import IOBase

import struct

import opcode

MAGIC = 0xcafebabe
MINOR_VERSION = 0x00
MAJOR_VERSION = 0x31

# access flags
ACC_PUBLIC    = 0x0001 # class-applicable
ACC_PRIVATE   = 0x0002
ACC_PROTECTED = 0x0004
ACC_STATIC    = 0x0008
ACC_FINAL     = 0x0010 #
ACC_SUPER     = 0x0020 #
ACC_VOLATILE  = 0x0040
ACC_TRANSIENT = 0x0080
ACC_INTERFACE = 0x0200 #
ACC_ABSTRACT  = 0x0400 #

# Field descriptors
DESC_BYTE    = 'B'
DESC_CHAR    = 'C'
DESC_DOUBLE  = 'D'
DESC_FLOAT   = 'F'
DESC_INT     = 'I'
DESC_LONG    = 'J'
DESC_SHORT   = 'S'
DESC_BOOLEAN = 'Z'
DESC_VOID    = 'V'

# to start with, String and Integer constants will be implemented and that's
# all:

# constant tags
CONSTANT_Class              =  7
#CONSTANT_Fieldref           =  9
#CONSTANT_Methodref          = 10
#CONSTANT_InterfaceMethodRef = 11
CONSTANT_String             =  8
CONSTANT_Integer            =  3
#CONSTANT_Float              =  4
#CONSTANT_Long               =  5
#CONSTANT_Double             =  6
#CONSTANT_NameAndType        = 12
CONSTANT_Utf8               =  1

ATTR_CODE = 'Code'


def u1(num):
    return struct.pack('B', 0x000000ff & num)

def u2(num):
    return struct.pack('BB', (0x0000ff00 & num) >> 8,
                              0x000000ff & num)

def u4(num):

    return struct.pack('BBBB', (0xff000000 & num) >> 24,
                               (0x00ff0000 & num) >> 16,
                               (0x0000ff00 & num) >> 8,
                               0x000000ff & num)

def fieldDescriptor(classname, arrayDimension = 0):
    
    ret = ''
    for i in range(arrayDimension):
        ret += '['

    ret += 'L'
    ret += classname.replace('.', '/')
    ret += ';'

    return ret

# fieldTypes and returnType should be a list of either DESC_FOO or returns
# from fieldDescriptor
def methodDescriptor(returnType = DESC_VOID, fieldTypes = []):

    ret = '('
    for fieldType in fieldTypes:
        ret += fieldType

    ret += ')'
    ret += returnType

    return ret

def getPos(stream):
    return '0x' + format(stream.tell(), 'x')

class JavaClass:

    def __init__(self, classname, superclass = 'java.lang.Object', access_flags = ACC_PUBLIC):

        assert isinstance(classname, basestring)

        self.constant_pool = []

        self.this_class  = self.classConstant(classname)
        self.super_class = self.classConstant(superclass)

        self.access_flags = access_flags;

        self.interfaces = []
        self.fields = []
        self.methods = []
        self.attributes = []

    # the next methods are to ensure reuse of constant values
    def utf8Constant(self, value):

        index = 0
        unicodeValue = unicode(value, 'utf-8')

        for const in self.constant_pool:

            if const.tag == CONSTANT_Utf8 and const.value == unicodeValue:
                return index + 1
            else:
                index += 1

        self.constant_pool.append(CONSTANT_Utf8_info(unicodeValue))
        return index + 1

    def integerConstant(self, value):

        index = 0;
        integerValue = int(value)

        for const in self.constant_pool:

            if const.tag == CONSTANT_Integer and const.value == integerValue:
                return index + 1
            else:
                index += 1

        self.constant_pool.append(CONSTANT_Integer_info(integerValue))
        return index + 1

    # FIXME refactor this and class and whatever to just switch on tag
    def stringConstant(self, value):
        
        utf8Index = self.utf8Constant(value)
        index = 0

        for const in self.constant_pool:

            if const.tag == CONSTANT_String and const.index == utf8Index:
                return index + 1
            else:
                index += 1

        self.constant_pool.append(CONSTANT_String_info(utf8Index))
        return index + 1

    def classConstant(self, value):

        utf8Index = self.utf8Constant(value.replace('.', '/'))
        index = 0

        for const in self.constant_pool:

            if const.tag == CONSTANT_Class and const.value == utf8Index:
                return index + 1
            else:
                index += 1

        self.constant_pool.append(CONSTANT_Class_info(utf8Index))
        return index + 1

    # interface implementation

    def implementedInterface(self, name):
        index = self.classConstant(name)

        if index not in self.interfaces:
            self.interfaces.append(index)

    def field(self, name, descriptor, access_flags = ACC_PUBLIC, attributes = []):
        # FIXME check for name clashes!
        self.fields.append(field_info(self, name, descriptor, access_flags, attributes))

    def method(self, name, descriptor, access_flags, attributes):
        # TODO assert the code attribute is present
        # FIXME check for clashes!
        self.methods.append(method_info(self, name, descriptor, access_flags, attributes))
 

    # stream output

    def write(self, stream):

        assert isinstance(stream, IOBase)
        
        stream.write(u4(MAGIC))
        stream.write(u2(MINOR_VERSION))
        stream.write(u2(MAJOR_VERSION))
        
        stream.write(u2(len(self.constant_pool) + 1))

        for constant in self.constant_pool:
            print "writing constant " + `constant` + " at " + getPos(stream)
            constant.write(stream)

        stream.write(u2(self.access_flags))
        stream.write(u2(self.this_class))
        stream.write(u2(self.super_class))

        stream.write(u2(len(self.interfaces)))
        for interface in self.interfaces:
            stream.write(u2(interface))

        stream.write(u2(len(self.fields)))
        for field in self.fields:
            print "writing field " + `field`  + " at " + getPos(stream)
            field.write(stream)

        stream.write(u2(len(self.methods)))
        for method in self.methods:
            print "writing method " + `method` + " at " + getPos(stream)
            method.write(stream)

        
        print "writing attribute count 0x" + format(len(self.attributes), 'x') + " at " + getPos(stream)
        stream.write(u2(len(self.attributes)))
        for attribute in self.attributes:
            print "writing class attribute " + `attribute` + " at " + getPos(stream)
            attribute.write(stream)


class ConstantTableEntry(object):

    def __init__(self, tag):

        assert isinstance(tag, int)

        self.tag = tag
        self.value = None
        self.bytes = []

    def write(self, stream):
        stream.write(u1(self.tag))
        stream.write(self.bytes)


class CONSTANT_Utf8_info(ConstantTableEntry):
    
    def __init__(self, value): # value is some Python string

        assert isinstance(value, unicode)

        ConstantTableEntry.__init__(self, CONSTANT_Utf8)
        self.value = value
        self.bytes = self.value.encode('utf-8')

    def write(self, stream):
        stream.write(u1(self.tag))
        l = len(self.bytes)
        stream.write(u2(l))
        stream.write(self.bytes)


class CONSTANT_Integer_info(ConstantTableEntry):
    
    def __init__(self, value):

        assert isinstance(value, int)

        ConstantTableEntry.__init__(self, CONSTANT_Integer)

        # value is already an integer
        self.value = value # int(value)
        self.bytes = u4(value)


# base class for the various magic string structures

class ConstantStringTableEntry(ConstantTableEntry):

    def __init__(self, tag, index):

        assert isinstance(index, int) and index >= 0
        
        ConstantTableEntry.__init__(self, tag)
        self.value = index
        self.bytes = u2(index)

class CONSTANT_String_info(ConstantStringTableEntry):
    
    def __init__(self, index):

        ConstantStringTableEntry.__init__(self, CONSTANT_String, index)


class CONSTANT_Class_info(ConstantStringTableEntry):

    def __init__(self, index):

        ConstantStringTableEntry.__init__(self, CONSTANT_Class, index)

# attributes
# TODO wire this into class and utility methods

class attrib_info(object):
    
    def __init__(self, owningClass, name, info):

        # FIXME assert that info is a byte array
        
        self.name_index = owningClass.utf8Constant(name)
        self.info = info

    def write(self, stream):
        stream.write(u2(self.name_index))
        stream.write(u4(len(self.info)))
        stream.write(self.info)


SIZE_OF_EXCEPTION_TABLE_ENTRY = 8

EMPTY_METHOD = u1(opcode.getOperation('return').opcode)

class Code_attribute(object):

    def __init__(self, owningClass, max_stack = 0, max_locals = 0, code = EMPTY_METHOD, exception_table = [], attributes = []):

        self.attribute_name_index = owningClass.utf8Constant(ATTR_CODE)

        # Size of max_stack, max_locals, code_length, exception_table_length,
        # attributes_count = 12.
        # Size of attribute.name_index, length = 6
        self.attribute_length = len(code) + SIZE_OF_EXCEPTION_TABLE_ENTRY * len (exception_table) + reduce(lambda x, y: x + len(y.info) + 6, attributes, 0) + 12

        self.max_stack       = max_stack
        self.max_locals      = max_locals
        self.code            = code
        self.exception_table = exception_table
        self.attributes      = attributes

    def write(self, stream):

        print 'Writing ' + `self` + ' at ' + getPos(stream) + ': ' + `self.attribute_name_index` + ', ' + `self.attribute_length`
        
        stream.write(u2(self.attribute_name_index))
        stream.write(u4(self.attribute_length))
        stream.write(u2(self.max_stack))
        stream.write(u2(self.max_locals))
        stream.write(u4(len(self.code)))
        stream.write(self.code)
        stream.write(u2(len(self.exception_table)))
        for exception in self.exception_table:
            exception.write(stream)

        stream.write(u2(len(self.attributes)))
        for attribute in self.attributes:
            attribute.write(stream)


# fields

class field_info(object):
    
    def __init__(self, owningClass, name, descriptor, access_flags, attributes):
        
        self.name_index       = owningClass.utf8Constant(name)
        self.descriptor_index = owningClass.utf8Constant(descriptor)

        self.access_flags = access_flags
        self.attributes = attributes

    def write(self, stream):

        # print '  writing field access flags ' + format(self.access_flags, 'x') + ' at ' + getPos(stream)

        stream.write(u2(self.access_flags))
        stream.write(u2(self.name_index))
        stream.write(u2(self.descriptor_index))

        stream.write(u2(len(self.attributes)))
        for attrib in self.attributes:
            attrib.write(stream)

# methods


class method_info(field_info):
    None



