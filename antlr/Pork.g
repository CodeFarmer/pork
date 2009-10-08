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
from classfile import arrayDescriptor, fieldDescriptor, methodDescriptor
from classfile import ACC_PUBLIC, ACC_STATIC
from classfile import DESC_BOOLEAN, DESC_BYTE, DESC_CHAR, DESC_DOUBLE, DESC_FLOAT, DESC_INT, DESC_LONG, DESC_SHORT, DESC_VOID

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
currentClassSymbols = {}

def classDef(className):

    global currentClass

    if not classDefs.has_key(className):
        ret = JavaClass(className)
        classDefs[className] = ret
    else:
        ret = classDefs[className]

    currentClass = ret
    currentClassSymbols = {}
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
classDef  : classLine constantLine* methodDef+ ;

/* this will change! just getting method constants working to start with */
/* FIXME */
constantLine
    : CONSTANT name=WORD ((cm=classMethod { currentClassSymbols[$name.text] = $cm.index ; }) | (cf=classField { currentClassSymbols[$name.text] = $cf.index ; }));

classMethod returns [index]
    : c=className m=methodSignature lineEnd
    {
        const = currentClass.methodConstant($c.text, $m.methodName, $m.methodDesc) ;
        $index = [const >> 8 & 0xff, const & 0xff];
    };

classField returns [index]
    : c=className t=typeName w=WORD lineEnd
    {
        const = currentClass.fieldConstant($c.text, $w.text, arrayDescriptor($t.desc, $t.arrayDim));
        $index = [const >> 8 & 0xff, const & 0xff];
    };

/*
 * TODO: make stackLine and localLine optional, and either allow defaults, or
 * guess through static analysis
 */
methodDef returns [meth]
@init { body = '' }
    : m=methodLine s=stackLine l=localLine (op=operation { body += $op.bytes ; } )+ { $meth = currentClass.method($m.methodName, $m.methodDesc, $m.accessMask, [Code_attribute(currentClass, $s.size, $l.size, body)]) ; } ;

stackLine returns [size] : STACK s=INTEGER lineEnd { $size = int($s.text, 16) ; } ;
localLine returns [size] : LOCAL s=INTEGER lineEnd { $size = int($s.text, 16) ; } ;


methodLine returns [methodName, methodDesc, accessMask]
@init {
    $accessMask = 0;
}
    : METHOD (acc=accessClause { $accessMask = $acc.mask ; })? m=methodSignature lineEnd
    {
        $methodName = $m.methodName ;
        $methodDesc = $m.methodDesc ;
    } ;

methodSignature returns [methodName, methodDesc]
    :  t=typeName m=methodName a=methodArgs 
    {
        $methodName = $m.text ;
        $methodDesc = methodDescriptor($t.desc, $a.args);
    };

methodArgs returns [args]
@init { $args = [] }
    : LEFTBRACKET ((a=typeName { args.append(arrayDescriptor($a.desc, $a.arrayDim)) }) (COMMA b=typeName { args.append(arrayDescriptor($b.desc, $b.arrayDim)) })* )? RIGHTBRACKET ;

methodName : WORD | INIT ;

lineEnd : SEMICOLON ;

classLine returns [clazz]
    : CLASS c=className lineEnd { $clazz = classDef($c.text); } ;

className : WORD (DOT WORD)* ;

typeName returns [desc, arrayDim]
@init { $arrayDim = 0; }
    : (T_BOOLEAN ({ $desc = DESC_BOOLEAN ; }) | T_BYTE ({ $desc = DESC_BYTE ; }) | T_CHAR ({ $desc = DESC_CHAR ; }) | T_DOUBLE ({ $desc = DESC_DOUBLE ; })| T_FLOAT ({ $desc = DESC_FLOAT ; }) | T_INT ({ $desc = DESC_INT ; }) | T_LONG ({ $desc = DESC_LONG ; }) | T_SHORT ({ $desc = DESC_SHORT ; }) | (T_VOID { $desc = DESC_VOID ; }) | (c=className { $desc = fieldDescriptor($c.text) ; })) (ARRAYDIM { $arrayDim = $arrayDim + 1; })* ;

accessClause returns [mask]
@init { $mask = 0; }
    : ((A_STATIC { $mask |= ACC_STATIC ; }) | (A_PUBLIC { $mask |= ACC_PUBLIC ; }))+ ; /* obviously more go here */


operation returns [bytes]
@init { args = [] }
    : mnemonic=WORD
      (arg=(INTEGER { args.append(int($arg.text, 16)) ; }) | (arg=STRING_LITERAL { args.append(currentClass.stringConstant($arg.text[1:-1])) ; }) | (symb=symbol { args += $symb.index ; }) )* 
      lineEnd { $bytes = byteString($mnemonic.text, args) ; } ;


/* FIXME write a proper error message for this */
/* This returns a two-byte list */
symbol returns [index] : DOLLAR w=WORD { $index = currentClassSymbols[$w.text] ;} ;

/* accessModifier : AM_PUBLIC | AM_PRIVATE | AM_PROTECTED | AM_STATIC | AM_FINAL | AM_INTERFACE | AM_ABSTRACT ; */


