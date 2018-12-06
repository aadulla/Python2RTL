# given canvas and images present
# get width and height of canvas
# get location, width, height of image
# make a 2d array with canvas width and height, populate with zeros
# populate images on array with x's
# given start and end point, can only move in 4 directirons (up, right, down, left)
# order list of moves in optimal path
#     figure out angle between current location adn end
#     then order directions in that manner
# after making a move, populate with 1
# 
# after changin direction, add command to draw canvas line

# given a grid, not allowed to put traces next to another one
# if crossing onto a "1", look at 3x3 square around that "1" to see which direction it is going
# tentatively put "a", then convert to "1\"

import copy
from Distance import *
from BlockClass import *

# def checkNotPresentGrid(grid,finishedGrids):
#     if finishedGrids==[]:
#         return True
#     for finishedGrid in finishedGrids:
#         if grid==finishedGrid:
#             return False
#     return True

def isComplete(currLocation,endLocation,dist):
    x1,y1=currLocation
    x2,y2=endLocation
    if distance(x1,y1,x2,y2)<=dist:
        return True
    return False

def getSlopeLeft(currentLocation,endLocation):
    x1,y1=currentLocation
    x2,y2=endLocation
    if x1==x2:
        if y2>y1:
            return "down"
        else:
            return "up"
    elif x2>x1:
        return "right"
    else:
        slope=-((y2-y1)/(x2-x1))
        return slope
        
        
# def getMovesLstLeft(currentLocation,endLocation,prevMove,step):
#     slope=getSlopeLeft(currentLocation,endLocation)
#     # print("slope",slope)
#     # print("slope",slope)
#     if slope=="down":
#         return [(0,-step),(step,0),(0,step),(-step,0)]
#     elif slope=="up":
#         return [(0,step),(step,0),(0,-step,(-step,0))]
#     elif slope=="right":
#         if endLocation[1]<currentLocation[1]:
#             return [(0,step),(-step,0),(0,-step),(-step,0)]
#         else:
#             return [(0,-step),(-step,0),(0,step),(-step,0)]
#     if slope==0:
#         return [(step,0),(0,step),(0,-step),(-step,0)]
#     elif slope>=1:
#         if prevMove==(0,-step):
#             return [(0,-step),(step,0),(0,step),(-step,0)]
#         elif prevMove==(step,0):
#             return [(step,0),(0,-step),(0,step),(-step,0)]
#         else:
#             return [(step,0),(0,-step),(0,step),(-step,0)]
#     elif slope>=0:
#         if prevMove==(0,-step):
#             return [(0,-step),(step,0),(0,step),(-step,0)]
#         elif prevMove==(step,0):
#             return [(step,0),(0,-step),(0,step),(-step,0)]
#         else:
#             return [(step,0),(0,-step),(0,step),(-step,0)]
#     elif slope>=-1:
#         if prevMove==(step,0):
#             return [(step,0),(0,step),(0,-step),(-step,0)]
#         elif prevMove==(0,step):
#             return [(0,step),(step,0),(0,-step),(-step,0)]
#         else:
#             return [(step,0),(0,step),(0,-step),(-step,0)]
#     elif slope<-1:
#         if prevMove==(step,0):
#             return [(step,0),(0,step),(0,-step),(-step,0)]
#         elif prevMove==(0,step):
#             return [(0,step),(step,0),(0,-step),(-step,0)]
#         else:
#             return  [(step,0),(0,step),(0,-step),(-step,0)]
# 
# 
# def getMovesLstLeftDown(currentLocation,endLocation,prevMove,step):
#     slope=getSlopeLeft(currentLocation,endLocation)
#     # print("slope",slope)
#     # print("slope",slope)
#     if slope=="down":
#         return [(0,-step),(step,0),(0,step),(-step,0)]
#     elif slope=="up":
#         return [(0,step),(step,0),(0,-step,(-step,0))]
#     elif slope=="right":
#         if endLocation[1]<currentLocation[1]:
#             return [(0,step),(-step,0),(0,-step),(-step,0)]
#         else:
#             return [(0,-step),(-step,0),(0,step),(-step,0)]
#     if slope==0:
#         return [(step,0),(0,step),(0,-step),(-step,0)]
#     elif slope>=1:
#         if prevMove==(0,-step):
#             return [(0,-step),(step,0),(0,step),(-step,0)]
#         elif prevMove==(step,0):
#             return [(step,0),(0,-step),(0,step),(-step,0)]
#         else:
#             return [(0,-step),(step,0),(0,step),(-step,0)]
#     elif slope>=0:
#         if prevMove==(0,-step):
#             return [(0,-step),(step,0),(0,step),(-step,0)]
#         elif prevMove==(step,0):
#             return [(step,0),(0,-step),(0,step),(-step,0)]
#         else:
#             return [(0,-step),(step,0),(0,step),(-step,0)]
#     elif slope>=-1:
#         if prevMove==(step,0):
#             return [(step,0),(0,step),(0,-step),(-step,0)]
#         elif prevMove==(0,step):
#             return [(0,step),(step,0),(0,-step),(-step,0)]
#         else:
#             return [(0,step),(step,0),(0,-step),(-step,0)]
#     elif slope<-1:
#         if prevMove==(step,0):
#             return [(step,0),(0,step),(0,-step),(-step,0)]
#         elif prevMove==(0,step):
#             return [(0,step),(step,0),(0,-step),(-step,0)]
#         else:
#             return  [(0,step),(step,0),(0,-step),(-step,0)]

