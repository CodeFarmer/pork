package org.joellercoaster;

import org.joellercoaster.pork.Sample;

class Nothing
{

    public String name;
    public int number;

    public static void main(String[] argv) {

        System.out.println("About to get void from Sample...");
        
        Sample.returnNothing();

        System.out.println("Done.");

    }

}
