from tkinter import *
from PIL import Image, ImageTk
from Tester import *

####################################
# customize these functions
####################################

#example input to type into textbox:


# a=5
# b=4
# a=(a//1)
# n=((a+3)+(a+(a+1)))
# b=((b//2)+(a+1))
# c=((a-b)*a)
# d=((a+b)+c)
# e=(c*d)
# f=(a-(b//a))
# g=(f//(((b-c)*d)*(a-9)))



def init(data):
    pass
    

def mousePressed(event, data):
    pass
    
def callback(data):
    input = data.text.get("1.0",END)
    test(input)
    pass
    
def keyPressed(event, data):
    passE
    

def redrawAll(canvas,data):
    pass


####################################
# use the run function as-is
####################################EE

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
    width=1200
    height= 700
    data.width = width
    data.height = height
    data.text=""
    root = Tk()
    root.resizable(width=False, height=False) # prevents resizing window
    init(data)
    # create the root and the canvas
    canvas = Canvas(root, width=500, height=500)
    canvas.configure(bd=0, highlightthickness=0, background="white")
    canvas.pack()
    b= Button(root, text="Synthesize Blocks", command=lambda:callback(data))
    b.pack()
    data.text = Text(root)
    data.text.place(x=10,y=10,anchor="nw",width=400,height=400)
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    # redrawAll(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")
run()