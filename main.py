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
    data = get_main_data(url)
    zapis_dat(data, vystupni_soubor)


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
    
    return vysledky
    
def get_data_from_link(link,okrsek):
    odp_serveru = requests.get(link)
    soup = BeautifulSoup(odp_serveru.text, 'html.parser') 

    head_table_tag = soup.find("table", {"class": "table"})
    vsechny_tr_head = head_table_tag.find_all("tr") 
    vysledky_head = {}
    if not okrsek:
        for tr in vsechny_tr_head[2:]:
            td_na_radku_head = tr.find_all("td")
            vysledky_head = {
                "registered": td_na_radku_head[3].get_text(),
                "envelopes": td_na_radku_head[4].get_text(),
                "valid": td_na_radku_head[7].get_text(),
            }
            break
    else:
        for tr in vsechny_tr_head[-1:]:
            td_na_radku_head = tr.find_all("td")
            vysledky_head = {
                "registered": td_na_radku_head[0].get_text(),
                "envelopes": td_na_radku_head[1].get_text(),
                "valid": td_na_radku_head[4].get_text(),
            }
            break

    table_tag = soup.find("div", {"id": "core"})
    vsechny_tr = table_tag.find_all("tr")
    vysledky_parties = []
    for tr in vsechny_tr[4:-1]:
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

def combine_data(tr_tag):

    if len(tr_tag) >= 3: 
        link_td = tr_tag[2].find("a") 
        link = "https://volby.cz/pls/ps2017nss/" + link_td['href']
        data_from_link = get_data_from_link(link,False)

        if (data_from_link["parties"]) == []:
            data_from_link = okrsek(link)

        return {
            "code": tr_tag[0].getText(),
            "location": tr_tag[1].getText(),
            "registered": data_from_link["head"].get("registered"),  
            "envelopes": data_from_link["head"].get("envelopes"),
            "valid": data_from_link["head"].get("valid"),
            "parties": data_from_link["parties"]
        }

def zapis_dat(data, jmeno_souboru):

    if isinstance(data, list) and isinstance(data[0], dict):
        parties_data = []
        for item in data:
            if item is not None and isinstance(item, dict):
                if "parties" in item:
                    parties_data.append(item["parties"])
                    del item["parties"]

        headers_parties = []
        for party in parties_data[1]:
            if party is not None and isinstance(party, dict):
                if "strana" in party:
                    headers_parties.append(party["strana"])

        headers = list(data[0].keys()) + headers_parties
        
    with open(jmeno_souboru, "w", newline="") as f:
        writer = csv.DictWriter(f, delimiter=";", fieldnames=headers)
        writer.writeheader()  
        
        for i, row in enumerate(data):
            if row:
                row.update({party_name: '' for party_name in headers_parties})
                if i < len(parties_data):
                    for party in parties_data[i]:
                        if party["strana"] in row:
                            row[party["strana"]] = party["hlasy"]

                writer.writerow(row)

        
def okrsek(link):

    odp_serveru = requests.get(link) 
    soup = BeautifulSoup(odp_serveru.text, 'html.parser') 

    table_tag = soup.find("div", {"id": "publikace"}) 
    vsechny_tr = table_tag.find_all("tr") 

    for tr in vsechny_tr[1:2]:
        td_na_radku_count = tr.find_all("td")
    max_okrsek = len(td_na_radku_count)

    for tr in vsechny_tr[1:2]: 
        td_na_radku = tr.find_all("td") 
        big_dict = []
        for i in range(max_okrsek):
            link_td = td_na_radku[i].find("a")
            if link_td:
                link_in = "https://volby.cz/pls/ps2017nss/" + link_td['href']
            data_okrsky = get_data_from_link(link_in,True)
            big_dict.append(data_okrsky)

    vysledky_parties = {}
    vysledky_head = {'envelopes': 0, 'registered': 0, 'valid': 0}

    for result in big_dict:

        vysledky_head['envelopes'] += int(result['head']['envelopes'])
        vysledky_head['registered'] += int(result['head']['registered'].replace('\xa0', '').replace(' ', ''))
        vysledky_head['valid'] += int(result['head']['valid'])

        for party in result['parties']:
            party_name = party['strana']
            votes = int(party['hlasy'])
            if party_name in vysledky_parties:
                vysledky_parties[party_name] += votes
            else:
                vysledky_parties[party_name] = votes

    vysledky_parties_list = [{'strana': party, 'hlasy': str(votes)} for party, votes in vysledky_parties.items()]
    return {
        "head": vysledky_head,
        "parties": vysledky_parties_list
    }
    
        
if __name__ == "__main__":
    main()