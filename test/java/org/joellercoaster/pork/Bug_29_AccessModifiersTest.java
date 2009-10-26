package org.joellercoaster.pork;

import java.lang.reflect.Field;
import java.lang.reflect.Method;
import java.lang.reflect.Modifier;

import junit.framework.TestCase;

public class Bug_29_AccessModifiersTest
    extends TestCase
{

    //// FIELDS ////

    public Bug_29_AccessModifiersTest(String name) {
        super(name);
    }

    public void testPrivateField()
        throws NoSuchFieldException
    {

        Field field = AccessModifiers.class.getDeclaredField("ONE");
        assertTrue((field.getModifiers() & Modifier.PRIVATE) != 0);

    }

    public void testProtectedField()
        throws NoSuchFieldException
    {

        Field field = AccessModifiers.class.getDeclaredField("TWO");
        assertTrue((field.getModifiers() & Modifier.PROTECTED) != 0);

    }


    /* yes, a lot of this gets implicitly tested elsewhere too */
    public void testStaticField()
        throws NoSuchFieldException
    {

        Field field = AccessModifiers.class.getDeclaredField("TWO");
        assertTrue((field.getModifiers() & Modifier.STATIC) != 0);

    }

    public void testNonStaticField()
        throws NoSuchFieldException
    {

        Field field = AccessModifiers.class.getDeclaredField("someState");
        assertTrue((field.getModifiers() & Modifier.STATIC) == 0);

    }

    //// METHODS ////

    public void testProtectedMethod()
        throws NoSuchMethodException
    {

        Method method = AccessModifiers.class.getDeclaredMethod("getOne");
        assertTrue((method.getModifiers() & Modifier.PROTECTED) != 0);

    }

    public void testStaticMethod()
        throws NoSuchMethodException
    {

        Method method = AccessModifiers.class.getDeclaredMethod("getOne");
        assertTrue((method.getModifiers() & Modifier.STATIC) != 0);

    }


}
