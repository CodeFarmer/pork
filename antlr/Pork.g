/*
 * Joel's combination pork grammar and ANTLR learning sandbox, bear with me.
 */

grammar Pork;

options {
    language=Python;
}


tokens {
     COLON     = ':'  ;
     SEMICOLON = ';'  ;
     NEWLINE   = '\n' ;
     DOT       = '.'  ;
}


@header {
import sys
import traceback

from PorkLexer import PorkLexer
}


LETTER      : 'a'..'b' | 'A'..'Z' ;
DIGIT       : '0'..'9' ;
HEXDIGIT    : DIGIT | 'A'..'E' | 'a'..'e' ;

labelDef    : label COLON NEWLINE ;
instruction : offset? opcode argument* comment? NEWLINE;

offset      : integer ;
integer     : (DIGIT)+ | '0x' (HEXDIGIT HEXDIGIT)+ ;

comment     : SEMICOLON .* ;

argument    : (integer | label) ;

opcode      : LETTER+ ;
label       : LETTER+ ;
