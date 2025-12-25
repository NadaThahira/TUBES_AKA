import streamlit as st
import time
import matplotlib.pyplot as plt
import pandas as pd

# 1. KONFIGURASI HALAMAN & STYLE
st.set_page_config(page_title="Analisis Algoritma", layout="centered")

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
    .rekursif-box { background-color: #3B82F6; border-color: #60A5FA; }
    .iteratif-box { background-color: #EC4899; border-color: #F472B6; }
    .label-text { margin: 0; font-size: 1.5rem !important; font-weight: 900 !important; color: #FFFFFF !important; }
    .value-text { margin: 0; font-size: 2.5rem !important; font-weight: bold !important; color: #FFFFFF !important; }
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
    if i <= 0: return 0
    if n % i == 0 and i % 2 == 0:
        return i + jumlah_faktor_genap_rekursif(n, i - 1)
    return jumlah_faktor_genap_rekursif(n, i - 1)

# 3. INPUT USER
st.markdown("### 🔢 Input Bilangan")
n = st.number_input("Masukkan bilangan bulat positif:", min_value=1, step=1, value=10)

if st.button("🚀 Jalankan Analisis"):
    # --- PERHITUNGAN UTAMA ---
    start_it = time.time()
    hasil_it = jumlah_faktor_genap_iteratif(n)
    waktu_it = time.time() - start_it

    start_rek = time.time()
    hasil_rek = jumlah_faktor_genap_rekursif(n, n)
    waktu_rek = time.time() - start_rek

    # --- BOX HASIL ---
    st.markdown("### 🏁 Hasil Penjumlahan")
    c1, c2 = st.columns(2)
    with c1: st.markdown(f'<div class="result-box rekursif-box"><p class="label-text">REKURSIF</p><p class="value-text">{hasil_rek}</p></div>', unsafe_allow_html=True)
    with c2: st.markdown(f'<div class="result-box iteratif-box"><p class="label-text">ITERATIF</p><p class="value-text">{hasil_it}</p></div>', unsafe_allow_html=True)

    # --- METRIK WAKTU ---
    st.markdown("### ⏱️ Waktu Eksekusi")
    m1, m2, m3 = st.columns(3)
    selisih = abs(waktu_rek - waktu_it)
    with m1: st.metric(label="Iteratif", value=f"{waktu_it:.6f} s")
    with m2: st.metric(label="Rekursif", value=f"{waktu_rek:.6f} s")
    with m3: st.metric(label="Selisih", value=f"{selisih:.8f} s")

    # --- DATA UNTUK GRAFIK & TABEL PERFORMA ---
    st.markdown("---")
    st.markdown("### 📈 Grafik & Tabel Performa")
    
    input_sizes = [10, 50, 100, 200, 400, 600, 800, 1000]
    results = []

    for size in input_sizes:
        # Iteratif
        t_start = time.time()
        jumlah_faktor_genap_iteratif(size)
        t_it = time.time() - t_start
        
        # Rekursif
        t_start = time.time()
        try:
            jumlah_faktor_genap_rekursif(size, size)
            t_rek = time.time() - t_start
        except RecursionError:
            t_rek = None
        
        results.append({
            "Ukuran Input (N)": size,
            "Waktu Iteratif (detik)": t_it,
            "Waktu Rekursif (detik)": t_rek
        })

    df_perf = pd.DataFrame(results)

    # Menampilkan Grafik
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(df_perf["Ukuran Input (N)"], df_perf["Waktu Rekursif (detik)"], marker="o", label="Rekursif", color='#3B82F6')
    ax.plot(df_perf["Ukuran Input (N)"], df_perf["Waktu Iteratif (detik)"], marker="o", label="Iteratif", color='#EC4899')
    ax.set_ylabel("Waktu (s)")
    ax.set_xlabel("N")
    ax.legend()
    ax.grid(True, alpha=0.3)
    st.pyplot(fig)

    # MENAMPILKAN TABEL DATA GRAFIK
    st.markdown("#### 📋 Tabel Nilai Kenaikan Grafik")
    # Styling agar angka tidak disingkat (scientific notation)
    st.dataframe(df_perf.style.format({
        "Waktu Iteratif (detik)": "{:.8f}",
        "Waktu Rekursif (detik)": "{:.8f}"
    }), use_container_width=True)

    # --- DETAIL DATA ---
    st.markdown("---")
    st.markdown("### 📋 Detail Data")
    faktor_genap = [i for i in range(1, n + 1) if n % i == 0 and i % 2 == 0]
    st.write(f"Ditemukan **{len(faktor_genap)}** faktor genap dari angka **{n}**.")
    if faktor_genap:
        st.markdown(f'<div style="background-color: rgba(151, 166, 195, 0.1); padding: 15px; border-radius: 10px; border: 1px solid #464b5d;"><code style="color: var(--text-color); font-weight: bold;">{", ".join(map(str, faktor_genap))}</code></div>', unsafe_allow_html=True)
    else:
        st.info("Tidak ada faktor genap.")

    # --- TABS ANALISIS ---
    st.markdown("---")
    tab1, tab2 = st.tabs(["📝 Kesimpulan Analisis", "💻 Kode Algoritma"])
    
    with tab1:
        pemenang = "Iteratif" if waktu_it < waktu_rek else "Rekursif"
        st.markdown(f"""
        <div class="info-container">
            <h4 style="color: var(--text-color); margin-top: 0;">Analisis Efisiensi</h4>
            <p style="color: var(--text-color);">Pada input <b>{n}</b>, metode <b>{pemenang}</b> bekerja lebih cepat.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.table(pd.DataFrame({
            "Aspek": ["Time Complexity", "Space Complexity", "Metode"],
            "Iteratif": ["O(n)", "O(1)", "Looping"],
            "Rekursif": ["O(n)", "O(n)", "Stacking"]
        }))

    with tab2:
        st.code(f"def iteratif(n):\n    # Looping 1 to n\ndef rekursif(n, i):\n    # Callback self", language="python")
