## Flask-JS2

**Flask-JS2** adalah kerangka kerja flask yang disederhanakan yang memungkinkan konfigurasi dan pengaturan aplikasi Flask dengan integrasi front-end JavaScript secara cepat. Dengan hanya dua file konfigurasi JSON, Anda dapat dengan mudah mengatur dan mengelola aspek back-end dan front-end dari aplikasi.

### Instalasi

Untuk menginstal Flask-JS2, cukup masukkan ke dalam proyek Anda dan pastikan Anda memiliki file konfigurasi yang diperlukan.

### File Konfigurasi

Ada dua file konfigurasi JSON utama yang diperlukan:

1. **server_cfg.min**: File ini digunakan untuk mengatur konfigurasi back-end.
2. **fe_cfg.min**: File ini digunakan untuk mengatur konfigurasi front-end.


### Penggunaan

Untuk menggunakan Flask-JS2 dalam proyek Anda, ikuti langkah-langkah berikut:

1. **Impor modul Flask_J2S** dari Flask-JS2:
    ```python
    from Flask_J2S import Processing
    ```

2. **Inisialisasi instance Flask_J2S** dengan path ke file konfigurasi Anda:
    ```python
    sin = Processing(path_modul="./cfg/modul.min", config_path="./cfg/server_cfg.min")
    ```

3. **Jalankan server**:
    ```python
    data = sin.Run_Server()
    ```

### Contoh

Berikut adalah contoh lengkap tentang cara mengatur dan menjalankan aplikasi Flask menggunakan Flask-JS2:

```python
from Flask_J2S import Processing

# Inisialisasi instance Processing dengan path konfigurasi
sin = Processing(path_modul="./cfg/modul.min", config_path="./cfg/server_cfg.min")

# Jalankan server
data = sin.Run_Server()
```

### Cara Running
1. **Generate Routes**:
    ```bash
      python app.py generate
    ```

2. **Generate Front-End**:
   ```bash
      pyhton app.py set-fe
    ```

3. **Run Program**:
   ```bash
      python app.py 
    ```


### Detail Konfigurasi

#### server_cfg.min

File ini berisi konfigurasi untuk server back-end. Termasuk pengaturan seperti host server, port, konfigurasi database, dan pengaturan terkait back-end lainnya.

#### fe_cfg.min

File ini berisi konfigurasi untuk pengaturan front-end. Termasuk pengaturan seperti framework front-end yang digunakan, lokasi file statis, pengaturan mesin template, dan konfigurasi terkait front-end lainnya.

### Struktur Direktori

Direktori proyek Anda harus terlihat seperti ini:


```
your_project/
|
+-- cfg/			#Folder Tempat Menyimpan Semua Konfigurasi
|   +-- server_cfg.min		#Konfigurasi Untuk Server dan BE
|   +-- fe_cfg.min		#Konfigurasi Untuk Front-End
|   +-- modul.min		#Konfigurasi Untuk Library
|
+-- app.py
```


### Dokumentasi Lengkap

Untuk Dokumentasi Lengkap nya ada Di : https://github.com/staykimin/Flask-J2S
