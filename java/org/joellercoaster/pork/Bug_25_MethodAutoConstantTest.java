package org.joellercoaster.pork;

import junit.framework.TestCase;

public class Bug_25_MethodAutoConstantTest
    extends TestCase
{

    public Bug_25_MethodAutoConstantTest(String name) {
        super(name);
    }

    public void testMethodCall() {
        assertEquals(1, MethodAutoConstant.callReturnOne());
    }

}
