import copy

def getLinesAndIndents(program):
    lines=program.splitlines()
    programLinesLst=[]
    for line in lines:
        indent=line.count("    ")
        if line.strip()!="":
            programLinesLst.append([line.strip(),indent])
    return programLinesLst
    
def getLineElements(programLine):
    tokens=["=","+","-","*","/","(",")"]
    programLine.strip()
    programLine=programLine.replace(" ","")
    element=""
    elementsLst=[]
    for char in programLine:
        if char not in tokens:
            element+=char
        else:
            if element!="":
                elementsLst.append(element)
            elementsLst.append(char)
            element=""
    if element!="":
        elementsLst.append(element)
    while "/" in elementsLst:
        index=elementsLst.index("/")
        elementsLst.remove("/")
        elementsLst[index]="//"
    return elementsLst

def extractFunctions(programLinesLst):
    functionsLst=[]
    functionLines=[]
    for i in range(len(programLinesLst)):
        if programLinesLst[i][0].startswith("def"):
            indent=programLinesLst[i][1]
            functionLines.append(programLinesLst[i])
            for j in range (i+1,len(programLinesLst)):
                if programLinesLst[j][1]==indent+1:
                    functionLines.append(programLinesLst[j])
                else:
                    functionsLst.append(functionLines)
                    functionLines=[]
                    break
    if functionLines!=[]:
        functionsLst.append(functionLines)
    return functionsLst

def extractFunctionDefinition(functionsLst):
    for function in functionsLst:
        functionDeclaration=function[0][0]
        functionDeclaration=functionDeclaration.replace("def ","")
        functionName=""
        for char in functionDeclaration:
            if char!="(":
                functionName+=char
            else:
                break
        functionDeclaration=functionDeclaration.replace(functionName,"")
        functionDeclaration=functionDeclaration.replace("(","")
        functionDeclaration=functionDeclaration.replace(")","")
        functionDeclaration=functionDeclaration.replace(":","")
        parameterLst=[]
        parameter=""
        for char in functionDeclaration:
            if char!=",":
                parameter+=char
            else:
                parameterLst.append(parameter)
                parameter=""
        parameterLst.append(parameter)
        function.pop(0)
        function.insert(0,[functionName,parameterLst])
    return functionsLst

def getStorageVariable(operationsLst):
    return operationsLst[0], operationsLst[2:]