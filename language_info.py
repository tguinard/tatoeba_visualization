#!/usr/bin/python3

from bs4 import BeautifulSoup
from urllib import request

family_rownames = {"Linguistic classification:", "Language family", "Purpose"} 

def get_info(iso):
    values = {}

    url = 'http://en.wikipedia.org/wiki/ISO_639:%s' % iso
    bs = BeautifulSoup(request.urlopen(url).read())
    
    infobox = bs.find_all('table', {'class': 'infobox'})[0]
    name = infobox.find_all('th')[0].get_text()
    family = ""
    for tr in infobox.find_all('tr'):
        try:
            rowname = tr.find_all('th')[0].get_text().strip()
        except:
            continue
        if rowname in family_rownames:
            family = tr.find_all('td')[0].find_all('a')[0].get_text()
            break
    return family

def unaliased(family):
    aliases = {
        'constructed languages': 'Constructed Language',
        'International auxiliary language': 'Constructed Language',
        'constructed language': 'Constructed Language',
    }
    return aliases.get(family) or family

isos = {
    'toki': 'Constructed Language',
    'avk': 'Constructed Language',
    'cycl': 'Constructed Language',
    'ben': 'Indo-European',
}
for line in open('isos.txt'):
    iso = line.split()[0]
    if iso.lower() not in isos:
        isos[iso] = unaliased(get_info(iso))

out = open('families.txt', 'w')
for iso, info in isos.items():
    out.write('%s %s\n' % (iso, info))
out.close()
