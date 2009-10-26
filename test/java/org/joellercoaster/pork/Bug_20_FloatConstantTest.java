package org.joellercoaster.pork;

import junit.framework.TestCase;

public class Bug_20_FloatConstantTest
    extends TestCase
{

    public Bug_20_FloatConstantTest(String name) {
        super(name);
    }

    public void testFloatLiteral() {

        assertEquals(0.1f, FloatConstant.returnPointOne());

    }

}
