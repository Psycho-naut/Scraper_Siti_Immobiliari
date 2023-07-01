import requests
from re import U
from bs4 import BeautifulSoup
import csv

with open('offrocasa.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['nome','prezzo', 'metri', 'locali', 'link'])

print("Script per eseguiro lo scraper del sito Offrocasa.com")
print("\n")


URL="https://www.offrocasa.com/"


citta=input("Inserisci la città: ")
citta.lower()
prezzo=input("Inserisci prezzo massimo: ")

URL= URL + "affitti-" + str(citta) + ".html" + "?prezzomax=" + str(prezzo)
r = requests.get(URL)
s = BeautifulSoup(r.text, "lxml")
page=s.select('[class="search-paginator tr-nav-pagin"]')

    
def gira_pagina(url,richiesta,ogg_soap,class_select):
    for p in class_select:
        num=p.find_all('a', {'rel': 'nofollow'})
        if len(num) == 0:
            print("Pagine disponibili: 1")
        else:
            print("Pagine disponibili: ",len(num))

gira_pagina(URL,r,s,page)
C=int(input("Inserisci il numero di pagine da visualizzare: "))
for o in range(0,C +1):
    request_url = URL
    if o > 0:
        request_url = URL + "&page=" + str(o)
        r = requests.get(request_url)
        s = BeautifulSoup(r.text, "lxml")
        results=s.select('[class="clearfix search-result-list-item"]')
        for result in results:
            nome=result.findChildren('div', {'class': 'title'})
            if len(nome) == 0:
                continue
            n=str(nome[0].text)
            caratteri=" \n \t 0123456789 €" 
            for i in range(len(caratteri)):
                n=n.replace(caratteri[i],"")
            prezzo=result.findChildren('div', {'class': 'prezzo'})
            if prezzo == 0:
                continue
            p=prezzo[0].text
            metri=result.findChildren('div', {'class' :'subtitle-text'})
            try:
                if metri == 0:
                    continue
                m=metri[0].text
            except IndexError:
                m="Dato non Presente"
            locali=result.findChildren('div', {"class": "locali"})
            try:
                if locali == 0:
                    continue
                l=str(locali[0].text)
                caratteri2=" \n \t Locali" 
                for i in range(len(caratteri2)):
                    l=l.replace(caratteri2[i],"")
            except IndexError:
                l="Dato non Presente"
            URL2="https://www.offrocasa.com"
            link=result.findChildren('a', {'class': 'link-to-realestate'})
            k= URL2 + link[0].get("href")
            with open('offrocasa.csv', 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([n,p,m,l,k])
