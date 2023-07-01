# SCRIPT PER RECUPERARE INFORMAZIONI SULLE CASE IN AFFITTO
import os
import sys
import requests
from os import name
from re import U
from bs4 import BeautifulSoup
import csv

with open('affitti.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['via', 'prezzo', 'link'])

print("Ricerca su Immobiliare.it")
city=input("Inserisci il nome della città: ") # INSERIRE NOME CITTÀ
city=city.lower() # CONVERTE LE LETTERE MAIUSCOLE IN MINUSCOLO
URL="https://www.immobiliare.it/affitto-case/" + city

A=input("La cerchi una casa in provincia? si/no: ")
if A == "si":
    URL=URL + "-provincia"
elif A != "no":
    sys.exit("Errore: Inserisci una delle seguenti opzioni: si/no")

B=int(input("Prezzo minimo: "))
B2=int(input("Prezzo massimo: "))

# CONTO LE PAGINE
print("Searching . . .")
for i in range(100):
    request_URL=URL + "?pag=" + str(i)
    resp=requests.get(request_URL)
    #print(resp.status_code)
    #print(request_URL)
    if resp.status_code == 200:
        continue
    elif resp.status_code != 200:
        #print("Le pagine di annunci sono: ",i-1)
        break
page=(i -1)

URL=URL + "?prezzoMinimo=" + str(B) + "&prezzoMassimo=" + str(B2)
print("Pagine :",page)
C=int(input("Quante pagine vuoi consultare? "))
for pag in range(1,C +1):
    request_url = URL
    if pag > 1:
        request_url=URL + "&pag=" + str(pag)
    resp = requests.get(request_url)
    soup = BeautifulSoup(resp.text, "lxml")
    results = soup.select('[class="nd-list__item in-realEstateResults__item"]')
    for result in results:
        via = result.findChildren('a', {'class': 'in-card__title'})
        if len(via) == 0:
            continue
        via1 = via[0].text
        link= via[0].get("href")
        prezzo = result.findChildren('li', {'class': 'nd-list__item in-feat__item in-feat__item--main in-realEstateListCard__features--main'})
        if len(prezzo) == 1:
            prezzo1= prezzo[0].text
            with open('affitti.csv', 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([via1, prezzo1, link])

