# Klasifikasi Kenaikan Harga Produsen Padi Bulan Berikutnya di 16 Negara Asia Periode 2022–2024

Kelompok **17 (Sop Pak Min Klaten)**, kelas **IF-B**, Data Science 2026/2027, UPN “Veteran” Yogyakarta. Repository ini digunakan untuk proyek akhir yang sama pada kelas teori dan praktikum.

## Ringkasan dan status

Proyek ini mengkaji apakah riwayat harga dapat membantu mengenali kenaikan harga nominal produsen padi satu bulan ke depan. Metode yang dipilih adalah **klasifikasi biner**: kelas 1 berarti naik, sedangkan kelas 0 berarti turun atau tetap. Data berasal dari FAOSTAT Producer Prices.

`Projek.ipynb` memuat alur dari Business Understanding, pengumpulan dan pemahaman data, EDA, cleaning, preprocessing, hingga evaluasi dan kesimpulan. Model yang dievaluasi adalah Decision Tree, Random Forest, dan SVM dengan kernel linear. Ketiganya dibandingkan dengan dua baseline pada pembagian waktu yang sama.

Evaluasi akhir memakai **145 contoh uji dari 14 negara pada 2024**. Berikut perbandingan macro-F1 pada contoh uji yang sama.

| Model atau baseline | Macro-F1 uji |
|---|---:|
| Baseline persistensi arah | 0,6344 |
| Random Forest | 0,6171 |
| Decision Tree | 0,5927 |
| SVM kernel linear | 0,5133 |
| Baseline mayoritas latih | 0,3379 |

Random Forest memperoleh skor tertinggi di antara model terlatih. Selisihnya terhadap baseline persistensi arah adalah **−0,0173**, sehingga target peningkatan macro-F1 belum tercapai.

## Fokus Business Understanding

Business Understanding menjelaskan masalah pemantauan arah harga, status calon stakeholder, tujuan SMART yang dipisah menjadi lima unsur, definisi target, asumsi, metrik, risiko, nilai penggunaan, dan pemetaan stakeholder–data. **Bagian 6 notebook adalah Metrik keberhasilan.**

Ukuran utama pengujian adalah macro-F1. Tambahan informasi dinilai dari selisih terhadap pembanding sederhana terbaik pada contoh uji yang sama. Selisih positif belum membuktikan manfaat operasional atau keuntungan finansial. Ukuran ini menjadi dasar penilaian hasil klasifikasi pada data uji.

## Anggota dan kontribusi

| Nama | NIM | Kelas | Progress 1 | Progress 2 | Progress 3 | Progress 4 |
|---|---|---|---|---|---|---|
| Ghazian Muhammad Al Faruq | 123240013 | IF-B | Perumusan masalah, tujuan SMART, penelusuran sumber, dan penulisan penjelasan. | Cleaning dan pemeriksaan kalender serta cakupan negara. | Penulisan penjelasan perbandingan validasi dan contoh prediksi. | Kesimpulan sementara dan jawaban atas pertanyaan Business Understanding. |
| M. Affan Musyafa' | 123240155 | IF-B | Perumusan masalah, penelusuran sumber, dan penulisan penjelasan data. | EDA, visualisasi, dan feature selection. | Penulisan interpretasi hasil awal model. | Analisis FP dan FN serta grafik riwayat harga. |
| Firraz Muhammad Raihan Daffa | 123240170 | IF-B | Penelusuran sumber, kamus data, dan penulisan penjelasan. | Audit kualitas data dan preprocessing. | Pemilihan model, proses training, pengaturan parameter, dan hasil modelling. | Pembahasan keterbatasan data dan model. |
| Jauza Ilham Mahardhika Putra | 123240174 | IF-B | Penelusuran sumber dan seleksi data penelitian. | Audit kualitas data dan EDA. | Pemilihan model, proses training, pengaturan parameter, dan hasil modelling. | Evaluasi dan pemilihan model terbaik. |

## Isi repo

```text
17_IF-B_Sop-Pak-Min-Klaten/
├── Projek.ipynb
├── dashboard_app.py
├── .streamlit/
│   └── config.toml
├── README.md
├── requirements.txt
├── .python-version
├── .gitignore
├── LICENSE
└── data/
    ├── README.md
    ├── raw/
    │   └── faostat_rice_producer_prices.csv
    └── results/
        └── dashboard_results.json
```

Notebook yang sama digunakan untuk melanjutkan seluruh tahapan proyek. Dataset asli disimpan satu kali. Notebook menyimpan hasil audit dan grafik. Dashboard juga memakai ekspor prediksi per contoh yang tersimpan di dalam repo.

## Cara menjalankan

Gunakan **Python 3.13.12** sesuai `.python-version`. Versi pustaka untuk pengolahan, visualisasi, dan evaluasi model tercantum di [requirements.txt](requirements.txt).

