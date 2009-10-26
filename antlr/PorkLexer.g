lexer grammar PorkLexer;

options {
    language=Python;
    filter=true;
}

CLASS    : '.class'    ;
METHOD   : '.method'   ;
FIELD    : '.field'    ;
STACK    : '.stack'    ;
LOCAL    : '.local'    ;
CONSTANT : '.constant' ;

ARRAYDIM : '[]' ;

COLON        : ':' ;
SEMICOLON    : ';' ;
/* NEWLINE      : '\n'; */
DOT          : '.' ;
LEFTBRACKET  : '(' ;
RIGHTBRACKET : ')' ;
COMMA        : ',' ;
DOLLAR       : '$' ;
AT           : '@' ;
EQUALS       : '=' ;
fragment MINUS        : '-' ;

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

INIT   : '<init>'   ;
CLINIT : '<clinit>' ;

STRING_LITERAL : QUOTE .* QUOTE ;

FLOAT_LITERAL : MINUS? DIGIT+ DOT DIGIT+ ;

/* TODO return the actual integer, and allow non-hex (not in that order) */
HEX_INTEGER : MINUS? HEX_PREFIX (HEXDIGIT HEXDIGIT)+ ;
DEC_INTEGER : MINUS? DIGIT+ ;

T_BOOL   : 'boolean' ;
T_BYTE   : 'byte'   ;
T_CHAR   : 'char'   ;
T_DOUBLE : 'double' ;
T_FLOAT  : 'float'  ;
T_INT    : 'int'    ;
T_LONG   : 'long'   ;
T_SHORT  : 'short'  ;
T_VOID   : 'void'   ;

A_PUBLIC    : 'public'    ;
A_PROTECTED : 'protected' ;
A_PRIVATE   : 'private'   ;
A_STATIC    : 'static'    ;
A_FINAL     : 'final'     ;

WORD   : (LETTER | '_') (LETTER | '_' | DIGIT)* ;

WHITESPACE : ( '\t' | '\r' | '\n' | ' ' | '\u000C' )+ { $channel = HIDDEN; } ;


