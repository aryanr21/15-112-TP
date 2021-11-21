from cmu_112_graphics import *
from matplotlib.pyplot import draw
import pandas as pd
from stockData import *
import random

###################
# Main App
###################

def appStarted(app):

    app.profile = list() #profile activated in current runtime
    #Stored as [First name, Last name, username]

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
    app.signUpReset = [[app.width//6,app.height//7.1,[''],'accountScreen','inactive'],[app.width//6,app.height//6,[''],'accountScreen','inactive'],[app.width//6,app.height//5.22,[''],'accountScreen','inactive'],
                        [app.width//6,app.height//4.6,[''],'accountScreen','inactive']]
    app.loginData = [[app.width//2.2,app.height//7.1,[''],'accountScreen','inactive'],[app.width//2.2,app.height//6,[''],'accountScreen','inactive']]
    app.loginReset = [[app.width//2.2,app.height//7.1,[''],'accountScreen','inactive'],[app.width//2.2,app.height//6,[''],'accountScreen','inactive']]

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

    #Dashboard variables
    app.stockNamesScreens = [[],[],[],[],[]]
    app.stockScreenSpace = app.height//60

    #Variables for navigation buttons and application logo on top
    app.logoWidth = app.width//16
    app.logoHeight = app.height//19
    app.navButtons = [[(app.width//2.3,app.height//12),'Home'],[(app.width//1.87,app.height//12),'Portfolio'],[(app.width//1.57,app.height//12),'Eye Track'],[(app.width//1.57,app.height//45),'Log out']]


#General functions used on different screens
def drawButton(app,canvas,lst):
    for values in lst:
        idx = int()
        if values[0] == (values[0][0],values[0][1]):
            idx = lst.index(values)
        canvas.create_rectangle(values[0][0],values[0][1],values[0][0]+app.buttonWidth,values[0][1]+app.buttonHeight,fill='light blue',width=2)
        canvas.create_text((2*values[0][0]+app.buttonWidth)//2,(2*values[0][1]+app.buttonHeight)//2,text = values[1],font=f"Times {app.width//80} bold")

def checkBounds(app,x,y,lst):
    for values in lst:
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

def screenTop(app,canvas):
    #Create logo
    #ADD MORE FEATURES TO LOGO
    canvas.create_rectangle(0,0,app.logoWidth,app.logoHeight,fill ='white')

    #Create navigation buttons to differnt screens.
    

def stockListAdder(stock,stockList):
    for screen in stockList:
        if len(screen) < 8:
            screen.append(stock)
            break
        else:
            continue
    return stockList

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

#Below functions used to add values to database.
def newUserData(lst):
    dataDict = {'First name':[],'Last name':[],'Username': [],'Password':[]}
    firstName = lst[0][2]
    lastName = lst[1][2]
    userName = lst[2][2]
    password = lst[3][2]
    dataDict['First name'] = [firstName[0].join(firstName[1:])]
    dataDict['Last name'] = [lastName[0].join(lastName[1:])]
    dataDict['Username'] = [userName[0].join(userName[1:])]
    dataDict['Password'] = [password[0].join(password[1:])]
    return dataDict

#Below function compiles the data entered by logging in user.
def existingUserData(lst):
    dataDict = {'Username':[],'Password':[]}
    userName = lst[0][2]
    password = lst[1][2]
    dataDict['Username'] = userName[0].join(userName[1:])
    dataDict['Password'] = password[0].join(password[1:])
    return dataDict

#Below function checks if entered username exists in database
def checkUserExistence(username):
    data = pd.read_csv('/Users/aryanrawat/Desktop/CMU/CS/TP research/UIUX/userData.csv') #csv will have to be changed to your current file
    for usernames in data['Username']:
        if username == usernames:
            return True
    
    return False

#Below function used by user to see if password matches given username
def passwordCheck(username,password):
    data = pd.read_csv('/Users/aryanrawat/Desktop/CMU/CS/TP research/UIUX/userData.csv')
    i = 0
    for usernames in data['Username']:
        if username == usernames:
            if str(password) == str(data['Password'][i]):
                return True
        i += 1
    
    return False

#Function to add user to database
def addUserToDatabase(datadictionary):
    df = pd.DataFrame(datadictionary)
    df.to_csv('/Users/aryanrawat/Desktop/CMU/CS/TP research/UIUX/userData.csv',mode='a',index=False,header=False)

#Function to fetch existing user profile details
def getUserProfile(profile):
    data = pd.read_csv('/Users/aryanrawat/Desktop/CMU/CS/TP research/UIUX/userData.csv')
    i = 0
    dataList = []
    for usernames in data['Username']:
        if profile == usernames:
            dataList.append(data['First name'][i])
            dataList.append(data['Last name'][i])
            dataList.append(usernames)
        i += 1
    
    return dataList

#Fn to see if user clicked on any sign up text boxes
def checkSignUpClick(app,x,y):
    for values in app.signUpData:
        x1 = values[0] + app.textBoxWidth
        y1 = values[1] + app.textBoxHeight
        if (((x >= values[0]) and (x <= x1)) and ((y >= values[1]) and (y <= y1))):
            return (values[0],values[1])
    return False

#Fn to see if user clicked on any log in text boxes
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
    clickFlag = checkBounds(app,event.x,event.y,app.buttonList)
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
            if userType == 'New':
                userData = newUserData(app.signUpData)
                username = userData['Username'][0]
                if checkUserExistence(username) == False:
                    app.signUpFlag = bool()
                    addUserToDatabase(userData)
                    app.profile = getUserProfile(username)
                    app.mode = 'dashboardScreen'
                else:
                    app.showMessage('Username already taken! Please enter another username.')
            
            else:
                userData = existingUserData(app.loginData)
                if checkUserExistence(userData['Username']) == True:
                    if passwordCheck(userData['Username'],userData['Password']) == True:
                        app.profile = getUserProfile(userData['Username'])
                        app.signUpFlag = bool()
                        app.mode = 'dashboardScreen'
                    else:
                        app.showMessage('Incorrect Password!')
                else:
                    app.showMessage('Username does not exist!')

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
    drawButton(app,canvas,app.buttonList)
    
#####################################
# Step 3: loading screen
#####################################

def loadingScreen_timerFired(app):
    if app.idx == len(app.loadingScreenCoords)-1:
        app.mode = 'dashboardScreen'
    
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

#####################################
# Step 4: Dashboard screen
#####################################

def priceChangeColor(symbol):
    if symbol == '+':
        return 'green'
    else:
        return 'red'

def stockScreen(app,canvas,i):
    space = 0
    for stockTicker in app.stockNamesScreens[i]:
        stockFetch = stock(stockTicker)
        color = priceChangeColor(stockFetch.priceMetrics()['Daily change'][0])
        canvas.create_text(app.width//8.8,app.height//2 + space,text=stockTicker,fill='Black',font='Times 15 bold')
        canvas.create_text(app.width//3.5,app.height//2 + space,text=stockFetch.priceMetrics()['Last recorded price'],fill=color,font='Times 15 bold')
        canvas.create_text(app.width//5,app.height//2 + space,text=stockFetch.priceMetrics()['Daily change'],fill=color,font='Times 15 bold')
        space += app.stockScreenSpace

def dashboardScreen_mousePressed(app,event):
    positionCheck = checkBounds(app,event.x,event.y,app.navButtons)    
    if positionCheck != False:
        if positionCheck == (1069.0, 166):
            app.mode = 'portfolioScreen'
        elif positionCheck == (1273.0, 166):
            app.mode = 'eyeTrackScreen'
        elif positionCheck == (1273.0, 44):
            app.signUpData = app.signUpReset
            app.loginData = app.loginReset
            app.profile = list()
            app.mode = 'accountScreen'


def dashboardScreen_redrawAll(app,canvas):
    #Below code creates background for screen
    canvas.create_image(app.width//2, app.height//2, image=ImageTk.PhotoImage(app.landingScreenImage))
    #code in line 390-421 creates textbox for stock screen
    canvas.create_rectangle(app.width//6.7,app.height//3,app.width//8 + app.width//8.8,app.height//3 + app.buttonHeight,fill='light blue')
    canvas.create_text((app.width//10 + app.buttonWidth),(app.height//3.34 + app.buttonHeight),text = 'Stock Screen',font='Times 18 bold')
    canvas.create_rectangle(app.width//12,app.height//2.3,app.width//16 + app.width//4,app.height//2 + app.height//3,fill='light blue')
    #code in line 421-423 creates labels for stock screen
    canvas.create_text(app.width//8.8,app.height//2 - app.height//25,text='Ticker',fill='Blue',font='Times 17 bold italic')
    canvas.create_text(app.width//3.5,app.height//2 - app.height//25,text='Change',fill='Blue',font='Times 17 bold italic')
    canvas.create_text(app.width//5,app.height//2 - app.height//25,text='Price',fill='Blue',font='Times 17 bold italic')
    stockScreen(app,canvas,0)
    screenTop(app,canvas)
    drawButton(app,canvas,app.navButtons)

#####################################
# Step 4: Portfolio screen
#####################################

def portfolioScreen_redrawAll(app,canvas):
    canvas.create_image(app.width//2, app.height//2, image=ImageTk.PhotoImage(app.landingScreenImage))
    #Lines 451- for portfolio area
    canvas.create_rectangle(app.width//25,app.height//3,app.width//25 + app.width//2.2,app.height//3 + app.height//1.6,fill = 'light blue')
    canvas.create_text(app.width//12,app.height//2.7,text='Stock ticker',fill='black',font='Times 17 bold')
    canvas.create_text(app.width//6,app.height//2.7,text='Avg Price',fill='black',font='Times 17 bold')
    canvas.create_text(app.width//4,app.height//2.7,text='Quantity',fill='black',font='Times 17 bold')
    canvas.create_text(app.width//3,app.height//2.7,text='LTP',fill='black',font='Times 17 bold')
    canvas.create_text(app.width//2.3,app.height//2.7,text='Profit/Loss',fill='black',font='Times 17 bold')





    screenTop(app,canvas)
    drawButton(app,canvas,app.navButtons)

runApp(width=2000, height=2000)



