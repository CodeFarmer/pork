package org.joellercoaster;

import junit.framework.TestCase;

import org.joellercoaster.pork.Sample;

class NothingTest
    extends TestCase
{

    public void testNothing() { 
        Sample.returnNothing();
    }

    /* testing declaration of return types */
    public void testReturnZero() {
        assertTrue(Sample.returnZero() == 0);
    }

    /* testing declaration of single int argument */
    public void testReturnIntUnchanged() {
        assertTrue(Sample.returnIntUnchanged(42) == 42);
    }

    /* testing declaration of multiple args */
    public void testAddTwoInts() {
        assertTrue(Sample.addTwoInts(2, 3) == 5);
    }


}