def getMovesLstLeft(currentLocation,endLocation,prevMove,step):
    slope=getSlopeLeft(currentLocation,endLocation)
    # print("slope",slope)
    # print("slope",slope)
    if slope=="down":
        return [(0,-step),(step,0),(0,step)]
    elif slope=="up":
        return [(0,step),(step,0),(0,-step)]
    elif slope=="right":
        if endLocation[1]<currentLocation[1]:
            return [(0,step),(-step,0),(0,-step)]
        else:
            return [(0,-step),(-step,0),(0,step)]
    if slope==0:
        return [(step,0),(0,step),(0,-step)]
    elif slope>=1:
        if prevMove==(0,-step):
            return [(0,-step),(step,0),(0,step)]
        elif prevMove==(step,0):
            return [(step,0),(0,-step),(0,step)]
        else:
            return [(step,0),(0,-step),(0,step)]
    elif slope>=0:
        if prevMove==(0,-step):
            return [(0,-step),(step,0),(0,step)]
        elif prevMove==(step,0):
            return [(step,0),(0,-step),(0,step)]
        else:
            return [(step,0),(0,-step),(0,step)]
    elif slope>=-1:
        if prevMove==(step,0):
            return [(step,0),(0,step),(0,-step)]
        elif prevMove==(0,step):
            return [(0,step),(step,0),(0,-step)]
        else:
            return [(step,0),(0,step),(0,-step)]
    elif slope<-1:
        if prevMove==(step,0):
            return [(step,0),(0,step),(0,-step)]
        elif prevMove==(0,step):
            return [(0,step),(step,0),(0,-step)]
        else:
            return  [(step,0),(0,step),(0,-step)]


