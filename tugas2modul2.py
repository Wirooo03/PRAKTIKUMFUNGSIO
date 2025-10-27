#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tugas 2 Modul 2: Lazy-Functional Programming dengan Generator
Implementasi menggunakan kedua jenis generator:
1. Fungsi Generator (dengan yield)
2. Generator Expression

Ketentuan:
- Minimal 1 soal dengan fungsi generator
- Minimal 1 soal dengan generator expression  
- Demonstrasi manual dengan while + next() + try-except StopIteration
- Dilarang menggunakan for loop untuk output
"""

# Data karyawan yang akan diolah
karyawan = [
    {'nama': 'Zaky', 'gaji': 5000000, 'bonus': 1000000, 'status_aktif': True},
    {'nama': 'Fitra', 'gaji': 4500000, 'bonus': None, 'status_aktif': True},
    {'nama': 'Fia', 'gaji': 5200000, 'bonus': 500000, 'status_aktif': True},
    {'nama': 'Adit', 'gaji': 6000000, 'bonus': 1000000, 'status_aktif': False},
    {'nama': 'Faizal', 'gaji': 4000000, 'bonus': 700000, 'status_aktif': True},
    {'nama': 'Radan', 'gaji': 5500000, 'bonus': 'tidak ada', 'status_aktif': True},
    {'nama': 'Wempy', 'gaji': 4800000, 'bonus': 600000, 'status_aktif': True},
    {'nama': 'Alfi', 'gaji': 5000000, 'bonus': 800000, 'status_aktif': False},
    {'nama': 'Hakim', 'gaji': 5200000, 'bonus': 1000000, 'status_aktif': True},
    {'nama': 'Rama', 'gaji': None, 'bonus': 750000, 'status_aktif': True}
]

print("=" * 80)
print("TUGAS 2 MODUL 2: LAZY-FUNCTIONAL PROGRAMMING DENGAN GENERATOR")
print("=" * 80)

# ========================================================================================
# SOAL 1: Filter Karyawan Aktif (Generator Expression)
# ========================================================================================

def soal_1():
    print("\n" + "=" * 50)
    print("SOAL 1: FILTER KARYAWAN AKTIF (Generator Expression)")
    print("=" * 50)
    print("Menggunakan Generator Expression untuk filter karyawan dengan status_aktif == True")
    
    # Generator Expression - Lazy evaluation, hanya menghasilkan nilai saat diminta
    karyawan_aktif_gen = (k for k in karyawan if k['status_aktif'] == True)
    
    print(f"Generator object: {karyawan_aktif_gen}")
    print(f"Type: {type(karyawan_aktif_gen)}")
    print("\nDemonstrasi manual dengan while + next() + try-except:")
    print("-" * 50)
    
    # Demonstrasi manual sesuai ketentuan
    hasil = []
    while True:
        try:
            next_karyawan = next(karyawan_aktif_gen)
            print(f"Yield: {next_karyawan}")
            hasil.append(next_karyawan)
        except StopIteration:
            print(">>> Iterator sudah selesai! Generator exhausted.")
            break
    
    print(f"\nHasil akhir: {len(hasil)} karyawan aktif ditemukan")
    return hasil

# ========================================================================================
# SOAL 2: Nama Karyawan dengan Data Invalid (Fungsi Generator)
# ========================================================================================

def generate_invalid_employees(employees):
    """
    Fungsi Generator untuk menghasilkan nama karyawan dengan data tidak valid.
    Menggunakan yield untuk lazy evaluation - nilai dihasilkan satu per satu saat diminta.
    
    Args:
        employees: List data karyawan
        
    Yields:
        str: Nama karyawan dengan gaji atau bonus bukan integer
    """
    print(">>> Memulai generator untuk mencari data invalid...")
    
    for emp in employees:
        # Cek apakah gaji bukan integer (None atau tipe lain)
        gaji_invalid = not isinstance(emp['gaji'], int)
        
        # Cek apakah bonus bukan integer (None, string, atau tipe lain)  
        bonus_invalid = not isinstance(emp['bonus'], int)
        
        # Yield nama jika ada data yang invalid
        if gaji_invalid or bonus_invalid:
            print(f">>> Data invalid ditemukan: {emp['nama']} (gaji: {emp['gaji']}, bonus: {emp['bonus']})")
            yield emp['nama']

def soal_2():
    print("\n" + "=" * 50)
    print("SOAL 2: NAMA KARYAWAN DATA INVALID (Fungsi Generator)")
    print("=" * 50)
    print("Menggunakan Fungsi Generator dengan yield untuk lazy evaluation")
    
    # Buat generator object dari fungsi generator
    invalid_gen = generate_invalid_employees(karyawan)
    
    print(f"Generator object: {invalid_gen}")
    print(f"Type: {type(invalid_gen)}")
    print("\nDemonstrasi manual dengan while + next() + try-except:")
    print("-" * 50)
    
    # Demonstrasi manual sesuai ketentuan
    hasil = []
    while True:
        try:
            invalid_name = next(invalid_gen)
            print(f"Output: {invalid_name}")
            hasil.append(invalid_name)
        except StopIteration:
            print(">>> Iterator sudah selesai! Generator exhausted.")
            break
    
    print(f"\nHasil akhir: {len(hasil)} karyawan dengan data invalid")
    return hasil

# ========================================================================================
# SOAL 3: Kontribusi Kompensasi Karyawan (Fungsi Generator)
# ========================================================================================

def calculate_valid_employees_compensation(employees):
    """
    Generator function untuk menghitung data karyawan aktif dengan data valid.
    
    Args:
        employees: List data karyawan
        
    Yields:
        tuple: (nama, kompensasi) untuk karyawan aktif dengan data valid
    """
    print(">>> Generator: Mencari karyawan aktif dengan data valid...")
    
    for emp in employees:
        # Filter: hanya karyawan aktif
        if not emp['status_aktif']:
            continue
            
        # Filter: hanya data valid (gaji dan bonus harus integer)
        if not isinstance(emp['gaji'], int) or not isinstance(emp['bonus'], int):
            print(f">>> Skip {emp['nama']}: data invalid (gaji: {emp['gaji']}, bonus: {emp['bonus']})")
            continue
        
        # Hitung kompensasi total
        kompensasi = emp['gaji'] + emp['bonus']
        print(f">>> Valid: {emp['nama']} - Kompensasi: {kompensasi:,}")
        
        yield (emp['nama'], kompensasi)

def generate_contribution_data(employees):
    """
    Generator function untuk menghitung kontribusi setiap karyawan terhadap total kompensasi.
    Menggunakan lazy evaluation untuk efisiensi memori.
    
    Args:
        employees: List data karyawan
        
    Yields:
        dict: Data kontribusi karyawan dengan format yang diminta
    """
    print(">>> Generator: Memulai perhitungan kontribusi...")
    
    # Pertama, kumpulkan data valid dan hitung total (ini perlu dilakukan dua kali)
    valid_data = list(calculate_valid_employees_compensation(employees))
    total_kompensasi = sum(comp for _, comp in valid_data)
    
    print(f">>> Total kompensasi semua karyawan valid: {total_kompensasi:,}")
    print(">>> Menghitung kontribusi individual...")
    
    # Generator untuk menghasilkan data kontribusi satu per satu
    for nama, kompensasi in valid_data:
        kontribusi_persen = (kompensasi / total_kompensasi) * 100
        
        result = {
            'nama': nama,
            'kompensasi': kompensasi,
            'kontribusi': f"{kontribusi_persen:.2f}%"
        }
        
        print(f">>> Yield kontribusi: {nama} = {kontribusi_persen:.2f}%")
        yield result

def soal_3():
    print("\n" + "=" * 50) 
    print("SOAL 3: KONTRIBUSI KOMPENSASI KARYAWAN (Fungsi Generator)")
    print("=" * 50)
    print("Menggunakan Fungsi Generator dengan yield untuk lazy computation")
    
    # Buat generator object dari fungsi generator
    kontribusi_gen = generate_contribution_data(karyawan)
    
    print(f"Generator object: {kontribusi_gen}")
    print(f"Type: {type(kontribusi_gen)}")
    print("\nDemonstrasi manual dengan while + next() + try-except:")
    print("-" * 50)
    
    # Demonstrasi manual sesuai ketentuan
    hasil = []
    while True:
        try:
            kontribusi_data = next(kontribusi_gen)
            print(f"Output: {kontribusi_data}")
            hasil.append(kontribusi_data)
        except StopIteration:
            print(">>> Iterator sudah selesai! Generator exhausted.")
            break
    
    print(f"\nHasil akhir: {len(hasil)} karyawan dengan kontribusi dihitung")
    return hasil

# ========================================================================================
# MAIN EXECUTION
# ========================================================================================

def main():
    """
    Fungsi utama untuk menjalankan semua soal dengan demonstrasi generator
    """
    try:
        print("Memulai pengolahan data karyawan dengan Lazy-Functional Programming...")
        print(f"Total data karyawan: {len(karyawan)}")
        
        # Jalankan semua soal
        hasil_1 = soal_1()
        hasil_2 = soal_2()
        hasil_3 = soal_3()
        
        # Summary
        print("\n" + "=" * 80)
        print("RANGKUMAN HASIL PENGOLAHAN DATA")
        print("=" * 80)
        print(f"1. Karyawan aktif: {len(hasil_1)} orang")
        print(f"2. Karyawan data invalid: {len(hasil_2)} orang - {hasil_2}")
        print(f"3. Karyawan kontribusi valid: {len(hasil_3)} orang")
        
        print("\n" + "=" * 80)
        print("ANALISIS IMPLEMENTASI GENERATOR")
        print("=" * 80)
        print("✅ Soal 1: Generator Expression - Lazy filtering")
        print("✅ Soal 2: Fungsi Generator dengan yield - Lazy validation")  
        print("✅ Soal 3: Fungsi Generator dengan yield - Lazy computation")
        print("✅ Semua menggunakan while + next() + try-except StopIteration")
        print("✅ Tidak menggunakan for loop untuk output")
        
        print("\nKeuntungan Lazy-Functional Programming:")
        print("- Memory efficient: Data diproses satu per satu, tidak sekaligus")
        print("- CPU efficient: Computation on-demand, hanya saat diminta")
        print("- Scalable: Bisa menangani dataset besar tanpa memory overflow")
        print("- Composable: Generator bisa di-chain dengan generator lain")
        
    except Exception as e:
        print(f"Error dalam eksekusi: {e}")
        raise

if __name__ == "__main__":
    main()
