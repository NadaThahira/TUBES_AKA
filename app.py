import streamlit as st
import time
import matplotlib.pyplot as plt
import pandas as pd

# 1. KONFIGURASI HALAMAN & STYLE
st.set_page_config(page_title="Analisis Algoritma", layout="centered")

st.markdown("""
    <style>
    [data-testid="stMetricLabel"] {
        font-size: 1.5rem !important;
        font-weight: 800 !important;
        color: #FF4B4B !important; 
        text-transform: uppercase;
    }
    [data-testid="stMetricValue"] {
        font-size: 2rem !important;
        font-weight: bold !important;
    }
    .result-box {
        padding: 25px;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 10px;
        border: 3px solid;
    }
    .rekursif-box {
        background-color: #3B82F6; 
        border-color: #60A5FA;
    }
    .iteratif-box {
        background-color: #EC4899; 
        border-color: #F472B6;
    }
    .label-text {
        margin: 0;
        font-size: 1.8rem !important;
        font-weight: 900 !important;
        color: #FFFFFF !important;
        letter-spacing: 2px;
    }
    .value-text {
        margin: 0;
        font-size: 3rem !important;
        font-weight: bold !important;
        color: #FFFFFF !important;
    }
    .analysis-card {
        background-color: #262730;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #FF4B4B;
        margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("📊 Analisis Kompleksitas Algoritma")
st.subheader("Penjumlahan Faktor Genap (Iteratif vs Rekursif)")
st.markdown("---")

# ALGORITMA
def jumlah_faktor_genap_iteratif(n):
    total = 0
    for i in range(1, n + 1):
        if n % i == 0 and i % 2 == 0:
            total += i
    return total

def jumlah_faktor_genap_rekursif(n, i):
    if i <= 0:
        return 0
    if n % i == 0 and i % 2 == 0:
        return i + jumlah_faktor_genap_rekursif(n, i - 1)
    else:
        return jumlah_faktor_genap_rekursif(n, i - 1)

# INPUT USER
st.markdown("### 🔢 Input Bilangan")
n = st.number_input("Masukkan bilangan bulat positif:", min_value=1, step=1, value=10)

if st.button("🚀 Jalankan Analisis"):
    # 1. Hitung Waktu
    start_iter = time.time()
    hasil_iteratif = jumlah_faktor_genap_iteratif(n)
    waktu_iteratif = time.time() - start_iter

    start_rek = time.time()
    hasil_rekursif = jumlah_faktor_genap_rekursif(n, n)
    waktu_rekursif = time.time() - start_rek

    # 2. Tampilan Hasil Box
    st.markdown("### 🏁 Hasil Penjumlahan")
    col_res1, col_res2 = st.columns(2)
    with col_res1:
        st.markdown(f'<div class="result-box rekursif-box"><p class="label-text">REKURSIF</p><p class="value-text">{hasil_rekursif}</p></div>', unsafe_allow_html=True)
    with col_res2:
        st.markdown(f'<div class="result-box iteratif-box"><p class="label-text">ITERATIF</p><p class="value-text">{hasil_iteratif}</p></div>', unsafe_allow_html=True)

    # 3. Metrik Waktu
    st.markdown("### ⏱️ Waktu Eksekusi")
    col1, col2, col3 = st.columns(3)
    selisih = abs(waktu_rekursif - waktu_iteratif)
    with col1: st.metric(label="Algoritma Iteratif", value=f"{waktu_iteratif:.6f} s")
    with col2: st.metric(label="Algoritma Rekursif", value=f"{waktu_rekursif:.6f} s")
    with col3: st.metric(label="Selisih Waktu", value=f"{selisih:.8f} s")

    # 4. Pengumpulan Data untuk Grafik & Tabel
    st.markdown("---")
    st.markdown("### 📈 Grafik & Tabel Performa")
    input_sizes = [1, 10, 20, 50, 100, 200, 500, 1000]
    data_points = []

    for ukuran in input_sizes:
        t0 = time.time()
        jumlah_faktor_genap_iteratif(ukuran)
        ti = time.time() - t0
        
        t1 = time.time()
        jumlah_faktor_genap_rekursif(ukuran, ukuran)
        tr = time.time() - t1
        data_points.append({"n": ukuran, "Iteratif (s)": ti, "Rekursif (s)": tr})

    df = pd.DataFrame(data_points)

    # Tampilan Grafik
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(df["n"], df["Rekursif (s)"], marker="o", label="Rekursif", color='#3B82F6', linewidth=2)
    ax.plot(df["n"], df["Iteratif (s)"], marker="o", label="Iteratif", color='#EC4899', linewidth=2)
    ax.set_xlabel("Ukuran Input (n)")
    ax.set_ylabel("Waktu (detik)")
    ax.legend()
    ax.grid(True, linestyle='--', alpha=0.5)
    st.pyplot(fig)

    # Tampilan Tabel
    st.table(df)

    # 5. ANALISIS
    st.markdown("### 🔍 Penjelasan Hasil Analisis")

    # Menentukan siapa yang lebih cepat secara otomatis
    pemenang = "Iteratif" if waktu_iteratif < waktu_rekursif else "Rekursif"
    
    # Pesan berdasarkan hasil hitungan
    if n < 50:
        pesan_performa = f"Untuk angka kecil seperti <b>{n}</b>, kedua cara ini sama-sama sangat cepat. Perbedaan waktunya sangat tipis sehingga hampir tidak terasa."
    else:
        pesan_performa = f"Pada angka <b>{n}</b>, terlihat bahwa cara <b>{pemenang}</b> memberikan hasil yang lebih instan dibandingkan cara lainnya."

    st.markdown(f"""
    <div class="analysis-card">
        <h4>1. Mana yang Lebih Cepat?</h4>
        <p>{pesan_performa}</p>
        
        <h4>2. Mengapa Hasilnya Berbeda?</h4>
        <p>Bayangkan kita sedang menghitung tangga:</p>
        <ul>
            <li><b>Cara Pink (Iteratif):</b> Seperti orang yang langsung melangkah satu per satu hingga selesai. Cara ini sangat stabil dan efisien meski tangganya sangat tinggi.</li>
            <li><b>Cara Biru (Rekursif):</b> Seperti orang yang memanggil temannya untuk melangkah, lalu temannya memanggil teman lain lagi. Untuk tangga pendek ini terlihat mudah, tapi jika tangganya sangat tinggi, proses "panggil-memanggil" ini membuat waktu tunggu jadi lebih lama.</li>
        </ul>

        <h4>3. Kesimpulan dari Grafik</h4>
        <p>Perhatikan tabel dan grafik di atas. Semakin besar angka yang Anda masukkan, garis <b>Biru (Rekursif)</b> biasanya akan mulai naik lebih tinggi di atas garis <b>Pink (Iteratif)</b>. Ini membuktikan bahwa cara <b>Iteratif</b> bekerja lebih ringan dan cepat saat menghadapi tugas yang berat.</p>
    </div>
    """, unsafe_allow_html=True)