def getMovesLstLeftDown(currentLocation,endLocation,prevMove,step):
    slope=getSlopeLeft(currentLocation,endLocation)
    # print("slope",slope)
    # print("slope",slope)
    if slope=="down":
        return [(0,-step),(step,0),(0,step)]
    elif slope=="up":
        return [(0,step),(step,0),(0,-step)]
    elif slope=="right":
        if endLocation[1]<currentLocation[1]:
            return [(0,step),(-step,0),(0,-step)]
        else:
            return [(0,-step),(-step,0),(0,step)]
    if slope==0:
        return [(step,0),(0,step),(0,-step)]
    elif slope>=1:
        if prevMove==(0,-step):
            return [(0,-step),(step,0),(0,step)]
        elif prevMove==(step,0):
            return [(step,0),(0,-step),(0,step)]
        else:
            return [(0,-step),(step,0),(0,step)]
    elif slope>=0:
        if prevMove==(0,-step):
            return [(0,-step),(step,0),(0,step)]
        elif prevMove==(step,0):
            return [(step,0),(0,-step),(0,step)]
        else:
            return [(0,-step),(step,0),(0,step)]
    elif slope>=-1:
        if prevMove==(step,0):
            return [(step,0),(0,step),(0,-step)]
        elif prevMove==(0,step):
            return [(0,step),(step,0),(0,-step)]
        else:
            return [(0,step),(step,0),(0,-step)]
    elif slope<-1:
        if prevMove==(step,0):
            return [(step,0),(0,step),(0,-step)]
        elif prevMove==(0,step):
            return [(0,step),(step,0),(0,-step)]
        else:
            return  [(0,step),(step,0),(0,-step)]


def getSlopeRight(currentLocation,endLocation):
    x1,y1=currentLocation
    x2,y2=endLocation
    if x1==x2:
        if y2>y1:
            return "down"
        else:
            return "up"
    elif x1>x2:
        return "left"
    else:
        slope=-((y2-y1)/(x2-x1))
        return slope
        
def getMovesLstRight(currentLocation,endLocation,prevMove,step):
    slope=getSlopeRight(currentLocation,endLocation)
    # print("slope",slope)
    if slope=="down":
        return [(0,step),(step,0),(0,-step)]
    elif slope=="up":
        return [(0,-step),(step,0),(0,step)]
    elif slope=="left":
        if endLocation[1]<currentLocation[1]:
            return [(0,-step),(-step,0),(0,step)]
        else:
            return [(0,step),(-step,0),(step,0)]
    else:
        if slope==0:
            return [(step,0),(0,step),(0,-step)]
        elif slope>=1:
            if prevMove==(0,-step):
                return [(0,-step),(step,0),(0,step)]
            elif prevMove==(step,0):
                return [(step,0),(0,-step),(0,step)]
            else:
                return [(0,-step),(step,0),(0,step)]
        elif slope>=0:
            if prevMove==(0,-step):
                return [(0,-step),(step,0),(0,step)]
            elif prevMove==(step,0):
                return [(step,0),(0,-step),(0,step)]
            else:
                return [(step,0),(0,-step),(0,step)]
        elif slope>=-1:
            if prevMove==(step,0):
                return [(step,0),(0,step),(0,-step)]
            elif prevMove==(0,step):
                return [(0,step),(step,0),(0,-step)]
            else:
                return [(step,0),(0,step),(0,-step)]
        elif slope<-1:
            if prevMove==(step,0):
                return [(step,0),(0,step),(0,-step)]
            elif prevMove==(0,step):
                return [(0,step),(step,0),(0,-step)]
            else:
                return [(0,step),(step,0),(0,-step)]
    
