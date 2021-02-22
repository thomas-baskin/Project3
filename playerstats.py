# %%
import pandas as pd
import numpy as np
#import matplotlib.pyplot as plt

from bs4 import BeautifulSoup 
import requests


def getPlayer(dataList, columns,URL):
    page = requests.get(URL)
    soup = BeautifulSoup(page.content,'html.parser')
    all_per_game = soup.find("div",{"id":"all_per_game"})
    all_per_game = soup.find("div",{"id":"div_per_game"})
    columns = []
    for th in soup.findAll("th",scope="col"):
        columns.append(th.text)
        #print(th.text) #each th.text is the col header
        #print(th.get("aria-label"))
    all_rows = all_per_game.find("tbody")
    print("-----------")
    dataList = []
    for td in all_rows:
        try:
            list1 = []
            for j in td:
                list1.append(j.text)
            dataList.append(list1)
        except:
            pass
    return dataList, columns


jamesleList = []
jamesleColumns = []
jamesleList, jamesleColumns = getPlayer(jamesleList,jamesleColumns,"https://www.basketball-reference.com/players/j/jamesle01.html")
# %%
jamesledf = pd.DataFrame(jamesleList, columns=jamesleColumns) 
jamesledf = jamesledf.fillna(0)

kareemList = []
kareemColumns = []
kareemList, kareemColumns = getPlayer(kareemList,kareemColumns,"https://www.basketball-reference.com/players/a/abdulka01.html")
kareemdf = pd.DataFrame(kareemList, columns=kareemColumns)
kareemdf = kareemdf.fillna(0)

jordanList = []
jordanColumns = []
jordanList, jordanColumns = getPlayer(jordanList,jordanList,"https://www.basketball-reference.com/players/j/jordami01.html")
jordandf = pd.DataFrame(jordanList, columns=jordanColumns)
jordandf = jordandf.fillna(0)

russelList = []
russelColumns = []
russelList, russelColumns = getPlayer(russelList,russelColumns,"https://www.basketball-reference.com/players/r/russebi01.html")
russeldf = pd.DataFrame(russelList, columns=russelColumns)
russeldf = russeldf.fillna(0)

display(jamesledf.head())
# %%
