from bs4 import BeautifulSoup
import requests
from pprint import pprint

odp_serveru = requests.get("https://www.volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj=12&xobec=589276&xokrsek=1&xvyber=7103") 
soup = BeautifulSoup(odp_serveru.text, 'html.parser') 

head_table_tag = soup.find("table", {"class": "table"})
vsechny_tr_head = head_table_tag.find_all("tr") 
vysledky_head = {}
for tr in vsechny_tr_head[-1:]:
        td_na_radku_head = tr.find_all("td")
        vysledky_head = {
            "registered": td_na_radku_head[0].get_text(),
            "envelopes": td_na_radku_head[1].get_text(),
            "valid": td_na_radku_head[4].get_text(),
        }
        break
print(vysledky_head)