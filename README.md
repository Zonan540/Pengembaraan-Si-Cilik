# Pengembaraan Si Cilik!

Permainan pembelajaran dalam pelayar untuk kanak-kanak umur 6–8 tahun (Matematik, Sains, English). **100% percuma.** Dibina sebagai PWA, boleh dipasang di skrin utama telefon/tablet dan berfungsi tanpa internet.

## Struktur repo

| Folder | Isi |
|---|---|
| `site/` | Fail untuk deploy (index.html, manifest, service worker, ikon, `_headers`). Terus deploy folder ini ke Netlify. |
| `docs/` | Lembaran semakan soalan fasa 2–4, dan `BACA-SAYA.txt` (cara deploy & guna). |
| `tests/` | Skrip ujian Playwright (auto-play, invariant soalan, responsif, mod ibu bapa). |

## Deploy ke Netlify

Set **Publish directory** = `site` (tiada build command). Setiap kali kemas kini, naikkan `CACHE_VERSION` dalam `site/sw.js`.

## Ujian (pilihan)

```
pip install playwright && python3 tests/zones8.py
```

Versi semasa: 5.0. Mod ibu bapa: butang di menu (soalan matematik sebagai pintu).
