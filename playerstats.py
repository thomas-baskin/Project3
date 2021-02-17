# %%
import pandas as pd
import numpy as np
#import matplotlib.pyplot as plt

from bs4 import BeautifulSoup 
import requests

def getStats():
    page = requests.get("https://www.basketball-reference.com/players/j/jamesle01.html")
    soup = BeautifulSoup(page.content,'html.parser')
    all_per_game = soup.find("div",{"id":"all_per_game"})
    all_per_game = soup.find("div",{"id":"div_per_game"})
    #getColumnHeads = soup.find("thead").find("tr")
    for th in soup.findAll("th",scope="col"):
        print(th.text) #each th.text is the col header
        #print(th.get("aria-label"))
    all_rows = all_per_game.find("tbody")
    print("-----------")
    print(all_rows)
    

if __name__ == "__main__":
    getStats()
# %%
