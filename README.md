# HSK — takrorlash

Xitoy tili kitoblari bo'yicha flashcard va gap mashqlari ilovasi (Telegram Mini App sifatida ham ishlaydi).

## Kitoblar

| Kitob | Darslar | So'zlar | Gaplar |
|---|---|---|---|
| 新HSK教程 1 | 15 | 315 | 144 |
| 新HSK教程 2 | 15 | 210 | 157 |
| 标准汉语会话360句 1 | 8 | 309 (★ 169 — lug'at kengaytmasi) | 80 (kitobdagi standart gaplar) |

## Bo'limlar

- **Kartalar** — so'zlar: 汉 → o'zbekcha yoki o'zbekcha → 汉, "Qiyin so'zlar" to'plami.
- **Gaplar** — gap tarjimasi mashqi:
  - *O'zbekcha → 汉语*: so'z kartochkalaridan xitoycha gapni tuzasiz (ortiqcha so'zlar ham bor);
  - *汉语 → o'zbekcha*: gapni o'qib, tarjimasini eslaysiz;
  - *🎧 Tinglab tuzish*: gapni eshitib, kartochkalardan tuzasiz.
- **Ro'yxat** — kitobning barcha so'zlari, qidiruv va holat bo'yicha filtr.

Natijalar har bir kitob uchun alohida saqlanadi (brauzerda va Telegram CloudStorage'da).

## Yangi kitob yoki so'z qo'shish

Ma'lumotlar `books/src/` papkasida:

- `<id>.lessons.json` — darslar sarlavhasi va tarjimasi;
- `<id>.words.tsv` — `ieroglif ⇥ pinyin ⇥ o'zbekcha ⇥ dars ⇥ ★(0/1) ⇥ [darslar]`;
- `<id>.extra.tsv` — (ixtiyoriy) qo'shimcha so'zlar, ★ bilan;
- `<id>.sents.json` — `[dars, "so'zlar bo'sh joy bilan", "pinyin har so'zga", "o'zbekcha", [boshqa to'g'ri tartiblar]]`.

O'zgartirgandan keyin:

```bash
python3 tools/build_books.py
```

Yangi kitob uchun `tools/build_books.py` dagi `BOOKS` ro'yxatiga yozuv qo'shing va `index.html` ga `<script src="books/<id>.js">` qatorini qo'shing.

360句 kitobidagi gaplar — kitobning o'z "标准句" ro'yxatidan; 新HSK教程 1 va 2 uchun gaplar har bir darsning so'zlari va grammatikasi asosida tuzilgan.
