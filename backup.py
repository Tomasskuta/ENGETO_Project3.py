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
    get_main_data(url)

def get_main_data(url):    
    #get data from url
    odp_serveru = requests.get(url) #stahl sem cely html kod stranky z odkazu
    #parsovani
    soup = BeautifulSoup(odp_serveru.text, 'html.parser') # promenna + typ parseru
    #najdu vsechny tabulky
    table_tag = soup.find("div", {"id": "core"}) 

    vsechny_tr = table_tag.find_all("tr") 

    vysledky = []

    for tr in vsechny_tr[2:-2]: #ignoruju prvni 2 a posledni 2 radky at mi to nedela binec
        td_na_radku = tr.find_all("td") #na radsich najdu vsechny bunky
        data = combine_data(td_na_radku)
        vysledky.append(data)
    
    pprint(vysledky)
    
def get_data_from_link(link):
    odp_serveru = requests.get(link) 

    soup = BeautifulSoup(odp_serveru.text, 'html.parser') 
    table_tag = soup.find("table", {"class": "table"})
    vsechny_tr = table_tag.find_all("tr") 

    for tr in vsechny_tr[2:]:
        td_na_radku = tr.find_all("td")
        return {
            "registered": td_na_radku[3].get_text(),
            "envelopes": td_na_radku[4].get_text(),
            "valid": td_na_radku[7].get_text(),
        }


def combine_data(tr_tag: "bs4.element.ResultSet"):
    """
    Z kazdeho radku (tr) vyber urcite bunky (td)[index])
    a zabal je do slovniku
    """
    if len(tr_tag) >= 3: #osetreni aby program bral radky kde jsou alespon 3 elementy - cislo, jmeno, link
        link_td = tr_tag[2].find("a") #v tretim tagu center hledam tag mezi a a pak z nej bereme href odkaz
        link = "https://volby.cz/pls/ps2017nss/" + link_td['href']
        data_from_link = get_data_from_link(link)

        if data_from_link is None:
            data_from_link = {
                "registered": "N/A",
                "envelopes": "N/A",
                "valid": "N/A",
            }
    
        return {
            "cislo": tr_tag[0].getText(),
            "jmeno": tr_tag[1].getText(),
            "registered": data_from_link["registered"],  
            "envelopes": data_from_link["envelopes"],
            "valid": data_from_link["valid"]
        }

if __name__ == "__main__":
    main()