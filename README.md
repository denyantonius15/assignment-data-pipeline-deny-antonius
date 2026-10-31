# Data Pipeline Assignment

## Deskripsi Dataset
Dataset otomotif untuk latihan pemeriksaan, pembersihan,
dan transformasi data menggunakan Python.

## Sumber Dataset
Dataset_Sesi_3.zip dari materi assignment.
Input utama: data/raw/automobileEDA_dirty_training.csv

## Kondisi Awal Dataset
- Jumlah baris: 205
- Jumlah kolom: 30
- Kolom dengan missing values: transaction_date = 2, make = 2, num-of-doors = 2, stroke = 4, horsepower = 3, price = 3, horsepower-binned = 1
- Jumlah baris duplikat tambahan: 4
- Kolom dengan tipe data belum sesuai: transaction_date bertipe str padahal berisi tanggal 
- Penulisan kategori belum konsisten: kolom make, body-style, drive-wheels, dan fuel-system ada huruf besar dan kecil (alfa-romero/ ALFA-ROMERO, audi/ Audi, bmw/ BMW, sedan/ SEDAN/ Sedan, rwd/ RWD, mpfi/ MPFI/ Mpfi)
- Permasalahan lain: Format tanggal belum konsisten, contoh: 2025-01-01, 02/01/2025, 01-03-2025, 04-Jan-2025

## Data Cleaning

### Permasalahan dan Metode Penanganan

| Permasalahan | Kolom terkait | Metode | Alasan |
| Missing values | transaction_date, make, num-of-doors, stroke, horsepower, price, horsepower-binned | Menghapus baris yang memiliki nilai kosong menggunakan dropna() | Mempertahankan baris dengan data lengkap tanpa mengisi nilai berdasarkan perkiraan |
| Baris duplikat | Seluruh kolom sebagai dasar perbandingan | Menghapus duplikat menggunakan drop_duplicates() dan mempertahankan kemunculan pertama | Menghindari penghitungan data yang sama berulang kali |
| Spasi berlebih | make | Menghapus spasi di awal dan akhir teks menggunakan str.strip() | Menyeragamkan penulisan kategori |
| Kapitalisasi tidak konsisten | make, body-style, drive-wheels, fuel-system | Mengubah teks menjadi huruf kecil menggunakan str.lower() | Menyatukan kategori yang sama tetapi berbeda kapitalisasi |
| Format tanggal beragam dan tipe data masih teks | transaction_date | Mengonversi tanggal menjadi datetime berdasarkan format yang ditemukan | Menyeragamkan representasi tanggal dan memperbaiki tipe datanya |

Penghapusan spasi diterapkan pada seluruh kolom teks. Berdasarkan pemeriksaan awal, spasi berlebih ditemukan pada kolom `make`.

Nilai `AWD` diubah menjadi `awd`, tetapi tidak digabung dengan `4wd` karena belum ada dasar untuk menyatakan keduanya sebagai kategori yang sama.

### Penanganan Tanggal

Konversi kolom `transaction_date` menggunakan empat format berikut:

| Contoh nilai awal | Format pembacaan | Tanggal hasil konversi |
| 2025-01-01 | %Y-%m-%d | 2025-01-01 |
| 02/01/2025 | %d/%m/%Y | 2025-01-02 |
| 01-03-2025 | %m-%d-%Y | 2025-01-03 |
| 04-Jan-2025 | %d-%b-%Y | 2025-01-04 |

Format bulan-hari-tahun untuk tanggal numerik dengan tanda hubung ditentukan berdasarkan pola nilai dan urutan tanggal pada pemeriksaan awal.

Program akan menghentikan proses apabila terdapat tanggal tidak kosong yang gagal dibaca oleh seluruh format tersebut.

### Urutan Cleaning

1. Membuat salinan DataFrame agar proses cleaning tidak mengubah data awal dalam memori.
2. Menghapus spasi di awal dan akhir teks.
3. Menyeragamkan kapitalisasi pada kolom yang bermasalah.
4. Mengonversi kolom tanggal menjadi datetime.
5. Menghapus baris duplikat setelah penulisan diseragamkan.
6. Menghapus baris yang masih memiliki missing values.

### Hasil Cleaning
Sebelum cleaning = 205 
Duplikat yang dihapus = 4 
Baris yang dihapus karena missing values setelah penghapusan duplikat = 15
Sesudah cleaning = 186

Total baris yang dihapus adalah 19, sekitar 9,27% dari dataset awal. Jumlah kolom tetap 30.

### Missing Values Sebelum dan Sesudah Cleaning

