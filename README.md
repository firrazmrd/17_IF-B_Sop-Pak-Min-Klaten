# Klasifikasi Kenaikan Harga Produsen Padi Bulan Berikutnya di 16 Negara Asia Periode 2022–2024

Kelompok **17 — Sop Pak Min Klaten**, **IF-B**, Praktikum Data Science 2026/2027, UPN “Veteran” Yogyakarta.

## Status dan ruang lingkup

**Progress 1: Business Understanding**, mengikuti sembilan butir capaian presentasi yang diberikan. Metode: **klasifikasi biner**, 1 = naik dan 0 = tidak naik (turun atau tetap) pada bulan berikutnya.

Notebook saat ini hanya memuat Business Understanding. Pengumpulan data dalam notebook, EDA, cleaning, preprocessing, Modeling, Evaluation dan Conclusion merupakan tahap lanjutan. Panduan menyebut pengumpulan 30 Oktober 2026 sudah mencakup pengumpulan data sampai preprocessing. Versi Progress 1 ini belum mencakup seluruh tahapan pada tenggat tersebut.

## Anggota dan kontribusi

| Nama | NIM | Kelas | Kontribusi awal (bersama) |
|---|---|---|---|
| Ghazian Muhammad Al Faruq | 123240013 | IF-B | Perumusan masalah, stakeholder, tujuan, metrik, asumsi, risiko, dan pemetaan data. |
| M. Affan Musyafa' | 123240155 | IF-B | Perumusan masalah, stakeholder, tujuan, metrik, asumsi, risiko, dan pemetaan data. |
| Firraz Muhammad Raihan Daffa | 123240170 | IF-B | Perumusan masalah, stakeholder, tujuan, metrik, asumsi, risiko, dan pemetaan data. |
| Jauza Ilham Mahardhika Putra | 123240174 | IF-B | Perumusan masalah, stakeholder, tujuan, metrik, asumsi, risiko, dan pemetaan data. |

Menurut keterangan kelompok, tahap awal Business Understanding dikerjakan bersama oleh seluruh anggota dengan kontribusi setara. Kolom kontribusi mencatat cakupan pekerjaan yang dilakukan bersama. Catatan kontribusi diperbarui saat tahap berikutnya dikerjakan.

## Isi repository

```text
.
├── README.md
├── Projek.ipynb
├── data/
│   ├── README.md
│   └── raw/faostat_rice_producer_prices.csv
├── .gitignore
└── LICENSE
```

CSV dipertahankan utuh dan hanya nama berkas yang dipersingkat. Isi repository saat ini mendukung tahap Business Understanding dan akan dikembangkan mengikuti capaian berikutnya.

## Cara membuka

1. Buka `Projek.ipynb` melalui JupyterLab, Jupyter Notebook, atau VS Code dengan dukungan notebook.
2. Baca sel Markdown secara berurutan. Tidak ada sel kode atau instalasi pustaka analisis yang diperlukan pada tahap ini. GitHub juga dapat menampilkan isi notebook.
3. Periksa sumber, batas cakupan dan checksum CSV pada `data/README.md`.

## Pemetaan capaian Progress 1

| No. | Capaian | Lokasi di notebook |
|---:|---|---|
| 1 | Judul spesifik dan ruang lingkup tepat | Bagian 1 |
| 2 | Judul selaras dengan tujuan dan metrik | Bagian 1, 3–5 |
| 3 | Pernyataan masalah dan stakeholder | Bagian 2 |
| 4 | Tujuan SMART | Bagian 3 |
| 5 | Metrik keberhasilan | Bagian 5 |
| 6 | Asumsi dan batasan | Bagian 6 |
| 7 | Risiko dan etika beserta mitigasi | Bagian 7 |
| 8 | Nilai bisnis dan use-case | Bagian 8 |
| 9 | Pemetaan stakeholder–data | Bagian 9 |

## Sumber dan lisensi

[FAOSTAT Producer Prices](https://www.fao.org/faostat/en/#data/PP), Food and Agriculture Organization of the United Nations. Snapshot lokal diperoleh 15 Oktober 2026 dan diverifikasi 26 Oktober 2026. Atribusi, skema ringkas, filter penelitian dan checksum ada pada `data/README.md`.

`LICENSE` mempertahankan lisensi MIT proyek asli. Lisensi tersebut tidak menggantikan lisensi dataset FAO, yaitu CC BY 4.0 dengan [ketentuan tambahan basis data FAO](https://www.fao.org/contact-us/terms/db-terms-of-use/en). FAO tidak memberikan endorsement terhadap proyek ini.
