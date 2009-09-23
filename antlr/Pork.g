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
}


@header {
import sys
import traceback

from PorkLexer import PorkLexer
}


LETTER      : 'a'..'b' | 'A'..'Z' ;
DIGIT       : '0'..'9' ;
HEXDIGIT    : DIGIT | 'A'..'E' | 'a'..'e' ;

basicType : 'boolean' | 'char' | 'double' | 'float' | 'int' | 'long' ;
void      : 'void' ;

labelDef    : label COLON NEWLINE ;
instruction : offset? opcode argument* comment? NEWLINE;
directive   : DOT (classDirective | methodDirective | staticMethodDirective ) NEWLINE;

classDirective  : 'class' className ;
className       : word (DOT word)*  ;
typeName : className | basicType ;
arrayTypeName : typeName LEFTSQUARE RIGHTSQUARE ;

methodDirective       : 'method' methodDescriptor ;
staticMethodDirective : 'staticMethod' methodDescriptor ;
methodDescriptor      : (typeName | void) word LEFTBRACKET typeDescriptor* RIGHTBRACKET ;
typeDescriptor : typeName | arrayTypeName ;

offset  : integer ;
integer : (DIGIT)+ | '0x' (HEXDIGIT HEXDIGIT)+ ;

comment  : SEMICOLON .* ;

argument : (integer | label) ;

opcode   : LETTER+ ;
word     : (LETTER | '_')+ ;
label    : word ;

