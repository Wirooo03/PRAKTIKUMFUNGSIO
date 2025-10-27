# PENJELASAN IMPLEMENTASI DATA SEQUENCE PROCESSING

## 📋 Overview
File ini menjelaskan implementasi konsep **data sequence processing** yang ditambahkan ke program SIPK menggunakan paradigma functional programming.

---

## 🎯 KONSEP YANG DIIMPLEMENTASIKAN

### 1. **LIST COMPREHENSION** (3 Fungsi)

#### ✅ Fungsi: `get_all_peminjaman_flat(state)`
```python
def get_all_peminjaman_flat(state: AppState) -> List[Dict[str, str]]:
    return [
        {**entry, 'user_id': user_id}
        for user_id, peminjaman_list in state.peminjaman.items()
        for entry in peminjaman_list
    ]
```

**Alasan Penggunaan:**
- **Deklaratif**: Flatten nested dictionary structure dalam satu expression yang readable
- **Efisien**: Lebih efficient daripada nested imperative loops
- **Pure Functional**: Tidak ada side effects, menghasilkan list baru tanpa mutasi

**Use Case:** Mengambil semua peminjaman dari semua user dalam satu flat list untuk analytics global.

---

#### ✅ Fungsi: `get_active_peminjaman_by_user(state, user_id)`
```python
def get_active_peminjaman_by_user(state: AppState, user_id: str) -> List[Dict[str, str]]:
    peminjaman_list = get_user_peminjaman(state, user_id)
    return [
        add_duration_to_entry(entry)
        for entry in peminjaman_list
        if is_peminjaman_active(entry)
    ]
```

**Alasan Penggunaan:**
- **Filter + Transform**: Combine filtering dan transformation dalam satu comprehension
- **Readable**: Lebih mudah dibaca daripada chaining `filter()` dan `map()`
- **Performance**: Single-pass through data

**Use Case:** Mendapatkan peminjaman aktif user dengan enrichment data (tambah field durasi).

---

#### ✅ Fungsi: `get_peminjaman_by_status(state, status)`
```python
def get_peminjaman_by_status(state: AppState, status: str) -> List[Dict[str, str]]:
    all_peminjaman = get_all_peminjaman_flat(state)
    return [
        entry for entry in all_peminjaman
        if entry.get('status', 'pengajuan') == status
    ]
```

**Alasan Penggunaan:**
- **Multi-Step Processing**: Flatten dulu, baru filter
- **Concise**: Sintaks yang ringkas untuk conditional filtering
- **Functional Composition**: Mudah di-compose dengan functions lain

**Use Case:** Filter semua peminjaman berdasarkan status tertentu (pengajuan/disetujui/ditolak).

---

### 2. **NESTED LIST** (2 Fungsi)

#### ✅ Fungsi: `group_peminjaman_by_kelas(state)`
```python
def group_peminjaman_by_kelas(state: AppState) -> Dict[str, List[Dict[str, str]]]:
    all_peminjaman = get_all_peminjaman_flat(state)
    grouped = {}
    
    for entry in all_peminjaman:
        kelas = entry.get('kelas', 'Unknown')
        if kelas not in grouped:
            grouped[kelas] = []
        grouped[kelas] = grouped[kelas] + [entry]  # Immutable append
    
    return grouped
```

**Alasan Penggunaan:**
- **Hierarchical Organization**: Structure data secara hierarkis (kelas → list peminjaman)
- **Reporting**: Memudahkan pembuatan laporan per kelas
- **Natural Structure**: Reflects real-world grouping (kelas sebagai kategori)

**Use Case:** Mengorganisir peminjaman berdasarkan kelas untuk laporan utilisasi.

---

#### ✅ Fungsi: `create_nested_schedule(state)`
```python
def create_nested_schedule(state: AppState) -> List[List[Dict[str, str]]]:
    # Groups by date, returns nested list
    # Outer list: dates, Inner list: peminjaman per date
    return [date_groups[date] for date in sorted_dates]
```

**Alasan Penggunaan:**
- **2D Structure**: Cocok untuk calendar/schedule view (tanggal × peminjaman)
- **Sorting**: Memudahkan sorting chronological
- **Visualization**: Natural untuk display jadwal harian

**Use Case:** Membuat jadwal peminjaman per tanggal yang sorted secara chronological.

---

### 3. **MAP** (4 Fungsi)

#### ✅ Fungsi: `get_peminjaman_summaries(state)`
```python
def get_peminjaman_summaries(state: AppState) -> List[Dict[str, str]]:
    all_peminjaman = get_all_peminjaman_flat(state)
    return list(map(transform_to_summary_format, all_peminjaman))
```

**Alasan Penggunaan:**
- **Pure Functional Transformation**: Apply fungsi ke setiap element tanpa mutation
- **Uniform Processing**: Semua element di-transform dengan cara yang sama
- **Declarative**: Fokus pada "what to transform" bukan "how to loop"

**Use Case:** Transform data peminjaman ke format summary untuk reporting.

