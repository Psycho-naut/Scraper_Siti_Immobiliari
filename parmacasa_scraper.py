import os
import string
import sys
import requests
from re import U
from bs4 import BeautifulSoup
import csv

with open('parmacasa.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['nome', 'via', 'prezzo', 'metri', 'link'])


min=input("Inserisci prezzo minimo: ")
max=input("Inserisci prezzo massimo: ")
print("Tipi ricerca Appartamenti disponibili: Monolocale,Bilocale,Trilocale")
tip=input("Inserisci tipo di Appartamento: Default premi INVIO: ")
tip=tip.lower()
com=input("Inserisci Comune: ")
com=com.lower()
tip2="appartamento"

URL="https://www.parmacasa.it/annunci/case-e-appartamenti/affitto/"


if tip == "":
    URL=URL + str(com) + "/" + str(tip2) + "/prezzo_min-" + str(min) + ",prezzo_max-" + str(max)
elif tip != "":
    URL=URL + str(com) + "/" + str(tip) + "/prezzo_min-" + str(min) + ",prezzo_max-" + str(max)

r = requests.get(URL)
s = BeautifulSoup(r.text, "lxml")

#print(URL)
#print(r)

results=s.select('[class="list-item property-box-2"]')
pages=s.select('[class="pagination"]')
#print(pages)

for page in pages:
    num=page.findChildren('a', {'class': 'page-link'})
    if len(num) == 0:
        continue
    print("Pagine disponibili: ",len(num) - 1)
p=len(num)
#print(p)

C=int(input("Quante pagine vuoi consultare? "))
for o in range(0,C +1):
    request_url = URL
    if o > 0:
        request_url = URL + "?page=" + str(o)
        #print(request_url)
        r = requests.get(request_url)
        s = BeautifulSoup(r.text, "lxml")
        results=s.select('[class="list-item property-box-2"]')
        for result in results:
            URL2="https://www.parmacasa.it/"
            nome=result.findChildren('a', {'class': 'text-truncate'})
            link=URL2 + nome[0].get("href")
            if len(nome) == 0:
                continue
            n=nome[0].text
            via=result.findChildren('h5', {'class': 'location'})
            if len(via) == 0:
                continue
            caratteri=" \n \t €"
            v=str(via[0].text)
            for i in range(len(caratteri)):
                v=v.replace(caratteri[i],"")
            prezzo=result.findChildren('div', {'class': 'price-ratings-box row m-0'})
            if len(prezzo) == 0:
                continue
            p=str(prezzo[0].text)
            caratteri2=" \n \t "
            for i in range(len(caratteri2)):
                p=p.replace(caratteri2[i],"")
            metri=result.findChildren('div', {'class': 'item-flex-icone-caratteristiche'})
            if len(metri) == 0:
                continue
            caratteri=" \n \t "
            m=str(metri[0].text)
            for i in range(len(caratteri)):
                m=m.replace(caratteri[i],"")
            with open('parmacasa.csv', 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([n, v, p, m, link])
