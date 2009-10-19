#! /usr/bin/env python


import sys

from antlr3.main import ParserMain
from Pork import Pork


def main(argv, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr):
    main = ParserMain("PorkLexer", Pork)
    main.stdin = stdin
    main.stdout = stdout
    main.stderr = stderr
    main.execute(argv)


if __name__ == '__main__':
    main(sys.argv)

