import copy
from BlockClass import *

def getOutputLst(blocksLst):
    outputsLst=[]
    if blocksLst==[]:
        return outputsLst
    for block in blocksLst:
        outputsLst.append(block.getOutput())
    return outputsLst

# def getVarsLst(varDict):
#     varsLst=[]
#     for var in varDict:
#         if var!=None:
#             varsLst.append(var+str(varDict[var]))
#         else:
#             varsLst.append(None)
#     return varsLst

# def blocksScheduler(blocksLst,varDictCounter):
#     currentLevelBlocksLst=[]
#     finishedBlocksLst=[]
#     scheduledBlocksLst=[]
#     varsLst=varDictCounter.getVarsLst()
#     while len(blocksLst)!=0:
#         tmpBlocksLst=copy.copy(blocksLst)
#         for block in blocksLst:
#             input1Dependency,input2Dependency=block.getInputDependenciesTraced()
#             outputsLst=getOutputLst(finishedBlocksLst)
#             print("operation", block.operation)
#             print ("inputs", input1Dependency, input2Dependency)
#             checkAvailableVarsLst=varsLst+outputsLst
#             print("checks", checkAvailableVarsLst)
#             if (isinstance(input1Dependency,int) and isinstance(input2Dependency,int)) or (isinstance(input1Dependency,int) and input2Dependency in checkAvailableVarsLst) or (input1Dependency in checkAvailableVarsLst and isinstance(input2Dependency,int)) or (input1Dependency in checkAvailableVarsLst and input2Dependency in checkAvailableVarsLst):
#                 currentLevelBlocksLst.append(block)
#                 tmpBlocksLst.remove(block)
#                 print("scheduled", block.operation)
#                 print("scheduled output", block.output)
#         finishedBlocksLst.extend(copy.copy(currentLevelBlocksLst))
#         if currentLevelBlocksLst!=[]:
#             scheduledBlocksLst.append(copy.copy(currentLevelBlocksLst))
#         currentLevelBlocksLst=[]
#         blocksLst=copy.copy(tmpBlocksLst)
#         tmpBlocksLst=[]
#         for j in blocksLst:
#             print ("remaining", j.operation)
#         for j in finishedBlocksLst:
#             print ("to look at", j.operation)
#         print("-----------------------------------------------------")
#     return scheduledBlocksLst

def blocksScheduler(blocksLst,varDictCounter):
    currentLevelBlocksLst=[]
    finishedBlocksLst=[]
    scheduledBlocksLst=[]
    varsLst=varDictCounter.getVarsLst()
    outputsLst=[]
    while len(blocksLst)!=0:
        tmpBlocksLst=copy.copy(blocksLst)
        for block in blocksLst:
            input1Dependency,input2Dependency=block.getInputDependenciesRaw()
            # print("operation", block.operation)
            # print ("inputs", input1Dependency, input2Dependency)
            checkAvailableVarsLst=varsLst+finishedBlocksLst+outputsLst
            # print("checks", checkAvailableVarsLst)
            if (isinstance(input1Dependency,int) and isinstance(input2Dependency,int)) or (isinstance(input1Dependency,int) and input2Dependency in checkAvailableVarsLst) or (input1Dependency in checkAvailableVarsLst and isinstance(input2Dependency,int)) or (input1Dependency in checkAvailableVarsLst and input2Dependency in checkAvailableVarsLst):
                currentLevelBlocksLst.append(block)
                tmpBlocksLst.remove(block)
                if block.getOperation().getName()=="store":
                    outputsLst.append(block.getOutput())
                # print("scheduled", block.operation)
                # print("scheduled output", block.output)
        finishedBlocksLst.extend(copy.copy(currentLevelBlocksLst))
        if currentLevelBlocksLst!=[]:
            scheduledBlocksLst.append(copy.copy(currentLevelBlocksLst))
        currentLevelBlocksLst=[]
        blocksLst=copy.copy(tmpBlocksLst)
        tmpBlocksLst=[]
        # for j in blocksLst:
        #     print ("remaining", j.operation)
        # for j in finishedBlocksLst:
        #     print ("to look at", j.operation)
        # print("-----------------------------------------------------")
        # for i in checkAvailableVarsLst:
        #     print(i)
        # print("length", len(checkAvailableVarsLst))
        # print("-------------------------------------")
        # print("yay")
    return scheduledBlocksLst