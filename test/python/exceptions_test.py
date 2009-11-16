#! /usr/bin/env python

import unittest
from unittest import TestCase

from antlr3 import ANTLRInputStream, CommonTokenStream

from PorkLexer import PorkLexer
from Pork import Pork, classDefs

from classfile import CONSTANT_Fieldref, CONSTANT_Integer
from classfile import Code_attribute


def findMethod(clazz, name):
    
    for m in clazz.methods:
        if clazz.constant_pool[m.name_index - 1].value == name:
            return m

    return None

def getCodeAttribute(method):

    for attr in method.attributes:
        if isinstance(attr, Code_attribute):
            return attr

    return None

class ExceptionsTest(TestCase):


    def setUp(self):

        lexer = PorkLexer(ANTLRInputStream(open('prk/24-exceptions.prk')))
        parser = Pork(CommonTokenStream(lexer))
        parser.porkfile()

        self.clazz = classDefs['org.joellercoaster.pork.Exceptions']

    def testExceptionTableGenerated(self):

        meth = findMethod(self.clazz, 'dereferenceNullWithCatch')

        self.assertTrue(meth != None)

        extable = getCodeAttribute(meth).exception_table

        self.assertTrue(len(extable) > 0)


if __name__ == '__main__':
    unittest.main()



 
