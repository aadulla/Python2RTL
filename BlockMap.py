from tkinter import *
from OperationClasses import *
from PIL import Image, ImageTk
from Distance import *
from Route import *
from BlockClass import *
from GateMap import *


####################################
# customize these functions
####################################

def init(canvas,data):
    data.locationLst=[]
    data.image=None
    data.ySeparation=50
    data.canvasMap=[]
    data.objects=[]
    data.lines=[]
    canvasMap=[]
    for i in range(data.height):
        tmpLst=[]
        for j in range (data.width):
            tmpLst.append(0)
        canvasMap.append(tmpLst)
    drawBlocks(canvas,data,canvasMap)
    drawBlockConnections(canvas,data,canvasMap)
    data.canvasMap=canvasMap

def mousePressed1(event,data):
    print(event.x,event.y)
    # print(data.canvasMap[event.y][event.x])
    for location in data.locationLst:
        x1,y1=location
        x2,y2=event.x,event.y
        if distance(x1,y1,x2,y2)<100:
            index=data.locationLst.index(location)
            block=data.flattenBlocksLst[index]
            print("operation:",block.operation)
            print(block.operation.arithmeticUnit)
            break
            
def mousePressed2(event,data):
    for location in data.locationLst:
        x1,y1=location
        x2,y2=event.x,event.y
        if distance(x1,y1,x2,y2)<100:
            index=data.locationLst.index(location)
            block=data.flattenBlocksLst[index]
            block.operation.arithmeticUnit.drawDeeper(data)
            break

def keyPressed(event, data):
    if event.keysym=="Up":
        for block in data.flattenBlocksLst:
            block.centerY+=20
        for line in data.lines:
            line[0][1]+=20
            line[1][1]+=20
        for location in data.locationLst:
            location[1]+=20
    elif event.keysym=="Down":
        for block in data.flattenBlocksLst:
            block.centerY-=20
        for line in data.lines:
            line[0][1]-=20
            line[1][1]-=20
        for location in data.locationLst:
            location[1]-=20
    elif event.keysym=="Right":
        for block in data.flattenBlocksLst:
            block.centerX+=20
        for line in data.lines:
            line[0][0]+=20
            line[1][0]+=20
        for location in data.locationLst:
            location[0]+=20
    elif event.keysym=="Left":
        for block in data.flattenBlocksLst:
            block.centerX-=20
        for line in data.lines:
            line[0][0]-=20
            line[1][0]-=20
        for location in data.locationLst:
            location[0]-=20
    pass

def flatten(lst):
    if lst==[]:
        return []
    if isinstance(lst[0],list):
        return flatten(lst[0])+flatten(lst[1:])
    else:
        return [lst[0]]+flatten(lst[1:])

def routeInterpreter(canvas,data,commandsLst):
    #add in filtering for steps
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

