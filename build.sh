#!/bin/sh
if [ ! -f sentences.csv ]; then
    wget http://downloads.tatoeba.org/exports/sentences.tar.bz2
    tar -xjf sentences.tar.bz2
fi
if [ ! -f links.csv ]; then
    wget http://downloads.tatoeba.org/exports/links.tar.bz2
    tar -xjf links.tar.bz2
fi
if [ ! -f graph.txt ]; then
    ./process.py
fi
if [ ! -f isos.txt ]; then
    ./iso_to_language.py
fi
if [ ! -f families.txt ]; then
    ./language_info.py
fi
if [ ! -f matrix.json ]; then
    ./make_matrix.py
fi
