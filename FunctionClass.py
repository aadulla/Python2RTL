class Function(object):
    def __init__(self,function,varDict):
        self.name=function[0][0]
        self.parameterLst=function[0][1]
        if self.parameterLst[0]=="":
            self.parameterLst=None
        self.blocksLst=self.blocksLst(self.function[1:],varDict)
    def getBlocksLst(self,function,varDict):
        blocksLst=[]
        for line in function:
            lineElements=getLineElements(line)
            var,operations=getStorageVariable(lineElements)
            reducedOperations=reduceArithmeticOperationsLst(expression)
            recursedOperations=recurseArithmeticOperations(reducedOperations)
            fullOperations=StoreOperation(var,recursedOperations)
            blocksLst.append(convertBlockToLst(recurseTree(fullOperations,varDict,var)) )
        return blocksLst