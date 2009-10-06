lexer grammar PorkLexer;

options {
    language=Python;
    filter=true;
}

CLASS  : '.class' ;
METHOD : '.method' ;
STACK  : '.stack' ;
LOCAL  : '.local' ;

COLON        : ':' ;
SEMICOLON    : ';' ;
/* NEWLINE      : '\n'; */
DOT          : '.' ;
LEFTBRACKET  : '(' ;
RIGHTBRACKET : ')' ;
LEFTSQUARE   : '[' ;
RIGHTSQUARE  : ']' ;
SINGLEQUOTE  : '\'';
COMMA        : ',' ;

/*
AM_PUBLIC    : 'public' ;
AM_PRIVATE   : 'private' ;
AM_PROTECTED : 'protected' ;
AM_STATIC    : 'static' ;
AM_FINAL     : 'final' ;
AM_INTERFACE : 'interface' ;
*/

fragment LETTER   : 'a'..'z' | 'A'..'Z' ;
fragment DIGIT    : '0'..'9' ;
fragment HEXDIGIT : '0'..'9' | 'A..E' | 'a'..'e' ;
fragment HEX_PREFIX : '0x' ;

/* TODO return the actual integer, and allow non-hex (not in that order) */
INTEGER : HEX_PREFIX (HEXDIGIT HEXDIGIT)+ ;

/* Consider not having these as tokens? */
T_INT  : 'int'  ;
T_VOID : 'void' ;

WORD   : (LETTER | '_') (LETTER | '_' | DIGIT)* ;

WHITESPACE : ( '\t' | '\r' | '\n' | ' ' | '\u000C' )+ { $channel = HIDDEN; } ;


