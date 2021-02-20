# %%
import pandas as pd
import numpy as np
#import matplotlib.pyplot as plt

from bs4 import BeautifulSoup 
import requests
page = requests.get("https://www.basketball-reference.com/players/j/jamesle01.html")
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
data = []
for td in all_rows:
    try:
        list1 = []
        for j in td:
            list1.append(j.text)
        data.append(list1)
    except:
        print ("------")
print(data)
# %%
df = pd.DataFrame(data, columns=columns) 
display(df.head())
# %%
