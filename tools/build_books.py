#!/usr/bin/env python3
"""books/src/* manbalaridan books/*.js fayllarini yasaydi.

Ishga tushirish:  python3 tools/build_books.py

Manba fayllar (har bir kitob uchun <id>.*):
  <id>.lessons.json  [[dars sarlavhasi (xitoycha), o'zbekcha tarjimasi], ...]
  <id>.words.tsv     ieroglif \t pinyin \t o'zbekcha \t dars \t ★(0/1) \t [qaysi darslarda, masalan "10, 13"]
  <id>.extra.tsv     (ixtiyoriy) qo'shimcha so'zlar: ieroglif \t pinyin \t o'zbekcha \t dars — ★ bilan belgilanadi
  <id>.sents.json    [[dars, "so'zlar bo'sh joy bilan", "pinyin (har so'zga bittadan, _ = so'z ichidagi bo'shliq)", "o'zbekcha", [boshqa to'g'ri tartiblar]], ...]
"""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'books', 'src')
OUT = os.path.join(ROOT, 'books')
PUN = set('，。！？、：；,.!?')

BOOKS = [
    dict(id='xin1', title='新HSK教程 1', short='HSK 1', store='hsk1book', cloud='p', keyPy=False,
         star="kitobdagi, lekin HSK 1 imtihonidan tashqari so'z", starShort="darajadan tashqari so'z"),
    dict(id='xin2', title='新HSK教程 2', short='HSK 2', store='hsk_xin2', cloud='p_xin2', keyPy=True,
         star="kitobdagi, lekin HSK 2 darajasidan tashqari so'z", starShort="darajadan tashqari so'z"),
    dict(id='s360_1', title='标准汉语会话360句 1', short='360句 1', store='hsk_s360_1', cloud='p_s360_1', keyPy=True,
         star="qo'shimcha so'z (词语扩展 — lug'at kengaytmasi)", starShort="qo'shimcha so'z"),
]


def read_tsv(path):
    rows = []
    if not os.path.exists(path):
        return rows
    for n, line in enumerate(open(path, encoding='utf-8'), 1):
        line = line.rstrip('\n')
        if not line.strip():
            continue
        cols = line.split('\t')
        if len(cols) < 4:
            sys.exit(f'{path}:{n}: kamida 4 ustun kerak: {line!r}')
        rows.append(cols)
    return rows


def build(b):
    bid = b['id']
    lessons = json.load(open(os.path.join(SRC, bid + '.lessons.json'), encoding='utf-8'))
    nl = len(lessons)
    words, seen = [], set()
    for cols in read_tsv(os.path.join(SRC, bid + '.words.tsv')):
        hz, py, uz, l = cols[0], cols[1], cols[2], int(cols[3])
        star = int(cols[4]) if len(cols) > 4 and cols[4] else 0
        ls = cols[5] if len(cols) > 5 and cols[5] else str(l)
        key = hz + '|' + py if b['keyPy'] else hz
        if key in seen:
            sys.exit(f'{bid}: takroriy so\'z {key}')
        seen.add(key)
        words.append([hz, py, uz, l, star, ls])
    main_hz = {w[0] for w in words}
    for cols in read_tsv(os.path.join(SRC, bid + '.extra.tsv')):
        hz, py, uz, l = cols[0], cols[1], cols[2], int(cols[3])
        if hz in main_hz:
            continue  # asosiy ro'yxatda bor — takrorlamaymiz
        main_hz.add(hz)
        words.append([hz, py, uz, l, 1, str(l)])
    for w in words:
        if not 1 <= w[3] <= nl:
            sys.exit(f'{bid}: {w[0]} — dars raqami noto\'g\'ri: {w[3]}')
    words.sort(key=lambda w: w[3])  # barqaror: dars ichida tartib saqlanadi

    sents = []
    path = os.path.join(SRC, bid + '.sents.json')
    if os.path.exists(path):
        for s in json.load(open(path, encoding='utf-8')):
            l, zh, py, uz = s[0], s[1], s[2], s[3]
            zt, pt = zh.split(' '), py.split(' ')
            if len(zt) != len(pt):
                sys.exit(f'{bid}: gap va pinyin soni mos emas ({len(zt)} ≠ {len(pt)}): {zh} | {py}')
            for a, p in zip(zt, pt):
                if (a in PUN) != (p in PUN):
                    sys.exit(f'{bid}: tinish belgisi mos emas: {a} / {p} — {zh}')
            if not 1 <= l <= nl:
                sys.exit(f'{bid}: gap dars raqami noto\'g\'ri: {zh}')
            sents.append(s)

    data = dict(b, lessons=lessons, words=words, sents=sents)
    js = ('// Avtomatik yasalgan: python3 tools/build_books.py — books/src/ dagi fayllarni tahrirlang.\n'
          '(window.BOOKS=window.BOOKS||[]).push(' + json.dumps(data, ensure_ascii=False, separators=(',', ':')) + ');\n')
    open(os.path.join(OUT, bid + '.js'), 'w', encoding='utf-8').write(js)
    stars = sum(1 for w in words if w[4])
    print(f'{bid}: {nl} dars, {len(words)} so\'z (★ {stars}), {len(sents)} gap')


for b in BOOKS:
    build(b)
