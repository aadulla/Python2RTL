class VariableDictionary(object):
    def __init__(self):
        self.varDict={None:None}
    def addVariable(self,varName):
        self.varDict[varName]=0
    def setVariable(self,varName,varValue):
        self.varDict[varName]=varValue
    def incrementVariable(self,varName):
        if varName!=None:
            self.varDict[varName]=self.varDict[varName]+1
    def incrementAllVariables(self):
        for var in self.varDict:
            if var!=None:
                self.incrementVariable(var)
    def getVariableValue(self,varName):
        return self.varDict[varName]
    def getVariableFull(self,varName):
        return varName + str(self.varDict[varName])
    def removeVariable(self,varName):
        self.varDict.remove(varName)
    def checkPresent(self,varName):
        if varName in self.varDict:
            return True
        else:
            return False
    def getVarsLst(self):
        varsLst=[]
        for var in self.varDict:
            if var!=None:
                varsLst.append(var+str(self.varDict[var]))
            else:
                varsLst.append(None)
        return varsLst
    def __repr__(self):
        returnStr=""
        for var in self.varDict:
            if var==None:
                retrunStr=returnStr + "None: None" + "\n"
            else:
                returnStr=returnStr + var + ": " + str(self.varDict[var]) + "\n"
        return returnStr
            