from OperationClasses import *

class Block(object):
    number=0
    def __init__(self,operation,input1Dependency,input2Dependency,output):
        self.operation=operation
        self.input1DependencyRaw,self.input2DependencyRaw=input1Dependency,input2Dependency
        self.input1DependencyTraced,self.input2DependencyTraced=self.getInputDependenciesTraced()
        self.output=output
        Block.number+=1
        self.num=Block.number
    def setInputDependenciesRaw(self,input1Dependency,input2Dependency):
        self.input1DependencyRaw=input1Dependency
        self.input2DependencyRaw=input2Dependency
    def setInputDependenciesTraced(self,input1Dependency,input2Dependency):
        self.input1DependencyTraced,self.input2DependencyTraced=input1Dependency,input2Dependency
    def setOutput(self,output):
        self.output=output
    def getInputDependenciesRaw(self):
        return self.input1DependencyRaw,self.input2DependencyRaw
    def getInputDependenciesTraced(self):
        if isinstance(self.input1DependencyRaw,Block):
            input1DependencyTraced=self.input1DependencyRaw.getOutput()
        else:
            input1DependencyTraced=self.input1DependencyRaw
        if isinstance(self.input2DependencyRaw,Block):
            input2DependencyTraced=self.input2DependencyRaw.getOutput()
        else:
            input2DependencyTraced=self.input2DependencyRaw
        return input1DependencyTraced,input2DependencyTraced
    def getInputDependenciesNoVarCounter(self):
        input1Dependency,input2Dependency=self.getInputDependenciesTraced()
        if not isinstance(input1Dependency,int):
            input1DependencyVar=""
            for char in input1Dependency:
                if char not in string.digits:
                    input1DependencyVar+=char
                else:
                    break
        else:
            input1DependencyVar=input1Dependency
        if not isinstance(input2Dependency,int):
            input2DependencyVar=""
            for char in input2Dependency:
                if char not in string.digits:
                    input2DependencyVar+=char
                else:
                    break
        else:
            input2DependencyVar=input2Dependency
        return input1DependencyVar,input2DependencyVar
    def getOutput(self):
        return self.output
    def getOutputNoVarCounter(self):
        outputVar=""
        for char in self.output:
            if char not in string.digits:
                outputVar+=char
            else:
                break
        return outputVar
    def getResult(self,varDictValues):
        if self.operation.getName()=="store":
            self.operation.storeValue(varDictValues)
        else:
            self.operation.compute(varDictValues)
        return self.operation.getResult()
    def __repr__(self):
        return "operation: " + str(self.operation) + "\n" + "input1Dependency: " + str(self.input1DependencyRaw) + "\n" + "input2Dependency: " + str(self.input2DependencyRaw) + "\n" + "output: " + str(self.output) + "\n" + str(self.num) + "\n"