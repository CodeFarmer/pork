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

porkfile : line+ ;
line     : (labeldef | classDef | methodDef)? comment? NEWLINE ;

labeldef : label COLON ;
label    : WORD ;

className : WORD (DOT WORD)* ;

classDef returns [clazz]
    : CLASS c=className { $clazz = classDef($c.text); } ;

/* only empty method defs so far */
methodDef returns [method]
    : METHOD /* accessModifier* */ m=methodName LEFTBRACKET RIGHTBRACKET { $method = currentClass.method($m.text, methodDescriptor(), ACC_PUBLIC | ACC_STATIC, []) ; } ;

methodName : WORD ;

/* accessModifier : PUBLIC | PRIVATE | PROTECTED | STATIC | FINAL | INTERFACE | ABSTRACT ; */

comment : SEMICOLON .* ;

/* Lexer */

fragment LETTER   : 'a'..'z' | 'A'..'Z' ;
fragment HEXDIGIT : '0..9' | 'A..E' | 'a'..'e' ;

WORD   : (LETTER | '_')+ ;
CLASS  : '.class' ;
METHOD : '.method' ;

INTEGER : HEXDIGIT+ ;

WHITESPACE : ( '\t' | ' ' | '\u000C' )+ { $channel = HIDDEN; } ;