# def getMovesLstRight(currentLocation,endLocation,prevMove,step):
#     slope=getSlopeRight(currentLocation,endLocation)
#     # print("slope",slope)
#     if slope=="down":
#         return [(0,step),(step,0),(0,-step),(-step,0)]
#     elif slope=="up":
#         return [(0,-step),(step,0),(0,step),(-step,0)]
#     elif slope=="left":
#         if endLocation[1]<currentLocation[1]:
#             return [(0,-step),(-step,0),(0,step),(-step,0)]
#         else:
#             return [(0,step),(-step,0),(step,0),(-step,0)]
#     else:
#         if slope==0:
#             return [(step,0),(0,step),(0,-step),(-step,0)]
#         elif slope>=1:
#             if prevMove==(0,-step):
#                 return [(0,-step),(step,0),(0,step),(-step,0)]
#             elif prevMove==(step,0):
#                 return [(step,0),(0,-step),(0,step),(-step,0)]
#             else:
#                 return [(0,-step),(step,0),(0,step),(-step,0)]
#         elif slope>=0:
#             if prevMove==(0,-step):
#                 return [(0,-step),(step,0),(0,step),(-step,0)]
#             elif prevMove==(step,0):
#                 return [(step,0),(0,-step),(0,step),(-step,0)]
#             else:
#                 return [(step,0),(0,-step),(0,step),(-step,0)]
#         elif slope>=-1:
#             if prevMove==(step,0):
#                 return [(step,0),(0,step),(0,-step),(-step,0)]
#             elif prevMove==(0,step):
#                 return [(0,step),(step,0),(0,-step),(-step,0)]
#             else:
#                 return [(step,0),(0,step),(0,-step),(-step,0)]
#         elif slope<-1:
#             if prevMove==(step,0):
#                 return [(step,0),(0,step),(0,-step),(-step,0)]
#             elif prevMove==(0,step):
#                 return [(0,step),(step,0),(0,-step),(-step,0)]
#             else:
#                 return [(0,step),(step,0),(0,-step),(-step,0)]
 

def notNextTo(grid,endLocation,move,space):
    right=[]
    left=[]
    if move[0]==0:
        dir=move[1]
        if dir<1:
            step=-1
        else:
            step=1
        for j in range(0,dir,step):
            right.append(grid[endLocation[1]-j][endLocation[0]+1:endLocation[0]+space])
        for j in range(0,dir,step):   
            left.append(grid[endLocation[1]-j][endLocation[0]-space:endLocation[0]])

    else:
        dir=move[0]
        tmpLst=[]
        if dir<1:
            step=-1
        else:
            step=1
        for j in range(0,dir,step):
            for i in range (1,space+1):
                tmpLst.append(grid[endLocation[1]+i][endLocation[0]-j])
            right.append(tmpLst)
            tmpLst=[]
        for j in range(0,dir,step):
            for i in range (1,space+1):
                tmpLst.append(grid[endLocation[1]+i][endLocation[0]-j])
            left.append(tmpLst)
            tmpLst=[]
    netSeenDict={}
    for i in right:
        for j in i:
            if j!=0 and j!=9:
                if j in netSeenDict:
                    netSeenDict[j]+=1
                else:
                    netSeenDict[j]=1
    for i in left:
        for j in i:
            if j!=0 and j!=9:
                if j in netSeenDict:
                    netSeenDict[j]+=1
                else:
                    netSeenDict[j]=1
    for key,val in netSeenDict.items():
        if val<=2:
            # print("too close")
            return False
    return True

# def notNextTo(grid,endLocation,move):
#     right=[]
#     left=[]
#     space=10
#     if move[0]==0:
#         dir=move[1]
#         right=[]
#         for j in range(0,dir):
#         if endLocation[0]<len(grid[0])-space:
#             right.append(grid[endLocation[1]-j][endLocation[0]+1:endLocation[0]+space])
#             right=grid[endLocation[1]][endLocation[0]+1:endLocation[0]+space]
#         else:
#             right=[0]
#         if endLocation[0]<len(grid[0])-space:
#             right=grid[endLocation[1]][endLocation[0]+1:endLocation[0]+space]
#         else:
#             right=[0]
#         if endLocation[0]>space:
#             left=grid[endLocation[1]][endLocation[0]-space:endLocation[0]]
#         else:
#             left=[0]
#     else:
#         if endLocation[1]<len(grid)-space:
#             for i in range (1,space+1):
#                 right.append(grid[endLocation[1]+i][endLocation[0]])
#         else:
#             right=[0]
#         if endLocation[1]>space:
#             for i in range (1,space+1):
#                 left.append(grid[endLocation[1]-i][endLocation[0]])
#         else:
#             left=[0]
#     rightCondition,leftCondition=False,False
#     rightCount=0
#     leftCount=0
#     for i in right:
#         if i!=0 and i!=9:
#             rightCount+=1
#     for i in left:
#         if i!=0 and i!=9:
#             leftCount+=1
#     if leftCount==1 or rightCount==1:
#         print("too close")
#         return False
#     return True

