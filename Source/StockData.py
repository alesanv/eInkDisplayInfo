
from bs4 import BeautifulSoup
import requests


class Stock:
    def __init__(self, symbol):
        self.symbol = symbol
        self.price = 0.0
        self.getPrice()
        
    #Get the price of a stock scraping Yahoo's data with beautiful soup
    def getPrice(self):
        try:
            stock=self.symbol
            url = f'https://finance.yahoo.com/quote/{stock}?p={stock}&.tsrc=fin-srch-v1'
            page = requests.get(url)
            soup = BeautifulSoup(page.text, 'lxml')
            self.price = soup.find('span',class_= 'Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)').text
        except:
            print("Error while getting stock price: " + self.symbol)
            
    #__str__ function is used to return a user-friendly string
    #representation of the object
    def __str__(self):
        return f"{self.symbol}: ${self.price}"
        

