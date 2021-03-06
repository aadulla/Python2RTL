from tkinter import *
from OperationClasses import *
from PIL import Image, ImageTk


####################################
# customize these functions
####################################

def init(data):
    data.locationLst=[]
    data.flattenBlocksLst=[]
    data.radius=25
    data.image=None

def distance(x1,y1,x2,y2):
    return (((x2-x1)**2)+((y2-y1)**2)**0.5)

def mousePressed(event,data):
    # for i in range(len(data.locationLst)):
    #     x,y=data.locationLst[i]
    #     if distance(event.x,event.y,x,y)<data.radius:
    #         print(data.flattenBlocksLst[i].getOperation())
    #         data.flattenBlocksLst[i].drawRTL(data)
    #         print("result",data.flattenBlocksLst[i].getResult(data.varDictValues))
    #         break
    pass
def keyPressed(event, data):
    # use event.char and event.keysym
    pass

def flatten(lst):
    #this function, given a list "lst", returns a flattened version of the list
    #which is a 1D list of all the elements in lst
    if lst==[]:
        #base case: got to the end of the lst
        return []
    if isinstance(lst[0],list):
        #check to see if the first index of lst is a list
        return flatten(lst[0])+flatten(lst[1:])
    else:
        #if first index of lst is not a list, add it to the return list
        return [lst[0]]+flatten(lst[1:])

