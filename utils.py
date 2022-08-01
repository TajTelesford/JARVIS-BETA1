from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import re
import time
import asyncio
from tqdm import tqdm, trange
import csv
from os.path import exists

# STOCKS

#############################################################################################################
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_experimental_option('excludeSwitches', ['enable-logging'])


# grabbing the figure id's
def figure_id(div):
    idList = []
    FigureId = div.find_all(name="article")
    for ID in FigureId:
        item = ID['class']
        idList.append(item[4][4:])
    return idList


# getting page source
def get_page_source(url):
    d = webdriver.Chrome('C:/Users/TajTe/Desktop/webdriver/chromedriver.exe', options=options)
    d.get(url)
    time.sleep(1.5)
    page = d.page_source
    d.close()

    return page


# getting the figure's stock trades/types/dates
def figure_stock(idlist):
    figureUrl = "https://www.capitoltrades.com/politicians/"
    Stock_List = []
    Stock_Date = []
    Stock_Type = []
    Stock_buy = []
    Stock_sell = []

    for i in tqdm(range(3), desc="LOADING STOCKS>>>", maxinterval=100):
        url = figureUrl + f"{idlist[i]}"

        page = get_page_source(url)

        doc = BeautifulSoup(page, "html.parser")
        stock = doc.find_all("h3", {"class": "q-fieldset issuer-name"})
        date = doc.find_all("div", {"class": "q-value"})
        trade_type = doc.find_all(class_=re.compile("q-field tx-type tx-type"))
        for items in stock:
            Stock_List.append(items.a.string)

        for d in date:
            Stock_Date.append(d.string)

        for typeofstock in trade_type:
            Stock_Type.append(typeofstock.string)

        for (s, t, d) in zip(Stock_List, Stock_Type, Stock_Date):
            if t == "buy":
                Stock_buy.append(f"{s} {t} {d}")
            if t == "sell":
                Stock_sell.append(f"{s} {t} {d}")

    return Stock_buy, Stock_sell


def dump_data_csv(buy, sell):
    data = stock_buy_sell_csv()
    data_list = []

    if if_file_exists(data):
        return
    else:
        for i in trange(len(buy)):
            data_list.append(("BUY", buy[i]))
        for i in trange(len(sell)):
            data_list.append(("SELL", sell[i]))

        with open(data, 'w') as file:

            csv_write = csv.writer(file)
            print("DUMPING DATA")
            csv_write.writerows(data_list)
            file.close()


def get_stocks():
    timePeriod = 30
    url = f"https://www.capitoltrades.com/politicians?txDate={timePeriod}d"

    page = requests.get(url).text
    document = BeautifulSoup(page, "html.parser")

    ids_for_pages = document.find(class_="q-cardlist__content")
    buy_list, sell_list = figure_stock(figure_id(ids_for_pages))
    print(buy_list)
    print(sell_list)
    dump_data_csv(buy_list, sell_list)


#######################################################################################################


def if_file_exists(path):
    file_exists = exists(path)
    return file_exists


def stock_buy_sell_csv():
    return "C:/Users/TajTe/PycharmProjects/pythonProject/StockData/stockdata.csv"
