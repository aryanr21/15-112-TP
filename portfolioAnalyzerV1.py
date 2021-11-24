from stockData import *
from datetime import datetime, timedelta
from stockChart import *
from datetime import datetime

# a = datetime.datetime(2021, 11, 23, 11, 51, 12, 947406)

def dataExtractor(ticker,dateStamp):
    startDay = dateStamp - timedelta(9)
    data = getChart(ticker,[int(startDay.year),int(startDay.month),int(startDay.day)],[int(dateStamp.year),int(dateStamp.month),int(dateStamp.day)],'1d')
    return data

#First function to check sentiment in market using last 7 days prices

def trendCalculator(data):
    result = []
    i = 1
    while i < len(data):
        percentChange = ((data.Close[i]-data.Close[i-1])/data.Close[i-1])*100
        result.append(percentChange)
        i += 1
    avgChange = sum(result)/len(result)
    return avgChange

def buyingSentimentAnalyzer(avgChange,ticker):
    companyData = stock(ticker)
    if avgChange >= 2.5:
        return f'The buying trend for {companyData.companyName()} is positive and strong'
    elif 0 <= avgChange < 2.5:
        return f'The buying trend for {companyData.companyName()} is positive and moderate'
    else:
        return f'The buying trend for {companyData.companyName()} is weak'

def sellingSentimentAnalyzer(avgChange,ticker):
    companyData = stock(ticker)
    if avgChange <= -2.5:
        return f'The selling trend for {companyData.companyName()} is positive and strong'
    elif -2.5 < avgChange <= 0:
        return f'The selling trend for {companyData.companyName()} is positive and moderate'
    else:
        return f'The selling trend for {companyData.companyName()} is weak'

def companySeperator(companyList):
    result = str()
    for company in companyList:
        data = stock(company)
        if company == companyList[-1]:
            result += data.companyName() + '.'
        else:
            result += data.companyName() + ', '
    return result

def similarCompanyTrend(ticker,avgChange,dateStamp):
    companyData = stock(ticker)
    similarCompanies = companyData.similarTrendingStocks()
    result = []
    for companies in similarCompanies:
        change = trendCalculator(dataExtractor(companies,dateStamp))
        if avgChange >= 1:
            if change >= 1:
                result.append(companies)
        elif avgChange <= -1:
            if change <= -1:
                result.append(companies)
        elif -1 < avgChange <= 0:
            if -1 < change <= 0:
                result.append(companies)
        elif 0 < avgChange < 1:
            if 0 < change < 1:
                result.append(companies)

    if len(result) == 0:
        return f'Recent {companyData.companyName()} trend different from similar companies such as {companySeperator(similarCompanies)}'
    
    elif len(result) >= len(similarCompanies)//2:
        return f'Recent {companyData.companyName()} trend similar to similar companies such as {companySeperator(result)}'
    
    else:
        return 'Mixed signals provided by similar stocks, ensure company being invested in is thoroughly analyzed.'

def habitAnalyzer(avgChange,ticker):
    if ('positive and strong' in buyingSentimentAnalyzer(avgChange,ticker)) or ('positive and strong' in sellingSentimentAnalyzer(avgChange,ticker)):
        return 'Investor has invested in a strong short term upswing/downswing of prices. Please ensure stock valuation is performed before purchase' 
    elif ('positive and moderate' in buyingSentimentAnalyzer(avgChange,ticker)) or ('positive and moderate' in sellingSentimentAnalyzer(avgChange,ticker)): 
        return 'Recent investment on moderate upswing/downswing of stock price. Please value stock before investing.'
    else:
        return None

# print(datetime.now())
# print(buyingSentimentAnalyzer(trendCalculator(dataExtractor('MRNA',a))))

# print(similarCompanyTrend('MRNA',trendCalculator(dataExtractor('MRNA',a)),a))
      








# print(trendCalculator(dataExtractor('TSLA',datetime.datetime(2021, 11, 23, 11, 51, 12, 947406))))





