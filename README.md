# 🌫️ Beijing Air Quality Dashboard

Dashboard interaktif kualitas udara Beijing dari 12 stasiun pemantauan (2013–2017).

---

## ▶️ Cara Menjalankan

### 1. Install Python
Download Python di 👉 https://www.python.org/downloads/

> ⚠️ Saat instalasi, **centang "Add Python to PATH"**

### 2. Siapkan Folder Proyek
Pastikan semua file berada dalam satu folder:
```
📁 beijing-dashboard
 ├── dashboard.py
 ├── all_data.csv
 └── requirements.txt
```

### 3. Buka Terminal di Folder Tersebut
```
cd lokasi/folder/beijing-dashboard
```
> 💡 Di Windows: klik kanan dalam folder → **"Open in Terminal"**

### 4. Install Library
```
pip install -r requirements.txt
```

### 5. Jalankan Dashboard
```
streamlit run dashboard.py
```
Lalu buka browser di: **http://localhost:8501** ✅

---

## ❓ Kendala Umum

| Masalah | Solusi |
|---|---|
| `python` tidak dikenali | Ulangi instalasi, centang "Add to PATH" |
| `pip` tidak dikenali | Coba `pip3 install -r requirements.txt` |
| Browser tidak muncul | Buka manual: http://localhost:8501 |

---

📦 Dataset: [PRSA Air Quality — UCI ML Repository](https://archive.ics.uci.edu/dataset/501/beijing+multi+site+air+quality+data)
