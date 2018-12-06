from tkinter import *
from OperationClasses import *
from PIL import Image, ImageTk
from Distance import *
from Route import *
from BlockClass import *
from ArithmeticUnitsClasses import *


####################################
# customize these functions
####################################

def init(canvas,data):
    data.locationLst=[]
    data.image=None
    data.ySeparation=50
    data.canvasMap=[]
    data.lines=[]
    canvasMap=[]
    data.gatesLst=[]
    data.locationLst=[]
    for i in range(data.height):
        tmpLst=[]
        for j in range (data.width):
            tmpLst.append(0)
        canvasMap.append(tmpLst)
    drawGates(canvas,data,canvasMap)
    drawGatesConnections(canvas,data,canvasMap,4,4)
    data.canvasMap=canvasMap

def mousePressed1(event,data):
    pass
            
def mousePressed2(event,data):
    pass

def keyPressed(event, data):
    if event.keysym=="Up":
        for gate in data.gatesLst:
            gate.centerY+=20
        for line in data.lines:
            line[0][1]+=20
            line[1][1]+=20
        for location in data.locationLst:
            location[1]+=20
    elif event.keysym=="Down":
        for gate in data.gatesLst:
            gate.centerY-=20
        for line in data.lines:
            line[0][1]-=20
            line[1][1]-=20
        for location in data.locationLst:
            location[1]-=20
    elif event.keysym=="Right":
        for gate in data.gatesLst:
            gate.centerX+=20
        for line in data.lines:
            line[0][0]+=20
            line[1][0]+=20
        for location in data.locationLst:
            location[0]+=20
    elif event.keysym=="Left":
        for gate in data.gatesLst:
            gate.centerX-=20
        for line in data.lines:
            line[0][0]-=20
            line[1][0]-=20
        for location in data.locationLst:
            location[0]-=20
    pass

def routeInterpreter(canvas,data,commandsLst):
    #add in filtering for steps
    if commandsLst==None:
        return
    startLocation=commandsLst[0]
    commandsLst=commandsLst[1:]
    xCount,yCount=0,0
    prevCommand=commandsLst[0]
    for command in commandsLst:
        if command==prevCommand:
            xCount=xCount+command[0]
            yCount=yCount+command[1]
        else:
            x1,y1=startLocation
            x2,y2=x1+xCount,y1+yCount
            data.lines.append([[x1,y1],[x2,y2]])
            canvas.create_line(x1,y1,x2,y2,width=1)
            startLocation=x2,y2
            prevCommand=command
            xCount,yCount=command[0],command[1]
    x1,y1=startLocation
    x2,y2=x1+xCount,y1+yCount
    data.lines.append([[x1,y1],[x2,y2]])
    canvas.create_line(x1,y1,x2,y2,width=1)

def drawTrace(canvas,data,startGate,endGate,inputLoc,canvasMap,net,step,space):
    startCX,startCY=startGate.getCoordinates()
    endCX,endCY=endGate.getCoordinates()
    
    width,height,scale=startGate.getDimensions()
    outputX,outputY,lineWidth=startGate.outputTraceOrigin
    
    startX=int(startCX+((outputX-(width/2))/scale))
    startY=int(startCY+((outputY-(height/2))/scale))
    
    offset=0
    seenNet=False
    for j in range (step):
        # print(canvasMap[startY+j][startX:startX+space*2])
        for i in range(1,space*2):
            if canvasMap[startY+j][startX+i]!=0 and canvasMap[startY+j][startX+i]!=9:
                # print("close to block")
                # print(canvasMap[startY+j][startX+i])
                offset+=i+10
                seenNet=True
                # print("----------------")
                # print(net,offset)
                # print("----------------")
                break
    if not seenNet:
        offset+=step
    startX=startX+offset
    actualStart=startX-offset,startY
        
    
    
    width,height,scale=endGate.getDimensions()
    if inputLoc==1:
        inputX,inputY,lineWidth=endGate.input1TraceOrigin
    elif inputLoc==2:
        inputX,inputY,lineWidth=endGate.input2TraceOrigin
    endX=int(endCX+((inputX-(width/2))/scale))
    endY=int(endCY+((inputY-(height/2))/scale))
    offset=0
    seenNet=False
    for j in range (step):
        # print(canvasMap[endY+j][endX:endX+space*2])
        for i in range(1,space*2):
            if canvasMap[endY+j][startX+i]!=0 and canvasMap[endY+j][endX+i]!=9:
                # print("close to block")
                # print(canvasMap[startY+j][startX+i])
                offset+=i+10
                seenNet=True
                # print("----------------")
                # print(net,offset)
                # print("----------------")
                break
    if not seenNet:
        offset+=step
    endX=endX-offset
    actualEnd=endX+offset,endY
    commandsLst=None
    # condition=False
    # for i in canvasMap:
    #     for j in i:
    #         if j==net:
    #             condition=True
    #             break
    # if startX>endX:
    #     if condition:
    #         commandsLst=routeRight(canvasMap,(endX,endY),actualEnd,(startX,startY),actualStart,net,step,space,canvas)
    #     else:
    #         step=-step
    #         commandsLst=routeLeft(canvasMap,(startX,startY),actualStart,(endX,endY),actualEnd,net,step,space,canvas,"down")
    # else:
    #     if condition:
    #         step=-step
    #         commandsLst=routeLeft(canvasMap,(endX,endY),actualEnd,(startX,startY),actualStart,net,step,space,canvas)
    #     else:
    #         commandsLst=routeRight(canvasMap,(startX,startY),actualStart,(endX,endY),actualEnd,net,step,space,canvas)
    # if commandsLst==None:
    #     canvas.create_line(actualStart,actualEnd)
    # else:
    #     routeInterpreter(canvas,data,commandsLst)

