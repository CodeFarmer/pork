/*
 * Joel's combination pork grammar and ANTLR learning sandbox, bear with me.
 */

grammar Pork;

options {
    language=Python;
}


tokens {
     COLON        = ':' ;
     SEMICOLON    = ';' ;
     NEWLINE      = '\n';
     DOT          = '.' ;
     LEFTBRACKET  = '(' ;
     RIGHTBRACKET = ')' ;
     LEFTSQUARE   = '[' ;
     RIGHTSQUARE  = ']' ;
     SINGLEQUOTE  = '\'';
}


@header {

import logging as log
import sys
import traceback

from classfile import JavaClass
from classfile import methodDescriptor
from classfile import ACC_PUBLIC, ACC_STATIC

from PorkLexer import PorkLexer

# DEBUG
log.basicConfig(level=log.DEBUG)

# each parse can contain multiple classDefs, optionally intermingled
classDefs = {}
currentClass = None

def classDef(className):

    global currentClass

    if not classDefs.has_key(className):
        ret = JavaClass(className)
        classDefs[className] = ret
    else:
        ret = classDefs[className]

    currentClass = ret
    return ret

}

/* Parser */

porkfile  : classDef+ ;
classDef  : classLine methodDef+ ;

methodDef  : methodLine (WORD)* ;

methodLine returns [meth]: METHOD m=methodName LEFTBRACKET RIGHTBRACKET lineEnd { $meth = currentClass.method($m.text, methodDescriptor(), ACC_PUBLIC | ACC_STATIC, []) ; } ;
methodName : WORD;

lineEnd : SEMICOLON ;

classLine returns [clazz]
    : CLASS c=className lineEnd { $clazz = classDef($c.text); } ;

className : WORD (DOT WORD)* ;

/* accessModifier : PUBLIC | PRIVATE | PROTECTED | STATIC | FINAL | INTERFACE | ABSTRACT ; */

/* Lexer */

fragment LETTER   : 'a'..'z' | 'A'..'Z' ;
fragment DIGIT    : '0..9' ;
fragment HEXDIGIT : '0..9' | 'A..E' | 'a'..'e' ;
fragment HEX_PREFIX : '0x' ;

WORD   : (LETTER | '_') (LETTER | '_' | DIGIT)* ;

CLASS  : '.class' ;
METHOD : '.method' ;

INTEGER : HEX_PREFIX (HEXDIGIT HEXDIGIT)+ ;

WHITESPACE : ( '\t' | '\r' | '\n' | ' ' | '\u000C' )+ { $channel = HIDDEN; } ;


