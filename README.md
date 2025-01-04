# Password-Cracker

Password Cracker adalah alat yang dirancang untuk menguji kekuatan hash password dengan berbagai metode cracking. Alat ini mendukung penggunaan melalui CLI (Command Line Interface) maupun antarmuka web yang mudah digunakan.

## Fitur Utama

Multi-Mode:
- CLI: Gunakan alat ini langsung melalui terminal untuk pengujian yang cepat dan fleksibel.
- Antarmuka Web: Tampilkan dan kelola proses cracking dengan progress real-time.

Metode Cracking:
- Dictionary Attack: Menggunakan wordlist untuk mencocokkan password yang umum digunakan.
- Brute Force Attack: Mencoba semua kemungkinan kombinasi karakter hingga panjang tertentu.
- Hybrid Attack: Gabungan wordlist dengan kombinasi karakter (suffix brute force).
- Rule-Based Attack: Memodifikasi wordlist dengan aturan tertentu, seperti mengganti huruf dengan simbol.
- Combination Attack: Menggabungkan dua kata dari wordlist untuk menghasilkan kombinasi password.

Dukungan Algoritma Hash:
- MD5
- SHA1
- SHA256
- bcrypt
- Argon2

Fitur Tambahan:
- Mendukung wordlist terkompresi (.gz).
- Menyimpan hasil cracking ke database SQLite dengan enkripsi.
- Progress bar real-time di antarmuka web menggunakan Flask-SocketIO.

## Instalasi
1. Clone repository:
   ```bash
   git clone https://github.com/JohanMaa/Password-Cracker.git

2. Install Dependencies:
   ```bash
   pip install -r requirements.txt

Dependencies:
- Flask
- Flask-SocketIO
- passlib
- cryptography


## Cara Menggunakan:

### 1. Mode CLI

### **Argumen CLI**

| **Argumen**             | **Keterangan**                                                                                 | **Contoh**                                  |
|-------------------------|------------------------------------------------------------------------------------------------|---------------------------------------------|
| `-a` / `--algorithm`    | Algoritma hashing yang digunakan. Mendukung: `md5`, `sha1`, `sha256`, `bcrypt`, `argon2`.      | `-a md5`                                    |
| `-ht` / `--hash_target` | Hash yang ingin dipecahkan.                                                                    | `-ht 5f4dcc3b5aa765d61d8327deb882cf99`      |
| `-w` / `--wordlist`     | File wordlist yang digunakan untuk dictionary atau hybrid attack.                              | `-w wordlist.txt`                           |
| `-b` / `--bruteforce`   | Aktifkan mode brute force.                                                                     | `-b`                                        |
| `-c` / `--charset`      | Kumpulan karakter yang digunakan untuk brute force. Default: `abcdefghijklmnopqrstuvwxyz`.     | `-c abc123`                                 |
| `-ml` / `--max_length`  | Panjang maksimum untuk kombinasi brute force.                                                  | `-ml 6`                                     |
| `--hybrid`              | Aktifkan hybrid attack (dictionary + brute force suffix).                                      | `--hybrid`                                  |
| `--rule-based`          | Aktifkan rule-based attack (transformasi pada wordlist).                                       | `--rule-based`                              |
| `-h` / `--help`         | Menampilkan bantuan dan daftar argumen CLI.                                                    | `-h`                                        |


Gunakan alat ini melalui terminal untuk pengujian langsung beikut sintaks dasar untuk setiap metode cracking:
- Dictionary Attack
   ```bash
   python password_cracker.py -a md5 -ht <hash> -w <wordlist>

- Brute Force Attack
   ```bash
   python password_cracker.py -a sha1 -ht <hash> -b -c abc123 -ml 6

- Hybrid Attack
   ```bash
   python password_cracker.py -a sha256 -ht <hash> --hybrid -w <wordlist> -c abc123 -ml 3

- Rule-Based Attack
   ```bash
   python password_cracker.py -a md5 -ht <hash> --rule-based -w <wordlist>

- Combination Attack
   ```bash
   python password_cracker.py -a sha256 -ht <hash> --combination -w <wordlist>

- Menampilkan Bantuan CLI:
   ```bash
   python password_cracker.py -h

### 2. Antarmuka Web

- Jalankan server:
   ```bash
   python password_cracker.py

- Akses antarmuka web:
   ```bash
   http://127.0.0.1:5000

- Isi formulir:
   - Masukkan hash.
   - Pilih algoritma hashing.
   - Unggah wordlist (opsional).
   - Pilih metode cracking (Dictionary, Brute Force, Hybrid).
   - Klik Start Cracking untuk memulai.

## Struktur Proyek
   ```csharp
   password-cracker/
   ├── password_cracker.py        # Program utama
   ├── templates/
   │   ├── index.html             # Antarmuka web
   │   ├── result.html            # Halaman hasil
   ├── static/
   │   ├── style.css              # Gaya antarmuka
   ├── requirements.txt           # Daftar dependensi
   ├── README.md                  # Dokumentasi proyek


