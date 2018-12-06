import copy
from PythonParser import *
from OperationAndBlockRecursion import *
from BlocksScheduler import *
from VariableDictionaryClass import *
from protoGUI import *

def getStorageVariable(operationsLst):
    return operationsLst[0], operationsLst[2:]

def convertBlockToLst(block,lst=None):
    if lst==None:
        lst=[]
    if not isinstance(block,Block):
        return
    else:
        lst.append(block)
        inputDependency1,inputDependency2=block.getInputDependenciesRaw()
        convertBlockToLst(inputDependency1,lst)
        convertBlockToLst(inputDependency2,lst)
        return lst

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
        print("B")
        print(b)
        c=recurseArithmeticOperations(b)
        d=StoreOperation(var,c)
        lst+=convertBlockToLst(recurseTree(d,varDictCounter,var)) 

    outLst=blocksScheduler(lst,varDictCounter1)
    
    for i in range(len(outLst)):
        for j in outLst[i]:
            print (j.operation)
        print("-------------------------")
        
    
    varDictValues=VariableDictionary()
    varDictValues.addVariable("a")
    varDictValues.setVariable("a",1)
    varDictValues.addVariable("b")
    varDictValues.setVariable("b",2)
    
    for i in range(len(outLst)):
        for j in outLst[i]:
            print (j.operation,end=" ")
        print() 
    
    print()
    print()
    
    for i in range(len(outLst)):
        for j in outLst[i]:
            print (j.operation,j.getResult(varDictValues),end=" ")
        print() 
    
    print(varDictCounter)
    print()
    print(varDictCounter1)
    print()
    print(varDictValues)
    run(outLst)

##############################################################################
    
    # tmp1Lst=[]
    # tmp2Lst=[]
    # outLst=[]
    # varLst=[]
    # for i in varDict1:
    #     if i!=None:
    #         varLst.append(i+str(varDict1[i]))
    #     else:
    #         varLst.append(None)
    # counter=0
    # while len(lst)!=0:
    #     lst2=copy.copy(lst)
    #     counter+=1
    #     if counter>10:
    #         break
    #     for i in lst:
    #         a,b=i.getInputDependenciesTraced()
    #         outputs=getOutputLst(tmp2Lst)
    #         print("operation", i.operation)
    #         print ("inputs", a, b)
    #         l=varLst+outputs
    #         print("checks", l)
    #         if (a in l) and (b in l):
    #             tmp1Lst.append(i)
    #             lst2.remove(i)
    #             print("scheduled", i.operation)
    #             print("scheduled output", i.output)
    #     tmp2Lst.extend(copy.copy(tmp1Lst))
    #     if tmp1Lst!=[]:
    #         outLst.append(copy.copy(tmp1Lst))
    #     tmp1Lst=[]
    
    #     print(len(lst2))
    #     for j in lst2:
    #         print ("remaining", j.operation)
    #     lst=copy.copy(lst2)
    #     for j in tmp2Lst:
    #         print ("to look at", j.operation)
    #     print("-----------------------------------------------------")
    #     lst2=[]
    # for i in range(len(outLst)):
    #     for j in outLst[i]:
    #         print (j.operation,end=" ")
    #     print()
    # print ("total ops: ", str(len(outLst)))