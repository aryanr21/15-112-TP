from cmu_112_graphics import *
from stockData import *
import random

###################
# Main App
###################

def appStarted(app):
    #Landing page and navigation variables
    app.mode = 'landingScreen'
    app.message = "Welcome to Eagle's eye! Click anywhere to continue" #Text for loading screen

    #Button creation variables
    app.buttonWidth = app.width//5 #General dimension for button
    app.buttonHeight = app.height//15 #General dimension for button
    app.buttonList = [(50,600,'loadingScreen'),(500,600,'loadingScreen')] #Contains coordinates of buttons and the app.mode it's in.
    
    #Text box variables
    #app.textBoxData has following format: [boxWidthStart,boxHeightStart,text,startingPos of text, screen, status]
    app.textBoxData = [[app.width//6,app.height//7.1,[''],'accountScreen','inactive'],[app.width//6,app.height//6,[''],'accountScreen','inactive'],[app.width//6,app.height//5.22,[''],'accountScreen','inactive'],
                        [app.width//6,app.height//4.6,[''],'accountScreen','inactive'],[app.width//2.2,app.height//7.1,[''],'accountScreen','inactive'],[app.width//2.2,app.height//6,[''],'accountScreen','inactive']]
    app.textBoxWidth = app.width//12
    app.textBoxHeight = app.height//80
    # app.textSpacing = app.width//1000

    #Account page variables
    #format of below list is: [Starting point list,label of box, fields in box, Ending x value, Ending y value]
    app.surroundingShapeList = [[[app.width//9,app.height//9],'Sign Up',['First Name','Last Name','Username','Password'],app.width//6.7,app.height//7],
                                [[app.width//2.5,app.height//9],'Log in',['Username','Password'],app.width//6.8,app.height//10]]

    #image insertion variable
    app.landingScreenImage = app.loadImage('landingScreen.jpg') 

    #Loading screen animation variables
    app.loadingScreenCoords = [] #All random coordinates for loading graph
    app.x0 = app.width//3.88
    app.y0 = app.height//5
    app.coordsDrawn = [(app.x0,app.y0)]
    app.timerDelay = 333
    app.idx = 0
    app.r = app.width//900 #radius used for loading screen animation.

#General functions used on different screens
def drawButton(app,canvas):
    for x,y in app.buttonList:
        idx = app.buttonList.index((x,y))
        canvas.create_rectangle(x,y,x+app.buttonWidth,y+app.buttonHeight,fill='turquoise',width=2)
        canvas.create_text((2*x+app.buttonWidth)//2,(2*y+app.buttonHeight)//2,text = app.buttonValue[idx][0],font=f"Times {app.width//30} bold")

def checkBounds(app,x,y):
    for x0,y0 in app.buttonList:
        x1 = x0 + app.buttonWidth
        y1 = y0 + app.buttonHeight
        if (((x >= x0) and (x <= x1)) and ((y >= y0) and (y <= y1))):
            return (x0,y0)    
    return False

def checkBoxClick(app,x,y):
    for values in app.textBoxData:
        x1 = values[0] + app.textBoxWidth
        y1 = values[1] + app.textBoxHeight
        if (((x >= values[0]) and (x <= x1)) and ((y >= values[1]) and (y <= y1))):
            return (values[0],values[1])
    return False

#Fn below created to set all textbox values to inactive.
def clickRefresh(app):
    for values in app.textBoxData:
        values[-1] = 'inactive'

def textBox(app,canvas):
    for x,y,textMessage,screen,status in app.textBoxData:
        if app.mode == screen:
            canvas.create_rectangle(x,y,x+app.textBoxWidth,y+app.textBoxHeight,fill='white',width=2,outline='black')
            spacing = 10
            altSpacing = 1 #Spacing for first variable
            i = 0
            for text in textMessage:
                if i == 0:
                    result = ''
                    canvas.create_text(x+altSpacing,(2*y+app.textBoxHeight)/2,text=result.join(text),fill='black')
                    i += 1
                else:
                    result = ''
                    canvas.create_text(x+spacing,(2*y+app.textBoxHeight)/2,text=result.join(text),fill='black')
                    spacing += 10
                    i += 1

                if spacing > app.width//8.8:
                    break

def wordTypeConcat(app):
    result = []
    for values in app.textBoxData:
        result = wordFormer(values[2])
        values[2] = result

#Fn to create Sign up/Log in boxes
def surroundingBox(app,canvas):
    for values in app.surroundingShapeList:
        canvas.create_rectangle(values[0][0],values[0][1],values[0][0] + values[-2], values[0][1] + values[-1],fill='light blue')
        canvas.create_text((2*values[0][0] + values[-2])/2,values[0][1] + 20,text=values[1],fill='black',font = 'Time 20 bold italic')
        labelGap = values[0][1] + 70
        for labels in values[2]:
            canvas.create_text(values[0][0] + 50,labelGap,text=labels,fill='black',font='Times 16 bold')
            labelGap += 50

##########################
# Step 1: Landing screen
##########################

def landingScreen_redrawAll(app,canvas):
    canvas.create_image(app.width//2, app.height//2, image=ImageTk.PhotoImage(app.landingScreenImage))
    canvas.create_text(app.width//2,app.height//2,text = app.message,font=f"Times {app.width//30} bold italic",fill='white')
    
def landingScreen_mousePressed(app,canvas):
    app.mode = 'accountScreen'
    coordGenerator(app)

##########################
# Step 2: Account screen
##########################

def accountScreen_mousePressed(app,event):
    clickRefresh(app)
    clickResult = checkBoxClick(app,event.x,event.y)
    if clickResult != False:
        for values in app.textBoxData:
            if values[-2] == 'accountScreen':
                xVal = values[0]
                yVal = values[1]
                if clickResult == (xVal,yVal):
                    values[-1] = 'active'

def accountScreen_keyPressed(app,event):
    for values in app.textBoxData:
        if values[-1] == 'active':
            if event.key == 'Delete':
                values[2].pop()
            elif event.key == 'Space':
                values[2].append(' ')
            else:
                values[2].append(str(event.key))
    
def accountScreen_redrawAll(app,canvas):
    canvas.create_image(app.width//2, app.height//2, image=ImageTk.PhotoImage(app.landingScreenImage))
    surroundingBox(app,canvas)
    textBox(app,canvas)
    

#####################################
# Step 3: loading screen
#####################################

def loadingScreen_timerFired(app):
    if app.idx == len(app.loadingScreenCoords)-1:
        app.mode = 'next'
    
    app.coordsDrawn.append(app.loadingScreenCoords[app.idx])
    app.idx += 1

def coordGenerator(app):
    i = 0
    j = app.width//30
    x0 = app.width//2 - app.width//7
    y0 = app.height//2 + app.height//10
    while i <= 6:
        app.loadingScreenCoords.append((x0 + j,y0 - j))
        i += 1
        j += app.width//30

def drawGraph(app,canvas):
    x0 = app.width//2 - app.width//7
    y0 = app.height//2 + app.height//10
    canvas.create_line(x0,y0,x0,y0-app.height//3,fill='black',width=3)
    canvas.create_line(x0,y0,x0+app.width//3,y0,fill='black',width=3)  
    
def loadingScreen_redrawAll(app,canvas):
    drawGraph(app,canvas)
    for x,y in app.coordsDrawn:
        canvas.create_oval(x-app.r,y-app.r,x+app.r,y+app.r,fill='black')

    canvas.create_text(app.width//1.8,app.height//5,text='Loading your dashboard...',fill='dark blue',font='Times 28 bold italic')

    if len(app.coordsDrawn) > 1:
        i = 1
        while i < len(app.coordsDrawn):
            canvas.create_line(app.coordsDrawn[i][0],app.coordsDrawn[i][1],app.coordsDrawn[i-1][0],app.coordsDrawn[i-1][1],width=3)
            i += 1
            
        
runApp(width=2000, height=2000)








