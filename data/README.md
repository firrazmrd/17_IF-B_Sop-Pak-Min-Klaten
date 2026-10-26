# Sumber dataset

Penerbit: **Food and Agriculture Organization of the United Nations (FAO)**.
Koleksi: **FAOSTAT Producer Prices**.

- [Portal koleksi](https://www.fao.org/faostat/en/#data/PP)
- [Metadata koleksi](https://www.fao.org/faostat/en/#data/PP/metadata)
- [Definisi harga produsen](https://www.fao.org/prices/en)
- [Ketentuan penggunaan basis data FAO](https://www.fao.org/contact-us/terms/db-terms-of-use/en)

## Snapshot yang dipertahankan

File asli pengguna: `Agricultural producer prices (Global, National - Annual, Monthly) - FAOSTAT.csv`.
Salinan dalam repo: `raw/faostat_rice_producer_prices.csv`, **byte sama dengan berkas asli**.

Snapshot diperoleh 15 Oktober 2026 (catatan konteks proyek); diverifikasi ulang 26 Oktober 2026. Metadata koleksi yang tersimpan mencatat pembaruan 9 Oktober 2026. Kolom tanggal pada CSV adalah bulan referensi, bukan tanggal publikasi.

Ukuran: **382.442 byte**, **5.341 baris**, **17 kolom**, **73 negara**, Januari 2010–Januari 2025. Ini cakupan berkas ekspor pengguna, bukan keseluruhan basis data FAOSTAT.

SHA-256:

```text
5f6470bc3e1284340aaa1022f032bdb8fb49c9aaf059054b41d19e3790636b76
```

Verifikasi pada PowerShell:

```powershell
Get-FileHash -Algorithm SHA256 -LiteralPath 'data/raw/faostat_rice_producer_prices.csv'
```

## Seleksi penelitian yang direncanakan

Gunakan `Item=Rice`, `Item Code=27`, `Frequency=Monthly`, kolom `Producer Price (LCU/tonne)`, flag harga `A`, tahun **2022–2024**, serta kode M49 Asia berikut:

`050, 064, 096, 144, 156, 360, 392, 398, 410, 417, 586, 608, 704, 764, 792, 860`.

Daftar tersebut menghasilkan 16 negara dengan observasi pada periode penelitian. Rusia tidak dimasukkan karena klasifikasi regional M49 menempatkannya di Eropa. Negara Asia lain pada berkas mentah tidak memiliki observasi pada rentang yang dipilih. Notebook Progress 1 belum menjalankan seleksi ini.

## Skema ringkas

| Kolom | Arti |
|---|---|
| `faostat` | Kode wilayah internal FAOSTAT; ID, bukan fitur numerik harga. |
| `M49 Code`, `Country` | Kode M49 dan nama negara. Pertahankan kode sebagai string tiga digit. |
| `Item Code`, `Item` | Kode dan nama komoditas; ekspor ini menggunakan 27/Rice. |
| `year`, `Months`, `date` | Tahun, nama bulan, dan tanggal representatif awal bulan. |
| `Producer Price (LCU/tonne)` | Harga nominal produsen dalam mata uang lokal per ton. |
| `Producer Price (LCU/tonne) flag` | Status nilai; `A` berarti angka resmi menurut penerbit. |
| `Producer Price (SLC/tonne)` dan flag | Harga dalam satuan mata uang lokal standar dan statusnya; seluruh nilai kosong pada ekspor ini. |
| `Producer Price (USD/tonne)` dan flag | Harga dolar AS per ton dan statusnya; seluruh nilai kosong pada ekspor ini. |
| `Producer Price Index (2014–2016 = 100)` dan flag | Indeks harga produsen dan statusnya; seluruh nilai kosong pada ekspor ini. |
| `Frequency` | Frekuensi; seluruh baris ekspor ini bulanan. |

Enam kolom kosong merupakan tiga ukuran alternatif beserta flag-nya. Kekosongan tersebut tidak sama dengan harga LCU yang hilang. Jangan membandingkan level LCU antarnegara atau mengisi bulan yang tidak tercatat dengan harga nol.

## Atribusi dan lisensi data

FAO. 2026. *FAOSTAT: Producer Prices*. Snapshot diakses 15 Oktober 2026. https://www.fao.org/faostat/en/#data/PP. Licence: CC BY 4.0, dengan ketentuan penggunaan basis data FAO. Seleksi cakupan dan analisis turunan merupakan pekerjaan penyusun proyek.

Redistribusi untuk penelitian disertai atribusi, penjelasan perubahan, dan ketentuan tambahan FAO. Tidak ada klaim bahwa FAO menjadi sponsor, menyetujui, atau memvalidasi proyek. Lisensi MIT pada akar repository tidak diterapkan ulang terhadap dataset ini.