def crossOver(grid,endLocation,move,net,visited,canvas,step):
    step=abs(step)
    factor=3
    for i in range(endLocation[1]-int(step*factor),endLocation[1]+int(step*factor)):
        for j in range(endLocation[0]-int(step*factor),endLocation[0]+int(step*factor)):
            if grid[i][j]==net and (j,i) not in visited and (j,i)!=endLocation:
        # print("yay")
        # print("--------")
        # print(net)
        # print(grid[endLocation[1]][endLocation[0]])
        # print(move)
        # print("----------")
                x,y=j,i
                canvas.create_line(endLocation,x,y,width=1)
                radius=step//1.5
                canvas.create_oval(x-radius,y-radius,x+radius,y+radius,fill="black")
                # print("crossed")
                return True,(0,0)
    if grid[endLocation[1]][endLocation[0]]!=0 and grid[endLocation[1]][endLocation[0]]!=9:
        try:
            x=endLocation[0]+move[0]
            y=endLocation[1]+move[1]
            if grid[y][x]==0:
                return True,move
            else:
                # print("cant coss")
                return False,None
        except:
            return False,None
    else:
        return True,None
        
def notOnTop(grid,currentLocation,net,move,step):
    count=0
    if move[0]==0:
        for i in range(currentLocation[1]-step,currentLocation[1]+step):
            if count==1:
                if grid[i][currentLocation[0]]==possNet:
                    return False
            if grid[i][currentLocation[0]]!=net and grid[i][currentLocation[0]]!=0 and grid[i][currentLocation[0]]!=9:
                possNet=grid[i][currentLocation[0]]
                count+=1
    else:
        for i in range(currentLocation[0]-step,currentLocation[0]+step):
            if count==1:
                if grid[currentLocation[1]][i]==possNet:
                    return False
            if grid[currentLocation[1]][i]!=net and grid[currentLocation[1]][i]!=0 and grid[currentLocation[1]][i]!=9:
                possNet=grid[currentLocation[1]][i]
                count+=1
    return True
        

def isValid(grid,currentLocation,actualEndLocation,move,net,visited,traversed,step,space,canvas):
    endLocation=(currentLocation[0]+move[0],currentLocation[1]+move[1])
    # if net=="a1":
    #     print()
    #     print()
    #     print()
    #     print()
    #     print()
    #     print()
    #     if (grid[endLocation[1]][endLocation[0]]==9):
    #         print(endLocation)
    #         print("i see a 9")
    # print("endLocation", endLocation)
    # print("item",grid[endLocation[1]][endLocation[0]])
    x1,y1=endLocation
    x2,y2=actualEndLocation
    dist=distance(x1,y1,x2,y2)
    if endLocation[0]<step or endLocation[0]>=len(grid[0])-step:
        return False,None
    elif endLocation[1]<step or endLocation[1]>=len(grid)-step:
        return False,None
    else:
        if not notOnTop(grid,currentLocation,net,move,step):
            # print("on top")
            return False,None
        if endLocation in visited:
            # print("visited")
            return False,"abort"
        else:
            condition,nextMove=crossOver(grid,endLocation,move,net,visited,canvas,step)
            if nextMove!=None:
                return True,nextMove
            if dist<=step*4 and grid[endLocation[1]][endLocation[0]]!=9:
                # print("close enough")
                return True,None
            else:
                # condition2,right,left=notNextTo(grid,endLocation,move)
                # if not condition2:
                #     print("too close")
                #     print(right)
                #     print(left)
                # if grid[endLocation[1]][endLocation[0]]==9:
                #     print("it is a 9")
                if grid[endLocation[1]][endLocation[0]]!=9 and notNextTo(grid,endLocation,move,space) and condition and (endLocation,move) not in traversed:
                # if grid[endLocation[1]][endLocation[0]]!=9 and notNextTo(grid,endLocation,move) and condition:
                    return True,None
                return False,None

