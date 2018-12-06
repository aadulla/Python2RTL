import copy
from PythonParser import *
from OperationAndBlockRecursion import *
from BlocksScheduler import *
from VariableDictionaryClass import *
from BlockMap import *

def test(program):
    # program="""
    # a=(a//1)
    # n=((a+3)+(a+(a+1)))
    # b=((b//2)+(a+1))
    # c=((a-b)*a)
    # d=((a+b)+c)
    # e=(c*d)
    # f=(a-(b//a))
    # g=(f//(((b-c)*d)*(a-9)))
    # """
    # a=(a+1)                   2 ops (add,store)
    # n=((a+3)+(a+(a+1)))       5 ops (add,add,add,add,store)
    # b=((b/2)+(a+1))           4 ops (div,add,add,store)
    # c=((a-b)*a)               3 ops (sub,mult,store)
    # d=((a+b)+c)               3 ops (add,add,store)
    # e=(c*d)                   2 ops (mult,store)
    # f=(a-(b/a))               3 ops (div,sub,store)
    # g=(f/(((b-c)*d)*(a-9)))   6 ops (sub,mult,sub,mult,div,store)
    # total ops = 28

    lines=program.strip().splitlines()
    varDictCounter=VariableDictionary()
    varDictCounter1=VariableDictionary()
    varDictValues=VariableDictionary()

    lst=[]
    for line in lines:
        a=getLineElements(line)
        if len(a)==3:
            varDictCounter.addVariable(a[0])
            varDictCounter1.addVariable(a[0])
            varDictValues.addVariable(a[0])
            varDictValues.setVariable(a[0],int(a[2]))
        else:
            var,a=getStorageVariable(a)
            b=reduceArithmeticOperationsLst(a)
            c=recurseArithmeticOperations(b)
            d=StoreOperation(var,c)
            lst+=convertBlockToLst(recurseTree(d,varDictCounter,var)) 
        
    outLst=blocksScheduler(lst,varDictCounter1)

    for i in range(len(outLst)):
        for j in outLst[i]:
            j.getResult(varDictValues)
    
    run(outLst,varDictValues)