| Kolom | Sebelum | Sesudah |
|---|---:|---:|
| transaction_date | 2 | 0 |
| make | 2 | 0 |
| num-of-doors | 2 | 0 |
| stroke | 4 | 0 |
| horsepower | 3 | 0 |
| price | 3 | 0 |
| horsepower-binned | 1 | 0 |
| **Total sel kosong** | **17** | **0** |

Kolom lainnya memiliki nol missing values sebelum dan sesudah cleaning.

Jumlah sel kosong berbeda dengan jumlah baris yang dihapus. Satu baris dapat memiliki lebih dari satu sel kosong, dan penghapusan missing values dilakukan setelah penghapusan duplikat.

### Kolom yang Mengalami Perubahan Nilai atau Tipe Data

- `transaction_date`: dikonversi dari teks menjadi datetime.
- `make`: spasi berlebih dihapus dan kapitalisasi diseragamkan.
- `body-style`: kapitalisasi diseragamkan.
- `drive-wheels`: kapitalisasi diseragamkan.
- `fuel-system`: kapitalisasi diseragamkan.

Penghapusan baris berlaku pada seluruh kolom dalam baris tersebut.

### Status Pengerjaan

Tahap data cleaning telah selesai dan menghasilkan DataFrame berisi 186 baris dan 30 kolom tanpa missing values. Data transformation dan penyimpanan processed dataset belum dilakukan.

## Data Transformation

### Kolom dan Metode Transformasi

| Kolom asal | Metode | Kolom hasil |
| horsepower | Min-Max Scaling | horsepower_normalized |
| aspiration | Encoding dua kategori | aspiration_encoded |

### Normalisasi Horsepower

Kolom `horsepower` dipilih karena merupakan fitur numerik yang menunjukkan tenaga mesin. Min-Max Scaling diterapkan untuk mengubah nilainya ke rentang 0–1 sesuai instruksi assignment.

Rumus yang digunakan:

horsepower_normalized = (horsepower - horsepower_min) / (horsepower_max - horsepower_min)

Nilai minimum dan maksimum dihitung dari dataset setelah cleaning. Jika seluruh nilai horsepower sama, hasil normalisasi diisi 0 untuk menghindari pembagian dengan nol.

Kolom asli `horsepower` dipertahankan agar dapat dibandingkan dengan hasil normalisasi.

### Encoding Aspiration

Kolom `aspiration` dipilih karena memiliki dua kategori, yaitu `std` dan `turbo`. Encoding mengubah kedua kategori tersebut menjadi representasi numerik.

| Nilai sebelum | Nilai sesudah |
| std | 0 |
| turbo | 1 |

Angka 0 dan 1 merupakan label kategori, bukan urutan atau peringkat. Hasil encoding disimpan dalam kolom baru `aspiration_encoded`, sedangkan kolom asli tetap dipertahankan.

### Perbandingan Sebelum dan Sesudah Transformasi

Perbandingan normalisasi berikut menunjukkan hubungan nilai awal dengan hasilnya. Contoh angka aktual akan dilengkapi berdasarkan output program.

| Nilai horsepower sebelum | Nilai horsepower_normalized sesudah |
| Nilai minimum pada data setelah cleaning | 0 |
| Nilai maksimum pada data setelah cleaning | 1 |

Perbandingan tersebut berlaku apabila nilai minimum dan maksimum berbeda.

### Perubahan Dataset

Transformasi menambahkan dua kolom:

- `horsepower_normalized`
- `aspiration_encoded`

Proses ini tidak menghapus baris atau kolom asal. Dengan input hasil cleaning sebanyak 186 baris dan 30 kolom, ukuran yang diharapkan setelah transformasi adalah 186 baris dan 32 kolom.


## Instalasi
python -m pip install -r requirements.txt

## Menjalankan Program
python src/pipeline.py


## Alur ETL

Pipeline mengikuti tiga tahap ETL (Extract, Transform, Load):

1. **Extract**: Fungsi `load_data()` membaca dataset mentah dari `data/raw/automobileEDA_dirty_training.csv`.
2. **Transform**: Fungsi `inspect_data()` memeriksa kondisi awal dataset, `clean_data()` membersihkan data, dan `transform_data()` melakukan normalisasi Min-Max pada `horsepower` serta encoding pada `aspiration`.
3. **Load**: Fungsi `save_data()` menyimpan hasil pengolahan sebagai file CSV di folder `data/processed/`.

Seluruh tahap dijalankan secara berurutan melalui fungsi `main()` dalam satu kali eksekusi `pipeline.py`. File dataset mentah tidak diubah.

## Lokasi Processed Dataset

Dataset hasil pengolahan disimpan di:

`data/processed/automobileEDA_processed.csv`

File ini dihasilkan secara otomatis oleh pipeline setelah proses cleaning dan transformasi selesai. Jika pipeline dijalankan ulang, file hasil pengolahan akan diperbarui.
