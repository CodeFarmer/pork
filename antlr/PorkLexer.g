lexer grammar PorkLexer;

options {
    language=Python;
    filter=true;
}

CLASS  : '.class' ;
METHOD : '.method' ;
STACK  : '.stack' ;
LOCAL  : '.local' ;

ARRAYDIM : '[]' ;

COLON        : ':' ;
SEMICOLON    : ';' ;
/* NEWLINE      : '\n'; */
DOT          : '.' ;
LEFTBRACKET  : '(' ;
RIGHTBRACKET : ')' ;
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

fragment QUOTE        : '"';

STRING_LITERAL : QUOTE .* QUOTE ;

/* TODO return the actual integer, and allow non-hex (not in that order) */
INTEGER : HEX_PREFIX (HEXDIGIT HEXDIGIT)+ ;

T_BOOL   : 'boolean' ;
T_BYTE   : 'byte'   ;
T_CHAR   : 'char'   ;
T_DOUBLE : 'double' ;
T_FLOAT  : 'float'  ;
T_INT    : 'int'    ;
T_LONG   : 'long'   ;
T_SHORT  : 'short'  ;
T_VOID   : 'void'   ;

A_PUBLIC : 'public' ;
A_STATIC : 'static' ;

WORD   : (LETTER | '_') (LETTER | '_' | DIGIT)* ;

WHITESPACE : ( '\t' | '\r' | '\n' | ' ' | '\u000C' )+ { $channel = HIDDEN; } ;


