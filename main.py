import requests
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from itertools import zip_longest
from itertools import product

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
    {"id_wisata": "OP01", "nama_objek": "Orchid Forest Cikole", "nama_daerah": "Bandung", "kategori": "Wisata Alam, Wisata Keluarga, Wisata Edukasi", "alamat": "Jl. Tangkuban Perahu Raya No.80E, Cikole, Lembang, Kabupaten Bandung Barat, Jawa Barat 40391, Indonesia", "kontak": "02282325888", "harga_tiket": 40000, "id_pajak": "PJ001", "id_guider": "1111", "id_asuransi": "AA01", "RoomID": "1", "id": "2021403001"},
    {"id_wisata": "OP02", "nama_objek": "Taman Impian Jaya Ancol", "nama_daerah": "Jakarta", "kategori": "Wisata Hiburan, Wisata Keluarga, Wisata Alam, Wisata Edukasi", "alamat": "Jl. Lodan Timur No.7, Ancol, Pademangan, Kota Jakarta Utara, Daerah Khusus Ibukota Jakarta 14430, Indonesia", "kontak": "02129222222", "harga_tiket": 25000,  "id_pajak": "PJ002", "id_guider": "2222", "id_asuransi": "AA02", "RoomID": "2", "id": "2021403002"},
    {"id_wisata": "OP03", "nama_objek": "Candi Borobudur", "nama_daerah": "Yogyakarta", "kategori": "Wisata Budaya, Wisata Sejarah, Wisata Religi", "alamat": "Jl. Badrawati No.1, Borobudur, Magelang, Jawa Tengah 56553, Indonesia", "kontak": "0293788210", "harga_tiket": 50000, "id_pajak": "PJ003", "id_guider": "3333", "id_asuransi": "AA03", "RoomID": "3", "id": "2021403003"},
    {"id_wisata": "OP04", "nama_objek": "Uluwatu Temple", "nama_daerah": "Bali", "kategori": "Wisata Budaya, Wisata Religi, Wisata Alam", "alamat": "Pecatu, Kec. Kuta Selatan, Kabupaten Badung, Bali", "kontak": "0361915078", "harga_tiket": 50000, "id_pajak": "PJ004", "id_guider": "4444", "id_asuransi": "AA04", "RoomID": "4", "id": "2021403004"},
    {"id_wisata": "OP05", "nama_objek": "Surabaya North Quay", "nama_daerah": "Surabaya", "kategori": "Wisata Hiburan, Wisata Keluarga, Wisata Kuliner", "alamat": "Jalan Perak Timur, Perak Utara, Pabean Cantian, Kota Surabaya, Jawa Timur 60161", "kontak": "081336101290", "harga_tiket": 50000, "id_pajak": "PJ005", "id_guider": "5555", "id_asuransi": "AA05", "RoomID": "5", "id": "2021403005"}
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

def get_wisata_index(id_wisata):
    for index, wisata in enumerate(data_wisata):
        if wisata['id_wisata'] == id_wisata:
            return index
    return None

# Endpoint untuk detail get id
@app.get("/wisata/{id_wisata}", response_model=Optional[Wisata])
def get_wisata_by_id(id_wisata: str):
    for wisata in data_wisata:
        if wisata['id_wisata'] == id_wisata:
            return Wisata(**wisata)
    return None

# Endpoint untuk memperbarui data wisata dengan hanya memasukkan id_wisata
@app.put("/wisata/{id_wisata}")
def update_wisata_by_id(id_wisata: str, wisata_baru: Wisata):
    index = get_wisata_index(id_wisata)
    if index is not None:
        data_wisata[index] = wisata_baru.dict()
        return {"message": "Data wisata berhasil diperbarui."}
    else:
        raise HTTPException(status_code=404, detail="Data wisata tidak ditemukan.")

# Endpoint untuk menghapus data wisata
@app.delete("/wisata/{id_wisata}")
def delete_wisata(id_wisata: str):
    index = get_wisata_index(id_wisata)
    if index is not None:
        del data_wisata[index]
        return {"message": "Data wisata berhasil dihapus."}
    else:
        raise HTTPException(status_code=404, detail="Data wisata tidak ditemukan.")










# Fungsi untuk mengambil data pajak dari web hosting lain
def get_data_pajak_from_web():
    url = "https://api-government.onrender.com/pajak"  # Ganti dengan URL yang sebenarnya
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail="Gagal mengambil data PAJAK dari web hosting.")

# Model untuk Data Pajak
class Pajak(BaseModel):
    id_pajak: str
    status_kepemilikan: str
    jenis_pajak: str
    tarif_pajak: float
    besar_pajak: float

# Endpoint untuk mendapatkan data pajak
@app.get("/pajak", response_model=List[Pajak])
def get_pajak():
    data_pajak = get_data_pajak_from_web()
    return data_pajak

