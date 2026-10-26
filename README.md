# Klasifikasi Kenaikan Harga Produsen Padi Bulan Berikutnya di 16 Negara Asia Periode 2022–2024

Kelompok **17 — Sop Pak Min Klaten**, kelas **IF-B**, Praktikum Data Science 2026/2027, UPN “Veteran” Yogyakarta.

## Ringkasan dan status

Proyek ini mengkaji apakah riwayat harga dapat membantu mengenali kenaikan harga nominal produsen padi satu bulan ke depan. Metode yang dipilih adalah **klasifikasi biner**: kelas 1 berarti naik, sedangkan kelas 0 berarti turun atau tetap. Data berasal dari FAOSTAT Producer Prices.

`Projek.ipynb` memuat **Business Understanding**, kemudian **Data Understanding**. Bagian data berisi pembacaan CSV, kamus data, audit kualitas dan cakupan, EDA, serta audit awal fitur, target, dan pembagian waktu. Tabel dan empat grafik Matplotlib/Seaborn sudah tersimpan dalam notebook. Kode disusun bertahap dengan penamaan DataFrame, `display()`, `plt.figure()`, dan `plt.show()` seperti notebook pertemuan. Pelatihan model dan evaluasi kinerjanya akan dikerjakan pada tahap berikutnya.

## Model yang dipilih

Model utama dalam rancangan adalah **Regresi Logistik dengan regularisasi L2**, menggunakan optimisasi **L-BFGS**. Pilihan ini mempertimbangkan 120 contoh latih, sedikit fitur, dan korelasi antarfitur harga. **Random Forest** menjadi pembanding untuk menguji pola nonlinier dan interaksi fitur.

Pemilihan akhir akan didasarkan pada macro-F1 validasi dan dibandingkan dengan baseline mayoritas serta persistensi arah. Data uji digunakan setelah model dikunci. Belum ada klaim bahwa salah satu model sudah memberikan kinerja terbaik karena tahap pelatihan belum dikerjakan.

## Anggota dan kontribusi

| Nama | NIM | Kelas | Kontribusi bersama |
|---|---|---|---|
| Ghazian Muhammad Al Faruq | 123240013 | IF-B | Perumusan masalah, penelusuran sumber, audit data, EDA, dan penulisan penjelasan. |
| M. Affan Musyafa' | 123240155 | IF-B | Perumusan masalah, penelusuran sumber, audit data, EDA, dan penulisan penjelasan. |
| Firraz Muhammad Raihan Daffa | 123240170 | IF-B | Perumusan masalah, penelusuran sumber, audit data, EDA, dan penulisan penjelasan. |
| Jauza Ilham Mahardhika Putra | 123240174 | IF-B | Perumusan masalah, penelusuran sumber, audit data, EDA, dan penulisan penjelasan. |

Seluruh anggota mengerjakan tahap ini bersama dengan kontribusi setara.

## Isi repo

```text
17_IF-B_Sop-Pak-Min-Klaten/
├── Projek.ipynb
├── README.md
├── requirements.txt
├── .python-version
├── .gitignore
├── LICENSE
└── data/
    ├── README.md
    └── raw/
        └── faostat_rice_producer_prices.csv
```

Notebook yang sama digunakan untuk melanjutkan seluruh tahapan proyek. Dataset asli disimpan satu kali. Seluruh hasil audit dan grafik ditampilkan di notebook, sehingga proses tidak membuat file hasil tambahan di repo.

## Cara menjalankan

Gunakan **Python 3.13.12**. Versi ini juga dicatat dalam `.python-version` dan diperiksa oleh sel kode pertama. Pustaka yang digunakan adalah pandas 2.3.3, NumPy 2.3.5, IPython 9.10.0, dan ipykernel 7.2.0.

