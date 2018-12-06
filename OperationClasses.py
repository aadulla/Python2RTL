from tkinter import *
from PIL import Image, ImageTk
from ArithmeticUnitsClasses import *

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
        self.arithmeticUnit=None
        self.operand1Computable,self.operand2Computable=0,0
    def setResult(self,result):
        self.result=result
    def getOperands(self):
        return self.operand1,self.operand2
    def getOperandsComputable(self,varDictValues=None):
        if varDictValues==None:
            return self.operand1Computable,self.operand2Computable
        else:
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
            self.operand1Computable=operand1
            self.operand2Computable=operand2
            return self.operand1Computable,self.operand2Computable
    def getResult(self):
        return self.result
    def getDepth(self):
        return self.depth
    def getName(self):
        return self.name
    def getToken(self):
        return self.token
    def draw(self,canvas,data,x,y,canvasMap):
        self.arithmeticUnit.draw(canvas,data,x,y,canvasMap)
    def redraw(self,canvas,data,x,y):
        self.arithmeticUnit.redraw(canvas,data,x,y)
    def drawRTL(self,canvas,data,centerX,centerY,canvasMap):
        return self.arithmeticUnit.drawRTL(canvas,data,centerX,centerY,canvasMap)
    def getArithmeticUnit(self):
        return self.arithmeticUnit
    def __repr__(self):
        return "%s(%s,%s)"%(self.name,self.operand1,self.operand2)

class StoreOperation(Operation):
    def __init__(self,operand1,operand2):
        self.depth=0
        super().__init__(operand1,operand2,self.depth,"=","store")
        self.width=377
        self.height=258
        self.input1TraceOrigin=(0,72,3.25)
        self.input2TraceOrigin=(0,191,3.25)
        self.outputTraceOrigin=(375,66,3.25)
        self.scale=5
    def increaseDepth(self):
        self.depth+=1
    def storeValue(self,varDictValues):
        operand1,operand2=self.getOperandsComputable(varDictValues)
        operand1=self.operand1
        varDictValues.setVariable(operand1,operand2)
        return operand1,operand2
    def draw(self,canvas,data,x,y,canvasMap):
        flipFlopImg=Image.open("FlipFlop.png")
        flipFlopImgResized=flipFlopImg.resize((int(self.width//self.scale),int(self.height//self.scale)),Image.ANTIALIAS)
        width=ImageTk.PhotoImage(flipFlopImgResized).width()
        height=ImageTk.PhotoImage(flipFlopImgResized).height()
        xStart=int(x-width//2)
        xEnd=int(x+width//2)
        yStart=int(y-height//2)
        yEnd=int(y+height//2)
        xPad=3
        yPad=3
        # canvas.create_rectangle(xStart-xPad,yStart-yPad,xEnd+xPad,yEnd+yPad,width=1)
        for i in range(xStart-xPad,xEnd+xPad+1):
            for j in range (yStart-yPad,yEnd+yPad+1):
                canvasMap[j][i]=9
        data.image=ImageTk.PhotoImage(flipFlopImgResized)
        label=Label(canvas,image=data.image)
        label.image=data.image
        canvas.create_image(x,y,image=data.image)
    def redraw(self,canvas,data,x,y):
        flipFlopImg=Image.open("FlipFlop.png")
        flipFlopImgResized=flipFlopImg.resize((int(self.width//self.scale),int(self.height//self.scale)),Image.ANTIALIAS)
        width=ImageTk.PhotoImage(flipFlopImgResized).width()
        height=ImageTk.PhotoImage(flipFlopImgResized).height()
        data.image=ImageTk.PhotoImage(flipFlopImgResized)
        label=Label(canvas,image=data.image)
        label.image=data.image
        canvas.create_image(x,y,image=data.image)
    def getShapeDimensions(self):
        return self.width,self.height,self.input1TraceOrigin,self.input2TraceOrigin,self.outputTraceOrigin,self.scale
        
class AddOperation(Operation):
    def __init__(self,operand1,operand2,depth):
        super().__init__(operand1,operand2,depth,"+","add")
    def compute(self,varDictValues):
        operand1,operand2=self.getOperandsComputable(varDictValues)
        self.result=operand1+operand2
        self.arithmeticUnit=EightBitAdder(operand1,operand2)
        return operand1,operand2
    def getShapeDimensions(self):
        return self.arithmeticUnit.getShapeDimensions()
    
class SubOperation(Operation):
    def __init__(self,operand1,operand2,depth):
        super().__init__(operand1,operand2,depth,"-","sub")
    def compute(self,varDictValues):
        operand1,operand2=self.getOperandsComputable(varDictValues)
        self.result=operand1-operand2
        self.arithmeticUnit=EightBitSubtractor(operand1,operand2)
        return operand1,operand2
    def getShapeDimensions(self):
        return self.arithmeticUnit.getShapeDimensions()
        
class MultOperation(Operation):
    def __init__(self,operand1,operand2,depth):
        super().__init__(operand1,operand2,depth,"x","mult")
    def compute(self,varDictValues):
        operand1,operand2=self.getOperandsComputable(varDictValues)
        self.result=operand1*operand2
        self.arithmeticUnit=EightBitMultiplier(operand1,operand2)
        return operand1,operand2
    def getShapeDimensions(self):
        return self.arithmeticUnit.getShapeDimensions()
        
class DivOperation(Operation):
    def __init__(self,operand1,operand2,depth):
        super().__init__(operand1,operand2,depth,"//","div")
        self.width=646
        self.height=439
        self.input1TraceOrigin=(5,112.25,6)
        self.input2TraceOrigin=(5,327.25,6)
        self.outputTraceOrigin=(644,219,5.25)
        self.scale=8
    def compute(self,varDictValues):
        operand1,operand2=self.getOperandsComputable(varDictValues)
        self.result=operand1//operand2
        return operand1,operand2
    def draw(self,canvas,data,x,y):
        eightBitDividerImg=Image.open("8BitDivider.png")
        width=ImageTk.PhotoImage(eightBitDividerImg).width()
        height=ImageTk.PhotoImage(eightBitDividerImg).height()
        eightBitDividerImgResized=eightBitDividerImg.resize((int(width//self.scale),int(height//self.scale)),Image.ANTIALIAS)
        data.image=ImageTk.PhotoImage(eightBitDividerImgResized)
        label=Label(canvas,image=data.image)
        label.image=data.image
        canvas.create_image(x,y,image=data.image)
    def getShapeDimensions(self):
        return self.width,self.height,self.input1TraceOrigin,self.input2TraceOrigin,self.outputTraceOrigin,self.scale
       