#!/usr/bin/python3

from bs4 import BeautifulSoup
from urllib import request


url = 'http://tatoeba.org/eng/stats/sentences_by_language'
bs = BeautifulSoup(request.urlopen(url).read())
table = bs.find_all('table', {'id': 'sentencesStats'})[0]

outfile = open('isos.txt', 'w')
for row in table.find_all('tr'):
    fields = row.find_all('td')
    iso = fields[2].get_text().strip()
    name = fields[3].get_text().strip()
    if name != 'unknown':
        outfile.write('%s %s\n' % (iso, name))
outfile.close()
