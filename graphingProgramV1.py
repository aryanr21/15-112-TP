from typing import final
from matplotlib.pyplot import draw, fill
from cmu_112_graphics import *
from stockChart import *
from datetime import date

def appStarted(app):
    app.r = 0.01
    app.data = getChart('AMZN',[2013,10,1],[2021,11,1],'1mo')

def intervalCreator(maxVal):
    delta = maxVal//4
    result = []
    i = 0
    while i <= 4:
        result.append(delta*i)
        i += 1
    return result

def drawLine(app,canvas,priceRange,dayRange):
    pointList = []
    priceList = [0]
    xPoslist = []
    startXVal = app.width//10
    startYVal = app.width//2
    finalXVal = app.width//1.05
    finalYValue = app.height//10
    timeFrame = len(dayRange)
    xUnits = (finalXVal-startXVal)/timeFrame
    yUnits = (startYVal-finalYValue)/(float(max(priceRange)) + max(priceRange)/2)
    n = 0
    pointList.append(startYVal)
    while n < len(priceRange)-1:
        xVal = startXVal + n*xUnits
        yVal = pointList[-1] - (priceRange[n]-priceList[-1])*yUnits
        if len(xPoslist) > 1:
            canvas.create_line(xPoslist[-1],pointList[-1],xVal,yVal,width=2)
        pointList.append(yVal)
        priceList.append(priceRange[n])
        xPoslist.append(xVal)
        n += 1
    
    drawYLabel(app,canvas,priceList,yUnits)
    drawXLabel(app,canvas,dayRange,xUnits)

def drawYLabel(app,canvas,priceList,yUnits):
    startXVal = app.width//10
    startYVal = app.width//2
    intervalList = intervalCreator(max(priceList) + max(priceList)/2)
    for values in intervalList:
        canvas.create_text(startXVal - app.width//20,startYVal - values*yUnits,text=values,font = 14)

def drawXLabel(app,canvas,timeRange,xUnits):
    startXVal = app.width//10
    startYVal = app.width//2
    timeInterval = intervalCreator(len(timeRange))
    for values in timeInterval:
        canvas.create_text(startXVal + values*xUnits,startYVal + app.height//20,text=timeRange[values],font = 14)    

def redrawAll(app,canvas):
    canvas.create_line(app.width//10,app.height//2,app.width//1.05,app.height//2,width=2)
    canvas.create_line(app.width//10,app.height//2,app.width//10,app.height//10,width=2)
    drawLine(app,canvas,app.data.Close,app.data.Date)

runApp(width = 700,height = 700)

