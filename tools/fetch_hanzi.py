#!/usr/bin/env python3
"""Kitoblardagi barcha ierogliflar uchun chiziq (stroke) ma'lumotlarini hanzi/ papkasiga yuklab oladi.

Ishga tushirish:  python3 tools/fetch_hanzi.py

Manba: hanzi-writer-data (Make Me a Hanzi loyihasidan, Arphic Public License).
Fayl nomi — ieroglifning kod nuqtasi (hex), masalan 你 -> hanzi/4f60.json.
Mavjud fayllar qayta yuklanmaydi.
"""
import glob, json, os, sys, urllib.parse, urllib.request
from concurrent.futures import ThreadPoolExecutor

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'books', 'src')
OUT = os.path.join(ROOT, 'hanzi')
CDN = 'https://cdn.jsdelivr.net/npm/hanzi-writer-data@2.0.1/'


def is_cjk(c):
    return '一' <= c <= '鿿'


chars = set()
for path in glob.glob(os.path.join(SRC, '*.tsv')):
    for line in open(path, encoding='utf-8'):
        chars.update(c for c in line.split('\t')[0] if is_cjk(c))
# gaplardagi ierogliflar ham (ismlar va h.k.) — ro'yxatda bo'lmasa ham kerak bo'lishi mumkin
for path in glob.glob(os.path.join(SRC, '*.sents.json')):
    for s in json.load(open(path, encoding='utf-8')):
        chars.update(c for c in s[1] if is_cjk(c))

os.makedirs(OUT, exist_ok=True)
todo = [c for c in sorted(chars) if not os.path.exists(os.path.join(OUT, f'{ord(c):x}.json'))]
print(f'{len(chars)} ta ieroglif, yuklanadi: {len(todo)}')


def fetch(c):
    try:
        raw = urllib.request.urlopen(CDN + urllib.parse.quote(c) + '.json', timeout=30).read()
        d = json.loads(raw)
        if not (isinstance(d.get('strokes'), list) and isinstance(d.get('medians'), list) and len(d['strokes']) == len(d['medians'])):
            return c, 'format'
        # faqat kerakli maydonlar, ixcham ko'rinishda
        slim = {'strokes': d['strokes'], 'medians': d['medians']}
        if 'radStrokes' in d:
            slim['radStrokes'] = d['radStrokes']
        with open(os.path.join(OUT, f'{ord(c):x}.json'), 'w', encoding='utf-8') as f:
            json.dump(slim, f, separators=(',', ':'))
        return c, None
    except Exception as e:  # noqa
        return c, str(e)


failed = []
with ThreadPoolExecutor(8) as ex:
    for c, err in ex.map(fetch, todo):
        if err:
            failed.append((c, err))
if failed:
    print('Yuklanmadi:', ' '.join(f'{c}({e})' for c, e in failed))
    sys.exit(1)
print('Tayyor:', len(os.listdir(OUT)), 'ta fayl')
