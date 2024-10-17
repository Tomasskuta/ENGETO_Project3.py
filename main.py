"""
projekt_3.py: třetí projekt do Engeto Online Python Akademie

author: Tomáš Škuta
email: tomasskuta@seznam.cz
discord: smajlikskutik
"""

import requests
from bs4 import BeautifulSoup
import csv
import argparse
import sys

def main(url: str, output_file: csv):
    '''
    Main app function
    '''
    data = get_main_data(url)
    zapis_dat(data, output_file)

def get_soup(url: str) -> BeautifulSoup:
    '''
    Function for getting soup from url
    '''
    response = requests.get(url)
    return BeautifulSoup(response.text, 'html.parser')

def is_valid_parties_data(parties: dict[str]) -> bool:
    '''
    Function for checking if we have data from first link - this is useful when city has more okrseks than one.
    '''
    for party, votes in parties.items():
        if not party.isdigit():
            return True
    return False

def get_main_data(url: str) -> list:
    '''
    Function for getting data, combining location and code and then scraping other data from link containing envelopes, parties etc.
    '''
    soup = get_soup(url)
    table_tag = soup.find("div", {"id": "core"})
    rows = table_tag.find_all("tr")

    results = []
    for row in rows[2:]:
        cells = row.find_all("td")
        data = combine_data(cells)
        results.append(data)
    
    return results

def get_data_from_link(link: str, okrsek: bool) -> dict[str]:
    '''
    Function for getting data from link, depends if okrsek is true or not. If yes function is edited to match different table than when city has only one okrsek.
    '''
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
            results_parties[cells[1].get_text()] = cells[2].get_text() #getting name of the party:votes

    return {"head": results_head, "parties": results_parties}

def combine_data(row_tag) -> dict[{dict}]:
    '''
    Function for combining data without link (location, code) and then all data from link. If we have no data from first link it means that city has more okrseks.
    '''
    if len(row_tag) >= 3:
        if len(row_tag) >= 3 and row_tag[2].find("a") is not None:
            link = "https://volby.cz/pls/ps2017nss/" + row_tag[2].find("a")['href'] #added start of the link since a href containts only remaining part of the link
            data_from_link = get_data_from_link(link, False)
        else:
            return None
        
        if not is_valid_parties_data(data_from_link["parties"]): #if not, script knows there is more okrseks
            data_from_link = okrsek(link)

        return {
            "code": row_tag[0].getText(),
            "location": row_tag[1].getText(),
            "registered": data_from_link["head"].get("registered"),
            "envelopes": data_from_link["head"].get("envelopes"),
            "valid": data_from_link["head"].get("valid"),
            "parties": data_from_link["parties"]
        }

def zapis_dat(data: list, output_file: csv) -> csv:
    '''
    Function for saving data to csv file.
    '''
    if not data or not isinstance(data[0], dict):
        return
    
    general_headers = list(data[0].keys() )
    general_headers.remove('parties')  #removing parties since we dont want to have column parties

    all_parties = []
    for item in data:
        if "parties" in item and item["parties"]:
            all_parties = list(item["parties"].keys()) #getting keys from parties dict - names of parties
            break  

    headers = general_headers + all_parties #now we have general header and instead of parties column, we have each party

    with open(output_file, "w", newline="", encoding='utf-8-sig') as f: #uft-8 coding would be enough, but with utf-8-sig also excel opens it with correct coding
        writer = csv.DictWriter(f, delimiter=";", fieldnames=headers)
        writer.writeheader()

        for item in data:
            if item is not None:
                row = item.copy() 
                parties = row.pop("parties", {})  #popping parties for clean dict 

                for party_name in all_parties:
                    row[party_name] = parties.get(party_name, '') #filling clean dict with actual party data/names

                writer.writerow(row)

def okrsek(link: str):
    '''
    Function for getting data from each okrsek in cities where there are more than one (more links).
    '''
    soup = get_soup(link)
    table_tag = soup.find("div", {"id": "publikace"})
    rows = table_tag.find_all("tr")

    for row in rows[1:2]:
        cells_count = row.find_all("td")
    max_okrsek = len(cells_count) #getting max number of okrsek for for loop below

    okrsek_all_data = []
    for row in rows[1:2]:
        cells = row.find_all("td")
        for okrsek in range(max_okrsek):
            link_td = cells[okrsek].find("a")
            if link_td:
                link_in = "https://volby.cz/pls/ps2017nss/" + link_td['href']
            data_okrsky = get_data_from_link(link_in, True) #getting data link by link
            okrsek_all_data.append(data_okrsky) #collecting all data, each link is one dict

    results_parties = {}
    results_head = {'envelopes': 0, 'registered': 0, 'valid': 0}

    for result in okrsek_all_data: #couting all dicts(each link one dict) together
        results_head['envelopes'] += int(result['head']['envelopes'].replace('\xa0', '').replace(' ', '')) #replacing whitescape or unwated characters from html
        results_head['registered'] += int(result['head']['registered'].replace('\xa0', '').replace(' ', ''))
        results_head['valid'] += int(result['head']['valid'].replace('\xa0', '').replace(' ', ''))

        for party_name, votes in result['parties'].items():
            votes = int(votes)
            if party_name in results_parties:
                results_parties[party_name] += votes
            else:
                results_parties[party_name] = votes

    return {"head": results_head, "parties": results_parties}

if __name__ == "__main__":
    '''
    This part only done when main is used. Not in case when just other function/s used from this script. Also two arguments defined here.
    '''
    parser = argparse.ArgumentParser(description='Process Czech election data from 2017. How to use it: python main.py "link" "output_file". For link visit https://www.volby.cz/pls/ps2017nss/ps3?xjazyk=CZ and choose City for which you want to scrape the data and use that link from city itself. More info with example in README.md.')
    parser.add_argument('url', type=str, help='The URL of the election data page. Must be in format "https://www.volby.cz/pls/ps2017nss/..." or "http://www.volby.cz/pls/ps2017nss/..."')
    parser.add_argument('output_file', type=str, help='The output CSV file name. Must be in format "name.csv"')
    args = parser.parse_args()

    if not args.url.startswith("http://www.volby.cz/pls/ps2017nss/") and not args.url.startswith("https://www.volby.cz/pls/ps2017nss/"):
        print("Error: The URL must start with 'http://www.volby.cz/pls/ps2017nss/' or 'https://www.volby.cz/pls/ps2017nss/'")
        print("Also format of command must be: url output_file")
        sys.exit(1)
    if not args.output_file.endswith(".csv"):
        print("Error: The NAME of csv output file must end with .csv'")
        print("Also format of command must be: url output_file")
        sys.exit(1)
    
    main(args.url, args.output_file)

