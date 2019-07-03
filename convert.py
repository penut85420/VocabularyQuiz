#!/usr/bin/env python3
"""
Convert tsv to json.
"""
import json
import sys
from os.path import splitext, basename, join

argc = len(sys.argv)
file_name = sys.argv[1] if argc > 1 else input('Covert source file: ').strip()
title = sys.argv[2] if argc > 2 else input('Vocabulary set title: ').strip()
output = join('./data/', basename(splitext(file_name)[0] + '.json'))

with open(file_name, 'r', encoding='UTF-8') as fin:
    data = [line.split('\t') for line in map(str.strip, fin.read().strip().split('\n'))]

new_data = dict()
new_data['title'] = title
new_data['vocabulary'] = list()

# print(data)

for eng, cht in data:
    term = {'eng': eng, 'cht': cht}
    new_data['vocabulary'].append(term)

with open(output, 'w', encoding='UTF-8') as fout:
    json.dump(new_data, fout, ensure_ascii=False, indent=2)
