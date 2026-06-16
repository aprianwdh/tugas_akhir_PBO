# 🦁 ZooBase — Sistem Manajemen Kebun Binatang

Aplikasi desktop berbasis **PyQt6** dan **SQLite** yang dirancang untuk mengelola database data hewan di kebun binatang secara efisien, modern, dan aman. Proyek ini dibuat sebagai Tugas Akhir untuk mata kuliah Pemrograman Berorientasi Objek (PBO).

---

## 👥 Anggota Kelompok

| No. | Nama Anggota | NIM 
| :--- | :--- | :--- |
| 1 | Aprian Widhi Wibowo | A710250006
| 2 | [Nama Anggota 2] | [NIM Anggota 2]
| 3 | [Nama Anggota 3] | [NIM Anggota 3]
| 4 | [Nama Anggota 4] | [NIM Anggota 4]

---

## 🚀 Fitur Utama

1. **Sistem Autentikasi Keamanan (Auth Page)**
   - Halaman **Sign In** dan **Sign Up** bagi pengguna baru sebelum mengakses database utama.
   - Keamanan penyimpanan kata sandi menggunakan enkripsi **SHA-256**.
   - Validasi input form yang aman dan interaktif.

2. **Manajemen Data Hewan (CRUD)**
   - **Create**: Menambahkan data hewan baru lengkap dengan foto, nama ilmiah, kategori, status kesehatan, diet, asal daerah, dan deskripsi.
   - **Read**: Menampilkan daftar hewan dalam bentuk grid kartu yang interaktif dan responsif.
   - **Update**: Mengedit/memperbarui informasi hewan yang sudah terdaftar.
   - **Delete**: Menghapus data hewan dari database dengan konfirmasi keamanan.

3. **Pencarian, Filter & Pengurutan Cepat**
   - Cari hewan secara real-time berdasarkan nama.
   - Filter hewan berdasarkan kategori (Mamalia, Burung, Reptil, dll.) dan status kesehatan (Sehat, Perawatan, Karantina).
   - Urutkan daftar hewan berdasarkan Abjad (A-Z, Z-A) atau tanggal masuk.

4. **Dasbor Statistik Real-Time**
   - Menyediakan statistik visual jumlah total hewan.
   - Grafik/representasi visual sebaran hewan berdasarkan kategori dan status kesehatan.

5. **Arsitektur Modular**
   - Kode sumber telah direfaktorisasi secara modular untuk memisahkan konfigurasi, logika database, komponen antarmuka (UI widgets), dan tampilan window (views).

---

## 🛠️ Prasyarat & Cara Instalasi

### 1. Prasyarat
Pastikan Anda sudah menginstal Python (versi 3.8 ke atas) di perangkat Anda.

### 2. Instalasi Dependensi
Instal pustaka PyQt6 dengan perintah berikut melalui terminal/command prompt:
```bash
pip install PyQt6
```

### 3. Menjalankan Aplikasi
Jalankan file utama `main.py` menggunakan Python:
```bash
python main.py
```

---

## 🎨 Palet Warna & Desain UI
Aplikasi ini mengadopsi tema modern minimalis (Glassmorphism/Dark Mode) dengan palet warna berikut:
- **Primary Color**: Dark Slate Gray (`#1E2022`)
- **Accent Color**: Deep Emerald Green (`#2C4A3E`) & Mint Accent (`#A3C6C4`)
- **Card Background**: Semi-transparent surface (`rgba(255, 255, 255, 0.05)`)
- **Typography**: Menggunakan font sistem modern (*Segoe UI* atau *SF Pro Display*) untuk tampilan yang bersih dan profesional.
