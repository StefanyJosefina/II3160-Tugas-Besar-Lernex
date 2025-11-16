# API Lernex (FastAPI)

API backend untuk platform Digital Learning Marketplace, Lernex.

## Stack Teknologi
* Python
* FastAPI
* Pydantic

---

## Menjalankan Aplikasi

1.  **Install dependencies** yang diperlukan:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Jalankan server** menggunakan Uvicorn:
    ```bash
    uvicorn app.main:app --reload
    ```
    * Server akan aktif di port `8000`.

---

## Dokumentasi & Pengujian API

Setelah server berjalan, FastAPI otomatis membuat halaman dokumentasi interaktif.

Buka salah satu URL berikut di browser Anda:

* **Swagger UI (Direkomendasikan)**
    * `http://127.0.0.1:8000/docs`
    * `http://localhost:8000/docs`
    * Gunakan ini untuk melihat dan menguji (POST, GET, DELETE) semua endpoint.

* **ReDoc UI (Alternatif)**
    * `http://127.0.0.1:8000/redoc`
    * `http://localhost:8000/redoc`
    * Gunakan ini untuk tampilan dokumentasi yang lebih rapi (read-only).
