"""
projekt_3.py: třetí projekt do Engeto Online Python Akademie
author: Tomáš Škuta
email: tomasskuta@seznam.cz
discord: smajlikskutik
"""

import requests
from bs4 import BeautifulSoup
from pprint import pprint

def main():
    url = "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103"
    vystupni_soubor = "test.csv"
    #get data from url
    odp_serveru = requests.get(url) #stahl sem cely html kod stranky z odkazu
    #parsovani
    soup = BeautifulSoup(odp_serveru.text, 'html.parser') # promenna + typ parseru
    #najdu vsechny tabulky
    table_tag = soup.find("div", {"id": "core"}) # kdyz tu dam all at najdu vsechny ty tabulky tak pak nejede to niz ?????????????????????????????????????????????
    #print(table_tag)
    vsechny_tr = table_tag.find_all("tr") 
    print(vsechny_tr[2:-2])




if __name__ == "__main__":
    main()