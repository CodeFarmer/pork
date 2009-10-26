package org.joellercoaster.pork;

import java.lang.reflect.Field;

import junit.framework.TestCase;

import org.joellercoaster.pork.Sample;

public class NothingTest
    extends TestCase
{

    public NothingTest(String name)
    {
        super(name);
    }

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

    public void testStaticMethodWithOjbectArgument() {
        Sample.acceptObject(this);
    }

    public void testStaticMethodWithCharArgument() {
        assertTrue(Sample.getNextChar('a') == 'b');
    }

    public void testStaticStringLiteral() {
        assertEquals("This is a String literal", Sample.getString());
    }

    /* this one is exactly the same under the hood as the previous test,
       but it's declared differently in the porkfile */
    public void testStaticStringFromConstantPool() {
        assertEquals("feep", Sample.getAnotherString());
    }

    public void testNonstaticMethod() {
        Sample sample = new Sample();
        assertTrue(sample.returnThis() == sample);
    }

    public void testStaticIntegerFromConstant() {
        assertTrue(Sample.returnTwentyFive() == 25);
    }

    public void testField() {
        Sample sample = new Sample();
        sample.setIntField(6);
        assertTrue(sample.fieldInt == 6);
        sample.setIntField(247);
        assertTrue(sample.fieldInt == 247);
    }

    public void testStaticInitializedField() {
        assertEquals("Hello, world.", Sample.HELLO_WORLD);
    }

    public void testStaticMethodWithLabelBranch() {
        assertEquals("Zero!",     Sample.recognizeZero(0));
        assertEquals("Not zero.", Sample.recognizeZero(1));
    }

    public void testAutoinitializedIntField() {
        assertEquals(515, Sample.constantInt);
    }

    public void testAutoinitializedStringField() {
        assertEquals("goo", Sample.constantString);
    }


    public void testFinalField()
        throws NoSuchFieldException {

        assertEquals("goo", Sample.finString);

        Class clazz = Sample.class ;
        Field field = clazz.getDeclaredField("finString");
        try {
            field.set(null, "ick");
            fail("Should have thrown exception trying to write to a final field");
        }
        catch (IllegalAccessException iae) {
        }

    }

}
