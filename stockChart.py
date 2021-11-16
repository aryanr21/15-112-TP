import time
import datetime
import pandas as pd
#Allows using un-verified files, which in the scope of this project is the csv file
#historical data
import ssl
import matplotlib.pyplot as plt

ssl._create_default_https_context = ssl._create_unverified_context
def getChart(ticker,periodOne,periodTwo,frequency):
    try:
        #Main code refrenced from:
        #https://learndataanalysis.org/source-code-download-historical-stock-data-from-yahoo-finance-using-python/
        startDate = int(time.mktime(datetime.datetime(periodOne[0], periodOne[1], periodOne[2], 23, 59).timetuple()))
        endDate = int(time.mktime(datetime.datetime(periodTwo[0], periodTwo[1], periodTwo[2], 23, 59).timetuple()))
        query_string = f'https://query1.finance.yahoo.com/v7/finance/download/{ticker}?period1={startDate}&period2={endDate}&interval={frequency}&events=history&includeAdjustedClose=true'
        df = pd.read_csv(query_string)
        return df
    except:
        return 'Please check data entered carefully!'

def drawLineGraph(chart,ticker):
    plt.figure(figsize=(10,5))
    plt.plot(chart.index,chart.Close)
    plt.title(f'{ticker} stock chart')
    plt.xlabel('Date index')
    plt.ylabel('Stock price ($)')
    plt.show()
    return ''

# print(drawLineGraph(getChart('AMZN',[2021,10,1],[2021,11,11],'1mo'),'AMZN'))