1. Buka terminal pada folder `17_IF-B_Sop-Pak-Min-Klaten`. Pastikan `python --version` menampilkan `Python 3.13.12`. Jika berbeda, pilih interpreter 3.13.12 terlebih dahulu.
2. Buat lingkungan virtual dan pasang pustaka berikut melalui PowerShell.

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\python.exe -m pip install -r requirements.txt
   ```

3. Buka `Projek.ipynb` di VS Code dengan ekstensi Jupyter atau melalui JupyterLab yang sudah terpasang. Pilih kernel dari `.venv` dengan Python 3.13.12.
4. Gunakan **Restart Kernel and Run All** agar seluruh sel dijalankan dari awal. Biarkan CSV pada lokasi yang tercantum di struktur repo. Kode tidak memerlukan akses internet saat dijalankan.
5. Periksa keluaran sel terakhir. Jika semua pemeriksaan lolos, alur data akan menampilkan `511 → 576 → 436 → 410`.

GitHub dapat digunakan untuk membaca penjelasan, tabel, dan grafik yang tersimpan tanpa menjalankan ulang notebook. Penjelasan sumber dan checksum tersedia di [data/README.md](data/README.md).

## Isi notebook dan hasil audit

| Bagian | Isi |
|---|---|
| Business Understanding, bagian 1–9 | Masalah, stakeholder, tujuan SMART, metode, metrik, asumsi, risiko, nilai penggunaan, dan pemetaan data. |
| Data Understanding 10.1–10.2 | Sumber dan lisensi, pemeriksaan snapshot, kamus seluruh kolom, serta seleksi negara dan periode. |
| Data Understanding 10.3–10.4 | Missing value, duplikasi, harga tidak positif, kalender bulanan, dan keterwakilan negara. |
| Data Understanding 10.5 | Distribusi perubahan harga dan penandaan nilai ekstrem pada jendela latih. |
| Data Understanding 10.6 | Audit fitur dan target, pembagian waktu, korelasi fitur, dan komposisi kelas. |
| Data Understanding 10.7 | Kesimpulan, keterbatasan, tindak lanjut, dan pemeriksaan hasil. |

Hasil yang diperoleh dari snapshot yang disertakan:

- Berkas asli memuat **5.341 baris, 17 kolom, dan 73 negara**. Seleksi 16 negara Asia pada 2022–2024 menghasilkan **511 observasi harga resmi**.
- Kalender penelitian memiliki **576 kombinasi negara-bulan**, termasuk **65 bulan yang tidak tercatat**. Penambahan kalender hanya menandai kekosongan dan tidak membuat harga baru.
- Audit fitur dan target menghasilkan **436 contoh lengkap**. Setelah 26 contoh pada batas waktu dikeluarkan, tersedia **120 latih, 145 validasi, dan 145 uji**.
- EDA jendela latih memakai **165 return bulanan**, dengan **9 nilai** ditandai oleh pagar IQR per negara. Nilai tersebut dipertahankan karena penandaan belum membuktikan adanya kesalahan data.

Harga LCU antarnegara tidak dibandingkan langsung. Eksplorasi yang dapat memengaruhi pemilihan fitur dibatasi pada data latih. Kelima fitur berasal dari harga dan kalender, sehingga bukan lima variabel sumber yang independen. Cakupan, tanggal publikasi yang tidak tersedia, dan seri yang pendek tetap membatasi penggunaan hasil.

## Laporan dan sumber data

Lampiran C pada [laporan proyek](https://docs.google.com/document/d/1kpoLL2OyEa3MtBHeF0fC8zz1tMHVTMoClQNWpYQM3xY/edit?tab=t.aigts47j05it) menjelaskan repo, isi notebook, dan cara mengulang audit.

FAO. 2026. *FAOSTAT: Producer Prices*. Snapshot diakses 15 Oktober 2026 dan diverifikasi ulang 26 Oktober 2026. [Portal koleksi](https://www.fao.org/faostat/en/#data/PP).

`LICENSE` mempertahankan lisensi MIT untuk kode proyek. Dataset menggunakan CC BY 4.0 dengan [ketentuan tambahan basis data FAO](https://www.fao.org/contact-us/terms/db-terms-of-use/en). Atribusi lengkap dan batas penggunaan data tercantum dalam `data/README.md`. Tidak ada klaim dukungan atau validasi dari FAO.
