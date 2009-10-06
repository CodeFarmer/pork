/*
 * Joel's combination pork grammar and ANTLR learning sandbox, bear with me.
 */

parser grammar Pork;

options {
    language=Python;
    tokenVocab=PorkLexer;
}

@header {

from io import FileIO
import logging as log
import os
import sys
import traceback

from classfile import Code_attribute, JavaClass
from classfile import fieldDescriptor, methodDescriptor
from classfile import ACC_PUBLIC, ACC_STATIC, DESC_INT, DESC_VOID

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

/*
 * TODO: make stackLine and localLine optional, and either allow defaults, or
 * guess through static analysis
 */
methodDef returns [meth]
@init { body = '' }
    : m=methodLine s=stackLine l=localLine (op=operation { body += $op.bytes ; } )+ { $meth = currentClass.method($m.methodName, $m.methodDesc, ACC_PUBLIC | ACC_STATIC, [Code_attribute(currentClass, $s.size, $l.size, body)]) ; } ;

stackLine returns [size] : STACK s=INTEGER lineEnd { $size = int($s.text, 16) ; } ;
localLine returns [size] : LOCAL s=INTEGER lineEnd { $size = int($s.text, 16) ; } ;


methodLine returns [methodName, methodDesc]
@init { args = [] }
    : METHOD t=typeName m=methodName LEFTBRACKET ((a=typeName { args.append($a.desc) }) (COMMA b=typeName { args.append($b.desc) })* )? RIGHTBRACKET lineEnd
    {
        $methodName = $m.text ;
        $methodDesc = methodDescriptor($t.desc, args); 
    } ;

methodName : WORD;

lineEnd : SEMICOLON ;

classLine returns [clazz]
    : CLASS c=className lineEnd { $clazz = classDef($c.text); } ;

className : WORD (DOT WORD)* ;

typeName returns [desc] : T_INT ({ $desc = DESC_INT ; }) | (T_VOID { $desc = DESC_VOID ; }) | (c=className { $desc = fieldDescriptor($c.text) ; }) ;

operation returns [bytes]
@init { args = [] }
    : mnemonic=WORD
      (arg=INTEGER { args.append(int($arg.text, 16)) ; } )* 
      lineEnd { $bytes = byteString($mnemonic.text, args) ; } ;

/* accessModifier : AM_PUBLIC | AM_PRIVATE | AM_PROTECTED | AM_STATIC | AM_FINAL | AM_INTERFACE | AM_ABSTRACT ; */


