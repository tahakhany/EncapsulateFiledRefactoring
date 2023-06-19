/* Before refactoring (Original version) */
class A
{
    private int testVariable; /* public field */
    private String testString;
    public String testStringB;
    public boolean testBoolean;

    void m(int i)
    {
        B.testVariableB = i * this.testVariable;
    }

    void main()
    {
        B objB = new B();
        A objA = new A();

        String testStringB = "test";

        testStringB = "hassan";

        objB.testStringB = "hossein";

        objA.testStringB = "reza";
    }
}
