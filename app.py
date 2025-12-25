import streamlit as st
import time
import matplotlib.pyplot as plt
import pandas as pd

# 1. KONFIGURASI HALAMAN & STYLE
st.set_page_config(page_title="Analisis Algoritma", layout="centered")

# CSS Adaptif untuk mendukung Light & Dark Mode
st.markdown("""
    <style>
    [data-testid="stMetricLabel"] {
        font-size: 1.2rem !important;
        font-weight: 800 !important;
        color: #FF4B4B !important; 
        text-transform: uppercase;
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
        font-size: 1.5rem !important;
        font-weight: 900 !important;
        color: #FFFFFF !important;
    }
    .value-text {
        margin: 0;
        font-size: 2.5rem !important;
        font-weight: bold !important;
        color: #FFFFFF !important;
    }
    .info-container {
        background-color: rgba(151, 166, 195, 0.1);
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #FF4B4B;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("📊 Analisis Kompleksitas Algoritma")
st.subheader("Penjumlahan Faktor Genap (Iteratif vs Rekursif)")
st.markdown("---")

# 2. DEFINISI ALGORITMA
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

# 3. INPUT USER
st.markdown("### 🔢 Input Bilangan")
n = st.number_input("Masukkan bilangan bulat positif:", min_value=1, step=1, value=10)

if st.button("🚀 Jalankan Analisis"):
    # --- PROSES PERHITUNGAN UTAMA ---
    start_iter = time.time()
    hasil_iteratif = jumlah_faktor_genap_iteratif(n)
    waktu_iteratif = time.time() - start_iter

    start_rek = time.time()
    hasil_rekursif = jumlah_faktor_genap_rekursif(n, n)
    waktu_rekursif = time.time() - start_rek

    # --- TAMPILAN HASIL BOX ---
    st.markdown("### 🏁 Hasil Penjumlahan")
    col_res1, col_res2 = st.columns(2)
    with col_res1:
        st.markdown(f'<div class="result-box rekursif-box"><p class="label-text">REKURSIF</p><p class="value-text">{hasil_rekursif}</p></div>', unsafe_allow_html=True)
    with col_res2:
        st.markdown(f'<div class="result-box iteratif-box"><p class="label-text">ITERATIF</p><p class="value-text">{hasil_iteratif}</p></div>', unsafe_allow_html=True)

    # --- METRIK WAKTU ---
    st.markdown("### ⏱️ Waktu Eksekusi")
    col1, col2, col3 = st.columns(3)
    selisih = abs(waktu_rekursif - waktu_iteratif)
    with col1: st.metric(label="Iteratif", value=f"{waktu_iteratif:.6f} s")
    with col2: st.metric(label="Rekursif", value=f"{waktu_rekursif:.6f} s")
    with col3: st.metric(label="Selisih", value=f"{selisih:.8f} s")

    # --- PENGUMPULAN DATA UNTUK GRAFIK & TABEL KENAIKAN ---
    st.markdown("---")
    st.markdown("### 📈 Grafik & Tabel Performa")
    
    # Ukuran input sampel untuk melihat trend kenaikan
    input_sizes = [10, 50, 100, 200, 400, 600, 800, 1000] 
    data_points = []

    for ukuran in input_sizes:
        # Hitung Iteratif
        t0 = time.time()
        jumlah_faktor_genap_iteratif(ukuran)
        ti = time.time() - t0
        
        # Hitung Rekursif
        t1 = time.time()
        try:
            # Batasi rekursif untuk n sangat besar agar tidak crash
            jumlah_faktor_genap_rekursif(ukuran, ukuran)
            tr = time.time() - t1
        except RecursionError:
            tr = None
            
        data_points.append({
            "Nilai N": ukuran, 
            "Waktu Iteratif (s)": f"{ti:.8f}", 
            "Waktu Rekursif (s)": f"{tr:.8f}" if tr is not None else "N/A"
        })

    df = pd.DataFrame(data_points)

    # Menampilkan Grafik
    fig, ax = plt.subplots(figsize=(8, 4))
    # Konversi kembali ke float untuk plotting
    ax.plot(df["Nilai N"], df["Waktu Rekursif (s)"].replace("N/A", 0).astype(float), marker="o", label="Rekursif", color='#3B82F6')
    ax.plot(df["Nilai N"], df["Waktu Iteratif (s)"].astype(float), marker="o", label="Iteratif", color='#EC4899')
    ax.set_ylabel("Waktu (detik)")
    ax.set_xlabel("Ukuran Input (N)")
    ax.legend()
    ax.grid(True, linestyle='--', alpha=0.5)
    st.pyplot(fig)

    # Menampilkan Tabel Kenaikan Data Grafik
    st.markdown("#### 📋 Tabel Detail Kenaikan Waktu")
    st.dataframe(df, use_container_width=True)

    # --- DETAIL DATA FAKTOR ---
    st.markdown("---")
    st.markdown("### 📂 Daftar Faktor Genap")
    faktor_genap = [i for i in range(1, n + 1) if n % i == 0 and i % 2 == 0]
    st.write(f"Ditemukan **{len(faktor_genap)}** faktor genap dari angka **{n}**.")
    
    if faktor_genap:
        teks_faktor = ", ".join(map(str, faktor_genap))
        st.markdown(f"""
            <div style="background-color: rgba(151, 166, 195, 0.1); padding: 15px; border-radius: 10px; border: 1px solid #464b5d;">
                <code style="color: var(--text-color); font-size: 1.1rem; font-weight: bold;">{teks_faktor}</code>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.info("Tidak ada faktor genap.")

    # --- BAGIAN ANALISIS KOMPLEKSITAS ---
    pemenang = "Iteratif" if waktu_iteratif < waktu_rekursif else "Rekursif"
    pesan_performa = f"Pada input <b>{n}</b>, metode <b>{pemenang}</b> terbukti lebih efisien."

    st.markdown("---")
    tab1, tab2 = st.tabs(["📝 Kesimpulan Analisis", "💻 Kode Algoritma"])

    with tab1:
        st.markdown(f"""
        <div class="info-container">
            <h4 style="color: var(--text-color); margin-top: 0;">Analisis Efisiensi</h4>
            <p style="color: var(--text-color);">{pesan_performa}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Tabel Big O
        df_comp = pd.DataFrame({
            "Metode": ["Iteratif", "Rekursif"],
            "Time Complexity": ["O(n)", "O(n)"],
            "Space Complexity": ["O(1)", "O(n)"],
            "Stabilitas": ["Sangat Stabil", "Kurang (Stack Overhead)"]
        })
        st.table(df_comp)

    with tab2:
        st.code(f"""
# Versi Iteratif
for i in range(1, n + 1):
    if n % i == 0 and i % 2 == 0:
        total += i

# Versi Rekursif
def logic(n, i):
    if i <= 0: return 0
    if n % i == 0 and i % 2 == 0:
        return i + logic(n, i - 1)
    return logic(n, i - 1)
        """, language="python")