def redrawAll(canvas,data):
    xSpacing=data.width/len(data.blocksLst)
    middle=data.height/2
    centerX=25
    locationLst=[]
    max=0
    for i in data.blocksLst:
        if len(i)>max:
            max=len(i)
    ySpacing=(data.height-data.radius*2)/max
    for level in data.blocksLst:
        num=len(level)
        backShift=num-1
        centerY=middle-(backShift*ySpacing/2)
        for block in level:
            block.draw(data,canvas,centerX,centerY)
            locationLst.append((centerX,centerY))
            centerY+=ySpacing
        centerX+=xSpacing
    data.locationLst=locationLst
    data.flattenBlocksLst=flatten(data.blocksLst)
    length1=40
    length2=length1+10
    for i in range(len(data.flattenBlocksLst)-1,-1,-1):
        input1,input2=data.flattenBlocksLst[i].getInputDependenciesRaw()
        if input1 in data.flattenBlocksLst and input2 in data.flattenBlocksLst.and data.flattenBlocksLst[i].getOperation().getName()!="store":
            index1=data.flattenBlocksLst.index(input1)
            index2=data.flattenBlocksLst.index(input2)
            if index2>index1:
                cx1,cy1=data.locationLst[i]
                cx2,cy2=data.locationLst[index2]
                startBlock=data.flattenBlocksLst[index2]
                endBlock=data.flattenBlocksLst[i]
                width,height,input1TraceOrigin,input2TraceOrigin,outputTraceOrigin,scale=startBlock.getShapeDimensions()
                outputX,outputY,lineWidth=outputTraceOrigin
                startX=cx2+((outputX-(width/2))/scale)
                startY=cy2+((outputY-(height/2))/scale)
                width,height,input1TraceOrigin,input2TraceOrigin,outputTraceOrigin,scale=endBlock.getShapeDimensions()
                inputX,inputY,lineWidth=input2TraceOrigin
                endX=cx1+((inputX-(width/2))/scale)
                endY=cy1+((inputY-(height/2))/scale)
                canvas.create_line(startX,startY,endX,endY,width=lineWidth/scale)
                endBlock.useInputPort(2)
        if input1 in data.flattenBlocksLst and data.flattenBlocksLst[i].getOperation().getName()!="store":
            index=data.flattenBlocksLst.index(input1)
            cx1,cy1=data.locationLst[i]
            cx2,cy2=data.locationLst[index]
            startBlock=data.flattenBlocksLst[index]
            endBlock=data.flattenBlocksLst[i]
            width,height,input1TraceOrigin,input2TraceOrigin,outputTraceOrigin,scale=startBlock.getShapeDimensions()
            outputX,outputY,lineWidth=outputTraceOrigin
            startX=cx2+((outputX-(width/2))/scale)
            startY=cy2+((outputY-(height/2))/scale)
            if cy2>cy1 and 2 in endBlock.getInputPorts():
                width,height,input1TraceOrigin,input2TraceOrigin,outputTraceOrigin,scale=endBlock.getShapeDimensions()
                inputX,inputY,lineWidth=input2TraceOrigin
                endX=cx1+((inputX-(width/2))/scale)
                endY=cy1+((inputY-(height/2))/scale)
                endBlock.useInputPort(2)
            else:
                width,height,input1TraceOrigin,input2TraceOrigin,outputTraceOrigin,scale=endBlock.getShapeDimensions()
                inputX,inputY,lineWidth=input1TraceOrigin
                endX=cx1+((inputX-(width/2))/scale)
                endY=cy1+((inputY-(height/2))/scale)
                endBlock.useInputPort(1)
            canvas.create_line(startX,startY,endX,endY,width=lineWidth/scale)
        if input2 in data.flattenBlocksLst and data.flattenBlocksLst[i].getOperation().getName()!="store":
            index=data.flattenBlocksLst.index(input2)
            cx1,cy1=data.locationLst[i]
            cx2,cy2=data.locationLst[index]
            startBlock=data.flattenBlocksLst[index]
            endBlock=data.flattenBlocksLst[i]
            width,height,input1TraceOrigin,input2TraceOrigin,outputTraceOrigin,scale=startBlock.getShapeDimensions()
            outputX,outputY,lineWidth=outputTraceOrigin
            startX=cx2+((outputX-(width/2))/scale)
            startY=cy2+((outputY-(height/2))/scale)
            if cy2>cy1 and 2 in endBlock.getInputPorts():
                width,height,input1TraceOrigin,input2TraceOrigin,outputTraceOrigin,scale=endBlock.getShapeDimensions()
                inputX,inputY,lineWidth=input2TraceOrigin
                endX=cx1+((inputX-(width/2))/scale)
                endY=cy1+((inputY-(height/2))/scale)
                endBlock.useInputPort(2)
            else:
                width,height,input1TraceOrigin,input2TraceOrigin,outputTraceOrigin,scale=endBlock.getShapeDimensions()
                inputX,inputY,lineWidth=input1TraceOrigin
                endX=cx1+((inputX-(width/2))/scale)
                endY=cy1+((inputY-(height/2))/scale)
                endBlock.useInputPort(1)
            canvas.create_line(startX,startY,endX,endY,width=lineWidth/scale)
                
                

    
    #     if input1 in data.flattenBlocksLst:
    # for i in range(len(data.flattenBlocksLst)):
    #     input1,input2=data.flattenBlocksLst[i].getInputDependenciesRaw()
    #     if input1 in data.flattenBlocksLst:
    #         index=data.flattenBlocksLst.index(input1)
    #         cx1,cy1=data.locationLst[i]
    #         cx2,cy2=data.locationLst[index]
    #         canvas.create_line(cx1,cy1,cx2,cy2)
    #     elif isinstance(input1,int):
    #         cx1,cy1=data.locationLst[i]
    #         canvas.create_line(cx1,cy1,cx1,cy1-length1)
    #         canvas.create_text(cx1,cy1-length2,text=str(input1),font="arial 20 bold")
    #     elif input1!=None:
    #         cx1,cy1=data.locationLst[i]
    #         canvas.create_line(cx1,cy1,cx1,cy1-length1)
    #         canvas.create_text(cx1,cy1-length2,text=input1[:1],font="arial 20 bold")
    #     if input2 in data.flattenBlocksLst:
    #         index=data.flattenBlocksLst.index(input2)
    #         cx1,cy1=data.locationLst[i]
    #         cx2,cy2=data.locationLst[index]
    #         canvas.create_line(cx1,cy1,cx2,cy2)
    #     elif isinstance(input2,int):
    #         cx1,cy1=data.locationLst[i]
    #         canvas.create_line(cx1,cy1,cx1,cy1+length1)
    #         canvas.create_text(cx1,cy1+length2,text=str(input2),font="arial 20 bold")
    #     elif input2!=None:
    #         cx1,cy1=data.locationLst[i]
    #         canvas.create_line(cx1,cy1,cx1,cy1+length1)
    #         canvas.create_text(cx1,cy1+length2,text=input2[:1],font="arial 20 bold")
    # centerX=25
    # for level in data.blocksLst:
    #     num=len(level)
    #     backShift=num-1
    #     centerY=middle-(backShift*ySpacing/2)
    #     for block in level:
    #         block.draw(data,canvas,centerX,centerY)
    #         centerY+=ySpacing
    #     centerX+=xSpacing
    # data.varDictValues.draw(canvas,data)
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

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        # redrawAllWrapper(canvas, data)
        

    def keyPressedWrapper(event, canvas, data):
        # keyPressed(event, data)
        # redrawAllWrapper(canvas, data)
        pass

    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.blocksLst=blocksLst
    data.varDictValues=varDictValues
    max=0
    for i in data.blocksLst:
        if len(i)>max:
            max=len(i)
    width=len(blocksLst)*100
    height= max*150
    data.width = width
    data.height = height
    root = Toplevel()
    root.resizable(width=False, height=False) # prevents resizing window
    init(data)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.configure(bd=0, highlightthickness=0, background="white")
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    redrawAll(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")
