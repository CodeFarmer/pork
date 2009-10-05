package org.joellercoaster;

import junit.framework.TestCase;

import org.joellercoaster.pork.Sample;

class NothingTest
    extends TestCase
{

    public void testSimpleStaticInvocation() { 
        Sample.returnNothing();
    }

    public void testStaticMethodWithReturnType() {
        assertTrue(Sample.returnZero() == 0);
    }

    public void testStaticMethodWithSingleIntArgument() {
        assertTrue(Sample.returnIntUnchanged(42) == 42);
    }

    public void testStaticMethodWithMultipleArguments() {
        assertTrue(Sample.addTwoInts(2, 3) == 5);
    }


}
