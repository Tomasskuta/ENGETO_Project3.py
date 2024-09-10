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
    #print(vsechny_tr[2])

    vysledky = []

    for tr in vsechny_tr[2:-2]:
        td_na_radku = tr.find_all("td")
        #print(td_na_radku[0].get_text())
        #print(td_na_radku[1].get_text())
        #link_td = td_na_radku[2].find("a")
        data = get_first_batch_of_data(td_na_radku)
        #if link_td and link_td.has_attr('href'):
            # Get the 'href' attribute (the link)
            #link = link_td['href']
            #print("https://volby.cz/pls/ps2017nss/"+link)
        vysledky.append(data)
        
    #print(td_na_radku)
    pprint(vysledky)
    
def get_first_batch_of_data(tr_tag: "bs4.element.ResultSet"):
    """
    Z kazdeho radku (tr) vyber urcite bunky (td)[index])
    a zabal je do slovniku
    """
    if len(tr_tag) >= 3: #osetreni aby program bral radky kde jsou alespon 3 elementy - cislo, jmeno, link
        link_td = tr_tag[2].find("a") #v tretim tagu center hledam tag mezi a a pak z nej bereme href odkaz
        link = "https://volby.cz/pls/ps2017nss/" + link_td['href']
        return {
            "cislo": tr_tag[0].getText(),
            "jmeno": tr_tag[1].getText(),
            "link": link,
        }


if __name__ == "__main__":
    main()