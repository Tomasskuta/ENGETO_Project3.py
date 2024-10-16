"""
projekt_3.py: třetí projekt do Engeto Online Python Akademie
author: Tomáš Škuta
email: tomasskuta@seznam.cz
discord: smajlikskutik
"""

import requests
from bs4 import BeautifulSoup
import csv

def main():
    url = "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103"
    output_file = "test.csv"
    data = get_main_data(url)
    zapis_dat(data, output_file)

def get_soup(url):
    response = requests.get(url)
    return BeautifulSoup(response.text, 'html.parser')

def get_main_data(url):
    soup = get_soup(url)

    table_tag = soup.find("div", {"id": "core"})
    rows = table_tag.find_all("tr")

    results = []
    for row in rows[2:-2]:
        cells = row.find_all("td")
        data = combine_data(cells)
        results.append(data)
    
    return results

def get_data_from_link(link, okrsek):
    soup = get_soup(link)

    head_table_tag = soup.find("table", {"class": "table"})
    rows_head = head_table_tag.find_all("tr")
    
    results_head = {}
    if not okrsek:
        for row in rows_head[2:]:
            cells_head = row.find_all("td")
            results_head = {
                "registered": cells_head[3].get_text(),
                "envelopes": cells_head[4].get_text(),
                "valid": cells_head[7].get_text(),
            }
            break
    else:
        for row in rows_head[-1:]:
            cells_head = row.find_all("td")
            results_head = {
                "registered": cells_head[0].get_text(),
                "envelopes": cells_head[1].get_text(),
                "valid": cells_head[4].get_text(),
            }
            break

    table_tag = soup.find("div", {"id": "core"})
    rows = table_tag.find_all("tr")
    results_parties = {}

    for row in rows[4:-1]:
        cells = row.find_all("td")
        if len(cells) > 2:
            results_parties[cells[1].get_text()] = cells[2].get_text()

    return {
        "head": results_head,
        "parties": results_parties
    }

def combine_data(row_tag):
    if len(row_tag) >= 3:
        link_td = row_tag[2].find("a")
        link = "https://volby.cz/pls/ps2017nss/" + link_td['href']
        data_from_link = get_data_from_link(link, False)

        if not data_from_link["parties"]:
            data_from_link = okrsek(link)

        return {
            "code": row_tag[0].getText(),
            "location": row_tag[1].getText(),
            "registered": data_from_link["head"].get("registered"),
            "envelopes": data_from_link["head"].get("envelopes"),
            "valid": data_from_link["head"].get("valid"),
            "parties": data_from_link["parties"]
        }

def zapis_dat(data, jmeno_souboru):
    if isinstance(data, list) and isinstance(data[0], dict):
        headers = list(data[0].keys())
        headers.remove('parties')

        all_parties = []

        for item in data:
            if item is not None and isinstance(item, dict):
                for party_name in item["parties"].keys():
                    if party_name not in all_parties: 
                        all_parties.append(party_name)

        headers += all_parties

    with open(jmeno_souboru, "w", newline="") as f:
        writer = csv.DictWriter(f, delimiter=";", fieldnames=headers)
        writer.writeheader()

        for item in data:
            if item is not None:
                row = item.copy()
                parties = row.pop("parties", {})  

                for party_name in all_parties:
                    row[party_name] = parties.get(party_name, '')  

                writer.writerow(row)

def okrsek(link):
    soup = get_soup(link)

    table_tag = soup.find("div", {"id": "publikace"})
    rows = table_tag.find_all("tr")

    for row in rows[1:2]:
        cells_count = row.find_all("td")
    max_okrsek = len(cells_count)

    big_dict = []
    for row in rows[1:2]:
        cells = row.find_all("td")
        for okrsek in range(max_okrsek):
            link_td = cells[okrsek].find("a")
            if link_td:
                link_in = "https://volby.cz/pls/ps2017nss/" + link_td['href']
            data_okrsky = get_data_from_link(link_in, True)
            big_dict.append(data_okrsky)

    results_parties = {}
    results_head = {'envelopes': 0, 'registered': 0, 'valid': 0}

    for result in big_dict:
        results_head['envelopes'] += int(result['head']['envelopes'])
        results_head['registered'] += int(result['head']['registered'].replace('\xa0', '').replace(' ', ''))
        results_head['valid'] += int(result['head']['valid'])

        for party_name, votes in result['parties'].items():
            votes = int(votes)
            if party_name in results_parties:
                results_parties[party_name] += votes
            else:
                results_parties[party_name] = votes

    return {
        "head": results_head,
        "parties": results_parties  
    }

if __name__ == "__main__":
    main()

