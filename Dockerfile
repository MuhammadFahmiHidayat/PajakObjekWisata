# Gunakan image Python sebagai base image
FROM python:3.12

# Set direktori kerja di dalam container
WORKDIR /app

# Copy requirements.txt dan menginstal dependensi
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy seluruh kode aplikasi ke dalam container
COPY . .

# Tentukan perintah untuk menjalankan aplikasi
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]