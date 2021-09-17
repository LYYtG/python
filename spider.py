#all weapons in Dark Souls
import requests
from bs4 import BeautifulSoup
import lxml
def no_class(tag):
    return not tag.has_attr('class')
i = 0;
wiki = 'https://darksouls.fandom.com';
ds = requests.get(wiki)
dsobj = BeautifulSoup(ds.content,'lxml')
weapon= dsobj.find_all('table', id = 'portal_content_3')
weapon_type = weapon[0].find_all('a')
for w in weapon_type:
    if(w['href'] == '/wiki/Weapon_Modification'):
        break;
    w_type = wiki+w['href']
    w_req = requests.get(w_type)
    #print(w_req)
    w_obj = BeautifulSoup(w_req.content,'lxml')
    w_s_type = w_obj.find_all('td',attrs = {"rowspan":"2"})
    for w1 in w_s_type:
        w1_1 = w1.find_all('a')
        for w2 in w1_1:
            if(w2!=None and w2.string != None and no_class(w2) and w2.string != 'AotA' and not 'damage' in w2['title']):
                print(w2.string)
        
print('done.')