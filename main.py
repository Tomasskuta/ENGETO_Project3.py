"""
projekt_3.py: třetí projekt do Engeto Online Python Akademie
author: Tomáš Škuta
email: tomasskuta@seznam.cz
discord: smajlikskutik
"""

import requests
from bs4 import BeautifulSoup
from pprint import pprint
import csv

def main():
    url = "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103"
    vystupni_soubor = "test.csv"
    get_main_data(url)

def get_main_data(url):    
    odp_serveru = requests.get(url) 
    soup = BeautifulSoup(odp_serveru.text, 'html.parser') 

    table_tag = soup.find("div", {"id": "core"}) 
    vsechny_tr = table_tag.find_all("tr") 

    vysledky = []
    for tr in vsechny_tr[2:-2]: 
        td_na_radku = tr.find_all("td") 
        data = combine_data(td_na_radku)
        vysledky.append(data)
    
    pprint(vysledky)
    
def get_data_from_link(link):
    odp_serveru = requests.get(link) 
    soup = BeautifulSoup(odp_serveru.text, 'html.parser') 

    head_table_tag = soup.find("table", {"class": "table"})
    vsechny_tr_head = head_table_tag.find_all("tr") 
    vysledky_head = {}
    for tr in vsechny_tr_head[2:]:
        td_na_radku_head = tr.find_all("td")
        vysledky_head = {
            "registered": td_na_radku_head[3].get_text(),
            "envelopes": td_na_radku_head[4].get_text(),
            "valid": td_na_radku_head[7].get_text(),
        }
        break

    table_tag = soup.find("div", {"id": "core"})
    vsechny_tr = table_tag.find_all("tr")
    vysledky_parties = []
    for tr in vsechny_tr[5:-1]:
        td_na_radku = tr.find_all("td")
        if len(td_na_radku) > 2:
            vysledky_party = {
                "strana": td_na_radku[1].get_text(),
                "hlasy": td_na_radku[2].get_text(),
            } 
            vysledky_parties.append(vysledky_party)   

    return {
        "head": vysledky_head,
        "parties": vysledky_parties
    }

def combine_data(tr_tag: "bs4.element.ResultSet"):
    """
    Z kazdeho radku (tr) vyber urcite bunky (td)[index])
    a zabal je do slovniku
    """
    if len(tr_tag) >= 3: 
        link_td = tr_tag[2].find("a") 
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
            "registered": data_from_link["head"].get("registered"),  
            "envelopes": data_from_link["head"].get("envelopes"),
            "valid": data_from_link["head"].get("valid"),
            "parties": data_from_link["parties"]
        }

if __name__ == "__main__":
    main()