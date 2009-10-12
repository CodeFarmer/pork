package org.joellercoaster.pork;

import junit.framework.TestCase;

import org.joellercoaster.pork.Sample;

public class Bug_18_NegativeBranchOffsetTest
    extends TestCase
{

    public Bug_18_NegativeBranchOffsetTest(String name)
    {
        super(name);
    }

    public void testStaticMethodWithBackwardsLabelBranch() {
        assertTrue(NegativeBranchOffset.lowestMultipleGreaterThanTen(3) == 12);
        assertTrue(NegativeBranchOffset.lowestMultipleGreaterThanTen(13) == 26); // don't ask
    }

} 
