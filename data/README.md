# Dataset harga produsen padi

Data diterbitkan oleh **Food and Agriculture Organization of the United Nations (FAO)** dalam koleksi **FAOSTAT Producer Prices**.

- [Portal koleksi](https://www.fao.org/faostat/en/#data/PP)
- [Metadata koleksi](https://www.fao.org/faostat/en/#data/PP/metadata)
- [Penjelasan harga produsen](https://www.fao.org/prices/en)
- [Ketentuan penggunaan basis data FAO](https://www.fao.org/contact-us/terms/db-terms-of-use/en)

## Berkas yang digunakan

`raw/faostat_rice_producer_prices.csv` adalah salinan utuh berkas pengguna yang bernama `Agricultural producer prices (Global, National - Annual, Monthly) - FAOSTAT.csv`. Hanya nama berkas yang dipersingkat. Isinya tidak diubah.

Menurut catatan proyek, snapshot diperoleh pada 15 Oktober 2026. Pemeriksaan ulang dilakukan pada 26 Oktober 2026. Metadata koleksi yang tersimpan mencatat pembaruan pada 9 Oktober 2026. Bulan pada CSV adalah bulan referensi, bukan tanggal publikasi.

| Keterangan | Nilai |
|---|---|
| Ukuran berkas | 382.442 byte |
| Baris dan kolom | 5.341 baris, 17 kolom |
| Cakupan berkas ekspor | 73 negara, Januari 2010–Januari 2025 |
| Frekuensi dan komoditas | Monthly, Rice, kode 27 |

Cakupan tersebut hanya menjelaskan berkas ekspor yang digunakan, bukan keseluruhan basis data FAOSTAT.

SHA-256 berkas:

```text
5f6470bc3e1284340aaa1022f032bdb8fb49c9aaf059054b41d19e3790636b76
```

Notebook memeriksa ukuran dan checksum sebelum memproses data. Pemeriksaan manual dari akar repo juga dapat dilakukan melalui PowerShell:

```powershell
Get-FileHash -Algorithm SHA256 -LiteralPath 'data/raw/faostat_rice_producer_prices.csv'
```

## Seleksi penelitian

`Projek.ipynb` membaca CSV asli, memeriksa komoditas `Rice` dengan kode 27 dan frekuensi `Monthly`, lalu memilih tahun **2022–2024**, harga `Producer Price (LCU/tonne)` dengan flag `A`, dan kode M49 Asia berikut:

`050, 064, 096, 144, 156, 360, 392, 398, 410, 417, 586, 608, 704, 764, 792, 860`.

Seleksi tersebut menghasilkan **511 observasi asli dari 16 negara**. Kode wilayah mengikuti [M49 PBB](https://unstats.un.org/unsd/methodology/m49/). Rusia tidak dimasukkan karena berada dalam kelompok statistik Eropa. Negara Asia lain yang tidak memiliki observasi dalam rentang terpilih tidak disertakan.

Kalender penelitian memiliki **576 kombinasi negara-bulan**, termasuk **65 bulan yang tidak tercatat**. Gap tetap kosong. Notebook tidak mengisi harga dengan nol, interpolasi, atau data sintetis.

## Skema ringkas

Kamus seluruh 17 kolom, tipe data, satuan, dan kegunaannya ditampilkan pada bagian **10.2** notebook. Ringkasannya sebagai berikut:

| Kolom | Arti dan penggunaan |
|---|---|
| `faostat` | ID wilayah internal FAOSTAT, bukan fitur numerik harga. |
| `M49 Code`, `Country` | Kode M49 dan nama negara. Kode dipertahankan sebagai teks tiga digit. |
| `Item Code`, `Item` | Identitas komoditas. Ekspor ini menggunakan 27/Rice. |
| `year`, `Months`, `date` | Tahun, nama bulan, dan tanggal representatif awal bulan. |
| `Producer Price (LCU/tonne)` | Harga nominal produsen dalam mata uang lokal per ton. |
| `Producer Price (LCU/tonne) flag` | Status nilai. `A` berarti angka resmi menurut penerbit. |
| Harga `SLC/tonne` dan flag | Ukuran mata uang lokal standar dan statusnya, seluruhnya kosong pada ekspor ini. |
| Harga `USD/tonne` dan flag | Harga dolar AS per ton dan statusnya, seluruhnya kosong pada ekspor ini. |
| Indeks harga produsen dan flag | Indeks dengan dasar 2014–2016 = 100 dan statusnya, seluruhnya kosong pada ekspor ini. |
| `Frequency` | Frekuensi observasi. Seluruh baris berfrekuensi bulanan. |

Enam kolom kosong merupakan tiga ukuran alternatif beserta flag-nya. Kekosongan tersebut berbeda dari gap pada kalender. Level harga LCU tidak digabung untuk membandingkan harga antarnegara karena mata uangnya berbeda.

## Atribusi dan lisensi

FAO. 2026. *FAOSTAT: Producer Prices*. Diakses 15 Oktober 2026. https://www.fao.org/faostat/en/#data/PP. Licence: CC BY 4.0, dengan ketentuan tambahan basis data FAO. Seleksi cakupan dan analisis turunan dijelaskan dalam notebook proyek.

Dataset disertakan untuk penelitian dengan atribusi kepada FAO. Lisensi MIT pada akar repo berlaku untuk kode proyek dan tidak menggantikan lisensi data. Tidak ada klaim bahwa FAO berpartisipasi, menyetujui, mendanai, atau memvalidasi proyek ini.