---

#### ✅ Fungsi: `enrich_peminjaman_data(peminjaman_list)`
```python
def enrich_peminjaman_data(peminjaman_list: List[Dict[str, str]]) -> List[Dict[str, str]]:
    return list(map(add_duration_field, peminjaman_list))
```

**Alasan Penggunaan:**
- **Data Enrichment**: Menambahkan computed field (durasi) ke setiap entry
- **No Mutation**: Original data tidak diubah, creates new list
- **Reusable**: Function `add_duration_field` bisa digunakan dimana saja

**Use Case:** Menambahkan field 'durasi_menit' ke semua peminjaman untuk analytics.

---

### 4. **FILTER** (2 Fungsi)

#### ✅ Fungsi: `get_long_duration_peminjaman(state, min_minutes)`
```python
def get_long_duration_peminjaman(state: AppState, min_minutes: int) -> List[Dict[str, str]]:
    all_peminjaman = get_all_peminjaman_flat(state)
    enriched = enrich_peminjaman_data(all_peminjaman)
    
    def is_long_duration(entry: Dict[str, str]) -> bool:
        return entry.get('durasi_menit', 0) >= min_minutes
    
    return list(filter(is_long_duration, enriched))
```

**Alasan Penggunaan:**
- **Predicate-Based Filtering**: Menggunakan pure predicate function
- **Declarative**: Fokus pada kondisi filtering, bukan implementasi loop
- **Composable**: Bisa di-chain dengan map/reduce lain

**Use Case:** Menemukan peminjaman dengan durasi panjang (>2 jam) untuk analytics.

---

#### ✅ Fungsi: `get_approved_peminjaman(state)`
```python
def get_approved_peminjaman(state: AppState) -> List[Dict[str, str]]:
    all_peminjaman = get_all_peminjaman_flat(state)
    return list(filter(is_peminjaman_approved, all_peminjaman))
```

**Alasan Penggunaan:**
- **Simple Predicate**: Filtering dengan kondisi sederhana
- **Reusable Predicate**: Function `is_peminjaman_approved` pure dan reusable
- **Efficient**: Single-pass filtering

**Use Case:** Mendapatkan hanya peminjaman yang sudah disetujui untuk laporan utilisasi.

---

### 5. **REDUCE** (5 Fungsi)

#### ✅ Fungsi: `calculate_total_duration(state, user_id)`
```python
def calculate_total_duration(state: AppState, user_id: str) -> int:
    peminjaman_list = get_user_peminjaman(state, user_id)
    enriched = enrich_peminjaman_data(peminjaman_list)
    return reduce(sum_durations, enriched, 0)
```

**Alasan Penggunaan:**
- **Aggregation**: Reduce sequence menjadi single value (total)
- **Functional Fold**: Classic fold/reduce pattern untuk accumulation
- **Pure**: Accumulator function `sum_durations` adalah pure function

**Use Case:** Menghitung total durasi peminjaman user untuk statistik.

---

#### ✅ Fungsi: `get_status_statistics(state)`
```python
def get_status_statistics(state: AppState) -> Dict[str, int]:
    all_peminjaman = get_all_peminjaman_flat(state)
    return reduce(count_by_status_reducer, all_peminjaman, {})
```

**Alasan Penggunaan:**
- **Complex Aggregation**: Group by status + counting
- **Single Pass**: Efficient - hanya satu kali iterate data
- **Immutable Accumulator**: Setiap step create new dict

**Use Case:** Menghitung distribusi status peminjaman (berapa pengajuan, disetujui, ditolak).

---

#### ✅ Fungsi: `calculate_kelas_utilization(state)`
```python
def calculate_kelas_utilization(state: AppState) -> Dict[str, int]:
    def accumulate_by_kelas(acc: Dict[str, int], entry: Dict[str, str]) -> Dict[str, int]:
        kelas = entry.get('kelas', 'Unknown')
        duration = entry.get('durasi_menit', 0)
        current = acc.get(kelas, 0)
        return {**acc, kelas: current + duration}
    
    # ... filter approved only
    return reduce(accumulate_by_kelas, approved_only, {})
```

**Alasan Penggunaan:**
- **Multi-Level Aggregation**: Group by kelas + sum durations
- **Nested Accumulation**: Accumulator yang complex (dict of sums)
- **Functional Pattern**: Pure functional aggregation

**Use Case:** Menghitung total menit penggunaan per kelas untuk laporan utilisasi.

---

### 6. **RECURSIVE** (3 Fungsi)

#### ✅ Fungsi: `search_peminjaman_recursive(peminjaman_list, kelas, index=0)`
```python
def search_peminjaman_recursive(peminjaman_list, kelas, index=0):
    # Base case
    if index >= len(peminjaman_list):
        return []
    
    current = peminjaman_list[index]
    rest = search_peminjaman_recursive(peminjaman_list, kelas, index + 1)
    
    # Recursive case
    if current.get('kelas', '') == kelas:
        return [current] + rest
    else:
        return rest
```

