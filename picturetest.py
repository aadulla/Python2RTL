from tkinter import *
from PIL import Image, ImageTk
from ArithmeticUnitsClasses import *
from GateClasses import *

####################################
# customize these functions
####################################

def init(data):
    pass
    

def mousePressed(event, data):
    pass
    

def keyPressed(event, data):
    # use event.char and event.keysym
    pass
    

def redrawAll(canvas,data):
    canvasMap=[]
    for i in range(data.height):
        tmpLst=[]
        for j in range (data.width):
            tmpLst.append(0)
        canvasMap.append(tmpLst)
    a=EightBitAdder(0,0)
    a.drawRTL(canvas,data,200,400,canvasMap)
    # ANDGateImg=Image.open("Full8BitAdder.png")
    # width=ImageTk.PhotoImage(ANDGateImg).width()
    # height=ImageTk.PhotoImage(ANDGateImg).height()
    # scale=1
    # ANDGateImgResized=ANDGateImg.resize((int(width//scale),int(height//scale)),Image.ANTIALIAS)
    # # ANDGateImgResized=ANDGateImgResized.rotate(90,expand=True)
    # data.image=ImageTk.PhotoImage(ANDGateImgResized)
    # label=Label(canvas,image=data.image)
    # label.image=data.image
    # startX=50
    # startY=300
    # print(width,height)
    # canvas.create_image(data.width/2,data.height/2,image=data.image)
    # ANDGateImg=Image.open("ANDGate.png")
    # width=ImageTk.PhotoImage(ANDGateImg).width()
    # height=ImageTk.PhotoImage(ANDGateImg).height()
    # scale=2.875
    # ANDGateImgResized=ANDGateImg.resize((int(width//scale),int(height//scale)),Image.ANTIALIAS)
    # ANDGateImgResized=ANDGateImgResized.rotate(270,expand=True)
    # data.image=ImageTk.PhotoImage(ANDGateImgResized)
    # label=Label(canvas,image=data.image)
    # label.image=data.image
    # canvas.create_image(startX+115,startY-100/scale,image=data.image)
    # canvas.create_image(startX+190,startY-100/scale,image=data.image)

    # canvas.create_line(startX+115,startY+4,startX+115,0,width=4)
    # canvas.create_line(startX+190,startY+4,startX+190,0,width=4)
    # canvas.create_line(startX+265,startY+4,startX+265,0,width=4)
    # canvas.create_line(startX+340,startY+4,startX+340,0,width=4)
    # canvas.create_line(startX+415,startY+4,startX+415,0,width=4)
    # canvas.create_line(startX+490,startY+4,startX+490,0,width=4)
    # canvas.create_line(startX+565,startY+4,startX+565,0,width=4)
    # canvas.create_line(startX+640,startY+4,startX+640,0,width=4)
    # canvas.create_line(startX+790,startY+4,startX+790,0,width=4)
    # 
    # canvas.create_line(startX+895,startY+229,1000,startY+229,width=4)
    # canvas.create_line(startX+3,startY+229,0,startY+229,width=4)
    # 
    # canvas.create_line(startX+115,startY+454,startX+115,1000,width=4)
    
    # scale=1
    # eightBitMultiplierImg=Image.open("Multiplier.png")
    # width=ImageTk.PhotoImage(eightBitMultiplierImg).width()
    # height=ImageTk.PhotoImage(eightBitMultiplierImg).height()
    # eightBitMultiplierImgResized=eightBitMultiplierImg.resize((int(width//scale),int(height//scale)),Image.ANTIALIAS)
    # data.image=ImageTk.PhotoImage(eightBitMultiplierImgResized)
    # label=Label(canvas,image=data.image)
    # label.image=data.image
    # startX=100
    # startY=100
    # print(width,height)
    # canvas.create_image(startX,startY,anchor="nw",image=data.image)
    # canvas.create_image(startX,startY+500,anchor="nw",image=data.image)
    # canvas.create_line(startX+61,startY+2,startX+61,0,width=4)
    # canvas.create_line(startX+136,startY+2,startX+136,0,width=4)
    # canvas.create_line(startX+286,startY+2,startX+286,0,width=4)
    # canvas.create_line(startX+361,startY+2,startX+361,0,width=4)
    # canvas.create_line(startX+436,startY+2,startX+436,0,width=4)
    # canvas.create_line(startX+511,startY+2,startX+511,0,width=4)
    # canvas.create_line(startX+586,startY+2,startX+586,0,width=4)
    # canvas.create_line(startX+661,startY+2,startX+661,0,width=4)
    # canvas.create_line(startX+736,startY+2,startX+736,0,width=4)
    # canvas.create_line(startX+811,startY+2,startX+811,0,width=4)
    # 
    # canvas.create_line(startX+31,startY+226,startX+31,800,width=2)
    # canvas.create_line(startX+68,startY+226,startX+68,800,width=2)
    # canvas.create_line(startX+105,startY+226,startX+105,800,width=2)
    # canvas.create_line(startX+143,startY+226,startX+143,800,width=2)
    # canvas.create_line(startX+180,startY+226,startX+180,800,width=2)
    # canvas.create_line(startX+218,startY+226,startX+218,800,width=2)
    # canvas.create_line(startX+255,startY+226,startX+255,800,width=2)
    # canvas.create_line(startX+293,startY+226,startX+293,800,width=2)
    # canvas.create_line(startX+405,startY+226,startX+405,800,width=2)
    # 
    
    




####################################
# use the run function as-is
####################################

def run():
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
    width=1500
    height= 2000
    data.width = width
    data.height = height
    root = Tk()
    root.resizable(width=False, height=False) # prevents resizing window
    init(data)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.configure(bd=0, highlightthickness=0, background="white")
    canvas.pack()
    
    scrollbar = Scrollbar(root)
    scrollbar.pack(side=RIGHT, fill=Y)
    
    
    scrollbar.config(command=canvas.yview)

    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    redrawAll(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")
run()