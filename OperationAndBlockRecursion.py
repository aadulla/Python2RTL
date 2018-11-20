import copy
from OperationClasses import *
from BlockClass import *

# def getVarDependency(operand,varDict):
#     name=operand
#     instance=varDict[operand]
#     return name + str(instance)

def getOperationOutput(operation,storageVariable):
    depth=str(operation.getDepth())
    return storageVariable+depth
    
def reduceArithmeticOperationsLst(tmpOperationsLst):
    operationsLst=copy.copy(tmpOperationsLst)
    if operationsLst[0]=="(":
        operationsLst.pop(0)
        operationsLst.pop()
    if operationsLst.count("(")==0 and operationsLst.count(")")==0:
        return operationsLst
    else:
        startIndex=operationsLst.index("(")
        count=0
        for i in range(startIndex+1,len(operationsLst)):
            if operationsLst[i]=="(":
                count+=1
            elif operationsLst[i]==")":
                count-=1
                if count<0:
                    endIndex=i+1
                    break
        if startIndex==0:
            return [reduceArithmeticOperationsLst(operationsLst[startIndex:endIndex])]+reduceArithmeticOperationsLst(operationsLst[endIndex:])
        else:
            return reduceArithmeticOperationsLst(operationsLst[0:startIndex])+[reduceArithmeticOperationsLst(operationsLst[startIndex:])]
            
def recurseArithmeticOperations(operationsLst,depth=0):
    if not isinstance(operationsLst,list):
        return operationsLst
    if operationsLst[1]=="+":
        return AddOperation(recurseArithmeticOperations(operationsLst[0],depth-1),recurseArithmeticOperations(operationsLst[2],depth-1),depth-1)
    elif operationsLst[1]=="-":
        return SubOperation(recurseArithmeticOperations(operationsLst[0],depth-1),recurseArithmeticOperations(operationsLst[2],depth-1),depth-1)
    elif operationsLst[1]=="*":
        return MultOperation(recurseArithmeticOperations(operationsLst[0],depth-1),recurseArithmeticOperations(operationsLst[2],depth-1),depth-1)
    elif operationsLst[1]=="/":
        return DivOperation(recurseArithmeticOperations(operationsLst[0],depth-1),recurseArithmeticOperations(operationsLst[2],depth-1),depth-1)

def recurseTree(operation,varDictCounter,storageVariable):
    if not isinstance(operation,Operation):
        # if operation in varDict:
            # return getVarDependency(operation,varDict)
        if varDictCounter.checkPresent(operation):
            return varDictCounter.getVariableFull(operation)
        elif isinstance(operation,int):
            return operation
    else:
        operand1,operand2=operation.getOperands()
        if operation.getDepth()==0 and operation.getName()=="store" and varDictCounter.checkPresent(storageVariable):
            operation.increaseDepth()
        output=getOperationOutput(operation,storageVariable)
        block=Block(operation,recurseTree(operand1,varDictCounter,storageVariable),recurseTree(operand2,varDictCounter,storageVariable),output)
        if operation.getName()=="store":
            if varDictCounter.checkPresent(storageVariable):
                varDictCounter.incrementVariable(storageVariable)
            else:
                varDictCounter.addVariable(storageVariable)
            # varDict[storageVariable]=1+varDict.get(storageVariable,-1)
        return block