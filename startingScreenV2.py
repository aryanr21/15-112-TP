from cmu_112_graphics import *
import pandas as pd
from stockData import *
import random

###################
# Main App
###################

def appStarted(app):
    #Landing page and navigation variables
    app.mode = 'landingScreen'
    app.message = "Welcome to Bull's eye! Click anywhere to continue" #Text for loading screen
    app.dummy = 0 #Variable created to have if statments with no impact.

    #Button creation variables
    app.buttonWidth = app.width//15 #General dimension for button
    app.buttonHeight = app.height//38 #General dimension for button
    app.buttonList = [[(app.width//6.5,app.height//3.85),'Sign me up!'],[(app.width//2.28,app.height//4.6),'Log in!']] #Contains coordinates of buttons and the app.mode it's in.
    
    #Text box variables
    #app.textBoxData has following format: [boxWidthStart,boxHeightStart,text,startingPos of text, screen, status]
    app.textBoxWidth = app.width//12
    app.textBoxHeight = app.height//80

    #Account page variables
    #format of below list is: [Starting point list,label of box, fields in box, Ending x value, Ending y value]
    app.surroundingShapeList = [[[app.width//9,app.height//9],'Sign Up',['First Name','Last Name','Username','Password'],app.width//6.7,app.height//7],
                                [[app.width//2.5,app.height//9],'Log in',['Username','Password'],app.width//6.8,app.height//10]]
    app.signUpFlag = bool() #flag used to see if new user or old
    #Variable below is buttons only for accountScreen

    app.signUpData = [[app.width//6,app.height//7.1,[''],'accountScreen','inactive'],[app.width//6,app.height//6,[''],'accountScreen','inactive'],[app.width//6,app.height//5.22,[''],'accountScreen','inactive'],
                        [app.width//6,app.height//4.6,[''],'accountScreen','inactive']]
    app.loginData = [[app.width//2.2,app.height//7.1,[''],'accountScreen','inactive'],[app.width//2.2,app.height//6,[''],'accountScreen','inactive']]

    #image insertion variable
    app.landingScreenImage = app.loadImage('landingScreen.jpg') #https://www.wibestbroker.com/important-types-of-stock-charts/

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
    for values in app.buttonList:
        idx = int()
        if values[0] == (values[0][0],values[0][1]):
            idx = app.buttonList.index(values)
        canvas.create_rectangle(values[0][0],values[0][1],values[0][0]+app.buttonWidth,values[0][1]+app.buttonHeight,fill='light blue',width=2)
        canvas.create_text((2*values[0][0]+app.buttonWidth)//2,(2*values[0][1]+app.buttonHeight)//2,text = values[1],font=f"Times {app.width//80} bold")

def checkBounds(app,x,y):
    for values in app.buttonList:
        x1 = values[0][0] + app.buttonWidth
        y1 = values[0][1] + app.buttonHeight
        if (((x >= values[0][0]) and (x <= x1)) and ((y >= values[0][1]) and (y <= y1))):
            return (values[0][0],values[0][1])    
    return False

#Fn below created to set all textbox values to inactive.
def clickRefresh(app):
    for values in app.signUpData:
        values[-1] = 'inactive'
    for values in app.loginData:
        values[-1] = 'inactive'

def textBoxSignUp(app,canvas):
    for x,y,textMessage,screen,status in app.signUpData:
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

def textBoxLogin(app,canvas):
    for x,y,textMessage,screen,status in app.loginData:
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

##########################
# Step 2: Account screen
##########################

def checkSignUpClick(app,x,y):
    for values in app.signUpData:
        x1 = values[0] + app.textBoxWidth
        y1 = values[1] + app.textBoxHeight
        if (((x >= values[0]) and (x <= x1)) and ((y >= values[1]) and (y <= y1))):
            return (values[0],values[1])
    return False

def checkLoginClick(app,x,y):
    for values in app.loginData:
        x1 = values[0] + app.textBoxWidth
        y1 = values[1] + app.textBoxHeight
        if (((x >= values[0]) and (x <= x1)) and ((y >= values[1]) and (y <= y1))):
            return (values[0],values[1])
    return False

def accountScreen_mousePressed(app,event):
    userType = str()
    clickRefresh(app)

    #Condition to check if user has entered all the fields
    clickFlag = checkBounds(app,event.x,event.y)
    if clickFlag != False:
        redFlag = False
        if clickFlag == (307.0,519.0): #Coordinates of sign up box
            for values in app.signUpData:
                if (len(values[2]) == 1) and (values[2][0] == ''):
                    app.showMessage('Please fill in all fields!')
                    redFlag = True
                    break
                else: 
                    userType = 'New'
        elif clickFlag == (877.0,434.0): #coordinates of login box
            for values in app.loginData:
                if (len(values[2]) == 1) and (values[2][0] == ''):
                    app.showMessage('Please fill in all fields!')
                    redFlag = True
                    break
                else:
                    userType = 'Old'
        #Condition to move to next screen
        if redFlag == False:
            coordGenerator(app)
            app.signUpFlag = bool()
            app.mode = 'loadingScreen'

    clickResultSignUp = checkSignUpClick(app,event.x,event.y)
    clickResultLogin = checkLoginClick(app,event.x,event.y)

    #Block of code below adds text to list that contains words/letters in the textbox.
    if clickResultSignUp != False:
        app.signUpFlag = True
        for values in app.signUpData:
            if values[-2] == 'accountScreen':
                xVal = values[0]
                yVal = values[1]
                if clickResultSignUp == (xVal,yVal):
                    values[-1] = 'active'
    elif clickResultLogin != False:
        app.signUpFlag = False
        for values in app.loginData:
            if values[-2] == 'accountScreen':
                xVal = values[0]
                yVal = values[1]
                if clickResultLogin == (xVal,yVal):
                    values[-1] = 'active'        

def accountScreen_keyPressed(app,event):
    if app.signUpFlag == True:
        for values in app.signUpData:
            if values[-1] == 'active':
                if event.key == 'Delete':
                    values[2].pop()
                elif event.key == 'Space':
                    values[2].append(' ')
                else:
                    values[2].append(str(event.key))
    else:
        for values in app.loginData:
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
    textBoxSignUp(app,canvas)
    textBoxLogin(app,canvas)
    drawButton(app,canvas)
    

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
    while i <= 5:
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








