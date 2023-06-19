class B
{
    public int testVariable; /* public field */
    public String testStringB;
    public boolean testBooleanB;

    void m(int i)
    {
        this.testVariable = i * A.testVariable;
        if(A.testVariable == testVariable){
        }
    }
}
