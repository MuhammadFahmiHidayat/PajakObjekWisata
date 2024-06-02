import requests
from typing import List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(
    title="Objek Wisata",
    description="API untuk mengelola data objek wisata",
    docs_url="/",  # Ubah docs_url menjadi "/"
)

@app.get("/")
async def read_root():
    return {"Data":"Successful"}

# Model untuk Data Wisata
class Wisata(BaseModel):
    id_wisata: str
    nama_objek: str
    nama_daerah: str
    kategori: str
    alamat: str
    kontak: str
    harga_tiket: int

# Dummy data untuk wisata
data_wisata = [
    {"id_wisata": "OP01", "nama_objek": "Orchid Forest Cikole", "nama_daerah": "Bandung", "kategori": "Wisata Alam, Wisata Keluarga, Wisata Edukasi", "alamat": "Jl. Tangkuban Perahu Raya No.80E, Cikole, Lembang, Kabupaten Bandung Barat, Jawa Barat 40391, Indonesia", "kontak": "02282325888", "harga_tiket": 40000},
    {"id_wisata": "OP02", "nama_objek": "Taman Impian Jaya Ancol", "nama_daerah": "Jakarta", "kategori": "Wisata Hiburan, Wisata Keluarga, Wisata Alam, Wisata Edukasi", "alamat": "Jl. Lodan Timur No.7, Ancol, Pademangan, Kota Jakarta Utara, Daerah Khusus Ibukota Jakarta 14430, Indonesia", "kontak": "02129222222", "harga_tiket": 25000},
    {"id_wisata": "OP03", "nama_objek": "Candi Borobudur", "nama_daerah": "Yogyakarta", "kategori": "Wisata Budaya, Wisata Sejarah, Wisata Religi", "alamat": "Jl. Badrawati No.1, Borobudur, Magelang, Jawa Tengah 56553, Indonesia", "kontak": "0293788210", "harga_tiket": 50000},
    {"id_wisata": "OP04", "nama_objek": "Uluwatu Temple", "nama_daerah": "Bali", "kategori": "Wisata Budaya, Wisata Religi, Wisata Alam", "alamat": "Pecatu, Kec. Kuta Selatan, Kabupaten Badung, Bali", "kontak": "0361915078", "harga_tiket": 50000},
    {"id_wisata": "OP05", "nama_objek": "Surabaya North Quay", "nama_daerah": "Surabaya", "kategori": "Wisata Hiburan, Wisata Keluarga, Wisata Kuliner", "alamat": "Jalan Perak Timur, Perak Utara, Pabean Cantian, Kota Surabaya, Jawa Timur 60161", "kontak": "081336101290", "harga_tiket": 30000}
]

# Endpoint untuk menambahkan data wisata
@app.post("/wisata")
def tambah_wisata(wisata: Wisata):
    data_wisata.append(wisata.dict())
    return {"message": "Data wisata berhasil ditambahkan."}

# Endpoint untuk mendapatkan data wisata
@app.get("/wisata", response_model=List[Wisata])
def get_wisata():
    return data_wisata

# Fungsi untuk mengambil data pajak dari web hosting lain
def get_data_pajak_from_web():
    url = "https://example.com/api/pajak"  # Ganti dengan URL yang sebenarnya
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail="Gagal mengambil data PAJAK dari web hosting.")

# Model untuk Data Pajak
class Pajak(BaseModel):
    id_pajak: int
    jenis_pajak: str
    tarif_pajak: float
    besar_pajak: float

# Endpoint untuk mendapatkan data pajak
@app.get("/pajak", response_model=List[Pajak])
def get_pajak():
    data_pajak = get_data_pajak_from_web()
    return data_pajak

# Fungsi untuk mengambil data tourguide dari web hosting lain
def get_data_tourGuide_from_web():
    url = "https://example.com/api/pajak"  # Ganti dengan URL yang sebenarnya
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail="Gagal mengambil data TOUR GUIDE dari web hosting.")

# Model untuk Data Tour Guide
class TourGuide(BaseModel):
    nama_guider: str
    profile: str
    fee: float

# Endpoint untuk mendapatkan data Tour Guide
@app.get("/tourGuide", response_model=List[TourGuide])
def get_tourGuide():
    data_tourGuide = get_data_tourGuide_from_web()
    return data_tourGuide

# Fungsi untuk mengambil data asuransi dari web hosting lain
def get_data_asuransi_from_web():
    url = "https://example.com/api/pajak"  # Ganti dengan URL yang sebenarnya
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail="Gagal mengambil data ASURANSI dari web hosting.")

# Model untuk Data Asuransi
class Asuransi(BaseModel):
    id_asuransi: int
    nama_wisata: str
    nama_daerah: str

# Endpoint untuk mendapatkan data asuransi
@app.get("/asuransi", response_model=List[Asuransi])
def get_asuransi():
    data_asuransi = get_data_asuransi_from_web()
    return data_asuransi

# Fungsi untuk mengambil data hotel dari web hosting lain
def get_data_hotel_from_web():
    url = "https://example.com/api/pajak"  # Ganti dengan URL yang sebenarnya
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail="Gagal mengambil data HOTEL dari web hosting.")

# Model untuk Data Hotel
class Hotel(BaseModel):
    id_room: int
    room_number: int
    room_type: str
    rate: str
    availability: int

# Endpoint untuk mendapatkan data hotel
@app.get("/hotel", response_model=List[Hotel])
def get_hotel():
    data_hotel = get_data_hotel_from_web()
    return data_hotel

# Fungsi untuk mengambil data bank dari web hosting lain
def get_data_bank_from_web():
    url = "https://example.com/api/pajak"  # Ganti dengan URL yang sebenarnya
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail="Gagal mengambil data BANK dari web hosting.")

# Model untuk Data Bank
class Bank(BaseModel):
    nik: int
    nama: str
    kabupaten: str

# Endpoint untuk mendapatkan data bank
@app.get("/bank", response_model=List[Bank])
def get_bank():
    data_bank = get_data_bank_from_web()
    return data_bank