def drawBlocks(canvas,data,canvasMap):
    xSpacing=(data.width-100)//len(data.blocksLst)
    middle=data.height//2
    centerX=100
    max=0
    for i in data.blocksLst:
        if len(i)>max:
            max=len(i)
    ySpacing=(data.height-data.ySeparation)//max
    for level in data.blocksLst:
        num=len(level)
        backShift=num-1
        centerY=middle-(backShift*ySpacing/2)
        for block in level:
            if block.getOperation().getName()=="store":
                block.draw(canvas,data,centerX-data.xSeparation//3,centerY,canvasMap)
                data.locationLst.append([centerX-data.xSeparation//3,centerY])
            else:
                block.draw(canvas,data,centerX,centerY,canvasMap)
                data.locationLst.append([centerX,centerY])
            centerY+=ySpacing
        centerX+=xSpacing
        
def drawTrace(canvas,data,startBlockIndex,endBlockIndex,canvasMap,net):
    # print(net)
    # if isinstance(net,int):
    #     endCX,endCY=data.locationLst[endBlockIndex]
    storeBlockInputOffsetDict={}
    blockNum=0
    for i in range(len(data.flattenBlocksLst)):
        if data.flattenBlocksLst[i].operation.getName()=="store":
            storeBlockInputOffsetDict[blockNum]=[i]
            blockNum+=1
    blockNum=0
    offsetCount=1
    for level in data.blocksLst:
        for block in level:
            if block.operation.getName()=="store":
                storeBlockInputOffsetDict[blockNum].append(offsetCount)
                blockNum+=1
                offsetCount+=1
        offsetCount=1
    startCX,startCY=data.locationLst[startBlockIndex]
    endCX,endCY=data.locationLst[endBlockIndex]
    startBlock=data.flattenBlocksLst[startBlockIndex]
    endBlock=data.flattenBlocksLst[endBlockIndex]
    width,height,input1TraceOrigin,input2TraceOrigin,outputTraceOrigin,scale=startBlock.getShapeDimensions()

    if startBlock.getOperation().getName()=="store":
        outputX,outputY,lineWidth=input1TraceOrigin
        for key,val in storeBlockInputOffsetDict.items():
            if val[0]==startBlockIndex:
                offset=val[1]
                break
        startX=int(startCX+((outputX-(width/2))/scale))-10*offset
        startY=int(startCY+((outputY-(height/2))/scale))
        actualStart=startX+10*offset,startY
    else:
        outputX,outputY,lineWidth=outputTraceOrigin
        startX=int(startCX+((outputX-(width/2))/scale))
        startY=int(startCY+((outputY-(height/2))/scale))
        offset=0
        # print(canvasMap[startY][startX:startX+16])
        seenNet=False
        for j in range (-5,5):
            # print(canvasMap[startY+j][startX:startX+16])
            for i in range(1,11):
                if canvasMap[startY+j][startX+i]!=0 and canvasMap[startY+j][startX+i]!=9:
                    # print("close to block")
                    # print(canvasMap[startY+j][startX+i])
                    offset+=i+10
                    seenNet=True
                    break
        if not seenNet:
            offset+=10
        startX=startX+offset
        actualStart=startX-offset,startY
    
    width,height,input1TraceOrigin,input2TraceOrigin,outputTraceOrigin,scale=endBlock.getShapeDimensions()
        
    if endBlock.getOperation().getName()=="store":
        inputX,inputY,lineWidth=input1TraceOrigin
        endX=int(endCX+((inputX-(width/2))/scale))-5
        endY=int(endCY+((inputY-(height/2))/scale))
        endBlock.useInputPort(1)
        # canvas.create_line(startX,startY,endX,endY,width=lineWidth/scale)
    elif startCX<endCX and 2 in endBlock.getInputPorts():
        inputX,inputY,lineWidth=input2TraceOrigin
        endX=int(endCX+((inputX-(width/2))/scale))-5
        endY=int(endCY+((inputY-(height/2))/scale))
        endBlock.useInputPort(2)
        # canvas.create_line(startX,startY,endX,endY,width=lineWidth/scale)
    else:
        inputX,inputY,lineWidth=input1TraceOrigin
        endX=int(endCX+((inputX-(width/2))/scale))-5
        endY=int(endCY+((inputY-(height/2))/scale))
    # print("start",startBlock.operation)
    # print(startX,startY)
    # print("end",endBlock.operation)
    # print(endX,endY)
    # print()
    actualEnd=endX+5,endY
    # commandsLst=route(canvasMap,(startX,startY),actualStart,(endX,endY),actualEnd,net,canvas)
    if endBlock.getOperation().getName()=="store":
        isStore=True
    else:
        isStore=False
    condition=False
    for i in canvasMap:
        for j in i:
            if j==net:
                condition=True
                break
    if startBlock.getOperation().getName()=="store":
        condition=False
    if endBlock.getOperation().getName()=="store":
        condition=True
    if condition==True:
        dir="right"
    else:
        dir="left"
    if dir=="right":
        print("right")
        step=5
        space=10
        commandsLst=routeRight(canvasMap,(startX,startY),actualStart,(endX,endY),actualEnd,net,step,space,canvas)
    else:
        print("left")
        step=-5
        space=10
        commandsLst=routeLeft(canvasMap,(endX,endY),actualEnd,(startX,startY),actualStart,net,step,space,canvas)
    
    
    
    routeInterpreter(canvas,data,commandsLst)
        # canvas.create_line(startX,startY,endX,endY,width=lineWidth/scale)

def getShorthandOutput(block):
    return str(block.getOutput()).replace("-","")
    
def joinUnits(blockSource,blockDest,input):
    print("yay")
    sourceGates=blockSource.arithmeticUnit.getOutputGates()
    if blockDest.getName()=="add" or blockDest.getName()=="sub":
        if input==1:
            inputGates=blockDest.arithmeticUnit.getInput1Gates()
            for i in range(0,16,2):
                inputGates[i].input1Gate=sourceGates[i//2] 
                inputGates[i+1].input1Gate=sourceGates[i//2] 
        else:
            inputGates=blockDest.arithmeticUnit.getInput2Gates()
            for i in range(0,16,2):
                inputGates[i].input2Gate=sourceGates[i//2] 
                inputGates[i+1].input2Gate=sourceGates[i//2] 
    elif blockDest.getName()=="mult":
        if input==1:
            inputGates=blockDest.arithmeticUnit.getInput1Gates()
            for i in range(8):
                for AND in inputGates[i]:
                    AND.input1Gate=sourceGates[i]
        else:
            inputGates=blockDest.arithmeticUnit.getInput2Gates()
            for i in range(8):
                for j in range(8):
                    inputGates[i][j].input2Gate=sourceGates[j]
            
    
def drawBlockConnections(canvas,data,canvasMap):
    for i in range(len(data.flattenBlocksLst)-1,-1,-1):
        input1,input2=data.flattenBlocksLst[i].getInputDependenciesRaw()
        print(i)
        # print("input1")
        # print(input1)
        # print()
        # print("input2")
        # print(input2)
        # print("----------------------")
        if input1 in data.flattenBlocksLst:
            # print(data.flattenBlocksLst[i])
            startBlockIndex=data.flattenBlocksLst.index(input1)
            endBlockIndex=i
            if data.flattenBlocksLst[startBlockIndex].getOperation().getName()=="store" or data.flattenBlocksLst[endBlockIndex].getOperation().getName()=="store":
                net=getShorthandOutput(input1)
            else:
                net=input1
            drawTrace(canvas,data,startBlockIndex,endBlockIndex,canvasMap,net)
        # elif isinstance(input1,int):
        #     endBlockIndex=i
        #     drawTrace(canvas,data,None,endBlockIndex,None,input1)
        else:
            for j in range(len(data.flattenBlocksLst)):
                if input1==data.flattenBlocksLst[j].getOutput():
                    startBlockIndex=j
                    endBlockIndex=i
                    net=input1
                    drawTrace(canvas,data,startBlockIndex,endBlockIndex,canvasMap,net)
                    startBlock=data.flattenBlocksLst[startBlockIndex]
                    endBlock=data.flattenBlocksLst[endBlockIndex]
                    if startBlock.operation.getName()!="store":
                        joinUnits(startBlock.operation,endBlock.operation,1)
                    else:
                        startOperation=startBlock.operation.operand2
                        joinUnits(startOperation,endBlock.operation,1)
        if input2 in data.flattenBlocksLst:
            # print(data.flattenBlocksLst[i])
            startBlockIndex=data.flattenBlocksLst.index(input2)
            endBlockIndex=i
            if data.flattenBlocksLst[startBlockIndex].getOperation().getName()=="store" or data.flattenBlocksLst[endBlockIndex].getOperation().getName()=="store":
                net=getShorthandOutput(input2)
            else:
                net=input2
            drawTrace(canvas,data,startBlockIndex,endBlockIndex,canvasMap,net)
        # elif isinstance(input2,int):
        #     endBlockIndex=i
        #     drawTrace(canvas,data,None,endBlockIndex,None,input2)
        else:
            for j in range(len(data.flattenBlocksLst)):
                if input2==data.flattenBlocksLst[j].getOutput():
                    startBlockIndex=j
                    endBlockIndex=i
                    net=input2
                    drawTrace(canvas,data,startBlockIndex,endBlockIndex,canvasMap,net)
                    startBlock=data.flattenBlocksLst[startBlockIndex]
                    endBlock=data.flattenBlocksLst[endBlockIndex]
                    if startBlock.operation.getName()!="store":
                        joinUnits(startBlock.operation,endBlock.operation,2)
                    else:
                        startOperation=startBlock.operation.operand2
                        joinUnits(startOperation,endBlock.operation,2)
            

def redrawAll(canvas,data):
    for block in data.flattenBlocksLst:
        block.redraw(canvas,data)
    for line in data.lines:
        canvas.create_line(line[0],line[1])
        
def callback(data):
    runRTL(data.blocksLst)
                
                
####################################
# use the run function as-is
####################################

def run(blocksLst,varDictValues):
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
    data.flattenBlocksLst=flatten(data.blocksLst)
    data.varDictValues=varDictValues
    data.xSeparation=225
    if len(data.blocksLst)>10:
        data.xSeparation+=5*len(data.blocksLst)-10
    max=0
    for i in data.blocksLst:
        if len(i)>max:
            max=len(i)
    width=(len(blocksLst)*data.xSeparation)+200
    height= max*150
    data.width = width
    data.height = height

    root = Toplevel()
    root.resizable(width=False, height=False) # prevents resizing window
    # create the root and the canvas
    canvas = Canvas(root, width=1500, height=800)
    canvas.configure(bd=0, highlightthickness=0, background="white")
    canvas.pack()
    b= Button(root, text="Synthesize RTL", command=lambda:callback(data))
    b.pack()
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
