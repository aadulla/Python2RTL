from tkinter import *
from PIL import Image, ImageTk


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
    operand1=abs(21)
    operand2=abs(1)
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
    for i in range(bitLength+1):
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
    # canvas.create_image(100,0,anchor="nw",image=data.image)
    # canvas.create_image(100,450,anchor="nw",image=data.image)
    # canvas.create_line(785,331,785,450,width=4)
    # canvas.create_line(785,450,75,450,width=4)
    # canvas.create_line(75,450,75,597.5,width=4)
    # canvas.create_line(75,597.5,125,597.5,width=4)
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
    width=900
    height= 700
    data.width = width
    data.height = height
    root = Tk()
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
run()