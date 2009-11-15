package org.joellercoaster.pork;

import junit.framework.TestCase;

public class Bug_24_Exceptions
    extends TestCase
{

    public Bug_24_Exceptions(String name) {
        super(name);
    }

    public void testCatchNPEInternally()
    {

        try {

            Exceptions.dereferenceNullWithoutCatch();
            fail ("The code you think should throw a null pointer exception? Not so much.");
        
        }
        catch (NullPointerException npe) {
        }

        Exceptions.dereferenceNullWithCatch();
    
    }

}