def makeMove(grid,currentLocation,move,net):
    endLocation=(currentLocation[0]+move[0],currentLocation[1]+move[1])
    item=grid[endLocation[1]][endLocation[0]]
    grid[endLocation[1]][endLocation[0]]=net
    # print("prevItem",item)
    return grid,endLocation,item

def undoMove(grid,currentLocation,move,item,commandsLst,visited):
    grid[currentLocation[1]][currentLocation[0]]=item
    x=currentLocation[0]-move[0]
    y=currentLocation[1]-move[1]
    currentLocation=(x,y)
    commandsLst.pop()
    visited.pop()
    return grid,currentLocation,commandsLst,visited


def routeLeft(grid,startLocation,actualStartLocation,endLocation,actualEndLocation,net,step,space,canvas,direction=None,currentLocation=None,prevMove=None,nextMove=None,commandsLst=None,visited=None,traversed=None,item=None):
    # print("left")
    # print("net",net)
    # print(startLocation,currentLocation,endLocation)
    if currentLocation==None:
        x1,y1=startLocation
        x2,y2=endLocation
        # canvas.create_oval(x1-3,y1-3,x1+3,y1+3,fill="blue")
        # canvas.create_oval(x2-3,y2-3,x2+3,y2+3,fill="red")
        currentLocation=startLocation
        grid[startLocation[1]][startLocation[0]]=net
    if commandsLst==None:
        commandsLst=[startLocation]
    if visited==None:
        visited=[]
        visited.append(startLocation)
    if traversed==None:
        traversed=[]
    # print("distance",distance(currentLocation[0],currentLocation[1],endLocation[0],endLocation[1]))
    if isComplete(currentLocation,endLocation,abs(step)*2):
        # if isStore:
        #     x,y=startLocation
        #     canvas.create_oval(x-3,y-3,x+3,y+3,fill="black")
        print("completed")
        x1,y1=startLocation
        x2,y2=actualStartLocation
        canvas.create_line(x1,y1,x1,y2,width=1)
        canvas.create_line(x1,y2,x2,y2,width=1)
        x1,y1=currentLocation
        x2,y2=actualEndLocation
        canvas.create_line(x1,y1,x1,y2,width=1)
        canvas.create_line(x1,y2,x2,y2,width=1)
        # canvas.create_line(startLocation,currentLocation,width=3,fill="blue")
        # commandsLst.append(prevMove)
        return commandsLst
    if nextMove!=None:
        moves=[nextMove]
    else:
        if direction=="down":
            moves=getMovesLstLeftDown(currentLocation,endLocation,prevMove,step)
        else:
            moves=getMovesLstLeft(currentLocation,endLocation,prevMove,step)
    for move in moves:
        # print("move",move)
        condition,nextMove=isValid(grid,currentLocation,endLocation,move,net,visited,traversed,step,space,canvas)
        if nextMove=="abort":
            return None
        if condition:
            oldLocation=currentLocation
            # print("did it")
            grid,currentLocation,item=makeMove(grid,currentLocation,move,net)
            traversed.append((currentLocation,move))
            visited.append(currentLocation)
            commandsLst.append(move)
            if nextMove==(0,0):
                commandsLst.append((0,0))
                return commandsLst
            prevMove=move
            tmpSolution=routeLeft(grid,startLocation,actualStartLocation,endLocation,actualEndLocation,net,step,space,canvas,direction,currentLocation,prevMove,nextMove,commandsLst,visited,traversed,item)
            if tmpSolution!=None:
                return tmpSolution
            grid,currentLocation,commandsLst,visited=undoMove(grid,currentLocation,move,item,commandsLst,visited)
    return None

