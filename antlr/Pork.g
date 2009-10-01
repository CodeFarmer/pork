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
     /* NEWLINE      = '\n'; */
     DOT          = '.' ;
     LEFTBRACKET  = '(' ;
     RIGHTBRACKET = ')' ;
     LEFTSQUARE   = '[' ;
     RIGHTSQUARE  = ']' ;
     SINGLEQUOTE  = '\'';
}


@header {

from io import FileIO
import logging as log
import os
import sys
import traceback

from classfile import Code_attribute, JavaClass
from classfile import methodDescriptor
from classfile import ACC_PUBLIC, ACC_STATIC

from jopcode import byteString ;

from PorkLexer import PorkLexer

# DEBUG
log.basicConfig(level=log.DEBUG)
def dump(o):
    if o:
        log.debug('DUMP: ' + `o`)

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

CLASS_OUTPUT_DIR = 'classes/'

def writeClasses():
    
    for className in classDefs.keys():
        log.debug('writing class ' + className)

        # make directory from classname
        path = className.replace('.', '/')
        dirPath = CLASS_OUTPUT_DIR + path[:path.rfind('/')]
        if not os.path.exists(dirPath):
            os.makedirs(dirPath)
                
        # write class file
        outfile = FileIO(CLASS_OUTPUT_DIR + path + '.class', 'w')
        classDefs[className].write(outfile)
        
        # TODO allow parser to be configured properly

}

/* Parser */

porkfile  : classDef+ { writeClasses() ; } ;
classDef  : classLine methodDef+ ;

methodDef returns [meth]
@init { body = '' }
    : m=methodLine s=stackLine l=localLine (op=operation { body += $op.bytes ; } )+ { $meth = currentClass.method($m.methodName, $m.methodDesc, ACC_PUBLIC | ACC_STATIC, [Code_attribute(currentClass, $s.size, $l.size, body)]) ; } ;

stackLine returns [size] : STACK s=INTEGER lineEnd { $size = int($s.text, 16) ; } ;
localLine returns [size] : LOCAL s=INTEGER lineEnd { $size = int($s.text, 16) ; } ;


methodLine returns [methodName, methodDesc]
    : METHOD m=methodName LEFTBRACKET RIGHTBRACKET lineEnd
    {
        $methodName = $m.text ;
        $methodDesc = methodDescriptor(); 
    } ;

methodName : WORD;

lineEnd : SEMICOLON ;

classLine returns [clazz]
    : CLASS c=className lineEnd { $clazz = classDef($c.text); } ;

className : WORD (DOT WORD)* ;

operation returns [bytes]
@init { args = [] }
    : mnemonic=WORD
      (arg=INTEGER { args.append(int($arg.text, 16)) ; } )* 
      lineEnd { $bytes = byteString($mnemonic.text, args) ; } ;

/* accessModifier : PUBLIC | PRIVATE | PROTECTED | STATIC | FINAL | INTERFACE | ABSTRACT ; */

/* Lexer */

fragment LETTER   : 'a'..'z' | 'A'..'Z' ;
fragment DIGIT    : '0'..'9' ;
fragment HEXDIGIT : '0'..'9' | 'A..E' | 'a'..'e' ;
fragment HEX_PREFIX : '0x' ;

INTEGER : HEX_PREFIX (HEXDIGIT HEXDIGIT)+ ;

WORD   : (LETTER | '_') (LETTER | '_' | DIGIT)* ;

CLASS  : '.class' ;
METHOD : '.method' ;
STACK  : '.stack' ;
LOCAL  : '.local' ;

WHITESPACE : ( '\t' | '\r' | '\n' | ' ' | '\u000C' )+ { $channel = HIDDEN; } ;


