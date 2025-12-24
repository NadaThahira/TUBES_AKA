import streamlit as st
import time
import matplotlib.pyplot as plt
import pandas as pd

# ==================================================
# KONFIGURASI HALAMAN
# ==================================================
st.set_page_config(page_title="Analisis Algoritma", layout="centered")

# Warna Terang yang Setone:
# Rekursif: #3B82F6 (Blue 500)
# Iteratif: #EC4899 (Pink 500)

st.markdown("""
    <style>
    /* Memperbesar dan mempertegas label metrik waktu */
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
    /* Styling kotak hasil penjumlahan */
    .result-box {
        padding: 25px;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 10px;
        border: 3px solid;
    }
    .rekursif-box {
        background-color: #3B82F6; /* Biru Terang */
        border-color: #60A5FA;
    }
    .iteratif-box {
        background-color: #EC4899; /* Pink Terang */
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

# ==================================================
# ALGORITMA
# ==================================================
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

# ==================================================
# INPUT USER
# ==================================================
st.markdown("### 🔢 Input Bilangan")
n = st.number_input("Masukkan bilangan bulat positif:", min_value=1, step=1, value=10)

if st.button("🚀 Jalankan Analisis"):
    # 1. Eksekusi Utama
    start_iter = time.time()
    hasil_iteratif = jumlah_faktor_genap_iteratif(n)
    waktu_iteratif = time.time() - start_iter

    start_rek = time.time()
    hasil_rekursif = jumlah_faktor_genap_rekursif(n, n)
    waktu_rekursif = time.time() - start_rek

    # 2. Tampilan Hasil (Box Berwarna)
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

    # Render Grafik
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(df["n"], df["Rekursif (s)"], marker="o", label="Rekursif", color='#3B82F6', linewidth=2)
    ax.plot(df["n"], df["Iteratif (s)"], marker="o", label="Iteratif", color='#EC4899', linewidth=2)
    ax.set_xlabel("Ukuran Input (n)"); ax.set_ylabel("Waktu (detik)"); ax.legend(); ax.grid(True, linestyle='--', alpha=0.5)
    st.pyplot(fig)

    # Render Tabel di bawah Grafik
    st.table(df)

    # 5. Analisis Dinamis
    st.markdown("### 🧠 Analisis Kompleksitas")
    pemenang = "Iteratif" if waktu_iteratif < waktu_rekursif else "Rekursif"
    
    # Logika untuk menjelaskan hasil yang mungkin berubah-ubah pada n kecil
    if n < 50:
        pesan_performa = f"""Meskipun hasil saat ini menunjukkan <b>{pemenang}</b> sedikit lebih cepat, 
        perbedaan pada n kecil ({n}) biasanya dipengaruhi oleh fluktuasi CPU, bukan efisiensi algoritma."""
    else:
        pesan_performa = f"Pada input n = {n}, algoritma <b>{pemenang}</b> menunjukkan performa aslinya."

    st.markdown(f"""
    <div class="analysis-card">
        <h4>1. Observasi Performa</h4>
        <p>{pesan_performa}</p>
        
        <h4>2. Kenapa Iteratif Unggul di Skala Besar?</h4>
        <p>Garis <b>Pink (Iteratif)</b> akan selalu lebih stabil karena menggunakan <i>Fixed Memory</i>. 
        Sedangkan garis <b>Biru (Rekursif)</b> harus mengelola <i>Call Stack</i>.</p>
    </div>
    """, unsafe_allow_html=True)
