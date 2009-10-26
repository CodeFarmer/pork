package org.joellercoaster.pork;

import junit.framework.TestCase;

public class Bug_27_NegativeConstantTest
    extends TestCase
{

    public Bug_27_NegativeConstantTest(String name) {
        super(name);
    }

    public void testNegativeFloatLiteral() {

        assertEquals( 0.1f, NegativeConstant.returnPointOne());
        assertEquals(-0.1f, NegativeConstant.returnMinusPointOne());

    }

    public void testNegativeIntLiteral() {

        assertEquals( 5, NegativeConstant.returnFive());
        assertEquals(-5, NegativeConstant.returnMinusFive());

        
    }

}
