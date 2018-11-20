class Operation(object):
    def __init__(self,operand1,operand2,depth,token,name):
        try:
            self.operand1=int(operand1)
        except:
            self.operand1=operand1
        try:
            self.operand2=int(operand2)
        except:
            self.operand2=operand2
        self.depth=depth
        self.token=token
        self.name=name
        self.result=None
    def getOperands(self):
        return self.operand1,self.operand2
    def getOperandsComputable(self,varDictValues):
        if isinstance(self.operand1,int):
            operand1=self.operand1
        elif isinstance(self.operand1,Operation):
            operand1=self.operand1.getResult()
        elif varDictValues.checkPresent(self.operand1):
            operand1=varDictValues.getVariableValue(self.operand1)
        else:
            operand1=self.operand1
        if isinstance(self.operand2,int):
            operand2=self.operand2
        elif isinstance(self.operand2,Operation):
            operand2=self.operand2.getResult()
        elif varDictValues.checkPresent(self.operand2):
            operand2=varDictValues.getVariableValue(self.operand2)
        else:
            operand1=self.operand2
        return operand1,operand2
    def getResult(self):
        return self.result
    def getDepth(self):
        return self.depth
    def getName(self):
        return self.name
    def __repr__(self):
        return "%s(%s,%s)"%(self.name,self.operand1,self.operand2)

class StoreOperation(Operation):
    def __init__(self,operand1,operand2):
        self.depth=0
        super().__init__(operand1,operand2,self.depth,"=","store")
    def increaseDepth(self):
        self.depth+=1
    def storeValue(self,varDictValues):
        operand1,operand2=self.getOperandsComputable(varDictValues)
        operand1=self.operand1
        varDictValues.setVariable(operand1,operand2)
        
class AddOperation(Operation):
    def __init__(self,operand1,operand2,depth):
        super().__init__(operand1,operand2,depth,"+","add")
    def compute(self,varDictValues):
        operand1,operand2=self.getOperandsComputable(varDictValues)
        self.result=operand1+operand2
    
class SubOperation(Operation):
    def __init__(self,operand1,operand2,depth):
        super().__init__(operand1,operand2,depth,"-","sub")
    def compute(self,varDictValues):
        operand1,operand2=self.getOperandsComputable(varDictValues)
        self.result=operand1-operand2
        
class MultOperation(Operation):
    def __init__(self,operand1,operand2,depth):
        super().__init__(operand1,operand2,depth,"*","mult")
    def compute(self,varDictValues):
        operand1,operand2=self.getOperandsComputable(varDictValues)
        self.result=operand1*operand2
        
class DivOperation(Operation):
    def __init__(self,operand1,operand2,depth):
        super().__init__(operand1,operand2,depth,"/","div")
    def compute(self,varDictValues):
        operand1,operand2=self.getOperandsComputable(varDictValues)
        self.result=operand1/operand2