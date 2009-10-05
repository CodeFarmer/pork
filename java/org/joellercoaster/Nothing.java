package org.joellercoaster;

import org.joellercoaster.pork.Sample;

class Nothing
{

    public String name;
    public int number;

    public static void main(String[] argv) {

        System.out.println("About to get void from Sample...");
        
        Sample.returnNothing();

        System.out.println("returnZero returned " 
                           + Sample.returnZero());

        System.out.println("returnIntUnchanged(42) returned "
                           + Sample.returnIntUnchanged(42));

        System.out.println("addTwoInts(2, 3) returns "
                           + Sample.addTwoInts(2, 3));

        System.out.println("Done.");

    }

}