def get_pajak_index(id_pajak):
    data_pajak = get_data_pajak_from_web()
    for index, pajak in enumerate(data_pajak):
        if pajak['id_pajak'] == id_pajak:
            return index
    return None

@app.get("/pajak/{id_pajak}", response_model=Optional[Pajak])
def get_pajak_by_id(id_pajak: str):
    data_pajak = get_data_pajak_from_web()
    for pajak in data_pajak:
        if pajak['id_pajak'] == id_pajak:
            return Pajak(**pajak)
    return None










# Fungsi untuk mengambil data tourguide dari web hosting lain
def get_data_tourGuide_from_web():
    url = "https://tour-guide-ks4n.onrender.com/tourguide"  # Ganti dengan URL yang sebenarnya
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail="Gagal mengambil data TOUR GUIDE dari web hosting.")

# Model untuk Data Tour Guide
class TourGuide(BaseModel):
    id_guider:str
    nama_guider: str
    profile: str
    fee: int
    status_ketersediaan: str

# Endpoint untuk mendapatkan data Tour Guide
@app.get("/tourGuide", response_model=List[TourGuide])
def get_tourGuide():
    data_tourGuide = get_data_tourGuide_from_web()
    return data_tourGuide

def get_tourGuide_index(id_guider):
    data_tourGuide = get_data_tourGuide_from_web()
    for index, tourGuide in enumerate(data_tourGuide):
        if tourGuide['id_guider'] == id_guider:
            return index
    return None

@app.get("/tourGuide/{id_guider}", response_model=Optional[TourGuide])
def get_tourGuide_by_id(id_guider: str):
    data_tourGuide = get_data_tourGuide_from_web()
    for tourGuide in data_tourGuide:
        if tourGuide['id_guider'] == id_guider:
            return TourGuide(**tourGuide)
    return None










# Fungsi untuk mengambil data asuransi dari web hosting lain
def get_data_asuransi_from_web():
    url = "https://eai-fastapi.onrender.com/asuransi"  # Ganti dengan URL yang sebenarnya
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail="Gagal mengambil data ASURANSI dari web hosting.")

# Model untuk Data Asuransi
class Asuransi(BaseModel):
    id_asuransi: str
    jenis_asuransi: str

def get_asuransi_index(id_asuransi):
    data_asuransi = get_data_asuransi_from_web()
    for index, asuransi in enumerate(data_asuransi):
        if asuransi['id_asuransi'] == id_asuransi:
            return index
    return None

@app.get("/asuransi", response_model=List[Asuransi])
def get_asuransi():
    data_asuransi = get_data_asuransi_from_web()
    return data_asuransi

@app.get("/asuransi/{id_asuransi}", response_model=Optional[Asuransi])
def get_asuransi_by_id(id_asuransi: str):
    data_asuransi = get_data_asuransi_from_web()
    for asuransi in data_asuransi:
        if asuransi['id_asuransi'] == id_asuransi:
            return Asuransi(**asuransi)
    return None










# Fungsi untuk mengambil data hotel dari web hosting lain
def get_data_hotel_from_web():
    url = "https://hotelbaru.onrender.com/rooms"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()  
    else:
        raise HTTPException(status_code=response.status_code, detail="Gagal mengambil data HOTEL dari web hosting.")

# Model untuk Data Hotel
class Hotel(BaseModel):
    RoomID: str
    RoomNumber: str
    RoomType: str
    Rate: int
    Availability: str

@app.get("/hotel", response_model=List[Hotel])
def get_hotel():
    data_hotel = get_data_hotel_from_web()
    return data_hotel

@app.get("/hotel/{RoomID}", response_model=Optional[Hotel])
def get_hotel_by_id(RoomID: str):
    data_hotel = get_data_hotel_from_web()
    for hotel in data_hotel:
        if hotel['RoomID'] == RoomID:
            return Hotel(**hotel)
    return None










# Fungsi untuk mengambil data bank dari web hosting lain
def get_data_bank_from_web():
    url = "https://jumantaradev.my.id/api/obj-wisata"  # Ganti dengan URL yang sebenarnya
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data['data']['data'] # Mengambil hanya bagian 'data' dari JSON
    else:
        raise HTTPException(status_code=response.status_code, detail="Gagal mengambil data BANK dari web hosting.")

# Model untuk Data Bank
class Bank(BaseModel):
    id: int
    saldo: int
    active_date: str
    expired_date: str

def get_bank_index(id):
    data_bank = get_data_bank_from_web()
    for index, bank in enumerate(data_bank):
        if bank['id'] == id:
            return index
    return None

@app.get("/bank", response_model=List[Bank])
def get_bank():
    data_bank = get_data_bank_from_web()
    return data_bank

