from tkinter import *
from PIL import Image, ImageTk

class Gate(object):
    def __init__(self,name,input1,input2):
        self.name=name
        self.input1=input1
        self.input2=input2
        self.scale=2
        self.input1Gate=None
        self.input2Gate=None
        self.centerX=None
        self.centerY=None
    def setScale(self,scale):
        self.scale=scale
    def getScale(self):
        return self.scale
    def getInputs(self):
        return self.input1,self.input2
    def getOutput(self):
        return self.output
    def getName(self):
        return self.name
    def getInputGates(self):
        return self.input1Gate,self.input2Gate
    def getCoordinates(self):
        return self.centerX,self.centerY
    def getDimensions(self):
        return self.width,self.height,self.scale
    def redraw(self,canvas,data):
        self.draw(canvas,data,self.centerX,self.centerY)
    def __repr__(self):
        return self.name + " Gate\nInput1: " + str(self.input1) + "\nInput2: " + str(self.input2) + "\nOutput: " + str(self.output) +"\n"
        
class ANDGate(Gate):
    def __init__(self,input1=0,input2=0):
        self.width=315
        self.height=195
        self.input1TraceOrigin=(2,35,3.5)
        self.input2TraceOrigin=(2,160,3.5)
        self.outputTraceOrigin=(314,97,3.25)
        super().__init__("AND",input1,input2)
        self.output=self.compute()
    def compute(self):
        return int(self.input1 and self.input2)
    def draw(self,canvas,data,centerX,centerY,canvasMap=None,rotation=0):
        ANDGateImg=Image.open("ANDGate.png")
        width=int(self.width//self.scale)
        height=int(self.height//self.scale)
        ANDGateImgResized=ANDGateImg.resize((width,height),Image.ANTIALIAS)
        ANDGateImgResized=ANDGateImgResized.rotate(rotation,expand=True)
        data.image=ImageTk.PhotoImage(ANDGateImgResized)
        label=Label(canvas,image=data.image)
        label.image=data.image
        canvas.create_image(centerX,centerY,image=data.image)
        self.centerX=centerX
        self.centerY=centerY
        if canvasMap!=None:
            xStart=int(centerX-width//2)
            xEnd=int(centerX+width//2)
            yStart=int(centerY-height//2)
            yEnd=int(centerY+height//2)
            xPad=2
            yPad=5
            # canvas.create_rectangle(xStart-xPad,yStart-yPad,xEnd+xPad,yEnd+yPad,width=1)
            for i in range(xStart-xPad,xEnd+xPad+1):
                for j in range (yStart-yPad,yEnd+yPad+1):
                    canvasMap[j][i]=9

class ORGate(Gate):
    def __init__(self,input1=0,input2=0):
        self.width=317
        self.height=195
        self.input1TraceOrigin=(2,35,3.5)
        self.input2TraceOrigin=(2,160,3.5)
        self.outputTraceOrigin=(314,97,3.25)
        super().__init__("OR",input1,input2)
        self.output=self.compute()
    def compute(self):
        return int(self.input1 or self.input2)
    def draw(self,canvas,data,centerX,centerY,canvasMap=None):
        ORGateImg=Image.open("ORGate.png")
        width=int(self.width//self.scale)
        height=int(self.height//self.scale)
        ORGateImgResized=ORGateImg.resize((width,height),Image.ANTIALIAS)
        data.image=ImageTk.PhotoImage(ORGateImgResized)
        label=Label(canvas,image=data.image)
        label.image=data.image
        canvas.create_image(centerX,centerY,image=data.image)
        self.centerX=centerX
        self.centerY=centerY
        if canvasMap!=None:
            xStart=int(centerX-width//2)
            xEnd=int(centerX+width//2)
            yStart=int(centerY-height//2)
            yEnd=int(centerY+height//2)
            xPad=2
            yPad=5
            # canvas.create_rectangle(xStart-xPad,yStart-yPad,xEnd+xPad,yEnd+yPad,width=1)
            for i in range(xStart-xPad,xEnd+xPad+1):
                for j in range (yStart-yPad,yEnd+yPad+1):
                    canvasMap[j][i]=9
        
class XORGate(Gate):
    def __init__(self,input1=0,input2=0):
        self.width=313
        self.height=195
        self.input1TraceOrigin=(0,35,3.5)
        self.input2TraceOrigin=(0,160,3.5)
        self.outputTraceOrigin=(312,97,3.25)
        super().__init__("XOR",input1,input2)
        self.output=self.compute()
    def compute(self):
        return int(self.input1 and (not self.input2)) or ((not self.input1) and self.input2)
    def draw(self,canvas,data,centerX,centerY,canvasMap=None):
        XORGateImg=Image.open("XORGate.png")
        width=int(self.width//self.scale)
        height=int(self.height//self.scale)
        XORGateImgResized=XORGateImg.resize((width,height),Image.ANTIALIAS)
        data.image=ImageTk.PhotoImage(XORGateImgResized)
        label=Label(canvas,image=data.image)
        label.image=data.image
        canvas.create_image(centerX,centerY,image=data.image)
        self.centerX=centerX
        self.centerY=centerY
        if canvasMap!=None:
            xStart=int(centerX-width//2)
            xEnd=int(centerX+width//2)
            yStart=int(centerY-height//2)
            yEnd=int(centerY+height//2)
            xPad=2
            yPad=5
            # canvas.create_rectangle(xStart-xPad,yStart-yPad,xEnd+xPad,yEnd+yPad,width=1)
            for i in range(xStart-xPad,xEnd+xPad+1):
                for j in range (yStart-yPad,yEnd+yPad+1):
                    canvasMap[j][i]=9
    