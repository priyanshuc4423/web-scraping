import requests
from bs4 import BeautifulSoup
import lxml
import csv

class Scrapedata:
    def __init__(self,url):
        self.csv_datas = [['name','product_id','price','brand','age','images','color','shoes sizes']]

        self.header =  {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'}
        self.url = url
    def shoesizes(self,productid):
        self.shoe_sizes = []
        shoe_url = f'https://www.totalsports.co.za/product/generateProductJSON.jsp?productId={productid}'
        self.res = requests.get(headers = self.header,url=shoe_url)
        self.sizes = self.res.json()['sizes']
        self.shoe_sizes = [size['name'] for size in self.sizes]
        return self.shoe_sizes

    def get_data(self):
        self.response = requests.get(headers=self.header,url=self.url)
        self.data = self.response.json()


    def csv_data(self,name):
        self.datalists = name
        with open(f"{self.datalists}",'w') as file:
            writer = csv.writer(file)
            writer.writerows(self.csv_datas)

    def datas(self):
        for item in self.data['data']['products'][:1]:
            self.name = item['name']
            self.namelist = self.name.split(" ")
            if "Women's" in self.namelist:
                self.age = 'women'
                self.dataname = 'women'
            else:
                self.age = 'men'
                self.dataname = 'men'
            self.product_id = item['productId']
            self.shoe = self.shoesizes(productid=item['productId'])
            self.pricerange = item['latestPriceRange']
            self.brand = item['brand']
            self.images = [item['defaultImages'],item['swapImage']]
            self.color = item['colors'][0]['name']
            self.csv_datas.append([self.name,self.product_id,self.pricerange,self.brand,self.age,self.images,self.color,self.shoe])
        self.csv_data(self.dataname)



URLS =['https://www.totalsports.co.za/search/ajaxResultsList.jsp?N=27sa&Ns=availability&Nrpp=73&page=1&baseState=27sa&cat=Sneakers&c=all',
       'https://www.totalsports.co.za/search/ajaxResultsList.jsp?N=27qt&Nrpp=112&page=1&baseState=27qt&cat=Sneakers&c=all']

def getdata(urls):
    urls = urls
    for url in urls:
        a = Scrapedata(url)
        a.get_data()
        a.datas()


getdata(urls=URLS)

