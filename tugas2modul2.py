#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tugas 2 Modul 2: Lazy-Functional Programming dengan Generator
EXTENDED: Processing Data Sequence dengan Functional Paradigm

Implementasi menggunakan:
1. Fungsi Generator (dengan yield)
2. Generator Expression
3. List Comprehension (untuk transformasi data yang perlu materialized)
4. Nested List (untuk grouping dan hierarchical data)
5. map() - untuk transformasi pure function
6. filter() - untuk filtering dengan pure function
7. reduce() - untuk aggregation operations
8. Rekursif - untuk processing hierarchical data

Ketentuan:
- Minimal 1 soal dengan fungsi generator
- Minimal 1 soal dengan generator expression  
- Demonstrasi manual dengan while + next() + try-except StopIteration
- Dilarang menggunakan lambda (gunakan pure functions)
- Implementasi deklaratif dengan functional paradigm
"""

from functools import reduce
from typing import List, Dict, Tuple, Any

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
print("EXTENDED: Processing Data Sequence dengan Functional Paradigm")
print("=" * 80)

# ========================================================================================
# PURE FUNCTIONS untuk MAP, FILTER, REDUCE (No Lambda - Functional Paradigm)
# ========================================================================================

def is_active_employee(emp: Dict[str, Any]) -> bool:
    """Pure function: Check if employee is active"""
    return emp.get('status_aktif', False)

def has_invalid_data(emp: Dict[str, Any]) -> bool:
    """Pure function: Check if employee has invalid gaji or bonus"""
    gaji_invalid = not isinstance(emp.get('gaji'), int)
    bonus_invalid = not isinstance(emp.get('bonus'), int)
    return gaji_invalid or bonus_invalid

def has_valid_data(emp: Dict[str, Any]) -> bool:
    """Pure function: Check if employee has valid gaji and bonus"""
    return not has_invalid_data(emp)

def get_employee_name(emp: Dict[str, Any]) -> str:
    """Pure function: Extract employee name"""
    return emp.get('nama', 'Unknown')

def calculate_total_compensation(emp: Dict[str, Any]) -> int:
    """Pure function: Calculate total compensation (gaji + bonus)"""
    gaji = emp.get('gaji', 0) if isinstance(emp.get('gaji'), int) else 0
    bonus = emp.get('bonus', 0) if isinstance(emp.get('bonus'), int) else 0
    return gaji + bonus

def add_compensation(acc: int, emp: Dict[str, Any]) -> int:
    """Pure function: Accumulator for reduce - sum total compensation"""
    return acc + calculate_total_compensation(emp)

def max_compensation(emp1: Dict[str, Any], emp2: Dict[str, Any]) -> Dict[str, Any]:
    """Pure function: Compare two employees and return one with higher compensation"""
    comp1 = calculate_total_compensation(emp1)
    comp2 = calculate_total_compensation(emp2)
    return emp1 if comp1 >= comp2 else emp2

def categorize_by_salary(emp: Dict[str, Any]) -> str:
    """Pure function: Categorize employee by salary range"""
    gaji = emp.get('gaji', 0) if isinstance(emp.get('gaji'), int) else 0
    if gaji >= 5500000:
        return 'Senior'
    elif gaji >= 4500000:
        return 'Mid-Level'
    else:
        return 'Junior'

def create_employee_summary(emp: Dict[str, Any]) -> Dict[str, Any]:
    """Pure function: Transform employee to summary format"""
    return {
        'nama': get_employee_name(emp),
        'kompensasi': calculate_total_compensation(emp),
        'kategori': categorize_by_salary(emp),
        'status': 'Aktif' if is_active_employee(emp) else 'Tidak Aktif'
    }

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
# FITUR BARU 1: ANALISIS DATA DENGAN MAP & FILTER (Pure Functions)
# ========================================================================================

def fitur_map_filter():
    """
    FITUR BARU: Menggunakan map() dan filter() dengan pure functions
    
    ALASAN PENGGUNAAN:
    - map(): Cocok untuk transformasi data 1-to-1 tanpa side effects
    - filter(): Cocok untuk seleksi data berdasarkan kondisi pure function
    - Kedua-duanya lazy evaluation (tidak langsung execute)
    - Deklaratif dan mudah di-compose
    """
    print("\n" + "=" * 80)
    print("FITUR BARU 1: ANALISIS DATA DENGAN MAP & FILTER")
    print("=" * 80)
    
    # Step 1: Filter karyawan aktif dengan data valid menggunakan filter()
    print("\n1. Filtering karyawan aktif dengan data valid (menggunakan filter):")
    print("-" * 50)
    
    # Compose multiple filters (functional composition)
    active_employees = filter(is_active_employee, karyawan)
    valid_active_employees = filter(has_valid_data, active_employees)
    
    print("Filter composition: filter(has_valid_data, filter(is_active_employee, karyawan))")
    
    # Step 2: Transform ke summary format menggunakan map()
    print("\n2. Transform ke summary format (menggunakan map):")
    print("-" * 50)
    
    employee_summaries = map(create_employee_summary, valid_active_employees)
    
    print("Map transformation: map(create_employee_summary, valid_active_employees)")
    print("\nDemonstrasi manual dengan while + next() + try-except:")
    print("-" * 50)
    
    # Demonstrasi manual
    hasil = []
    while True:
        try:
            summary = next(employee_summaries)
            print(f"Yield: {summary}")
            hasil.append(summary)
        except StopIteration:
            print(">>> Iterator sudah selesai!")
            break
    
    print(f"\nTotal karyawan valid & aktif: {len(hasil)}")
    return hasil

# ========================================================================================
# FITUR BARU 2: AGGREGATION DENGAN REDUCE (Pure Functions)
# ========================================================================================

def fitur_reduce_aggregation():
    """
    FITUR BARU: Menggunakan reduce() untuk aggregation operations
    
    ALASAN PENGGUNAAN reduce():
    - Perfect untuk operasi aggregation (sum, max, min, accumulation)
    - Pure function composition untuk fold operations
    - Mengganti imperative loop dengan deklaratif expression
    - Single pass iteration untuk efisiensi
    """
    print("\n" + "=" * 80)
    print("FITUR BARU 2: AGGREGATION DENGAN REDUCE")
    print("=" * 80)
    
    # Filter valid employees first
    valid_employees = list(filter(has_valid_data, karyawan))
    
    # 1. Total kompensasi menggunakan reduce
    print("\n1. Total kompensasi semua karyawan (reduce):")
    print("-" * 50)
    total_kompensasi = reduce(add_compensation, valid_employees, 0)
    print(f"reduce(add_compensation, valid_employees, 0)")
    print(f"Total kompensasi: Rp {total_kompensasi:,}")
    
    # 2. Karyawan dengan kompensasi tertinggi menggunakan reduce
    print("\n2. Karyawan dengan kompensasi tertinggi (reduce):")
    print("-" * 50)
    if valid_employees:
        top_employee = reduce(max_compensation, valid_employees)
        print(f"reduce(max_compensation, valid_employees)")
        print(f"Top employee: {get_employee_name(top_employee)}")
        print(f"Kompensasi: Rp {calculate_total_compensation(top_employee):,}")
    
    # 3. Rata-rata kompensasi (compose reduce operations)
    print("\n3. Rata-rata kompensasi (composed reduce):")
    print("-" * 50)
    if valid_employees:
        avg_compensation = total_kompensasi // len(valid_employees)
        print(f"Average: Rp {avg_compensation:,}")
    
    return {
        'total': total_kompensasi,
        'top_employee': top_employee if valid_employees else None,
        'average': avg_compensation if valid_employees else 0
    }

# ========================================================================================
# FITUR BARU 3: NESTED LIST & LIST COMPREHENSION untuk GROUPING
# ========================================================================================

def fitur_nested_list_comprehension():
    """
    FITUR BARU: Menggunakan List Comprehension dan Nested List
    
    ALASAN PENGGUNAAN:
    - List Comprehension: Deklaratif, readable, dan efficient untuk transformasi
    - Nested List: Perfect untuk hierarchical/grouped data structure
    - Materialized result (bukan lazy) karena perlu random access untuk grouping
    - Lebih pythonic dan functional dibanding imperative loop
    """
    print("\n" + "=" * 80)
    print("FITUR BARU 3: GROUPING DENGAN NESTED LIST & LIST COMPREHENSION")
    print("=" * 80)
    
    # Step 1: Categorize employees by salary level using list comprehension
    print("\n1. Kategorisasi karyawan (List Comprehension):")
    print("-" * 50)
    
    # List comprehension untuk filtering dan categorization
    senior = [emp for emp in karyawan if categorize_by_salary(emp) == 'Senior' and is_active_employee(emp)]
    mid_level = [emp for emp in karyawan if categorize_by_salary(emp) == 'Mid-Level' and is_active_employee(emp)]
    junior = [emp for emp in karyawan if categorize_by_salary(emp) == 'Junior' and is_active_employee(emp)]
    
    print(f"Senior (>= 5.5M): {[get_employee_name(e) for e in senior]}")
    print(f"Mid-Level (4.5M-5.5M): {[get_employee_name(e) for e in mid_level]}")
    print(f"Junior (< 4.5M): {[get_employee_name(e) for e in junior]}")
    
    # Step 2: Create nested list structure [category, [employees]]
    print("\n2. Nested List Structure (Hierarchical Data):")
    print("-" * 50)
    
    # Nested list: [[category, count, [employee_names]]]
    grouped_data = [
        ['Senior', len(senior), [get_employee_name(e) for e in senior]],
        ['Mid-Level', len(mid_level), [get_employee_name(e) for e in mid_level]],
        ['Junior', len(junior), [get_employee_name(e) for e in junior]]
    ]
    
    # Display nested structure
    for category, count, names in grouped_data:
        print(f"{category:10} | Count: {count} | Names: {names}")
    
    # Step 3: Flattened summary using nested list comprehension
    print("\n3. Flattened Summary (Nested List Comprehension):")
    print("-" * 50)
    
    # Nested list comprehension: flatten and transform
    flat_summary = [
        f"{name} ({category})"
        for category, _, names in grouped_data
        for name in names
    ]
    
    print("Nested comprehension: [f'{name} ({cat})' for cat, _, names in data for name in names]")
    print(f"Result: {flat_summary}")
    
    return grouped_data

# ========================================================================================
# FITUR BARU 4: RECURSIVE PROCESSING untuk HIERARCHICAL DATA
# ========================================================================================

def calculate_recursive_sum(employees: List[Dict[str, Any]], index: int = 0) -> int:
    """
    Pure recursive function: Calculate total compensation recursively
    
    ALASAN PENGGUNAAN REKURSIF:
    - Elegant untuk processing sequential data tanpa explicit loop
    - Pure function (no side effects)
    - Functional paradigm (immutable, declarative)
    - Base case + recursive case pattern
    """
    # Base case: reached end of list
    if index >= len(employees):
        return 0
    
    # Recursive case: current + rest
    current_compensation = calculate_total_compensation(employees[index])
    rest_compensation = calculate_recursive_sum(employees, index + 1)
    
    return current_compensation + rest_compensation

def filter_recursive(employees: List[Dict[str, Any]], predicate, index: int = 0, 
                    accumulated: List[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
    """
    Pure recursive function: Filter employees recursively
    
    ALASAN PENGGUNAAN REKURSIF:
    - Demonstrasi functional filtering tanpa built-in filter()
    - Tail recursion pattern (dengan accumulator)
    - Pure function composition
    """
    if accumulated is None:
        accumulated = []
    
    # Base case: processed all employees
    if index >= len(employees):
        return accumulated
    
    # Recursive case: check predicate and accumulate
    current = employees[index]
    if predicate(current):
        new_accumulated = accumulated + [current]  # Immutable append
    else:
        new_accumulated = accumulated
    
    return filter_recursive(employees, predicate, index + 1, new_accumulated)

def fitur_recursive_processing():
    """
    FITUR BARU: Recursive processing untuk demonstrasi functional paradigm
    """
    print("\n" + "=" * 80)
    print("FITUR BARU 4: RECURSIVE PROCESSING (Functional Paradigm)")
    print("=" * 80)
    
    # Filter valid employees recursively
    valid_employees = filter_recursive(karyawan, has_valid_data)
    
    print("\n1. Recursive Filtering:")
    print("-" * 50)
    print(f"filter_recursive(karyawan, has_valid_data)")
    print(f"Valid employees: {[get_employee_name(e) for e in valid_employees]}")
    
    # Calculate total compensation recursively
    print("\n2. Recursive Summation:")
    print("-" * 50)
    total = calculate_recursive_sum(valid_employees)
    print(f"calculate_recursive_sum(valid_employees)")
    print(f"Total compensation: Rp {total:,}")
    
    # Compare with reduce
    total_reduce = reduce(add_compensation, valid_employees, 0)
    print(f"\nVerification with reduce: Rp {total_reduce:,}")
    print(f"Match: {total == total_reduce} ✅")
    
    return {
        'valid_employees': valid_employees,
        'total_compensation': total
    }

# ========================================================================================
# MAIN EXECUTION
# ========================================================================================

def main():
    """
    Fungsi utama untuk menjalankan semua soal dengan demonstrasi generator
    dan fitur-fitur baru processing data sequence
    """
    try:
        print("Memulai pengolahan data karyawan dengan Lazy-Functional Programming...")
        print(f"Total data karyawan: {len(karyawan)}")
        
        # ===== SOAL ORIGINAL: GENERATOR =====
        print("\n" + "=" * 80)
        print("PART 1: ORIGINAL - GENERATOR IMPLEMENTATION")
        print("=" * 80)
        
        hasil_1 = soal_1()
        hasil_2 = soal_2()
        hasil_3 = soal_3()
        
        # ===== FITUR BARU: PROCESSING DATA SEQUENCE =====
        print("\n" + "=" * 80)
        print("PART 2: NEW FEATURES - DATA SEQUENCE PROCESSING")
        print("=" * 80)
        
        fitur_1 = fitur_map_filter()
        fitur_2 = fitur_reduce_aggregation()
        fitur_3 = fitur_nested_list_comprehension()
        fitur_4 = fitur_recursive_processing()
        
        # ===== SUMMARY =====
        print("\n" + "=" * 80)
        print("RANGKUMAN HASIL PENGOLAHAN DATA")
        print("=" * 80)
        
        print("\n📊 ORIGINAL FEATURES (Generator):")
        print(f"  1. Karyawan aktif: {len(hasil_1)} orang")
        print(f"  2. Karyawan data invalid: {len(hasil_2)} orang - {hasil_2}")
        print(f"  3. Karyawan kontribusi valid: {len(hasil_3)} orang")
        
        print("\n🚀 NEW FEATURES (Data Sequence Processing):")
        print(f"  4. Map & Filter: {len(fitur_1)} employee summaries created")
        print(f"  5. Reduce Aggregation:")
        print(f"     - Total kompensasi: Rp {fitur_2['total']:,}")
        print(f"     - Top employee: {get_employee_name(fitur_2['top_employee'])} "
              f"(Rp {calculate_total_compensation(fitur_2['top_employee']):,})")
        print(f"     - Average: Rp {fitur_2['average']:,}")
        print(f"  6. Nested List Grouping: {len(fitur_3)} categories")
        print(f"  7. Recursive Processing: {len(fitur_4['valid_employees'])} employees, "
              f"Total: Rp {fitur_4['total_compensation']:,}")
        
        print("\n" + "=" * 80)
        print("ANALISIS IMPLEMENTASI TEKNIK FUNCTIONAL PROGRAMMING")
        print("=" * 80)
        
        print("\n✅ GENERATOR (Lazy Evaluation):")
        print("  • Generator Expression - Lazy filtering (Soal 1)")
        print("  • Fungsi Generator dengan yield - Lazy validation (Soal 2)")
        print("  • Fungsi Generator dengan yield - Lazy computation (Soal 3)")
        print("  • Semua menggunakan while + next() + try-except StopIteration")
        
        print("\n✅ MAP & FILTER (Functional Transformation):")
        print("  • map() - Transform data dengan pure function (create_employee_summary)")
        print("  • filter() - Seleksi data dengan pure predicates (is_active, has_valid_data)")
        print("  • Function composition - Chain multiple filters")
        print("  • Lazy evaluation - Tidak execute sampai diminta")
        
        print("\n✅ REDUCE (Aggregation):")
        print("  • reduce() dengan add_compensation - Total kompensasi")
        print("  • reduce() dengan max_compensation - Find maximum")
        print("  • Pure function accumulator - No side effects")
        print("  • Single-pass iteration - Efficient")
        
        print("\n✅ LIST COMPREHENSION & NESTED LIST:")
        print("  • List comprehension - Deklaratif filtering & transformation")
        print("  • Nested list - Hierarchical data structure (grouping)")
        print("  • Nested comprehension - Flatten multi-level data")
        print("  • Materialized result - Random access untuk grouping")
        
        print("\n✅ RECURSIVE (Functional Paradigm):")
        print("  • Recursive filtering - Alternative to filter() tanpa loop")
        print("  • Recursive summation - Calculate total tanpa iteration")
        print("  • Pure functions - Immutable, no side effects")
        print("  • Base case + recursive case pattern")
        
        print("\n" + "=" * 80)
        print("ALASAN PEMILIHAN TEKNIK")
        print("=" * 80)
        
        print("\n🎯 Generator vs List Comprehension:")
        print("  • Generator: Untuk lazy evaluation, memory efficient, one-time iteration")
        print("  • List Comprehension: Untuk materialized data, random access, reusable")
        
        print("\n🎯 Map/Filter vs List Comprehension:")
        print("  • Map/Filter: Functional composition, lazy evaluation, pure function chains")
        print("  • List Comprehension: Lebih pythonic, readable, integrated filtering+mapping")
        
        print("\n🎯 Reduce vs Recursive:")
        print("  • Reduce: Built-in, optimized, standard aggregation operations")
        print("  • Recursive: Educational, pure functional paradigm, custom logic")
        
        print("\n🎯 Nested List:")
        print("  • Perfect untuk hierarchical/grouped data")
        print("  • Preserves structure untuk multi-level access")
        
        print("\n" + "=" * 80)
        print("KEUNTUNGAN FUNCTIONAL PROGRAMMING")
        print("=" * 80)
        print("✅ Pure Functions: Predictable, testable, no side effects")
        print("✅ Immutable Data: Thread-safe, easier reasoning")
        print("✅ Declarative: Apa yang ingin dicapai, bukan bagaimana")
        print("✅ Composable: Functions bisa di-chain dengan mudah")
        print("✅ Lazy Evaluation: Memory & CPU efficient")
        print("✅ No Lambda: Pure named functions untuk better debugging")
        
    except Exception as e:
        print(f"Error dalam eksekusi: {e}")
        raise

if __name__ == "__main__":
    main()
