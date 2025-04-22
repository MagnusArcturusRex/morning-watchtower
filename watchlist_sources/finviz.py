# watchlist_sources/finviz.py
import requests
from bs4 import BeautifulSoup

def get_finviz_gainers():
    url = "https://finviz.com/screener.ashx?v=111&s=ta_topgainers&f=sh_price_u10,sh_avgvol_o1000"
    headers = {'User-Agent': 'Mozilla/5.0'}
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')

    table = soup.find_all('table')[6]
    rows = table.find_all('tr')[1:]

    gainers = []
    for row in rows:
        cols = row.find_all('td')
        if len(cols) > 1:
            symbol = cols[1].text
            gainers.append(symbol)

    return gainers
