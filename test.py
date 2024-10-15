from bs4 import BeautifulSoup
import requests
from pprint import pprint

odp_serveru = requests.get("https://www.volby.cz/pls/ps2017nss/ps33?xjazyk=CZ&xkraj=12&xobec=589250") 
soup = BeautifulSoup(odp_serveru.text, 'html.parser') 

table_tag = soup.find("div", {"id": "publikace"}) 
vsechny_tr = table_tag.find_all("tr") 

for tr in vsechny_tr[1:2]: 
    td_na_radku_count = tr.find_all("td")
    #print(tr)

max_okrsek = len(td_na_radku_count)
#print(max_okrsek)

for tr in vsechny_tr[1:2]: 
    td_na_radku = tr.find_all("td")
    #pprint(td_na_radku)
    #pprint("gulo"+str(td_na_radku))
    data = []
    for i in range(max_okrsek):
        link_td = td_na_radku[i].find("a")
        if link_td:
            link_in = "https://volby.cz/pls/ps2017nss/" + link_td['href']
            #print(link_in)
            #print("kokooooooooooooot"+str(i+1))
            data.append(link_in)
pprint(data)

 
     


