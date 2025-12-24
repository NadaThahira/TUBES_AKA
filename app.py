import time
import matplotlib.pyplot as plt

# ==================================================
# ALGORITMA ITERATIF
# ==================================================
def jumlah_faktor_genap_iteratif(n):
    """
    Menghitung jumlah faktor genap dari n
    menggunakan metode iteratif.
    Kompleksitas waktu: O(n)
    """
    total = 0
    for i in range(1, n + 1):
        if n % i == 0 and i % 2 == 0:
            total += i
    return total


# ==================================================
# ALGORITMA REKURSIF
# ==================================================
def jumlah_faktor_genap_rekursif(n, i):
    """
    Menghitung jumlah faktor genap dari n
    menggunakan metode rekursif.
    Kompleksitas waktu: O(n)
    """
    if i == 0:
        return 0

    if n % i == 0 and i % 2 == 0:
        return i + jumlah_faktor_genap_rekursif(n, i - 1)
    else:
        return jumlah_faktor_genap_rekursif(n, i - 1)


# ==================================================
# ANALISIS RUNNING TIME
# ==================================================
def analisis_running_time():
    # Ukuran input yang diuji
    input_sizes = [1, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000]

    waktu_iteratif = []
    waktu_rekursif = []

    for n in input_sizes:
        # Uji iteratif
        start = time.time()
        jumlah_faktor_genap_iteratif(n)
        end = time.time()
        waktu_iteratif.append(end - start)

        # Uji rekursif
        start = time.time()
        jumlah_faktor_genap_rekursif(n, n)
        end = time.time()
        waktu_rekursif.append(end - start)

    return input_sizes, waktu_iteratif, waktu_rekursif


# ==================================================
# PROGRAM UTAMA
# ==================================================
if __name__ == "__main__":
    print("=== ANALISIS KOMPLEKSITAS ALGORITMA ===")
    print("Penjumlahan Faktor Genap (Iteratif vs Rekursif)\n")

    # Menjalankan analisis
    ukuran, iteratif, rekursif = analisis_running_time()

    # Menampilkan hasil dalam bentuk tabel sederhana
    print("Ukuran Input | Iteratif (detik) | Rekursif (detik)")
    print("-" * 50)
    for i in range(len(ukuran)):
        print(f"{ukuran[i]:11} | {iteratif[i]:16.6f} | {rekursif[i]:16.6f}")

    # ==================================================
    # MEMBUAT GRAFIK
    # ==================================================
    plt.figure()
    plt.plot(ukuran, iteratif, label="Iteratif")
    plt.plot(ukuran, rekursif, label="Rekursif")

    plt.xlabel("Ukuran Input (n)")
    plt.ylabel("Waktu Eksekusi (detik)")
    plt.title("Perbandingan Running Time Algoritma")
    plt.legend()
    plt.grid(True)

    plt.show()