@app.get("/bank/{id}", response_model=Optional[Bank])
def get_bank_by_id(id: int):
    data_bank = get_data_bank_from_web()
    for bank in data_bank:
        if bank['id'] == id:
            return Bank(**bank)
    return None













# Endpoint untuk mendapatkan data wisata beserta informasi pajak
class WisataPajak(BaseModel):
    id_pajak: str
    id_wisata: str
    nama_objek: str
    status_kepemilikan: str
    jenis_pajak: str
    tarif_pajak: float
    besar_pajak: int

# Endpoint untuk mendapatkan data gabungan objek wisata pajak
@app.get('/wisataPajak', response_model=List[WisataPajak])
def get_wisata_pajak():
    data_pajak = get_data_pajak_from_web()

    # Menggunakan zip_longest untuk menggabungkan data objek wisata dan data pajak
    gabungan_data = []
    for wisata, pajak in zip_longest(data_wisata, data_pajak, fillvalue={}):
        gabungan_data.append(WisataPajak(
            id_pajak = pajak.get('id_pajak', None),
            id_wisata = wisata.get('id_wisata', None),
            nama_objek = wisata.get('nama_objek', None),
            status_kepemilikan = pajak.get('status_kepemilikan', None),
            jenis_pajak = pajak.get('jenis_pajak', None),
            tarif_pajak = pajak.get('tarif_pajak', None),
            besar_pajak = pajak.get('besar_pajak', None)
        ))

    return gabungan_data

# Endpoint untuk mendapatkan data wisata beserta informasi pajak berdasarkan id_pajak
@app.get('/wisataPajak/{id_pajak}', response_model=List[WisataPajak])
def get_wisata_pajak_by_id(id_pajak: str):
    data_pajak = get_data_pajak_from_web()
    data_wisata_pajak = get_wisata_pajak()

    hasil = [wp for wp in data_wisata_pajak if wp.id_pajak == id_pajak]

    if not hasil:
        raise HTTPException(status_code=404, detail="Data wisata dengan id_pajak tersebut tidak ditemukan.")

    return hasil






# Endpoint untuk mendapatkan data wisata beserta informasi tour guide
class WisataTourGuide(BaseModel):
    id_wisata: str
    nama_objek: str
    nama_daerah: str
    kategori: str
    alamat: str
    kontak: str
    harga_tiket: int
    id_guider:str
    nama_guider: str
    profile: str
    fee: int
    status_ketersediaan: str

# Endpoint untuk mendapatkan data gabungan objek wisata dan tour guide
@app.get('/wisataTourGuide', response_model=List[WisataTourGuide])
def get_wisata_tourGuide():
    data_tourGuide = get_data_tourGuide_from_web()

    # Menggunakan zip_longest untuk menggabungkan data objek wisata dan data tour guide
    gabungan_data = []
    for wisata, tourGuide in zip_longest(data_wisata, data_tourGuide, fillvalue={}):
        gabungan_data.append(WisataTourGuide(
            id_wisata = wisata.get('id_wisata', None),
            nama_objek = wisata.get('nama_objek', None),
            nama_daerah = wisata.get('nama_daerah', None),
            kategori = wisata.get('kategori', None),
            alamat = wisata.get('alamat', None),
            kontak = wisata.get('kontak', None),
            harga_tiket = wisata.get('harga_tiket', None),
            id_guider = tourGuide.get('id_guider', None),
            nama_guider = tourGuide.get('nama_guider', None),
            profile = tourGuide.get('profile', None),
            fee = tourGuide.get('fee', None),
            status_ketersediaan = tourGuide.get('status_ketersediaan', None)
        ))

    return gabungan_data

# Endpoint untuk mendapatkan data wisata beserta informasi pajak berdasarkan id_pajak
@app.get('/wisataTourGuide/{id_guider}', response_model=List[WisataTourGuide])
def get_wisata_tourGuide_by_id(id_guider: str):
    data_tourGuide = get_data_tourGuide_from_web()
    data_wisata_tourGuide = get_wisata_tourGuide()

    hasil = [wp for wp in data_wisata_tourGuide if wp.id_guider == id_guider]

    if not hasil:
        raise HTTPException(status_code=404, detail="Data wisata dengan id_guider tersebut tidak ditemukan.")

    return hasil










# Endpoint untuk mendapatkan data wisata beserta informasi asuransi
class WisataAsuransi(BaseModel):
    id_wisata: str
    nama_objek: str
    alamat: str
    kontak: str
    id_asuransi: str
    jenis_asuransi: str

