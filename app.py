import streamlit as st
import time
import matplotlib.pyplot as plt

# KONFIGURASI HALAMAN
st.set_page_config(page_title="Analisis Algoritma", layout="centered")

# CSS Custom untuk mempertegas tulisan dan warna
st.markdown("""
    <style>
    /* Memperbesar dan mempertegas label metrik waktu */
    [data-testid="stMetricLabel"] {
        font-size: 1.5rem !important;
        font-weight: 800 !important;
        color: #FF4B4B !important; /* Warna merah cerah */
        text-transform: uppercase;
    }
    /* Memperbesar angka metrik waktu */
    [data-testid="stMetricValue"] {
        font-size: 2rem !important;
        font-weight: bold !important;
        color: #FFFFFF !important;
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
        background-color: #1E3A8A; /* Biru Tua */
        border-color: #3B82F6;
    }
    .iteratif-box {
        background-color: #880E4F; /* Magenta Tua */
        border-color: #C13584;
    }
    /* Style untuk teks REKURSIF/ITERATIF di dalam kotak */
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
    # Proses Hitung & Waktu
    start_iter = time.time()
    hasil_iteratif = jumlah_faktor_genap_iteratif(n)
    waktu_iteratif = time.time() - start_iter

    start_rek = time.time()
    hasil_rekursif = jumlah_faktor_genap_rekursif(n, n)
    waktu_rekursif = time.time() - start_rek

    # TAMPILAN HASIL (REKURSIF | ITERATIF)
    st.markdown("### 🏁 Hasil Penjumlahan")
    col_res1, col_res2 = st.columns(2)

    with col_res1:
        st.markdown(f"""
            <div class="result-box rekursif-box">
                <p class="label-text">REKURSIF</p>
                <p class="value-text">{hasil_rekursif}</p>
            </div>
            """, unsafe_allow_html=True)

    with col_res2:
        st.markdown(f"""
            <div class="result-box iteratif-box">
                <p class="label-text">ITERATIF</p>
                <p class="value-text">{hasil_iteratif}</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # PERBANDINGAN WAKTU
    st.markdown("### ⏱️ Waktu Eksekusi")
    col1, col2, col3 = st.columns(3)
    selisih = abs(waktu_rekursif - waktu_iteratif)

    with col1:
        st.metric(label="Algoritma Iteratif", value=f"{waktu_iteratif:.6f} s")

    with col2:
        st.metric(label="Algoritma Rekursif", value=f"{waktu_rekursif:.6f} s")

    with col3:
        st.metric(label="Selisih Waktu", value=f"{selisih:.7f} s")

    # GRAFIK ANALISIS
    st.markdown("---")
    st.markdown("### 📈 Grafik Perbandingan Running Time")

    input_sizes = [1, 10, 20, 50, 100, 200, 500, 1000]
    waktu_iter_list = []
    waktu_rek_list = []

    for ukuran in input_sizes:
        t0 = time.time()
        jumlah_faktor_genap_iteratif(ukuran)
        waktu_iter_list.append(time.time() - t0)

        t1 = time.time()
        jumlah_faktor_genap_rekursif(ukuran, ukuran)
        waktu_rek_list.append(time.time() - t1)

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(input_sizes, waktu_rek_list, marker="o", label="Rekursif", color='#1E3A8A', linewidth=2)
    ax.plot(input_sizes, waktu_iter_list, marker="o", label="Iteratif", color='#880E4F', linewidth=2)
    
    ax.set_xlabel("Ukuran Input (n)")
    ax.set_ylabel("Waktu (detik)")
    ax.legend()
    ax.grid(True, linestyle='--', alpha=0.6)
    
    st.pyplot(fig)

    #HASIL ANALISIS (TAMBAHAN BARU)
    st.markdown("### 🧠 Analisis Kompleksitas & Performa")
    
    # Menentukan algoritma mana yang lebih cepat
    pemenang = "Iteratif" if waktu_iteratif < waktu_rekursif else "Rekursif"
    
    st.markdown(f"""
    <div class="analysis-card">
        <h4>1. Analisis Notasi Big-O</h4>
        <ul>
            <li><b>Iteratif:</b> Menggunakan satu <i>loop</i> dari 1 sampai n, sehingga kompleksitasnya adalah <b>O(n)</b>.</li>
            <li><b>Rekursif:</b> Melakukan pemanggilan fungsi sebanyak n kali secara beruntun, kompleksitasnya juga <b>O(n)</b>.</li>
        </ul>
        <h4>2. Perbandingan Efisiensi</h4>
        <p>Berdasarkan pengujian pada n = {n}, algoritma <b>{pemenang}</b> lebih efisien secara waktu.</p>
        <ul>
            <li><b>Iteratif</b> lebih unggul dalam penggunaan memori karena tidak menambah beban <i>stack</i> pemanggilan fungsi.</li>
            <li><b>Rekursif</b> lebih elegan secara penulisan kode namun memiliki risiko <i>RecursionError</i> jika input terlalu besar (n > 1000).</li>
        </ul>
        <h4>3. Interpretasi Grafik</h4>
        <p>Semakin ke kanan arah grafik (n bertambah besar), selisih waktu antara metode <b>Navy (Rekursif)</b> dan <b>Magenta (Iteratif)</b> akan terlihat semakin lebar. 
        Ini membuktikan bahwa pertumbuhan beban kerja sangat berpengaruh pada performa algoritma rekursif di Python.</p>
    </div>
    """, unsafe_allow_html=True)
