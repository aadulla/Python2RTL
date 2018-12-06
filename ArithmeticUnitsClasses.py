from GateClasses import *
from tkinter import *
from PIL import Image, ImageTk
from Distance import *
from Route import *

#https://stackoverflow.com/questions/21871829/twos-complement-of-numbers-in-python
def toTwosComplement(bits, value):
    if value < 0:
        value = ( 1<<bits ) + value
    formatstring = '{:0%ib}' % bits
    return formatstring.format(value)

#https://stackoverflow.com/questions/26681469/writing-a-function-to-convert-twos-compliment-to-base-10-in-python
def bin(s):
    return 0 if not s else 2*bin(s[:-1]) + int(s[-1])

toDecimal = lambda s: bin(s[1:]) - int(s[0])*2**(len(s)-1)

    
class Adder(object):
    def __init__(self,input1,input2,carryIn):
        self.width=380
        self.height=380
        self.input1TraceOrigin=(2,127,3.25)
        self.input2TraceOrigin=(2,252,3.25)
        self.input3TraceOrigin=(188,2,3.25)
        self.output1TraceOrigin=(377,189,3.25)
        self.output2TraceOrigin=(188,377,3.25)
        self.scale=4
        self.input1=input1
        self.input2=input2
        self.carryIn=carryIn
        self.XOR1=XORGate(input1,input2)
        self.XOR1.input1Gate=None
        self.XOR1.input2Gate=None
        
        self.XOR2=XORGate(self.XOR1.getOutput(),carryIn)
        self.XOR2.input1Gate=self.XOR1
        self.XOR2.input2Gate=None
        
        self.AND1=ANDGate(input1,input2)
        self.AND1.input1Gate=None
        self.AND1.input2Gate=None
        
        self.AND2=ANDGate(self.XOR1.getOutput(),carryIn)
        self.AND2.input1Gate=self.XOR1
        self.AND2.input2Gate=None
        
        self.OR=ORGate(self.AND1.getOutput(),self.AND2.getOutput())
        self.OR.input1Gate=self.AND1
        self.OR.input2Gate=self.AND2
        
        self.gates=[self.XOR1,self.AND2,self.XOR2,self.AND1,self.OR]
        self.output=int(self.XOR2.getOutput())
        self.carryOut=int(self.OR.getOutput())
        self.locationLst=[]
    def setScale(self,scale):
        self.scale=scale
    def draw(self,canvas,data,centerX,centerY):
        adderImg=Image.open("FullAdder.png")
        adderImgResized=adderImg.resize((int(self.width//self.scale),int(self.height//self.scale)),Image.ANTIALIAS)
        data.image=ImageTk.PhotoImage(adderImgResized)
        label=Label(canvas,image=data.image)
        label.image=data.image
        canvas.create_image(centerX,centerY,image=data.image)
        
    def drawDeeper(self,data):
        root = Toplevel()
        width=800
        height=600
        root.resizable(width=False, height=False) # prevents resizing window
        canvas = Canvas(root, width=width, height=height)
        canvas.configure(bd=0, highlightthickness=0, background="white")
        canvas.pack()
        centerX=width/2
        centerY=height/2
        scale=self.XOR1.getScale()
        canvasMap=[]
        for i in range(height):
            tmpLst=[]
            for j in range (width):
                tmpLst.append(0)
            canvasMap.append(tmpLst)
        
        x=centerX-500/scale
        y=centerY-350/scale
        self.locationLst.append((x,y))
        self.XOR1.draw(canvas,data,x,y,canvasMap)
        
        x=centerX+500/scale
        y=centerY-290/scale
        self.locationLst.append((x,y))
        self.XOR2.draw(canvas,data,x,y,canvasMap)
        
        x=centerX-50/scale
        y=centerY+50/scale
        self.locationLst.append((x,y))
        self.AND1.draw(canvas,data,x,y,canvasMap)
        
        x=centerX-50/scale
        y=centerY+350/scale
        self.locationLst.append((x,y))
        self.AND2.draw(canvas,data,x,y,canvasMap)
        
        x=centerX+500/scale
        y=centerY+200/scale
        self.locationLst.append((x,y))
        self.OR.draw(canvas,data,x,y,canvasMap)
        
        drawGatesConnections(canvas,self.gates,canvasMap)
            
        root.bind("<Button-1>", lambda event: self.mousePressed(event,data))
        root.mainloop()

    def drawRTL(self,canvas,data,centerX,centerY,canvasMap):
        factor=5
        self.XOR1.setScale(self.XOR1.getScale()*factor)
        scale=self.XOR1.getScale()
        returnLst=[]
        
        x=centerX-550/scale
        y=centerY-350/scale
        self.locationLst.append((x,y))
        self.XOR1.draw(canvas,data,x,y,canvasMap)
        # returnLst.append((self.XOR1,(x,y)))
        returnLst.append(self.XOR1)
        
        self.XOR2.setScale(self.XOR2.getScale()*factor)
        scale=self.XOR2.getScale()
        x=centerX+500/scale
        y=centerY-290/scale
        self.locationLst.append((x,y))
        self.XOR2.draw(canvas,data,x,y,canvasMap)
        # returnLst.append((self.XOR2,(x,y)))
        returnLst.append(self.XOR2)
        
        self.AND1.setScale(self.AND1.getScale()*factor)
        scale=self.AND1.getScale()
        x=centerX-50/scale
        y=centerY+50/scale
        self.locationLst.append((x,y))
        self.AND1.draw(canvas,data,x,y,canvasMap)
        # returnLst.append((self.AND1,(x,y)))
        returnLst.append(self.AND1)
        
        self.AND2.setScale(self.AND2.getScale()*factor)
        scale=self.AND2.getScale()
        x=centerX-50/scale
        y=centerY+350/scale
        self.locationLst.append((x,y))
        self.AND2.draw(canvas,data,x,y,canvasMap)
        # returnLst.append((self.AND2,(x,y)))
        returnLst.append(self.AND2)
        
        self.OR.setScale(self.OR.getScale()*factor)
        scale=self.OR.getScale()
        x=centerX+500/scale
        y=centerY+200/scale
        self.locationLst.append((x,y))
        self.OR.draw(canvas,data,x,y,canvasMap)
        # returnLst.append((self.OR,(x,y)))
        returnLst.append(self.OR)
        return returnLst
        
    def mousePressed(self,event,data):
        for location in self.locationLst:
            x1,y1=location
            x2,y2=event.x,event.y
            if distance(x1,y1,x2,y2)<100:
                index=self.locationLst.index(location)
                print(self.gates[index])
    def getInputs(self):
        return self.input1,self.input2
    def getCarryIn(self):
        return self.carryIn
    def getOutput(self):
        return self.output
    def getCarryOut(self):
        return self.carryOut
    def getScale(self):
        return self.scale
    def getShapeDimensions(self):
        return self.width,self.height,self.input1TraceOrigin,self.input2TraceOrigin,self.input3TraceOrigin,self.output1TraceOrigin,self.output2TraceOrigin,self.scale
    def __repr__(self):
        return "Adder\nInput1: " + str(self.input1) + "\nInput2: " + str(self.input2) + "\nCarryIn: " + str(self.carryIn) + "\nOutput: " + str(self.output) +"\nCarryOut: " + str(self.carryOut) +"\n"

class EightBitAdder(object):
    def __init__(self,input1,input2,input2End=None):
        self.width=647
        self.height=440
        self.input1TraceOrigin=(0,112,6)
        self.input2TraceOrigin=(0,328,6)
        self.outputTraceOrigin=(645,225,5.25)
        self.scale=6
        self.locationLst=[]
        if input2End==None:
            self.input1Numerical=input1
            self.input2Numerical=input2
            input1=int(toTwosComplement(8,input1))
            input2=int(toTwosComplement(8,input2))
        else:
            strInput1=str(input1)
            if len(strInput1)!=8:
                zeroPads="0"*(8-len(strInput1))
                strInput1=zeroPads+strInput1
            self.input1Numerical=toDecimal(strInput1)
            strInput2=str(input2)
            if len(strInput2)!=7:
                zeroPads="0"*(7-len(strInput2))
                strInput2=zeroPads+strInput2
                strInput2=str(input2End)+strInput2
            self.input2Numerical=toDecimal(strInput2)
        self.input1=input1
        self.input2=input2
        addersLst=[]
        output=0
        if input2End!=None:
            for i in range(0,8):
                if i==0:
                    adder=Adder(input1%10,input2%10,0)
                    addersLst.append(adder)
                elif i==7:
                    adder=Adder(input1%10,input2End,addersLst[-1].getCarryOut())
                    adder.AND2.input2Gate=addersLst[-1].OR
                    adder.XOR2.input2Gate=addersLst[-1].OR
                    
                    addersLst.append(adder)
                else:
                    adder=Adder(input1%10,input2%10,addersLst[-1].getCarryOut())
                    adder.AND2.input2Gate=addersLst[-1].OR
                    adder.XOR2.input2Gate=addersLst[-1].OR
                    
                    addersLst.append(adder)
                output+=(int(addersLst[-1].getOutput()))*(10**i)
                input1//=10
                input2//=10
        else:
            for i in range(0,8):
                if i==0:
                    adder=Adder(input1%10,input2%10,0)
                    addersLst.append(adder)
                else:
                    adder=Adder(input1%10,input2%10,addersLst[-1].getCarryOut())
                    adder.AND2.input2Gate=addersLst[-1].OR
                    adder.XOR2.input2Gate=addersLst[-1].OR
                    
                    addersLst.append(adder)
                output+=(int(addersLst[-1].getOutput()))*(10**i)
                input1//=10
                input2//=10
        self.addersLst=addersLst
        self.output=int(output)
        strOutput=str(output)
        if len(strOutput)!=8:
            zeroPads="0"*(8-len(strOutput))
            strOutput=zeroPads+strOutput
        self.outputNumerical=toDecimal(strOutput)
        
        self.input1Gates=[]
        self.input2Gates=[]
        self.outputGates=[]
        for adder in self.addersLst:
            self.input1Gates.append(adder.XOR1)
            self.input1Gates.append(adder.AND1)
            self.input2Gates.append(adder.XOR1)
            self.input2Gates.append(adder.AND1)
            self.outputGates.append(adder.XOR2)
    def setScale(self,scale):
        self.scale=scale
    def getShapeDimensions(self):
        return self.width,self.height,self.input1TraceOrigin,self.input2TraceOrigin,self.outputTraceOrigin,self.scale
    def draw(self,canvas,data,centerX,centerY,canvasMap):
        eightBitAdderImg=Image.open("8BitAdder.png")
        width=ImageTk.PhotoImage(eightBitAdderImg).width()
        height=ImageTk.PhotoImage(eightBitAdderImg).height()
        eightBitAdderImgResized=eightBitAdderImg.resize((int(width//self.scale),int(height//self.scale)),Image.ANTIALIAS)
        width=ImageTk.PhotoImage(eightBitAdderImgResized).width()
        height=ImageTk.PhotoImage(eightBitAdderImgResized).height()
        xStart=int(centerX-width//2)
        xEnd=int(centerX+width//2)
        yStart=int(centerY-height//2)
        yEnd=int(centerY+height//2)
        xPad=3
        yPad=5
        # canvas.create_rectangle(xStart-xPad,yStart-yPad,xEnd+xPad,yEnd+yPad,width=1)
        for i in range(xStart-xPad,xEnd+xPad+1):
            for j in range (yStart-yPad,yEnd+yPad+1):
                canvasMap[j][i]=9
        data.image=ImageTk.PhotoImage(eightBitAdderImgResized)
        label=Label(canvas,image=data.image)
        label.image=data.image
        canvas.create_image(centerX,centerY,image=data.image)
    def drawDeeper(self,data):
        width,height,input1TraceOrigin,input2TraceOrigin,input3TraceOrigin,output1TraceOrigin,output2TraceOrigin,scale=self.addersLst[0].getShapeDimensions()
        root = Toplevel()
        root.resizable(width=False, height=False) # prevents resizing window
        canvasWidth=(width/scale*1)+(2*width/scale)
        canvasHeight=(height/scale*8)+(2*height/scale)
        canvas = Canvas(root, width=canvasWidth, height=canvasHeight)
        canvas.configure(bd=0, highlightthickness=0, background="white")
        canvas.pack()
        centerX=canvasWidth/2
        centerY=canvasHeight/2
        startY=centerY-((height*3)+(height/2))/scale
        for i in range(8):
            self.addersLst[i].draw(canvas,data,centerX,startY)
            startY+=height/scale
            self.locationLst.append((centerX,startY))
        startX=centerX-(width/2)/scale
        startY=centerY-((height*3)+(height/2))/scale-height/2/scale
        for i in range(7):
            carryStart=output2TraceOrigin
            x1,y1,lineWidth1=carryStart
            carryEnd=input3TraceOrigin
            x2,y2,lineWidth2=carryEnd
            x1=startX+x1/scale
            y1=startY+y1/scale
            startY+=height/scale
            x2=startX+x2/scale
            y2=startY+y2/scale
            canvas.create_line(x1,y1,x2,y2,width=(lineWidth1+lineWidth2)/2/scale)
        root.bind("<Button-1>", lambda event: self.mousePressed1(event,data))
        root.bind("<Double-1>", lambda event: self.mousePressed2(event,data))
        root.mainloop()
    def redraw(self,canvas,data,centerX,centerY):
        eightBitAdderImg=Image.open("8BitAdder.png")
        width=ImageTk.PhotoImage(eightBitAdderImg).width()
        height=ImageTk.PhotoImage(eightBitAdderImg).height()
        eightBitAdderImgResized=eightBitAdderImg.resize((int(width//self.scale),int(height//self.scale)),Image.ANTIALIAS)
        width=ImageTk.PhotoImage(eightBitAdderImgResized).width()
        height=ImageTk.PhotoImage(eightBitAdderImgResized).height()
        data.image=ImageTk.PhotoImage(eightBitAdderImgResized)
        label=Label(canvas,image=data.image)
        label.image=data.image
        canvas.create_image(centerX,centerY,image=data.image)
    def drawRTL(self,canvas,data,centerX,centerY,canvasMap):
        factor=5
        heightAdderAlone=600
        step=(heightAdderAlone-100)/factor
        centerY=centerY-step*3.5
        returnLst=[]
        for i in range(0,8):
            returnLst.extend(self.addersLst[i].drawRTL(canvas,data,centerX,centerY,canvasMap))
            canvas.create_text(centerX,centerY,text=str(i))
            centerY+=step
        return returnLst
        
    def mousePressed1(self,event,data):
        for location in self.locationLst:
            x1,y1=location
            x2,y2=event.x,event.y
            if distance(x1,y1,x2,y2)<100:
                index=self.locationLst.index(location)
                print(self.addersLst[index])
    def mousePressed2(self,event,data):
        for location in self.locationLst:
            x1,y1=location
            x2,y2=event.x,event.y
            if distance(x1,y1,x2,y2)<100:
                index=self.locationLst.index(location)
                self.addersLst[index].drawDeeper(data)
    def getInput1Gates(self):
        return self.input1Gates
    def getInput2Gates(self):
        return self.input2Gates
    def getOutputGates(self):
        return self.outputGates
    def getInputs(self):
        return self.input1,self.input2
    def getOutput(self):
        return self.output
    def getAddersLst(self):
        return self.addersLst
    def getCarryOut(self):
        return self.addersLst[-1].getCarryOut()
    def __repr__(self):
        return "8-bit Adder\nInput1: " + str(self.input1) + ", " + str(self.input1Numerical) + "\nInput2: " + str(self.input2) + ", " + str(self.input2Numerical) + "\nOutput: " + str(self.output) + ", " + str(self.outputNumerical) +"\n"

class Subtractor(object):
    def __init__(self,input1,input2,carryIn):
        self.width=455
        self.height=453
        self.input1TraceOrigin=(2,151,4)
        self.input2TraceOrigin=(2,301,4)
        self.input3TraceOrigin=(227.5,2,4)
        self.output1TraceOrigin=(452,226,4)
        self.output2TraceOrigin=(227.5,450,4)
        self.scale=4
        self.input1=input1
        self.input2=input2
        self.carryIn=carryIn
        self.XOR=XORGate(1,input2)
        self.adder=Adder(input1,self.XOR.getOutput(),carryIn)
        self.adder.XOR1.input2Gate=self.XOR
        self.adder.AND1.input2Gate=self.XOR
        self.componentsLst=[self.XOR,self.adder]
        self.output=self.adder.getOutput()
        self.carryOut=self.adder.getCarryOut()
        self.locationLst=[]
    def setScale(self,scale):
        self.scale=scale
    def draw(self,canvas,data,centerX,centerY):
        oneBitSubtractorImg=Image.open("1BitSubtractor.png")
        oneBitSubtractorImgResized=oneBitSubtractorImg.resize((int(self.width//self.scale),int(self.height//self.scale)),Image.ANTIALIAS)
        data.image=ImageTk.PhotoImage(oneBitSubtractorImgResized)
        label=Label(canvas,image=data.image)
        label.image=data.image
        canvas.create_image(centerX,centerY,image=data.image)
    def drawDeeper(self,data):
        root = Toplevel()
        width=800
        height=600
        root.resizable(width=False, height=False) # prevents resizing window
        canvas = Canvas(root, width=width, height=height)
        canvas.configure(bd=0, highlightthickness=0, background="white")
        canvas.pack()
        centerX=width/2
        centerY=height/2
        scale=self.XOR.getScale()
        
        self.adder.setScale(1)
        scale=self.adder.getScale()
        x=centerX-200/scale
        y=centerY+62/scale
        self.locationLst.append((x,y))
        self.XOR.draw(canvas,data,x,y)
        
        self.adder.setScale(1)
        scale=self.adder.getScale()
        x=centerX+55/scale
        y=centerY/scale
        self.locationLst.append((x,y))
        self.adder.draw(canvas,data,x,y)
            
        root.bind("<Button-1>", lambda event: self.mousePressed1(event,data))
        root.bind("<Double-1>", lambda event: self.mousePressed2(event,data))
        root.mainloop()
        
    def drawRTL(self,canvas,data,centerX,centerY,canvasMap):
        returnLst=[]
        returnLst.extend(self.adder.drawRTL(canvas,data,centerX,centerY,canvasMap))
        factor=5
        widthAdderAlone=800
        heightAdderAlone=600
        x=centerX-widthAdderAlone/2/factor
        y=centerY-heightAdderAlone/2/factor
        
        self.XOR.setScale(self.XOR.getScale()*factor)
        scale=self.XOR.getScale()
        width,height,scale=self.XOR.getDimensions()
        x=x
        y=centerY
        self.locationLst.append((x,y))
        self.XOR.draw(canvas,data,x,y,canvasMap)
        returnLst.append(self.XOR)
        
        return returnLst
        
    
    def mousePressed1(self,event,data):
        for location in self.locationLst:
            x1,y1=location
            x2,y2=event.x,event.y
            if distance(x1,y1,x2,y2)<100:
                index=self.locationLst.index(location)
                print(self.componentsLst[index])
    def mousePressed2(self,event,data):
        for location in self.locationLst:
            x1,y1=location
            x2,y2=event.x,event.y
            if distance(x1,y1,x2,y2)<100:
                index=self.locationLst.index(location)
                if index==1:
                    self.componentsLst[index].drawDeeper(data)
    def getInputs(self):
        return self.input1,self.input2
    def getCarryIn(self):
        return self.carryIn
    def getOutput(self):
        return self.output
    def getCarryOut(self):
        return self.carryOut
    def getShapeDimensions(self):
        return self.width,self.height,self.input1TraceOrigin,self.input2TraceOrigin,self.input3TraceOrigin,self.output1TraceOrigin,self.output2TraceOrigin,self.scale
    def __repr__(self):
        return "Subtractor\nInput1: " + str(self.input1) + "\nInput2: " + str(self.input2) + "\nCarryIn: " + str(self.carryIn) + "\nOutput: " + str(self.output) +"\nCarryOut: " + str(self.carryOut) +"\n"

class EightBitSubtractor(object):
    def __init__(self,input1,input2):
        self.input1Numerical=input1
        self.input2Numerical=input2
        self.width=648
        self.height=441
        self.input1TraceOrigin=(5,113,6)
        self.input2TraceOrigin=(5,329,6)
        self.outputTraceOrigin=(645,225,5.25)
        self.scale=6
        input1=int(toTwosComplement(8,input1))
        input2=int(toTwosComplement(8,input2))
        self.input1=input1
        self.input2=input2
        subtractorsLst=[]
        output=0
        for i in range(0,8):
            if i==0:
                subtractor=Subtractor(input1%10,input2%10,1)
                subtractorsLst.append(subtractor)
            else:
                subtractor=Subtractor(input1%10,input2%10,subtractorsLst[-1].getCarryOut())
                subtractor.adder.AND2.input2Gate=subtractorsLst[-1].adder.OR
                subtractor.adder.XOR2.input2Gate=subtractorsLst[-1].adder.OR
                
                subtractorsLst.append(subtractor)
            output+=(int(subtractorsLst[-1].getOutput()))*(10**i)
            input1//=10
            input2//=10
        self.subtractorsLst=subtractorsLst
        self.output=int(output)
        strOutput=str(output)
        if len(strOutput)!=8:
            zeroPads="0"*(8-len(strOutput))
            strOutput=zeroPads+strOutput
        self.outputNumerical=toDecimal(strOutput)
        self.locationLst=[]
        self.input1Gates=[]
        self.input2Gates=[]
        self.outputGates=[]
        for subtractor in self.subtractorsLst:
            self.input1Gates.append(subtractor.adder.XOR1)
            self.input1Gates.append(subtractor.adder.AND1)
            self.input2Gates.append(subtractor.XOR)
            self.input2Gates.append(subtractor.adder.AND1)
            self.outputGates.append(subtractor.adder.XOR2)
    def setScale(self,scale):
        self.scale=scale
    def getShapeDimensions(self):
        return self.width,self.height,self.input1TraceOrigin,self.input2TraceOrigin,self.outputTraceOrigin,self.scale
    def draw(self,canvas,data,x,y,canvasMap):
        eightBitSubtractorImg=Image.open("8BitSubtractor.png")
        width=ImageTk.PhotoImage(eightBitSubtractorImg).width()
        height=ImageTk.PhotoImage(eightBitSubtractorImg).height()
        eightBitSubtractorImgResized=eightBitSubtractorImg.resize((int(width//self.scale),int(height//self.scale)),Image.ANTIALIAS)
        width=ImageTk.PhotoImage(eightBitSubtractorImgResized).width()
        height=ImageTk.PhotoImage(eightBitSubtractorImgResized).height()
        xStart=int(x-width//2)
        xEnd=int(x+width//2)
        yStart=int(y-height//2)
        yEnd=int(y+height//2)
        xPad=3
        yPad=5
        # canvas.create_rectangle(xStart-xPad,yStart-yPad,xEnd+xPad,yEnd+yPad,width=1)
        for i in range(xStart-xPad,xEnd+xPad+1):
            for j in range (yStart-yPad,yEnd+yPad+1):
                canvasMap[j][i]=9
        data.image=ImageTk.PhotoImage(eightBitSubtractorImgResized)
        label=Label(canvas,image=data.image)
        label.image=data.image
        canvas.create_image(x,y,image=data.image)
    def drawDeeper(self,data):
        width,height,input1TraceOrigin,input2TraceOrigin,input3TraceOrigin,output1TraceOrigin,output2TraceOrigin,scale=self.subtractorsLst[0].getShapeDimensions()
        root = Toplevel()
        root.resizable(width=False, height=False) # prevents resizing window
        canvasWidth=(width/scale*1)+(2*width/scale)
        canvasHeight=(height/scale*8)+(2*height/scale)
        canvas = Canvas(root, width=canvasWidth, height=canvasHeight)
        canvas.configure(bd=0, highlightthickness=0, background="white")
        canvas.pack()
        centerX=canvasWidth/2
        centerY=canvasHeight/2
        startY=centerY-((height*3)+(height/2))/scale
        for i in range(8):
            self.subtractorsLst[i].draw(canvas,data,centerX,startY)
            startY+=height/scale
            self.locationLst.append((centerX,startY))
        startX=centerX-(width/2)/scale
        startY=centerY-((height*3)+(height/2))/scale-height/2/scale
        for i in range(7):
            carryStart=output2TraceOrigin
            x1,y1,lineWidth1=carryStart
            carryEnd=input3TraceOrigin
            x2,y2,lineWidth2=carryEnd
            x1=startX+x1/scale
            y1=startY+y1/scale
            startY+=height/scale
            x2=startX+x2/scale
            y2=startY+y2/scale
            canvas.create_line(x1,y1,x2,y2,width=(lineWidth1+lineWidth2)/2/scale)
        root.bind("<Button-1>", lambda event: self.mousePressed1(event,data))
        root.bind("<Double-1>", lambda event: self.mousePressed2(event,data))
        root.mainloop()
    def redraw(self,canvas,data,centerX,centerY):
        eightBitSubtractorImg=Image.open("8BitSubtractor.png")
        width=ImageTk.PhotoImage(eightBitSubtractorImg).width()
        height=ImageTk.PhotoImage(eightBitSubtractorImg).height()
        eightBitSubtractorImgResized=eightBitSubtractorImg.resize((int(width//self.scale),int(height//self.scale)),Image.ANTIALIAS)
        width=ImageTk.PhotoImage(eightBitSubtractorImgResized).width()
        height=ImageTk.PhotoImage(eightBitSubtractorImgResized).height()
        data.image=ImageTk.PhotoImage(eightBitSubtractorImgResized)
        label=Label(canvas,image=data.image)
        label.image=data.image
        canvas.create_image(centerX,centerY,image=data.image)
    def drawRTL(self,canvas,data,centerX,centerY,canvasMap):
        factor=5
        heightAdderAlone=600
        step=(heightAdderAlone-100)/factor
        centerY=centerY-step*3.5
        returnLst=[]
        for i in range(0,8):
            returnLst.extend(self.subtractorsLst[i].drawRTL(canvas,data,centerX,centerY,canvasMap))
            centerY+=step
        # print("in 8 bith subtractor",len(returnLst))
        # drawGatesConnections(canvas,returnLst,canvasMap,2,2)
        return returnLst
        
    def mousePressed1(self,event,data):
        for location in self.locationLst:
            x1,y1=location
            x2,y2=event.x,event.y
            if distance(x1,y1,x2,y2)<100:
                index=self.locationLst.index(location)
                print(self.subtractorsLst[index])
    def mousePressed2(self,event,data):
        for location in self.locationLst:
            x1,y1=location
            x2,y2=event.x,event.y
            if distance(x1,y1,x2,y2)<100:
                index=self.locationLst.index(location)
                self.subtractorsLst[index].drawDeeper(data)
    def getInput1Gates(self):
        return self.input1Gates
    def getInput2Gates(self):
        return self.input2Gates
    def getOutputGates(self):
        return self.outputGates
    def getInputs(self):
        return self.input1,self.input2
    def getOutput(self):
        return self.output
    def getSubtractorsLst(self):
        return self.subtractorsLst
    def __repr__(self):
        return "8-bit Subtractor\nInput1: " + str(self.input1) + ", " + str(self.input1Numerical) + "\nInput2: " + str(self.input2) + ", " + str(self.input2Numerical) + "\nOutput: " + str(self.output) + ", " + str(self.outputNumerical) +"\n"

class Multiplier(object):
    def __init__(self,input1a,input1b,input2a,input2b):
        #input1a:A 16 bits
        #input1b:B 1 bit
        #input2a:incoming 15 bits from previous stage
        #input2b: last 16 bit
        self.width=854
        self.height=455
        self.input1TraceOrigin=(61,2,4)
        self.input2TraceOrigin=(136,2,4)
        self.input3TraceOrigin=(286,2,4)
        self.input4TraceOrigin=(361,2,4)
        self.input5TraceOrigin=(436,2,4)
        self.input6TraceOrigin=(511,2,4)
        self.input7TraceOrigin=(586,2,4)
        self.input8TraceOrigin=(661,2,4)
        self.input9TraceOrigin=(736,2,4)
        self.input10TraceOrigin=(811,2,4)
        self.output1TraceOrigin=(61,2,4)
        self.output2TraceOrigin=(136,2,4)
        self.output2TraceOrigin=(211,2,4)
        self.output4TraceOrigin=(286,2,4)
        self.output5TraceOrigin=(361,2,4)
        self.output6TraceOrigin=(436,2,4)
        self.output7TraceOrigin=(511,2,4)
        self.output8TraceOrigin=(586,2,4)
        self.output9TraceOrigin=(736,2,4)
        self.scale=2
        self.input1a=input1a
        self.input1b=input1b
        self.input2a=input2a
        self.input2b=input2b
        self.andsLst=[]
        input1=0
        self.locationsLst=[]
        self.components=[]
        for i in range(0,8):
            andInput1=input1a%10
            andInput2=input1b
            AND=ANDGate(andInput1,andInput2)
            self.andsLst.append(AND)
            input1+=(int(self.andsLst[-1].getOutput()))*(10**i)
            input1a=input1a//10
        self.input1=input1
        self.eightBitAdder=EightBitAdder(input1,input2a,input2b)
        for i in range(0,8):
            self.eightBitAdder.addersLst[i].XOR1.input1Gate=self.andsLst[i]
            self.eightBitAdder.addersLst[i].AND1.input1Gate=self.andsLst[i]
        self.output=self.eightBitAdder.getOutput()
        self.carryOut=self.eightBitAdder.getCarryOut()
        self.components.append(self.eightBitAdder)
        for And in self.andsLst:
            self.components.append(And)
    def draw(self,canvas,data,x,y):
        multiplierImg=Image.open("Multiplier.png")
        multiplierImgResized=multiplierImg.resize((int(self.width//self.scale),int(self.height//self.scale)),Image.ANTIALIAS)
        data.image=ImageTk.PhotoImage(multiplierImgResized)
        label=Label(canvas,image=data.image)
        label.image=data.image
        canvas.create_image(x,y,image=data.image)
    def drawDeeper(self,data):
        full8BitAdderImg=Image.open("Full8BitAdder.png")
        width=ImageTk.PhotoImage(full8BitAdderImg).width()
        height=ImageTk.PhotoImage(full8BitAdderImg).height()
        scale=1
        root = Toplevel()
        root.resizable(width=False, height=False) # prevents resizing window
        canvasWidth=(width/scale*1)+(width/scale/2)
        canvasHeight=(height/scale*1)+(height/scale/2)
        canvas = Canvas(root, width=canvasWidth, height=canvasHeight)
        canvas.configure(bd=0, highlightthickness=0, background="white")
        canvas.pack()
        full8BitAdderImgResized=full8BitAdderImg.resize((int(width//scale),int(height//scale)),Image.ANTIALIAS)
        data.image=ImageTk.PhotoImage(full8BitAdderImgResized)
        label=Label(canvas,image=data.image)
        label.image=data.image
        centerX=canvasWidth/2/scale
        centerY=canvasHeight/2/scale
        canvas.create_image(centerX,centerY,image=data.image)
        self.locationsLst.append((centerX,centerY))
        centerX=centerX-width/2+115/scale
        centerY=centerY-height/2-100/(scale*2.875)
        for And in self.andsLst:
            And.setScale(scale*2.875)
            And.draw(canvas,data,centerX,centerY,270)
            self.locationsLst.append((centerX,centerY))
            centerX+=75/scale
        root.bind("<Button-1>", lambda event: self.mousePressed1(event,data))
        root.bind("<Double-1>", lambda event: self.mousePressed2(event,data))
        root.mainloop()
    def drawRTL(self,canvas,data,centerX,centerY,canvasMap):
        factor=5
        width,height,scale=self.andsLst[0].getDimensions()
        self.andsLst[0].setScale(self.andsLst[0].getScale()*factor)
        scale=self.andsLst[0].getScale()
        widthAdderAlone=600
        x=centerX-widthAdderAlone/2/factor
        heightAdderAlone=600
        step=(heightAdderAlone-100)/factor
        y=centerY-step*3.5
        returnLst=[]
        returnLst.extend(self.eightBitAdder.drawRTL(canvas,data,centerX,centerY,canvasMap))
        for i in range(0,8):
            if i!=0:
                self.andsLst[i].setScale(self.andsLst[i].getScale()*factor)
                scale=self.andsLst[i].getScale()
            self.andsLst[i].draw(canvas,data,x,y,canvasMap)
            returnLst.append(self.andsLst[i])
            y+=step
        # drawGatesConnections(canvas,returnLst,canvasMap,2,2)
        return returnLst
        
    def mousePressed1(self,event,data):
        for location in self.locationsLst:
            x1,y1=location
            x2,y2=event.x,event.y
            if distance(x1,y1,x2,y2)<100:
                index=self.locationsLst.index(location)
                print(self.components[index])
    def mousePressed2(self,event,data):
        for location in self.locationsLst:
            x1,y1=location
            x2,y2=event.x,event.y
            if distance(x1,y1,x2,y2)<100:
                index=self.locationsLst.index(location)
                self.components[index].drawDeeper(data)
    def setScale(self,scale):
        self.scale=scale
    def getInputs(self):
        return self.input1,self.input2
    def getOutput(self):
        return self.output
    def getCarryOut(self):
        return self.carryOut
    def __repr__(self):
        return "Multiplier\nInput1A: "+ str(self.input1a) + "\n" + "Input1B: "+ str(self.input1b) + "\n" + "Input1: " + str(self.input1) + "\n" + "Input2A: "+ str(self.input2a) + "\n" + "Input2B: "+ str(self.input2b) + "\n" + "output: "+ str(self.output)+ "\n" + "CarryOut: "+ str(self.carryOut) + "\n"

class EightBitMultiplier(object):
    def __init__(self,input1,input2):
        #input1=A
        #input2=B
        self.input1Numerical=input1
        self.input2Numerical=input2
        self.width=650
        self.height=425
        # self.keepoutRight=5
        # self.keepoutLeft=645
        # self.keepoutTop=0
        # self.keepoutBottom=420
        self.input1TraceOrigin=(5,111,6)
        self.input2TraceOrigin=(5,320,6)
        self.outputTraceOrigin=(645,213,5.25)
        self.scale=6
        input1=int(toTwosComplement(8,input1))
        input2=int(toTwosComplement(8,input2))
        self.input1=input1
        self.input2=input2
        self.multipliersLst=[]
        self.locationsLst=[]
        self.andsLst=[]
        output=0
        self.components=[]
        for i in range (0,7):
            multInput1a=input1
            multInput1b=input2%10
            multInput2=0
            if i==0:
                for i in range(0,8):
                    andInput1=multInput1a%10
                    andInput2=multInput1b
                    AND=ANDGate(andInput1,andInput2)
                    AND.setScale(15)
                    self.andsLst.append(AND)
                    multInput2+=(int(self.andsLst[-1].getOutput()))*(10**i)
                    multInput1a=multInput1a//10
                output=multInput2%10
                multInput2=multInput2//10
                input2=input2//10
                multInput1b=input2%10
                multiplier=Multiplier(input1,multInput1b,multInput2,0)
                for i in range(0,8):
                    multiplier.eightBitAdder.addersLst[i].XOR1.input2Gate=self.andsLst[i]
                    multiplier.eightBitAdder.addersLst[i].AND1.input2Gate=self.andsLst[i]
                
                self.multipliersLst.append(multiplier)
                self.components.append(multiplier)
            else:
                prevOutput=self.multipliersLst[-1].getOutput()
                output+=(prevOutput%10)*(10**i)
                multInput2=prevOutput//10
                prevCarryOut=self.multipliersLst[-1].getCarryOut()
                multiplier=Multiplier(input1,multInput1b,multInput2,prevCarryOut)
                for i in range(0,8):
                    if i==7:
                        multiplier.eightBitAdder.addersLst[i].XOR1.input2Gate=self.multipliersLst[-1].eightBitAdder.addersLst[i].OR
                        multiplier.eightBitAdder.addersLst[i].AND1.input2Gate=self.multipliersLst[-1].eightBitAdder.addersLst[i].OR
                    else:
                        multiplier.eightBitAdder.addersLst[i].XOR1.input2Gate=self.multipliersLst[-1].eightBitAdder.addersLst[i+1].XOR2
                        multiplier.eightBitAdder.addersLst[i].AND1.input2Gate=self.multipliersLst[-1].eightBitAdder.addersLst[i+1].XOR2
                self.multipliersLst.append(multiplier)
                self.components.append(multiplier)
            multiplier.setScale(4.5)
            input2=input2//10
        prevOutput=(self.multipliersLst[-1].getOutput())%10
        self.output=int(output+prevOutput*(10**7))
        strOutput=str(self.output)
        for And in self.andsLst:
            self.components.append(And)
        if len(strOutput)<8:
            zeroPads="0"*(8-len(strOutput))
            strOutput=zeroPads+strOutput
        self.outputNumerical=toDecimal(strOutput)
        self.input1Gates=[]
        self.input2Gates=[]
        self.outputGates=[]
        for i in range(7):
            if i==0:
                tmpInput1Gates=[]
                tmpInput2Gates=[]
                for AND in self.andsLst:
                    tmpInput1Gates.append(AND)
                    tmpInput2Gates.append(AND)
                self.input1Gates.append(tmpInput1Gates)
                self.input2Gates.append(tmpInput2Gates)
                tmpInput1Gates=[]
                tmpInput2Gates=[]
                for AND in self.multipliersLst[i].andsLst:
                    tmpInput1Gates.append(AND)
                    tmpInput2Gates.append(AND)
                self.input1Gates.append(tmpInput1Gates)
                self.input2Gates.append(tmpInput2Gates)
                self.outputGates.append(self.andsLst[0])
            else:
                tmpInput1Gates=[]
                tmpInput2Gates=[]
                for AND in self.multipliersLst[i].andsLst:
                    tmpInput1Gates.append(AND)
                    tmpInput2Gates.append(AND)
                self.input1Gates.append(tmpInput1Gates)
                self.input2Gates.append(tmpInput2Gates)
                self.outputGates.append(self.multipliersLst[i].eightBitAdder.addersLst[0].XOR2)
    def setScale(self,scale):
        self.scale=scale
    def getShapeDimensions(self):
        return self.width,self.height,self.input1TraceOrigin,self.input2TraceOrigin,self.outputTraceOrigin,self.scale
    def draw(self,canvas,data,x,y,canvasMap):
        eightBitMultiplierImg=Image.open("8BitMultiplier.png")
        eightBitMultiplierImgResized=eightBitMultiplierImg.resize((int(self.width//self.scale),int(self.height//self.scale)),Image.ANTIALIAS)
        width=ImageTk.PhotoImage(eightBitMultiplierImgResized).width()
        height=ImageTk.PhotoImage(eightBitMultiplierImgResized).height()
        xStart=int(x-width//2)
        xEnd=int(x+width//2)
        yStart=int(y-height//2)
        yEnd=int(y+height//2)
        xPad=3
        yPad=5
        # canvas.create_rectangle(xStart-xPad,yStart-yPad,xEnd+xPad,yEnd+yPad,width=1)
        for i in range(xStart-xPad,xEnd+xPad+1):
            for j in range (yStart-yPad,yEnd+yPad+1):
                canvasMap[j][i]=9
        data.image=ImageTk.PhotoImage(eightBitMultiplierImgResized)
        label=Label(canvas,image=data.image)
        label.image=data.image
        canvas.create_image(x,y,image=data.image)
    def redraw(self,canvas,data,centerX,centerY):
        eightBitMultiplierImg=Image.open("8BitMultiplier.png")
        eightBitMultiplierImgResized=eightBitMultiplierImg.resize((int(self.width//self.scale),int(self.height//self.scale)),Image.ANTIALIAS)
        width=ImageTk.PhotoImage(eightBitMultiplierImgResized).width()
        height=ImageTk.PhotoImage(eightBitMultiplierImgResized).height()
        data.image=ImageTk.PhotoImage(eightBitMultiplierImgResized)
        label=Label(canvas,image=data.image)
        label.image=data.image
        canvas.create_image(centerX,centerY,image=data.image)
    def drawDeeper(self,data):
        scale=self.multipliersLst[0].scale
        width=self.multipliersLst[0].width
        height=self.multipliersLst[0].height
        root = Toplevel()
        root.resizable(width=False, height=False) # prevents resizing window
        canvasWidth=(225*6/scale)+(width/scale*1)+(width/scale)
        canvasHeight=(height/scale*7)+(height/scale*1)+(height/scale)
        canvas = Canvas(root, width=canvasWidth, height=canvasHeight)
        canvas.configure(bd=0, highlightthickness=0, background="white")
        canvas.pack()
        startX=canvasWidth-width/scale
        startY=height/scale
        for multiplier in self.multipliersLst:
            multiplier.draw(canvas,data,startX,startY)
            self.locationsLst.append((startX,startY))
            startY+=height/scale
            startX-=225/scale
        startX,startY=self.locationsLst[0]
        startX=startX-width/2/scale
        startY=startY-height/2/scale
        x,y,lineWidth=self.multipliersLst[0].input3TraceOrigin
        startX=startX+x/scale
        startY=startY+y/scale
        andHeight=self.andsLst[0].height/self.andsLst[0].scale
        startY-=andHeight
        for And in self.andsLst:
            And.draw(canvas,data,startX,startY,270)
            self.locationsLst.append((startY,startY))
            startX+=75/scale
        
        # startX=canvasWidth
        # startY=centerY-((height*6)+(height/2))/scale-height/2/scale
        # for i in range(7):
        #     carryStart=output2TraceOrigin
        #     x1,y1,lineWidth1=carryStart
        #     carryEnd=input3TraceOrigin
        #     x2,y2,lineWidth2=carryEnd
        #     x1=startX+x1/scale
        #     y1=startY+y1/scale
        #     startY+=height/scale
        #     x2=startX+x2/scale
        #     y2=startY+y2/scale
        #     canvas.create_line(x1,y1,x2,y2,width=(lineWidth1+lineWidth2)/2/scale)
        root.bind("<Button-1>", lambda event: self.mousePressed1(event,data))
        root.bind("<Double-1>", lambda event: self.mousePressed2(event,data))
        root.mainloop()
        
        
    def drawRTL(self,canvas,data,centerX,centerY,canvasMap):
        factor=5
        widthAdderAlone=600
        xStep=(widthAdderAlone+250)/factor
        x=centerX-xStep*3.5
        heightAdderAlone=600
        yStep=(heightAdderAlone-100)/factor
        y=centerY-yStep*7.5
        returnLst=[]
        for i in range(0,7):
            returnLst.extend(self.multipliersLst[i].drawRTL(canvas,data,x,y,canvasMap))
            x+=xStep
            y+=yStep
        # x=centerX-xStep*3.5
        # y=centerY-yStep*3.5
        # for i in range(0,8):
    #         self.andsLst[i].setScale(self.andsLst[i].getScale()*factor)
    #         scale=self.andsLst[i].getScale()
        #     self.andsLst[i].draw(canvas,data,x,y,canvasMap)
        #     returnLst.append(self.andsLst[i])
        #     y+=step

        return returnLst
    
    def getInput1Gates(self):
        return self.input1Gates
    def getInput2Gates(self):
        return self.input2Gates
    def getOutputGates(self):
        return self.outputGates
        
    def mousePressed1(self,event,data):
        for location in self.locationsLst:
            x1,y1=location
            x2,y2=event.x,event.y
            if distance(x1,y1,x2,y2)<100:
                index=self.locationsLst.index(location)
                print(self.components[index])
    def mousePressed2(self,event,data):
        for location in self.locationsLst:
            x1,y1=location
            x2,y2=event.x,event.y
            if distance(x1,y1,x2,y2)<100:
                index=self.locationsLst.index(location)
                self.components[index].drawDeeper(data)
    def getOutput():
        return self.output
    def __repr__(self):
        return "8-bit Multiplier\nInput1: " + str(self.input1) + ", " + str(self.input1Numerical) + "\nInput2: " + str(self.input2) + ", " + str(self.input2Numerical) + "\nOutput: " + str(self.output) + ", " + str(self.outputNumerical) +"\n"
        