1. Buka terminal pada folder `17_IF-B_Sop-Pak-Min-Klaten`. Pastikan `python --version` menampilkan `Python 3.13.12`. Jika berbeda, pilih interpreter 3.13.12 terlebih dahulu.
2. Buat lingkungan virtual dan pasang pustaka berikut melalui PowerShell.

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\python.exe -m pip install -r requirements.txt
   ```

3. Buka `Projek.ipynb` di VS Code dengan ekstensi Jupyter atau melalui JupyterLab yang sudah terpasang. Pilih kernel dari `.venv` dengan Python 3.13.12.
4. Gunakan **Restart Kernel and Run All** agar seluruh sel dijalankan dari awal. Biarkan CSV pada lokasi yang tercantum di struktur repo. Kode tidak memerlukan akses internet saat dijalankan.
5. Periksa alur data `511 → 576 → 436 → 410` pada bagian Feature Selection dan hasil untuk 145 contoh uji pada bagian Evaluasi.

GitHub dapat digunakan untuk membaca penjelasan, tabel, dan grafik yang tersimpan tanpa menjalankan ulang notebook. Penjelasan sumber dan checksum tersedia di [data/README.md](data/README.md).

### Menjalankan dashboard Streamlit

Setelah memasang pustaka dengan langkah di atas, jalankan perintah berikut dari akar repo.

```powershell
.\.venv\Scripts\python.exe -m streamlit run dashboard_app.py
```

Buka alamat lokal yang tercetak di terminal. Streamlit biasanya menampilkan `http://localhost:8501`. Gunakan navigasi untuk membuka Ringkasan, Dataset, Klasifikasi, Evaluasi, atau Notebook. Tabel dataset dan prediksi dapat diunduh sebagai CSV sesuai filter. Di halaman Notebook, pilih bagian untuk membaca penjelasan, tabel, serta grafik yang tersimpan.

Dataset dapat ditelusuri berdasarkan tahun observasi hingga 2024. Pilihan tahun klasifikasi mengikuti **bulan sasaran** dan mencakup 2022 (latih), 2023 (validasi), dan 2024 (uji). Tahun tersebut memuat masing-masing 120, 145, dan 145 contoh. Dashboard menampilkan prediksi tersimpan untuk tiga model dan dua baseline, serta menghitung ringkasan metrik dari prediksi itu. Keluaran ini berasal dari `data/results/dashboard_results.json`, sementara perhitungan dan pelatihan tetap berada di notebook.

## Isi notebook dan hasil audit

| Tahap | Bagian notebook | Isi |
|---|---|---|
| Progress 1 | 1–10 | Business Understanding, tujuan SMART, metrik keberhasilan, sumber dan lisensi, kamus data, serta cakupan penelitian. |
| Progress 2 | 11–15 | EDA, audit kualitas, cleaning, preprocessing, dan feature selection. |
| Progress 3 | 16–19 | Pemilihan model, proses training, pengaturan parameter, perbandingan validasi, dan contoh prediksi. |
| Progress 4 | 20–24 | Evaluasi data uji, pemilihan model terbaik, analisis kesalahan, kesimpulan sementara, dan keterbatasan. |

Progress 4 menampilkan confusion matrix dan grafik macro-F1 uji, perbandingan skor latih dan uji, hasil per negara beserta jumlah contoh uji, serta riwayat harga pada contoh FP dan FN.

Hasil yang diperoleh dari snapshot yang disertakan:

- Berkas asli memuat **5.341 baris, 17 kolom, dan 73 negara**. Seleksi 16 negara Asia pada 2022–2024 menghasilkan **511 observasi harga resmi**.
- Kalender penelitian memiliki **576 kombinasi negara-bulan**, termasuk **65 bulan yang tidak tercatat**. Penambahan kalender hanya menandai kekosongan dan tidak membuat harga baru.
- Audit fitur dan target menghasilkan **436 contoh lengkap**. Setelah 26 contoh pada batas waktu dikeluarkan, tersedia **120 latih, 145 validasi, dan 145 uji**.
- EDA jendela latih memakai **165 return bulanan**, dengan **9 nilai** ditandai oleh pagar IQR per negara. Nilai tersebut dipertahankan karena penandaan belum membuktikan adanya kesalahan data.

Harga LCU antarnegara tidak dibandingkan langsung. Eksplorasi yang dapat memengaruhi pemilihan fitur dibatasi pada data latih. Empat fitur dasar yang dipakai di luar target dan identitas adalah bulan, perubahan harga satu bulan, perubahan harga tiga bulan, dan volatilitas tiga bulan. Fitur tersebut dibentuk dari kalender dan riwayat harga. Cakupan, tanggal publikasi yang tidak tersedia, dan seri yang pendek tetap membatasi penggunaan hasil.

## Laporan dan sumber data

Lampiran C pada [laporan proyek](https://docs.google.com/document/d/1kpoLL2OyEa3MtBHeF0fC8zz1tMHVTMoClQNWpYQM3xY/edit?tab=t.aigts47j05it) menjelaskan repo, isi notebook, dan cara mengulang audit.

FAO. 2026. *FAOSTAT: Producer Prices*. Snapshot diakses 15 Oktober 2026 dan diverifikasi ulang 26 Oktober 2026. [Portal koleksi](https://www.fao.org/faostat/en/#data/PP).

`LICENSE` mempertahankan lisensi MIT untuk kode proyek. Dataset menggunakan CC BY 4.0 dengan [ketentuan tambahan basis data FAO](https://www.fao.org/contact-us/terms/db-terms-of-use/en). Atribusi lengkap dan batas penggunaan data tercantum dalam `data/README.md`. Tidak ada klaim dukungan atau validasi dari FAO.
