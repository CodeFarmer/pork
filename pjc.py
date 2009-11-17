#! /usr/bin/env python


import sys

from antlr3 import ANTLRInputStream, CommonTokenStream
from antlr3.main import ParserMain
from Pork import Pork, writeClasses, classDefs, compileLineNumbers
from PorkLexer import PorkLexer


def main(argv, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr):

    errors = 0

    if len(argv) > 1:

        for arg in argv[1:]:
            lexer = PorkLexer(ANTLRInputStream(open(arg)))
            parser = Pork(CommonTokenStream(lexer))
            parser.porkfile()
            errors += parser._state.syntaxErrors

            if not errors:
                if True:
                    for clazz in classDefs.values():
                        fileName = arg[arg.rfind('/') + 1:]
                        print 'setting file name to ' + fileName
                        clazz.setSourceFile(fileName)
                
                writeClasses()
                classDefs.clear()

    else:

        lexer = PorkLexer(ANTLRInputStream(stdin))
        parser = Pork(CommonTokenStream(lexer))
        parser.porkfile()
        errors = parser._state.syntaxErrors
    

        if not errors:
            writeClasses()
                    
    return errors


if __name__ == '__main__':
    sys.exit(main(sys.argv))

