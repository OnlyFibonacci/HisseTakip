import requests
from bs4 import BeautifulSoup
import json
HEADERS = ({'User-Agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
            (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',\
            'Accept-Language': 'en-US, en;q=0.5'})
# Sayfayı indirin ve Beautiful Soup ile ayrıştırın


def gorselLinkGetir(hisse:str):
    url = f"https://tr.tradingview.com/symbols/BIST-{hisse}/"
    page = requests.get(url,headers=HEADERS)
    soup = BeautifulSoup(page.content, "html.parser")

    gorselLink = soup.find_all("div",attrs={"class":"tv-widget-idea__cover-wrap"})
    son3Gorsel=[]
    for i in range(3) :
        son3Gorsel.append(gorselLink[i].find("img").get("data-src"))
    return son3Gorsel



def temel(hisse:str):
    url = f"https://tr.tradingview.com/symbols/BIST-{hisse}/financials-statistics-and-ratios/"
    page = requests.get(url,headers=HEADERS)
    soup = BeautifulSoup(page.content, "html.parser")



    jsons = soup.find_all("script",attrs={"type":"application/prs.init-data+json"})

    bizim= jsons[3].__dict__['contents'][0]
    veri = json.loads(bizim)
    aciklama = veri[next(iter(veri))]['descriptions']

    yaziHali = ""
    for i in aciklama:
        if 'text' in aciklama[i]:
            yaziHali += aciklama[i]['text'] + "\n➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
    yaziHali += "Veriler Tradingview tarafından sağlanmaktadır."
    return yaziHali





    


