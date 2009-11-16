#! /usr/bin/env python

import unittest
from unittest import TestCase

from antlr3 import ANTLRInputStream, CommonTokenStream

from PorkLexer import PorkLexer
from Pork import Pork, classDefs

from classfile import SourceFile_attribute


def getSourceFileAttribute(clazz):

    for attr in clazz.attributes:
        if isinstance(attr, SourceFile_attribute):
            return attr

    return None

SOURCE_FILE = '33-line-number-tables.prk'

def DebugInfotest(TestCase):

    def setUp(self):

        lexer = PorkLexer(ANTLRInputStream(open(SOURCE_FILE)))
        parser = Pork(CommonTokenStream(lexer))
        parser.porkfile()

        self.clazz = classDefs['org.joellercoaster.pork.LineNumbers']

    def testClassFileAttributeSetting(self):

        self.assertEquals(SOURCE_FILE, getSourceFileAttribute(self.clazz).sourceFile)

    def testResettingSourceFileRaisesException(self):

        try:
            self.clazz.setSourceFile('something.prk');
            self.fail('Attempting to reset the class file attribute on a class should raise an exception')

        except:
            None
            
        


if __name__ == '__main__':
    unittest.main()

