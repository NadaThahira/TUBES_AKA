
import sys
sys.setrecursionlimit(15000) # Menaikkan batas tumpukan memori

import streamlit as st
import time
import matplotlib.pyplot as plt
import sys

# Meningkatkan limit rekursi untuk input yang lebih besar
sys.setrecursionlimit(20000)

# 1. Fungsi Iteratif
def sum_even_factors_iterative(n):
    total = 0
    for i in range(1, n + 1):
        if n % i == 0 and i % 2 == 0:
            total += i
    return total

# 2. Fungsi Rekursif
def sum_even_factors_recursive(n, current=1):
    if current > n:
        return 0
    
    current_val = 0
    if n % current == 0 and current % 2 == 0:
        current_val = current
        
    return current_val + sum_even_factors_recursive(n, current + 1)

# UI Streamlit
st.title("Analisis Kompleksitas: Faktor Genap")
st.write("Membandingkan efisiensi algoritma Iteratif vs Rekursif")

n_input = st.number_input("Masukkan bilangan (n):", min_value=1, value=100)

if st.button("Hitung & Bandingkan"):
    # Test Iteratif
    start_iter = time.perf_counter()
    res_iter = sum_even_factors_iterative(n_input)
    end_iter = time.perf_counter()
    time_iter = end_iter - start_iter

    # Test Rekursif
    start_rec = time.perf_counter()
    res_rec = sum_even_factors_recursive(n_input)
    end_rec = time.perf_counter()
    time_rec = end_rec - start_rec

    col1, col2 = st.columns(2)
    col1.metric("Iteratif (Hasil)", res_iter, f"{time_iter:.6f} s")
    col2.metric("Rekursif (Hasil)", res_rec, f"{time_rec:.6f} s")

    # --- Simulasi Grafik Perbandingan ---
    st.subheader("Grafik Running Time (1 sampai 2000)")
    sizes = [1, 10, 50, 100, 500, 1000, 1500, 2000]
    iter_times = []
    rec_times = []

    for s in sizes:
        # Iteratif time
        t0 = time.perf_counter()
        sum_even_factors_iterative(s)
        iter_times.append(time.perf_counter() - t0)
        
        # Rekursif time
        t0 = time.perf_counter()
        sum_even_factors_recursive(s)
        rec_times.append(time.perf_counter() - t0)

    fig, ax = plt.subplots()
    ax.plot(sizes, iter_times, label="Iteratif", marker='o', color = 'navy')
    ax.plot(sizes, rec_times, label="Rekursif", marker='s',  color = 'magenta')
    ax.set_xlabel("Ukuran Input (n)")
    ax.set_ylabel("Waktu (detik)")
    ax.legend()
    st.pyplot(fig)
