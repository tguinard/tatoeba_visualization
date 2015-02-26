#!/usr/bin/python3

import json
from collections import OrderedDict


def get_iso_to_name():
    iso_to_name = {}

    for line in open('isos.txt'):
        iso, name = line.split(' ', 1)
        iso_to_name[iso] = name.strip()
    return iso_to_name

def get_lang_ids(iso_to_name):
    weights = {}
    for line in open('graph.txt'):
        a, b, c = line.split()
        if not iso_to_name.get(a) or not iso_to_name.get(b):
            continue
        weight = int(c)
        weights.setdefault(a, 0)
        weights.setdefault(b, 0)
        weights[a] += weight
        weights[b] += weight
    ordered = sorted(weights.items(), key=lambda x: -x[1])
    lang_to_id = {}
    id_to_lang = []
    next_id = 0
    for lang, _ in ordered:
        lang_to_id[lang] = next_id
        id_to_lang.append(lang)
        next_id += 1
    return lang_to_id, id_to_lang
    

def get_matrix(lang_to_id, id_to_lang, max_lang):
    n = min(len(id_to_lang), max_lang)
    matrix = [[0]*n for _ in range(n)]
    for line in open('graph.txt'):
        a,b,c = line.split()

        if (lang_to_id.get(a) is None) or (lang_to_id.get(b) is None):
            continue
        if lang_to_id[a] >= max_lang or lang_to_id[b] >= max_lang:
            continue

        weight = int(c)
        i, j = lang_to_id[a], lang_to_id[b]

        if weight > 0:
            matrix[i][j] = weight
            matrix[j][i] = weight
    return matrix

def get_name_by_index(iso_to_name, id_to_lang, max_lang):
    name_by_index = []
    for iso in id_to_lang:
        name_by_index.append(iso_to_name[iso])
    return name_by_index[:max_lang]

def dedup(l):
    return list(OrderedDict.fromkeys(l))

def get_colors(id_to_lang, max_lang):
    color_order = ['#808080', '#00ffff', '#ffc0cb', '#008000', '#ff0000', '#ffa500', '#000000', '#0000ff', '#ffff00', ]

    iso_to_family = {}
    for line in open('families.txt'):
        iso, family = line.strip().split(' ', 1)
        iso_to_family[iso] = family

    families = []
    num_family = [0]
    for lang in id_to_lang[:max_lang]:
        families.append(iso_to_family[lang])
        num_family.append(len(set(families)))

    fam_to_color = {}
    labels = []
    colorlabels = []
    for fam, color in zip(dedup(families), color_order):
        fam_to_color[fam] = color
        labels.append(fam)
        colorlabels.append(color)
    
    colors = []
    for fam in families:
        colors.append(fam_to_color[fam])
    
    return colors, labels, colorlabels, num_family

max_lang = 50

iso_to_name = get_iso_to_name()
lang_to_id, id_to_lang = get_lang_ids(iso_to_name)
matrix = get_matrix(lang_to_id, id_to_lang, max_lang)
name_by_index = get_name_by_index(iso_to_name, id_to_lang, max_lang)
colors, labels, colorlabels, num_family = get_colors(id_to_lang, max_lang)
open('matrix.json', 'w').write("var matrix = " + json.dumps(matrix) + ";\n" + 
                                "var nameByIndex = " + json.dumps(name_by_index) + ";\n"
                                "var colors = " + json.dumps(colors) + ";\n"
                                "var labels = " + json.dumps(labels) + ";\n"
                                "var colorlabels = " + json.dumps(colorlabels) + ";\n"
                                "var num_family = " + json.dumps(num_family) + ";\n"
                        )
