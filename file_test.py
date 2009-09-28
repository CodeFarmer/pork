#! /usr/bin/env python

from io import FileIO
import logging as log
import unittest

from classfile import JavaClass, Code_attribute, fieldDescriptor, methodDescriptor, ACC_PUBLIC, ACC_STATIC, DESC_INT, DESC_VOID

class TestMinimalClass(unittest.TestCase):

    log.basicConfig(level=log.DEBUG)
    
    clazz = JavaClass("org.joellercoaster.Something")

    clazz.implementedInterface("java.io.Serializable")

    clazz.field('name', fieldDescriptor('java/lang.String'))
    clazz.field('number', DESC_INT)

    # FIXME hoo boy does this need refactoring!
    clazz.method('main',
                  methodDescriptor(DESC_VOID,
                                   fieldDescriptor('java/lang.String', 1)),
                  ACC_PUBLIC | ACC_STATIC,
                  [ Code_attribute(clazz, 0, 2) ])

    outfile = FileIO('classes/org/joellercoaster/Something.class', 'w')
    clazz.write(outfile)

if __name__ == '__main__':
    unittest.main()

