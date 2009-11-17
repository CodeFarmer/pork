#! /usr/bin/env python

import unittest
from unittest import TestCase

from antlr3 import ANTLRInputStream, CommonTokenStream

from PorkLexer import PorkLexer
from Pork import Pork, classDefs

from classfile import SourceFile_attribute, Code_attribute, LineNumberTable_attribute


def getSourceFileAttribute(clazz):

    for attr in clazz.attributes:
        if isinstance(attr, SourceFile_attribute):
            return attr

    return None

# FIXME these are in multiple tests, write a superclass
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


SOURCE_FILE = 'prk/33-line-number-tables.prk'

class DebugInfotest(TestCase):

    def setUp(self):

        # this is crap a sign that bug #31 is on the money
        classDefs.clear()

        lexer = PorkLexer(ANTLRInputStream(open(SOURCE_FILE)))
        parser = Pork(CommonTokenStream(lexer))
        parser.porkfile()

        self.clazz = classDefs['org.joellercoaster.pork.LineNumbers']
        self.clazz.setSourceFile(SOURCE_FILE)



    def testClassFileAttributeSetting(self):

        self.assertEquals(SOURCE_FILE, getSourceFileAttribute(self.clazz).sourceFile)

    def testResettingSourceFileRaisesException(self):

        try:
            self.clazz.setSourceFile('something.prk');
            self.fail('Attempting to reset the class file attribute on a class should raise an exception')

        except:
            None

    def testLineNumberInfoGenerated(self):

        code = getCodeAttribute(findMethod(self.clazz, 'countDownToZero'))
        for attr in code.attributes:
            if isinstance(attr, LineNumberTable_attribute):
                return

        self.fail('Code attribute for countDownToZero() did not itself have a line number table attribute')
            

if __name__ == '__main__':
    unittest.main()