# Endpoint untuk mendapatkan data gabungan objek wisata dan asuransi
@app.get('/wisataAsuransi', response_model=List[WisataAsuransi])
def get_wisata_asuransi():
    data_asuransi = get_data_asuransi_from_web()

    # Menggunakan zip_longest untuk menggabungkan data objek wisata dan asuransi
    gabungan_data = []
    for wisata, asuransi in zip_longest(data_wisata, data_asuransi, fillvalue={}):
        gabungan_data.append(WisataAsuransi(
            id_wisata = wisata.get('id_wisata', None),
            nama_objek = wisata.get('nama_objek', None),
            alamat = wisata.get('alamat', None),
            kontak = wisata.get('kontak', None),
            id_asuransi = asuransi.get('id_asuransi', None),
            jenis_asuransi = asuransi.get('jenis_asuransi', None)
        ))

    return gabungan_data

# Endpoint untuk mendapatkan data wisata beserta informasi pajak berdasarkan id_pajak
@app.get('/wisataAsuransi/{id_asuransi}', response_model=List[WisataAsuransi])
def get_wisata_asuransi_by_id(id_asuransi: str):
    data_asuransi = get_data_asuransi_from_web()
    data_wisata_asuransi = get_wisata_asuransi()

    hasil = [wp for wp in data_wisata_asuransi if wp.id_asuransi == id_asuransi]

    if not hasil:
        raise HTTPException(status_code=404, detail="Data wisata dengan id_asuransi tersebut tidak ditemukan.")

    return hasil










# Endpoint untuk mendapatkan data wisata beserta informasi hotel
class WisataHotel(BaseModel):
    id_wisata: str
    nama_objek: str
    nama_daerah: str
    kategori: str
    alamat: str
    kontak: str
    harga_tiket: int
    RoomID: str
    RoomNumber: str
    RoomType: str
    Rate: int
    Availability: str
# Endpoint untuk mendapatkan data gabungan objek wisata dan hotel
@app.get('/wisataHotel', response_model=List[WisataHotel])
def get_wisata_hotel():
    data_hotel = get_data_hotel_from_web()

    # Menggunakan zip_longest untuk menggabungkan data objek wisata dan data hotel
    gabungan_data = []
    for wisata, hotel in zip_longest(data_wisata, data_hotel, fillvalue={}):
        gabungan_data.append(WisataHotel(
            id_wisata = wisata.get('id_wisata', None),
            nama_objek = wisata.get('nama_objek', None),
            nama_daerah = wisata.get('nama_daerah', None),
            kategori = wisata.get('kategori', None),
            alamat = wisata.get('alamat', None),
            kontak = wisata.get('kontak', None),
            harga_tiket = wisata.get('harga_tiket', None),
            RoomID = hotel.get('RoomID', None),
            RoomNumber = hotel.get('RoomNumber', None),
            RoomType = hotel.get('RoomType', None),
            Rate = hotel.get('Rate', None),
            Availability = hotel.get('Availability', None)
        ))

    return gabungan_data

# Endpoint untuk mendapatkan data wisata beserta informasi pajak berdasarkan id_pajak
@app.get('/wisataHotel/{RoomID}', response_model=List[WisataHotel])
def get_wisata_hotel_by_id(RoomID: str):
    data_hotel = get_data_hotel_from_web()
    data_wisata_hotel = get_wisata_hotel()

    hasil = [wp for wp in data_wisata_hotel if wp.RoomID == RoomID]

    if not hasil:
        raise HTTPException(status_code=404, detail="Data wisata dengan RoomID tersebut tidak ditemukan.")

    return hasil










# Endpoint untuk mendapatkan data wisata beserta informasi hotel
class WisataBank(BaseModel):
    id_wisata: str
    nama_daerah: str
    harga_tiket: int
    id: int
    saldo: int
    active_date: str
    expired_date: str
    
# Endpoint untuk mendapatkan data gabungan objek wisata dan hotel
@app.get('/wisataBank', response_model=List[WisataBank])
def get_wisata_bank():
    data_bank = get_data_bank_from_web()

    # Menggunakan zip_longest untuk menggabungkan data objek wisata dan data hotel
    gabungan_data = []
    for wisata, bank in zip_longest(data_wisata, data_bank, fillvalue={}):
        gabungan_data.append(WisataBank(
            id_wisata=wisata.get('id_wisata', None),
            nama_daerah=wisata.get('nama_daerah', None),
            harga_tiket=wisata.get('harga_tiket', None),
            id=bank.get('id', None),
            saldo=bank.get('saldo', None),
            active_date=bank.get('active_date', None),
            expired_date=bank.get('expired_date', None)
        ))

    return gabungan_data

# Endpoint untuk mendapatkan data wisata beserta informasi pajak berdasarkan id_pajak
@app.get('/wisataBank/{id}', response_model=List[WisataBank])
def get_wisata_bank_by_id(id: int):
    data_bank = get_data_bank_from_web()
    data_wisata_bank = get_wisata_bank()

    hasil = [wp for wp in data_wisata_bank if wp.id == id]

    if not hasil:
        raise HTTPException(status_code=404, detail="Data wisata dengan id_bank tersebut tidak ditemukan.")

    return hasil