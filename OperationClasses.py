from tkinter import *
from PIL import Image, ImageTk

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
    def getToken(self):
        return self.token
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
        return operand1,operand2
    def draw(self,data,operand1,operand2):
        operand1=abs(operand1)
        operand2=abs(operand2)
        maxOperand=max(operand1,operand2)
        bitLength=maxOperand.bit_length()
        canvasHeight=data.height
        fullAdderImgHeight=450
        scale=fullAdderImgHeight/(canvasHeight/(bitLength+1))
        adderImg=Image.open("full adder.png")
        width=ImageTk.PhotoImage(adderImg).width()
        height=ImageTk.PhotoImage(adderImg).height()
        adderImgResized=adderImg.resize((int(width//scale),int(height//scale)),Image.ANTIALIAS)
        data.image=ImageTk.PhotoImage(adderImgResized)
        startX=100
        startY=0
        locationLst=[]
        root = Toplevel()
        canvas = Canvas(root, width=data.width, height=data.height)
        canvas.configure(bd=0, highlightthickness=0, background="white")
        canvas.pack()
        for i in range(bitLength+1):
            locationLst.append((startX,startY))
            label=Label(canvas,image=data.image)
            label.image=data.image
            canvas.create_image(startX,startY,anchor="nw",image=data.image)
            startY+=450/scale
        startX=100
        startY=0
        for i in range(bitLength):
            canvas.create_line(startX+(685/scale),startY+(331/scale),startX+(685/scale),startY+(450/scale),width=4/scale)
            canvas.create_line(startX+(685/scale),startY+(450/scale),startX-(25/scale),startY+(450/scale),width=4/scale)
            canvas.create_line(startX-(25/scale),startY+(450/scale),startX-(25/scale),startY+(597.5/scale),width=4/scale)
            canvas.create_line(startX-(25/scale),startY+(597.5/scale),startX+(25/scale),startY+(597.5/scale),width=4/scale)
            startY+=450/scale
    
class SubOperation(Operation):
    def __init__(self,operand1,operand2,depth):
        super().__init__(operand1,operand2,depth,"-","sub")
    def compute(self,varDictValues):
        operand1,operand2=self.getOperandsComputable(varDictValues)
        self.result=operand1-operand2
        return operand1,operand2
        
class MultOperation(Operation):
    def __init__(self,operand1,operand2,depth):
        super().__init__(operand1,operand2,depth,"x","mult")
    def compute(self,varDictValues):
        operand1,operand2=self.getOperandsComputable(varDictValues)
        self.result=operand1*operand2
        return operand1,operand2
        
class DivOperation(Operation):
    def __init__(self,operand1,operand2,depth):
        super().__init__(operand1,operand2,depth,"//","div")
    def compute(self,varDictValues):
        operand1,operand2=self.getOperandsComputable(varDictValues)
        self.result=operand1//operand2
        return operand1,operand2