import requests
from bs4 import BeautifulSoup 
import lxml
from stockChart import *

#The following class returns all the stock related data using Beautiful soup.
class stock(object):
    def __init__(self,ticker):
        self.ticker = ticker
        self.link = 'https://finance.yahoo.com/quote/' + self.ticker + '?p=' + self.ticker + '&.tsrc=fin-srch'

    #All stock price data is obtained from Yahoo Finance.

    #Function scrapes the name of the company
    def companyName(self):
        try:
            url = requests.get(self.link)
            soup = BeautifulSoup(url.text,'lxml')
            tagFinder = soup.find('h1',{'class': 'D(ib) Fz(18px)'})
            name = tagFinder.text
            if name == []: #Done to check if website did not return any value.
                return 'No val'
            return name
        except:
            return "Enter a valid ticker!"
        

    #Price metrics function: function returns all price related data. For eg: closing market price,
    #daily price change, and the day's closing time.Function below understood from following link:
    #https://www.youtube.com/watch?v=_Bu6povAuSU&t=1141s
    def priceMetrics(self):
        dataList = []
        try:
            url = requests.get(self.link)
            soup = BeautifulSoup(url.text,'lxml')
            tagFinder = soup.find('div',{'class' : 'D(ib) Mend(20px)'})
            spanList = tagFinder.find_all('span')
            for span in spanList:
                dataList.append(span.text)
            price = dataList[0].replace(',','')
            metricData = {'Last recorded price': float(price),'Daily change': dataList[1],'Status': dataList[2]}
            return metricData
        except:
            return "Enter a valid ticker!"

    #Additional technical metrics: Function return additional metrics related to technicals of
    #stock such as volume and opening price.
    def metrics(self):
        dataList = []
        try:
            url = requests.get(self.link)
            soup = BeautifulSoup(url.text,'lxml')
            tagFinder = soup.find('div',{'class' : 'Bxz(bb) D(ib) Va(t) Mih(250px)!--lgv2 W(100%) Mt(-6px) Mt(0px)--mobp Mt(0px)--mobl W(50%)!--lgv2 Mend(20px)!--lgv2 Pend(10px)!--lgv2 BdEnd--lgv2 Bdendc($seperatorColor)!--lgv2'})
            spanList = tagFinder.find_all('td')
            for metrics in spanList:
                dataList.append(metrics.text)
            return self.dataExtractor(dataList)
        except:
            return "Enter a valid ticker!"
    
    #Function below seperates the metric name and values and returns in readable format.
    def dataExtractor(self,data):
        metricInfo = []
        metricNumbers = []
        finalNumbers = []
        #loop to get key and value list
        for items in data:
            if (data.index(items)%2) == 0:
                metricInfo.append(items)
            else:
                metricNumbers.append(items)
        
        #loop to make numbers in values to convert to integer
        for values in metricNumbers:
            try:
                newVal = float(values.replace(',',''))
                finalNumbers.append(newVal)
            except:
                finalNumbers.append(values)
        metricData = zip(metricInfo,finalNumbers)
        return dict(metricData)

    #Extracts similar trending stocks in the market.
    def similarTrendingStocks(self):
        dataList = []
        try:
            url = requests.get(self.link)
            soup = BeautifulSoup(url.text,'lxml')
            tagFinder = soup.find('table',{'class' : 'W(100%) Pos(r) Tbl(f) Bdcl(c) BdB Bdc($seperatorColor)'})
            spanList = tagFinder.find_all('a')
            for span in spanList:
                dataList.append(span.text)
            return dataList
        except:
            return "Enter a valid ticker!"
    
    #Generates stock chart for given stock between period one 
    #and period two. The period is written in list format:
    #[year,month,day]. The frequency is either 1d for daily 
    # frequency or 1mo for monthly frequency.
    def chartGenerator(self,periodOne,periodTwo,frequency): 
        historicData = getChart(self.ticker,periodOne,periodTwo,frequency)
        drawLineGraph(historicData,self.ticker)
        return 'Printing complete!'

# a = stock('JNJ')
# print(a.companyName())
#print(a.priceMetrics())
# print(a.metrics())
# print(a.similarTrendingStocks())
# print(a.chartGenerator([2010,1,1],[2021,11,11],'1mo'))