def routeRight(grid,startLocation,actualStartLocation,endLocation,actualEndLocation,net,step,space,canvas,currentLocation=None,prevMove=None,nextMove=None,commandsLst=None,visited=None,traversed=None,item=None):
    # print("right")
    # print("net",net)
    # print(startLocation,currentLocation,endLocation)
    if currentLocation==None:
        x1,y1=startLocation
        x2,y2=endLocation
        # canvas.create_oval(x1-3,y1-3,x1+3,y1+3,fill="blue")
        # canvas.create_oval(x2-3,y2-3,x2+3,y2+3,fill="red")
        currentLocation=startLocation
        grid[startLocation[1]][startLocation[0]]=net
    if commandsLst==None:
        commandsLst=[startLocation]
    if visited==None:
        visited=[]
        visited.append(startLocation)
    if traversed==None:
        traversed=[]
    # print("distance",distance(currentLocation[0],currentLocation[1],endLocation[0],endLocation[1]))
    if isComplete(currentLocation,endLocation,abs(step)*2):
        # if isStore:
        #     x,y=currentLocation
        #     canvas.create_oval(x-3,y-3,x+3,y+3,fill="black")
        print("completed")
        x1,y1=startLocation
        x2,y2=actualStartLocation
        canvas.create_line(x1,y1,x1,y2,width=1)
        canvas.create_line(x1,y2,x2,y2,width=1)
        x1,y1=currentLocation
        x2,y2=actualEndLocation
        canvas.create_line(x1,y1,x1,y2,width=1)
        canvas.create_line(x1,y2,x2,y2,width=1)
        # commandsLst.append(prevMove)
        # canvas.create_line(startLocation,currentLocation,width=3,fill="red")
        return commandsLst
    if nextMove!=None:
        moves=[nextMove]
    else:
        moves=getMovesLstRight(currentLocation,endLocation,prevMove,step)
    for move in moves:
        # print("move",move)
        condition,nextMove=isValid(grid,currentLocation,endLocation,move,net,visited,traversed,step,space,canvas)
        if nextMove=="abort":
            return None
        if condition:
            oldLocation=currentLocation
            # print("did it")
            grid,currentLocation,item=makeMove(grid,currentLocation,move,net)
            traversed.append((currentLocation,move))
            visited.append(currentLocation)
            commandsLst.append(move)
            if nextMove==(0,0):
                commandsLst.append((0,0))
                return commandsLst
            prevMove=move
            tmpSolution=routeRight(grid,startLocation,actualStartLocation,endLocation,actualEndLocation,net,step,space,canvas,currentLocation,prevMove,nextMove,commandsLst,visited,traversed,item)
            if tmpSolution!=None:
                return tmpSolution
            grid,currentLocation,commandsLst,visited=undoMove(grid,currentLocation,move,item,commandsLst,visited)
    return None

# board = [
#         [ 0, 0, 0, 0, 0, 0, 0, 9, 0 ],
#         [ 0, 0, 0, 0, 0, 0, 0, 0, 0 ],
#         [ 0, 0, 0, 0, 1, 1, 1, 9, 0 ],
#         [ 0, 0, 0, 0, 9, 0, 0, 0, 9 ],
#         [ 0, 0, 0, 9, 0, 0, 0, 0, 9 ],
#         [ 0, 0, 9, 0, 0, 0, 0, 0, 0 ],
#         [ 0, 9, 9, 1, 1, 1, 0, 9, 0 ],
#         [ 0, 0, 0, 0, 0, 0, 0, 0, 0 ],
#         [ 0, 0, 0, 0, 0, 0, 0, 0, 0 ]
#         ]
# 
# for i in board:
#     for j in i:
#         print (j, end=" ")
#     print()
# print()
# 
# board=route(board,(4,8),(8,0))
# board=route(board,(0,0),(8,8))



    