def drawGatesConnections(canvas,data,canvasMap,step=5,space=10):
    for i in range(len(data.gatesLst)-1,-1,-1):
        print(i)
        input1,input2=data.gatesLst[i].getInputGates()
        if input1 in data.gatesLst:
            net=input1
            drawTrace(canvas,data,input1,data.gatesLst[i],1,canvasMap,net,step,space)
        if input2 in data.gatesLst:
            net=input2
            drawTrace(canvas,data,input2,data.gatesLst[i],2,canvasMap,net,step,space)
            
def drawGates(canvas,data,canvasMap):
    xSpacing=data.xSeparation
    middle=data.height//2
    centerX=100
    max=0
    for i in data.blocksLst:
        if len(i)>max:
            max=len(i)
    ySpacing=(data.height)//max
    for level in data.blocksLst:
        num=0
        for block in level:
            if block.operation.getName()!="store":
                num+=1
        if num%2==0:
            centerY=middle-800*(num/2-0.5)
        else:
            if num==1:
                centerY=middle
            else:
                centerY=middle-800*num/2
        for block in level:
            if block.operation.getName()!="store":
                print(block)
                print(centerX,centerY)
                data.gatesLst.extend(block.drawRTL(canvas,data,centerX,centerY,canvasMap))
                data.locationLst.append([centerX,centerY])
                centerY+=800
        centerX+=xSpacing
    
        
def redrawAll(canvas,data):
    for gate in data.gatesLst:
        gate.redraw(canvas,data)
    for line in data.lines:
        canvas.create_line(line[0],line[1])
    pass
                
                
####################################
# use the run function as-is
####################################

def runRTL(blocksLst):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper1(event, canvas, data):
        mousePressed1(event, data)
        #redrawAllWrapper(canvas, data)
    def mousePressedWrapper2(event, canvas, data):
        mousePressed2(event, data)
        

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)
        pass

    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.blocksLst=blocksLst
    data.xSeparation=225
    if len(data.blocksLst)>10:
        data.xSeparation+=5*len(data.blocksLst)-10
    max=0
    blocksLstNoStores=[]
    tmpLst=[]
    for i in data.blocksLst:
        for j in i:
            if j.operation.getName()!="store":
                tmpLst.append(j)
        blocksLstNoStores.append(tmpLst)
        tmpLst=[]
    for i in blocksLstNoStores:
        if len(i)>max:
            max=len(i)
    width=(len(blocksLst)*data.xSeparation)+200
    height= max*800
    data.width = width
    data.height = height

    root = Toplevel()
    root.resizable(width=False, height=False) # prevents resizing window
    # create the root and the canvas
    canvas = Canvas(root, width=1500, height=800)
    canvas.configure(bd=0, highlightthickness=0, background="white")
    canvas.pack()
    init(canvas,data)
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper1(event, canvas, data))
    root.bind("<Double-1>", lambda event:
                            mousePressedWrapper2(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    redrawAll(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")
