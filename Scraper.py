#import
from bs4 import BeautifulSoup
import requests
import re
from os.path import exists as file_exists
import time

#declaratie
hoogste = []
teller = 1
tijd = int(input("Program interval in seconds: "))

while True:
    print(teller, end = ": ")
    t= tijd
    hoogste = []

    #request de website
    url = 'https://www.blockchain.com/btc/unconfirmed-transactions'
    r = requests.get(url)
    if r.status_code == 200:
        soup = BeautifulSoup(r.text, 'html.parser')
        transacties = soup.find_all('div',{ "class" : "sc-1g6z4xm-0 hXyplo" })
    else:
        print("Er was een fout bij de download\nFoutcode:", r.status_code)

    print("request gelukt", end = ", ")

    #voor elke transactie
    for x in transacties:
        #maak de huidige leeg
        huidige = []

        #Steek een volgend object in huidigehash
        huidigehash = x.find_all('div', {"class" : "sc-6nt7oh-0 PtIAf"})

        #Haal alle tekst uit de hash en steek die in huidige
        for y in huidigehash:
            huidige.append(y.text)

        #Als de hoogste leeg is, sla dan de huidige op als hoogste
        if len(hoogste) == 0:
            hoogste = huidige

        #Vervang de waarde van BTC in str met de waarde in BTC in int
        for z in range(len(huidige)):
            if z == 2:
                huidige[z] = float(re.search("([0-9])+.([0-9])+", huidige[z]).group())
                hoogste[z] = float(hoogste[z])

        #Als een nieuwe hoogste wordt gevonden, vervang dan de vorige
        if huidige[2]>hoogste[2]:
            for a in range(len(huidige)):
                hoogste[a] = huidige[a]

        #converteer float van hoogste terug naar str
        for b in range(len(hoogste)):
            if b == 2:
                hoogste[b] = str(hoogste[b])

    print("Alle transacties gelukt", end = ", ")

    #schrijf naar een bestand

    #controleer of bestand bestaat
    if file_exists('Grootste_transacties.txt'):
        #zo ja, open in append modus
        f=open("Grootste_transacties.txt", "a")
    else:
        #zo nee, maak en open in write modus
        f=open("Grootste_transacties.txt", "w")


    #lees laatste lijn


    #vergelijk met de huidige hoogste


    #schrijf alle inhoud naar het bestand
    for x in hoogste:
        x=x+" "
        f.write(x)
    f.write("\n")

    #sluit het bestand
    f.close()

    print("file schrijven gelukt")

    while t>0:
        mins, secs = divmod(t, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs)
        print("refresh in: ", timer, end="\r")
        time.sleep(1)
        t -= 1

    teller+=1


input("End of program")
