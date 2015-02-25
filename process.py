#!/usr/bin/python3

from collections import Counter
from bs4 import BeautifulSoup
from urllib import request


id_to_lan = {}
for line in open('sentences.csv'):
    fields = line.split()
    id = int(fields[0])
    language = fields[1]
    id_to_lan[id] = language

graph = Counter()
for line in open('links.csv'):
    x,y = map(int, line.split())
    if x < y:
        lan1 = id_to_lan.get(x)
        lan2 = id_to_lan.get(y)
        if lan1 is not None and lan2 is not None:
            graph[tuple(sorted([lan1, lan2]))] += 1

outfile = open('graph.txt', 'w')
for langs, count in graph.most_common():
    outfile.write('%s %s %s\n' % (langs[0], langs[1], count))
outfile.close()