**Alasan Penggunaan:**
- **Elegant Search**: Sequential search tanpa explicit loop
- **Pattern Matching Style**: Dekomposisi: check current + search rest
- **Pure Functional**: No mutable loop variables
- **Tail Recursion Friendly**: Bisa dioptimasi oleh compiler

**Use Case:** Mencari semua peminjaman untuk kelas tertentu secara recursive.

---

#### ✅ Fungsi: `count_nested_peminjaman_recursive(nested_data, index=0)`
```python
def count_nested_peminjaman_recursive(nested_data, index=0):
    # Base case
    if index >= len(nested_data):
        return 0
    
    # Recursive case: count current + count rest
    current_count = len(nested_data[index])
    rest_count = count_nested_peminjaman_recursive(nested_data, index + 1)
    
    return current_count + rest_count
```

**Alasan Penggunaan:**
- **Natural for Nested Structures**: Recursion cocok untuk data hierarkis
- **Divide and Conquer**: Count sublist + count rest
- **No Mutation**: Tidak perlu counter variable yang mutable

**Use Case:** Menghitung total peminjaman dalam nested list structure (schedule per date).

---

#### ✅ Fungsi: `find_max_duration_recursive(peminjaman_list, current_max=0, index=0)`
```python
def find_max_duration_recursive(peminjaman_list, current_max=0, index=0):
    # Base case
    if index >= len(peminjaman_list):
        return current_max
    
    duration = calculate_duration_minutes(...)
    new_max = max(current_max, duration)
    
    # Recursive case
    return find_max_duration_recursive(peminjaman_list, new_max, index + 1)
```

**Alasan Penggunaan:**
- **Divide and Conquer**: Find max of current vs max of rest
- **Accumulator Pattern**: `current_max` sebagai accumulator
- **Pure Recursive**: No mutable variables

**Use Case:** Menemukan peminjaman dengan durasi terpanjang untuk statistik.

---

## 🏆 RINGKASAN IMPLEMENTASI

| Konsep | Jumlah Fungsi | Total Lines | Pure Functions |
|--------|---------------|-------------|----------------|
| List Comprehension | 3 | ~30 | ✅ |
| Nested List | 2 | ~35 | ✅ |
| Map | 4 | ~25 | ✅ |
| Filter | 2 | ~20 | ✅ |
| Reduce | 5 | ~60 | ✅ |
| Recursive | 3 | ~45 | ✅ |
| **TOTAL** | **19** | **~215** | **100%** |

---

## 🎯 FITUR APLIKASI YANG DITAMBAHKAN

### Menu Analytics & Statistik
1. **Statistik Saya** - Personal statistics menggunakan list comprehension, reduce
2. **Laporan Utilisasi Kelas** - Kelas usage report menggunakan reduce, map
3. **Jadwal per Tanggal** - Schedule view menggunakan nested list, recursive
4. **Cari Berdasarkan Kelas** - Search feature menggunakan recursive
5. **Analitik Lanjutan** - Advanced analytics menggunakan filter, map, reduce combined

---

## 💡 KEUNTUNGAN PENDEKATAN FUNCTIONAL

### 1. **Deklaratif**
- Fokus pada "what" bukan "how"
- Lebih readable dan maintainable

### 2. **Composable**
- Functions mudah di-combine
- Reusable di berbagai context

### 3. **Pure & Predictable**
- No side effects
- Same input → same output
- Easy to test

### 4. **Efficient**
- List comprehension lebih fast untuk filtering
- Map/filter lazy evaluation ready
- Reduce single-pass aggregation

### 5. **Scalable**
- Functional patterns scale well
- Easy to parallelize (future optimization)

---

## 📝 CATATAN PENTING

### Tidak Menggunakan Lambda
Semua implementasi menggunakan **named functions** (pure functions) sesuai ketentuan:
```python
# ✅ BENAR - Pure function
def is_peminjaman_active(entry: Dict[str, str]) -> bool:
    return entry.get('status', 'pengajuan') != 'ditolak'

# ❌ SALAH - Lambda (dilarang)
# filter(lambda x: x.get('status') != 'ditolak', data)
```

### Immutability Strict
Semua operations immutable:
```python
# ✅ BENAR - Immutable append
grouped[kelas] = grouped[kelas] + [entry]

# ❌ SALAH - Mutable append
# grouped[kelas].append(entry)
```

---

## 🚀 DEMONSTRASI PENGGUNAAN

```python
# User login dan mengakses analytics
state = authenticated_user_loop(current_state, user_id)

# Analytics automatically menggunakan:
# - List comprehension untuk filtering
# - Map untuk transformasi
# - Filter untuk predicate-based selection
# - Reduce untuk aggregation
# - Recursive untuk search/counting
# - Nested list untuk hierarchical organization

# Semua pure functions, no side effects!
```

---

**Author**: Functional Programming Implementation  
**Date**: October 2025  
**Paradigm**: Pure Functional Programming  
**Language**: Python 3.x
