import streamlit as st
import time
import matplotlib.pyplot as plt

# ==================================================
# KONFIGURASI HALAMAN
# ==================================================
st.set_page_config(page_title="Analisis Algoritma", layout="centered")

# CSS Custom untuk memperbesar font label metrik dan mengatur gaya kotak
st.markdown("""
    <style>
    [data-testid="stMetricLabel"] {
        font-size: 1.3rem !important;
        font-weight: bold !important;
        color: #31333F;
    }
    .result-box {
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 10px;
    }
    .rekursif-box {
        background-color: #E1E8F0;
        border: 1px solid #1E3A8A;
    }
    .iteratif-box {
        background-color: #FCE4EC;
        border: 1px solid #C13584;
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
    if i == 0:
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
    # Proses Hitung & Waktu
    start_iter = time.time()
    hasil_iteratif = jumlah_faktor_genap_iteratif(n)
    waktu_iteratif = time.time() - start_iter

    start_rek = time.time()
    hasil_rekursif = jumlah_faktor_genap_rekursif(n, n)
    waktu_rekursif = time.time() - start_rek

    # ==================================================
    # TAMPILAN HASIL (REKURSIF | ITERATIF)
    # ==================================================
    st.markdown("### 🏁 Hasil Penjumlahan")
    col_res1, col_res2 = st.columns(2)

    with col_res1:
        st.markdown(f"""
            <div class="result-box rekursif-box">
                <small>REKURSIF</small>
                <h2 style="margin:0; color:#1E3A8A;">{hasil_rekursif}</h2>
            </div>
            """, unsafe_allow_html=True)

    with col_res2:
        st.markdown(f"""
            <div class="result-box iteratif-box">
                <small>ITERATIF</small>
                <h2 style="margin:0; color:#C13584;">{hasil_iteratif}</h2>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ==================================================
    # PERBANDINGAN WAKTU (LABEL DIPERBESAR)
    # ==================================================
    st.markdown("### ⏱️ Waktu Eksekusi")
    col1, col2, col3 = st.columns(3)
    selisih = abs(waktu_rekursif - waktu_iteratif)

    with col1:
        st.metric(label="Algoritma Iteratif", value=f"{waktu_iteratif:.6f} s")

    with col2:
        st.metric(label="Algoritma Rekursif", value=f"{waktu_rekursif:.6f} s")

    with col3:
        st.metric(label="Selisih Waktu", value=f"{selisih:.6f} s")

    # ==================================================
    # GRAFIK ANALISIS
    # ==================================================
    st.markdown("---")
    st.markdown("### 📈 Grafik Perbandingan Running Time")

    input_sizes = [1, 10, 20, 50, 100, 200, 500, 1000]
    waktu_iter_list = []
    waktu_rek_list = []

    for ukuran in input_sizes:
        # Benchmark Iteratif
        t0 = time.time()
        jumlah_faktor_genap_iteratif(ukuran)
        waktu_iter_list.append(time.time() - t0)

        # Benchmark Rekursif
        t1 = time.time()
        jumlah_faktor_genap_rekursif(ukuran, ukuran)
        waktu_rek_list.append(time.time() - t1)

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(input_sizes, waktu_iter_list, marker="o", label="Iteratif", color='magenta', linewidth=2)
    ax.plot(input_sizes, waktu_rek_list, marker="o", label="Rekursif", color='navy', linewidth=2)
    
    ax.set_xlabel("Ukuran Input (n)")
    ax.set_ylabel("Waktu (detik)")
    ax.legend()
    ax.grid(True, linestyle='--', alpha=0.6)
    
    st.pyplot(fig)
