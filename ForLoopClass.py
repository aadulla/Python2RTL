class ForLoop(object):
    def __init__(self,counterVar,iterations,varDict,blocksLst):
        self.counterVar=counterVar
        varDict.addVariable(self.counterVar)
        self.iterations=iterations
        self.operation=AddOperation(varDict.getVariableFull(counterVar),1,0)
        operand1,operand2=self.operation.getOperands()
        varDict.incrementVariable(self.counterVar)
        output=varDict.getVariableFull(self.counterVar)
        self.blocksLst=blocksLst
        self.block=Block(self.operation,operand1,operand2,output)
        self.blocksLst.append(self.block)
    def incrementBlocksInputDependenciesCounters(self,varDict):
        for block in self.blocksLst:
            input1Dependency,input2Dependency=block.getInputDependenciesNoVarCounter()
            if not isinstance(input1Dependency,int):
                input1DependencySet=varDict.getVariableFull(input1Dependency)
            else:
                input1DependencySet=input1Dependency
            if not isinstance(input2Dependency,int):
                input2DependencySet=varDict.getVariableFull(input2Dependency)
            else:
                input2DependencySet=input2Dependency
            print("input dependencies", input1DependencySet, input2DependencySet)
            block.setInputDependenciesTraced(input1DependencySet,input2DependencySet)
    def incrementBlocksOutputCounters(self,varDict):
        for block in self.blocksLst:
            output=block.getOutputNoVarCounter()
            outputSet=varDict.getVariableFull(output)
            block.setOutput(outputSet)
    def incrementVarDictCounters(self,varDict):
        varDict.incrementAllVariables()
    def __repr__(self):
        returnStr=""
        for block in self.blocksLst:
            returnStr+=str(block)+"\n"
        return returnStr