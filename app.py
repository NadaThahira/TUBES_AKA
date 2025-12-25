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
    # --- PROSES PERHITUNGAN ---
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

    # --- GRAFIK PERFORMA ---
    st.markdown("---")
    st.markdown("### 📈 Grafik Performa")
    input_sizes = [1, 10, 20, 50, 100, 200, 500, 800] 
    data_points = []

    for ukuran in input_sizes:
        t0 = time.time()
        jumlah_faktor_genap_iteratif(ukuran)
        ti = time.time() - t0
        
        t1 = time.time()
        try:
            jumlah_faktor_genap_rekursif(ukuran, ukuran)
            tr = time.time() - t1
        except RecursionError:
            tr = None
            
        data_points.append({"n": ukuran, "Iteratif (s)": ti, "Rekursif (s)": tr})

    df = pd.DataFrame(data_points)
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(df["n"], df["Rekursif (s)"], marker="o", label="Rekursif", color='#3B82F6', linewidth=2)
    ax.plot(df["n"], df["Iteratif (s)"], marker="o", label="Iteratif", color='#EC4899', linewidth=2)
    ax.set_ylabel("Waktu (detik)")
    ax.set_xlabel("Nilai N")
    ax.legend()
    ax.grid(True, linestyle='--', alpha=0.5)
    st.pyplot(fig)

    # --- DETAIL DATA ---
    st.markdown("---")
    st.markdown("### 📋 Detail Data")
    faktor_genap = [i for i in range(1, n + 1) if n % i == 0 and i % 2 == 0]
    jumlah_faktor = len(faktor_genap)
    st.write(f"Ditemukan **{jumlah_faktor}** faktor genap dari angka **{n}**.")
    
    if jumlah_faktor > 0:
        teks_faktor = ", ".join(map(str, faktor_genap))
        st.markdown(f"""
            <div style="background-color: rgba(151, 166, 195, 0.1); padding: 20px; border-radius: 10px; border: 1px solid #464b5d;">
                <code style="color: var(--text-color); font-size: 1.2rem; font-weight: bold;">{teks_faktor}</code>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.info("Tidak ada faktor genap ditemukan.")

    # --- LOGIKA ANALISIS KOMPLEKSITAS ---
    pemenang = "Iteratif" if waktu_iteratif < waktu_rekursif else "Rekursif"
    if n < 50:
        pesan_performa = f"Untuk angka kecil seperti <b>{n}</b>, kedua cara ini sangat cepat. Perbedaan hampir tidak terasa."
    else:
        pesan_performa = f"Pada angka <b>{n}</b>, cara <b>{pemenang}</b> bekerja lebih efisien."

    # --- BAGIAN TAB: ANALISIS & KODE ---
    st.markdown("---")
    tab1, tab2 = st.tabs(["📝 Kesimpulan Analisis", "💻 Kode Algoritma"])

    with tab1:
        st.markdown(f"""
        <div class="info-container">
            <h4 style="color: var(--text-color); margin-top: 0;">1. Mana yang Lebih Cepat?</h4>
            <p style="color: var(--text-color);">{pesan_performa}</p>
        </div>
        <h4>📊 Kelas Kompleksitas</h4>
        """, unsafe_allow_html=True)
        
        # Tabel Kompleksitas
        df_comp = pd.DataFrame({
            "Aspek": ["Time Complexity", "Space Complexity", "Efisiensi"],
            "Iteratif": ["O(n)", "O(1)", "Tinggi"],
            "Rekursif": ["O(n)", "O(n)", "Rendah (Stack Overhead)"]
        })
        st.table(df_comp)

        st.markdown(f"""
        <div style="background-color: rgba(151, 166, 195, 0.05); padding: 15px; border-radius: 10px; border: 1px dashed #888;">
            <p style="color: var(--text-color); font-size: 0.9rem;">
                <b>Penjelasan:</b> Meskipun keduanya linear <b>O(n)</b>, rekursif membutuhkan ruang memori tambahan untuk menyimpan setiap tumpukan fungsi (<i>call stack</i>), sehingga cenderung lebih lambat pada input besar.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with tab2:
        st.code(f"""
# Algoritma Iteratif
def iteratif(n):
    total = 0
    for i in range(1, n + 1):
        if n % i == 0 and i % 2 == 0:
            total += i
    return total

# Algoritma Rekursif
def rekursif(n, i):
    if i <= 0: return 0
    if n % i == 0 and i % 2 == 0:
        return i + rekursif(n, i - 1)
    return rekursif(n, i - 1)
        """, language="python")
