import copy
from PythonParser import *
from OperationAndBlockRecursion import *
from BlocksScheduler import *
from VariableDictionaryClass import *
from protoGUI import *

def test():
    program1="""
    a=(a//1)
    n=((a+3)+(a+(a+1)))
    b=((b//2)+(a+1))
    c=((a-b)*a)
    d=((a+b)+c)
    e=(c*d)
    f=(a-(b//a))
    g=(f//(((b-c)*d)*(a-9)))
    """
    # a=(a+1)                   2 ops (add,store)
    # n=((a+3)+(a+(a+1)))       5 ops (add,add,add,add,store)
    # b=((b/2)+(a+1))           4 ops (div,add,add,store)
    # c=((a-b)*a)               3 ops (sub,mult,store)
    # d=((a+b)+c)               3 ops (add,add,store)
    # e=(c*d)                   2 ops (mult,store)
    # f=(a-(b/a))               3 ops (div,sub,store)
    # g=(f/(((b-c)*d)*(a-9)))   6 ops (sub,mult,sub,mult,div,store)
    # total ops = 28

    lines=program1.strip().splitlines()
    varDictCounter=VariableDictionary()
    varDictCounter1=VariableDictionary()
    varDictCounter.addVariable("a")
    varDictCounter1.addVariable("a")
    varDictCounter.addVariable("b")
    varDictCounter1.addVariable("b")
    lst=[]
    for line in lines:
        a=getLineElements(line)
        var,a=getStorageVariable(a)
        b=reduceArithmeticOperationsLst(a)
        c=recurseArithmeticOperations(b)
        d=StoreOperation(var,c)
        lst+=convertBlockToLst(recurseTree(d,varDictCounter,var)) 
        
    outLst=blocksScheduler(lst,varDictCounter1)
        
    
    varDictValues=VariableDictionary()
    varDictValues.addVariable("a")
    varDictValues.setVariable("a",1)
    varDictValues.addVariable("b")
    varDictValues.setVariable("b",2)

    for i in range(len(outLst)):
        for j in outLst[i]:
            j.getResult(varDictValues)
    
    run(outLst,varDictValues)

test()