package org.joellercoaster.pork.test ;

import java.util.Enumeration;

import junit.runner.SimpleTestCollector;
import junit.runner.TestCollector;
import junit.textui.TestRunner;

public class JUnit
{

    public static void main(String[] argv)
        throws ClassNotFoundException
    {

        TestRunner runner = new TestRunner();
        TestCollector collector = new SimpleTestCollector();
        for (Enumeration e = collector.collectTests() ; e.hasMoreElements() ; ) {
            String name = (String) e.nextElement();
            System.out.println(name);
            runner.run(Class.forName(name));
        }
    }
    
}
