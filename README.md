# HSK — takrorlash

Xitoy tili kitoblari bo'yicha flashcard ilovasi (Telegram Mini App sifatida ham ishlaydi).

## Kitoblar

| Kitob | Darslar | So'zlar |
|---|---|---|
| 新HSK教程 1 | 15 | 315 |
| 新HSK教程 2 | 15 | 210 |
| 标准汉语会话360句 1 | 8 | 311 (★ 169 — lug'at kengaytmasi) |

## Bo'limlar

- **Kartalar** — so'zlar: 汉 → o'zbekcha yoki o'zbekcha → 汉.
- **Ro'yxat** — kitobning barcha so'zlari va ularning ballari, qidiruv va filtr.
- **Sozlamalar** — filtrlar va sozlash: qaysi so'zlar chiqsin (yangi / qiyin / o'rganilmoqda / o'rganilgan), bir nechta darsni birga
  o'rganish, yangi so'zlar chegarasi, chiqish tartibi, ★ so'zlar, so'z uzunligi, avtomatik talaffuz, o'rganilgan chegarasi, "Bilmayman" bali.

## Ball tizimi

- **Bilaman** → +1 ball, **Bilmayman** → −2 ball, Sozlamalarda −1/−3 ham bor (chegarasi: −5 … +10).
- Keyingi karta tasodifiy tanlanadi, lekin balli yuqori so'z kamroq chiqadi: har +2 ball so'zni 2 baravar kamroq chiqaradi
  (−4 ball → 4×, 0 → 1×, +5 → ~⅙, +10 → ~1/32). Ketma-ket 3 ta kartada bitta so'z takrorlanmaydi.
- **5+ ball** (Sozlamalarda o'zgaradi) — so'z "o'rganilgan". Dars tanlovida va karta tepasida darsning bilish darajasi (%) ko'rsatiladi.
- "Qiyin so'zlar" — balli manfiy bo'lgan so'zlar.
- Ballar har bir kitob uchun alohida saqlanadi (brauzerda va Telegram CloudStorage'da).
- Qolgan qiymatlarni `index.html` dagi `PT` obyektida o'zgartirish mumkin.

## Yangi kitob yoki so'z qo'shish

Ma'lumotlar `books/src/` papkasida:

- `<id>.lessons.json` — darslar sarlavhasi va tarjimasi;
- `<id>.words.tsv` — `ieroglif ⇥ pinyin ⇥ o'zbekcha ⇥ dars ⇥ ★(0/1) ⇥ [darslar]`;
- `<id>.extra.tsv` — (ixtiyoriy) qo'shimcha so'zlar, ★ bilan;
- mavjud kitobga so'z qo'shsangiz, uni `build_books.py` dagi `added` ro'yxatiga ham yozing — Telegram'dagi eski ballar saqlanishi uchun;
- `<id>.sents.json` — gaplar (hozircha ilovada ishlatilmaydi).

O'zgartirgandan keyin:

```bash
python3 tools/build_books.py
```

Yangi kitob uchun `tools/build_books.py` dagi `BOOKS` ro'yxatiga yozuv qo'shing va `index.html` ga `<script src="books/<id>.js">` qatorini qo'shing.

Gap tuzish va ieroglif yozish mashqlari vaqtincha olib tashlangan; ular `74f24a2` commitida saqlangan.
