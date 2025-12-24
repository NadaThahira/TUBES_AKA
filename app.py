import streamlit as st
import time
import matplotlib.pyplot as plt

# ==================================================
# JUDUL APLIKASI
# ==================================================
st.set_page_config(page_title="Analisis Kompleksitas Algoritma", layout="centered")

st.title("📊 Analisis Kompleksitas Algoritma")
st.subheader("Penjumlahan Faktor Genap (Iteratif vs Rekursif)")
st.markdown("---")

# ==================================================
# DESKRIPSI APLIKASI
# ==================================================
st.markdown("""
Aplikasi ini digunakan untuk menganalisis dan membandingkan **efisiensi algoritma iteratif dan rekursif**
dalam menghitung **jumlah faktor genap dari suatu bilangan**.

Analisis dilakukan berdasarkan:
- ⏱️ Waktu eksekusi (running time)
- 📈 Grafik perbandingan performa
""")

# ==================================================
# ALGORITMA ITERATIF
# ==================================================
def jumlah_faktor_genap_iteratif(n):
    total = 0
    for i in range(1, n + 1):
        if n % i == 0 and i % 2 == 0:
            total += i
    return total

# ==================================================
# ALGORITMA REKURSIF
# ==================================================
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
n = st.number_input(
    "Masukkan bilangan bulat positif:",
    min_value=1,
    step=1,
    value=10
)

# ==================================================
# PERHITUNGAN
# ==================================================
if st.button("🚀 Jalankan Analisis"):
    # Iteratif
    start_iter = time.time()
    hasil_iteratif = jumlah_faktor_genap_iteratif(n)
    waktu_iteratif = time.time() - start_iter

    # Rekursif
    start_rek = time.time()
    hasil_rekursif = jumlah_faktor_genap_rekursif(n, n)
    waktu_rekursif = time.time() - start_rek

    st.success("Perhitungan selesai!")

    # ==================================================
    # OUTPUT HASIL
    # ==================================================
    st.markdown("## 🧮 Hasil Perhitungan")
    st.info(f"Jumlah faktor genap dari bilangan **{n}** adalah **{hasil_iteratif}**")
    
    st.markdown("## ⏱️ Perbandingan Waktu Eksekusi")

    col1, col2, col3 = st.columns(3)
    
    selisih_waktu = abs(waktu_rekursif - waktu_iteratif)
    
    with col1:
        st.metric(
            label="Algoritma Iteratif",
            value=f"{waktu_iteratif:.6f} detik"
        )
    
    with col2:
        st.metric(
            label="Algoritma Rekursif",
            value=f"{waktu_rekursif:.6f} detik"
        )
    
    with col3:
        st.metric(
            label="Selisih Waktu",
            value=f"{selisih_waktu:.6f} detik"
        )
    
    # --------------------------------------------------
    # KESIMPULAN OTOMATIS
    # --------------------------------------------------
    st.markdown("## 🧠 Kesimpulan Otomatis")
    
    if waktu_iteratif < waktu_rekursif:
        st.success(
            "Algoritma **Iteratif** memiliki waktu eksekusi lebih cepat "
            "dibandingkan algoritma Rekursif pada pengujian ini."
        )
    elif waktu_iteratif > waktu_rekursif:
        st.warning(
            "Algoritma **Rekursif** memiliki waktu eksekusi lebih cepat "
            "dibandingkan algoritma Iteratif pada pengujian ini."
        )
    else:
        st.info(
            "Kedua algoritma memiliki waktu eksekusi yang hampir sama "
            "pada pengujian ini."
        )
    
        st.markdown("---")

    # ==================================================
    # ANALISIS RUNNING TIME UNTUK BERBAGAI INPUT
    # ==================================================
    st.markdown("### 📈 Grafik Perbandingan Running Time")

    input_sizes = [1, 10, 20, 50, 100, 200, 500, 1000]
    waktu_iter = []
    waktu_rek = []

    for ukuran in input_sizes:
        start = time.time()
        jumlah_faktor_genap_iteratif(ukuran)
        waktu_iter.append(time.time() - start)

        start = time.time()
        jumlah_faktor_genap_rekursif(ukuran, ukuran)
        waktu_rek.append(time.time() - start)

    # ==================================================
    # GRAFIK
    # ==================================================
   
    fig, ax = plt.subplots()
    
    ax.plot(input_sizes, waktu_iter, marker="o", label="Iteratif", color = 'magenta')
    ax.plot(input_sizes, waktu_rek, marker="o", label="Rekursif", color = 'navy')
    
    ax.set_xlabel("Ukuran Input (n)")
    ax.set_ylabel("Waktu Eksekusi (detik)")
    ax.set_title("Perbandingan Running Time Algoritma")
    ax.legend()
    ax.grid(True)
    
    st.pyplot(fig)
