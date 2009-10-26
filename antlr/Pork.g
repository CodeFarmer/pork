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
import logging
from logging import DEBUG, INFO
import os
import sys
import traceback

from classfile import Code_attribute, ConstantValue_attribute, JavaClass
from classfile import arrayDescriptor, fieldDescriptor, methodDescriptor
from classfile import ACC_PUBLIC, ACC_FINAL, ACC_STATIC
from classfile import DESC_BOOLEAN, DESC_BYTE, DESC_CHAR, DESC_DOUBLE, DESC_FLOAT, DESC_INT, DESC_LONG, DESC_SHORT, DESC_VOID

from compiler import buildMethodBody, calculateLabelOffset
from compiler import Instruction, LabelRef, SymbolRef, FieldSymbol, FloatSymbol, IntegerSymbol, MethodSymbol, StringSymbol

from PorkLexer import PorkLexer

# DEBUG
logging.basicConfig()
log = logging.getLogger('parser')
log.setLevel(INFO)

def dump(o):
    if o and log.getEffectiveLevel() <= DEBUG:
        log.debug('DUMP: ' + `o`)

# each parse can contain multiple classDefs, optionally intermingled
classDefs = {}
currentClass = None
currentClassSymbols = None

def classDef(className):

    global currentClass, currentClassSymbols

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

        if log.getEffectiveLevel() <= INFO:
            log.info('writing class ' + className)

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

porkfile  : classDef+ ;
classDef  : classLine constantLine* fieldLine* methodDef+ ;

/* this will change! just getting method constants working to start with */
/* FIXME */
constantLine
    : CONSTANT name=WORD ((cm=classMethod { currentClassSymbols[$name.text] = $cm.symbol ; }) | (cf=classField { currentClassSymbols[$name.text] = $cf.symbol ; }) | (ci=classInteger { currentClassSymbols[$name.text] = $ci.symbol ; }) | (cs=classString { currentClassSymbols[$name.text] = $cs.symbol ; } )| (cf=classFloat { currentClassSymbols[$name.text] = $cf.symbol ; }));

classMethod returns [symbol]
    : c=className m=methodSignature lineEnd
    {
        $symbol = MethodSymbol(currentClass, $c.text, $m.methodName, $m.methodDesc) ;
    };

classField returns [symbol]
    : c=className t=typeName w=WORD lineEnd
    {
        $symbol = FieldSymbol(currentClass, $c.text, $w.text, arrayDescriptor($t.desc, $t.arrayDim)) ;
    };

classInteger returns [symbol]
    : i=integer lineEnd
    {
        $symbol = IntegerSymbol(currentClass, $i.intVal);
    };

classString returns [symbol]
    : s=STRING_LITERAL lineEnd
    {
        $symbol = StringSymbol(currentClass, s.text[1:-1]) ;
    };

classFloat returns [symbol]
    : f=float lineEnd
    {
        $symbol = FloatSymbol(currentClass, $f.floatVal);
    };

/*
 * TODO: make stackLine and localLine optional, and either allow defaults, or
 * guess through static analysis
 */
methodDef returns [meth]
@init { 
    operations = [] ;
    labels = {} ;
}
    : m=methodLine s=stackLine l=localLine ((la=label { labels[$la.name] = calculateLabelOffset($la.name, operations) ; } )| (op=operation { operations.append($op.op) ; } ))+ { 
        $meth = currentClass.method($m.methodName, $m.methodDesc, $m.accessMask, [Code_attribute(currentClass, $s.size, $l.size, buildMethodBody(operations, currentClassSymbols, labels))]) ;
        currentClassSymbols[$m.methodName] = MethodSymbol(currentClass, currentClass.name, $m.methodName, $m.methodDesc);
    } ;

stackLine returns [size] : STACK s=integer lineEnd { $size = $s.intVal ; } ;
localLine returns [size] : LOCAL s=integer lineEnd { $size = $s.intVal ; } ;

integer returns [intVal] : (s=HEX_INTEGER {$intVal = int($s.text, 16) ;}) | (s=DEC_INTEGER {$intVal = int($s.text, 10) ;}) ;

/* gets own section because we might want more than one float format */
float returns [floatVal] : f=FLOAT_LITERAL { $floatVal = float($f.text) ; } ;

/* FIXME void fields are legal */
/* NOTE that fields automatically get added to the symbol table */
fieldLine returns [fieldName, fieldDesc, accessMask, val]
@init {
    $accessMask = 0;
    $val = None;
}
    : FIELD (acc=accessClause { $accessMask = $acc.mask ; })? t=typeName f=WORD (EQUALS ((v=integer { $val = v; }) | (s=STRING_LITERAL { $val=$s.text[1:-1]; })))? lineEnd 
    { 
        attribs = [] ;
        if $val:
            attribs = [ConstantValue_attribute(currentClass, $t.desc, $val)] ;

        currentClass.field($f.text, $t.desc, $accessMask, attribs) ;
        currentClassSymbols[$f.text] = FieldSymbol(currentClass, currentClass.name, $f.text, $t.desc);

    } ;

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

methodName : WORD | INIT | CLINIT ;

lineEnd : SEMICOLON ;

classLine returns [clazz]
    : CLASS c=className lineEnd { $clazz = classDef($c.text); } ;

className : WORD (DOT WORD)* ;

typeName returns [desc, arrayDim]
@init { $arrayDim = 0; }
    : (T_BOOLEAN ({ $desc = DESC_BOOLEAN ; }) | T_BYTE ({ $desc = DESC_BYTE ; }) | T_CHAR ({ $desc = DESC_CHAR ; }) | T_DOUBLE ({ $desc = DESC_DOUBLE ; })| T_FLOAT ({ $desc = DESC_FLOAT ; }) | T_INT ({ $desc = DESC_INT ; }) | T_LONG ({ $desc = DESC_LONG ; }) | T_SHORT ({ $desc = DESC_SHORT ; }) | (T_VOID { $desc = DESC_VOID ; }) | (c=className { $desc = fieldDescriptor($c.text) ; })) (ARRAYDIM { $arrayDim = $arrayDim + 1; })* ;

accessClause returns [mask]
@init { $mask = 0; }
    : ((A_STATIC { $mask |= ACC_STATIC ; }) | (A_PUBLIC { $mask |= ACC_PUBLIC ; }) | (A_FINAL { $mask |= ACC_FINAL ; }) )+ ; /* obviously more go here */


operation returns [op]
@init { args = [] }
    : mnemonic=WORD
      ((iarg=integer { args.append($iarg.intVal) ; }) | (arg=STRING_LITERAL { args.append(currentClass.stringConstant($arg.text[1:-1])) ; }) | (symb=symbolref { args.append(SymbolRef($symb.name)) ; }) | (la=labelref { args.append(LabelRef($la.name)) ; }) )* 
      lineEnd { $op = Instruction($mnemonic.text, args) ; } ;


/* FIXME write a proper error message for this */
/* This returns a two-byte list */
symbolref returns [name] : DOLLAR w=WORD { $name=$w.text ;} ;

/* FIXME seriously consider ditching this syntax and just using symbols */
labelref returns [name] : AT w=WORD { $name=$w.text ; } ;

/* accessModifier : AM_PUBLIC | AM_PRIVATE | AM_PROTECTED | AM_STATIC | AM_FINAL | AM_INTERFACE | AM_ABSTRACT ; */

/* FIXME implement me! */
label returns [name]: w=WORD COLON { $name=$w.text ;} ;


