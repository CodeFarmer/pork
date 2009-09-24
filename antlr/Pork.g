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

/* Parser */

porkfile : line+ ;
line     : (labeldef | classDef)? comment? NEWLINE ;

labeldef : label COLON ;
label    : WORD ;

className : WORD (DOT WORD)* ;
classDef : CLASS className ;

comment : SEMICOLON .* ;
/* Lexer */

fragment LETTER : 'a'..'z' | 'A'..'Z' ;
WORD   : (LETTER | '_')+ ;
CLASS  : '.class' ;

WHITESPACE : ( '\t' | ' ' | '\u000C' )+ { $channel = HIDDEN; } ;


