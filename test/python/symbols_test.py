#! /usr/bin/env python

import unittest
from unittest import TestCase

from antlr3 import ANTLRInputStream, CommonTokenStream

from PorkLexer import PorkLexer
from Pork import Pork, classDefs

from classfile import CONSTANT_Fieldref, CONSTANT_Integer


class SymbolsTest(TestCase):


    def setUp(self):

        lexer = PorkLexer(ANTLRInputStream(open('prk/26-unused-constants.prk')))
        parser = Pork(CommonTokenStream(lexer))
        parser.porkfile()

        self.clazz = classDefs['org.joellercoaster.pork.UnusedConstants']


    def findFieldInfo(self, fieldName, typeDesc):

        for const in self.clazz.constant_pool:

            if const.tag == CONSTANT_Fieldref:

                classConst = self.clazz.constant_pool[const.value - 1]
                cnameConst = self.clazz.constant_pool[classConst.value - 1]
                nAndTConst = self.clazz.constant_pool[const.secondValue - 1]
                nameConst  = self.clazz.constant_pool[nAndTConst.value - 1]
                typeConst  = self.clazz.constant_pool[nAndTConst.secondValue - 1]

                if cnameConst.value == unicode(self.clazz.name.replace('.', '/')) and nameConst.value == unicode(fieldName) and typeConst.value == unicode(typeDesc):
                    return const

        return None


    def findConstantInt(self, value):

        for const in self.clazz.constant_pool:

            if const.tag == CONSTANT_Integer and const.value == value:
                return const

        return None


    def testUsedSymbolInClass(self):

        self.assertTrue(self.findConstantInt(1) != None)

    def testUnusedSymbolNotInClass(self):
        
        self.assertTrue(self.findConstantInt(2) == None)


    def testUsedAutoFieldRefInClass(self):

        self.assertTrue(self.findFieldInfo('fieldA', 'I') != None)

    def testUnsedAutoFieldRefNotInClass(self):

        self.assertTrue(self.findFieldInfo('fieldB', 'I') == None)


if __name__ == '__main__':
    unittest.main()

