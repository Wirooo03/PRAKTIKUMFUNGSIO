#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Program CLI: Sistem Informasi Peminjaman Kelas (SIPK) – Login/Register + CRUD
Tema: Peminjaman Kelas per akun (setiap user hanya bisa mengelola datanya sendiri)

Ketentuan yang dipenuhi:
1) Data akun dalam dictionary -> accounts = {id: password}
2) Data profil nested dictionary -> profiles = {id: {"nama":..., "alamat":..., "hp":...}}
3) Daftar menu aplikasi dalam bentuk tuple -> MAIN_MENU (diakses memakai slicing)
4) Register: buat akun (ID & password)
5) Login: hanya akun terdaftar
6) CRUD data (peminjaman kelas) hanya setelah login
7) Validasi input dengan while/try-except
8) Data Tambahan per akun: "peminjaman" bertipe LIST of DICT
   - Alasan memilih LIST: data peminjaman perlu urutan waktu/entri,
     mudah diakses via indeks untuk Update/Delete, dan fleksibel.

Catatan:
- Tiap operasi CRUD hanya mengelola peminjaman milik akun login (key: user_id).
- ROOMS disimpan sebagai TUPLE (immutable, daftar referensi kelas).
- Format tanggal: YYYY-MM-DD ; jam: HH:MM (24 jam).
"""

from typing import Dict, List
from datetime import datetime

# ---------------------------- Penyimpanan Data ---------------------------- #
accounts: Dict[str, str] = {}  # {user_id: password}
profiles: Dict[str, Dict[str, str]] = {}  # {user_id: {"nama":..., "alamat":..., "hp":...}}

# Data tambahan per akun: daftar peminjaman kelas (sequence: LIST of DICT)
# Struktur peminjaman: {"kelas": str, "tanggal": "YYYY-MM-DD", "mulai": "HH:MM", "selesai": "HH:MM", "keperluan": str, "status": "pengajuan"|"disetujui"|"ditolak"}
peminjaman: Dict[str, List[Dict[str, str]]] = {}  # {user_id: [pinjam1, pinjam2, ...]}

# Daftar kelas sebagai TUPLE (referensi statis)
ROOMS = (
    "Kelas-101", "Kelas-102", "Kelas-103",
    "Lab-201", "Lab-202",
    "Aula-301"
)

# ---------------------------- Menu (Tuple + Slicing) ---------------------------- #
MAIN_MENU = (
    "Register",
    "Login",
    "Keluar",
    # elemen ekstra untuk contoh slicing (tidak tampil di awal)
    "Bantuan",
    "Tentang",
)

AUTH_MENU = (
    "Lihat Profil",
    "Ubah Profil",
    "Peminjaman Kelas (CRUD)",
    "Logout",
)

CRUD_MENU = (
    "Ajukan Peminjaman (Create)",
    "Lihat Daftar Peminjaman (Read)",
    "Ubah Peminjaman (Update)",
    "Batalkan Peminjaman (Delete)",
    "Kembali",
)

STATUS_OPSI = ("pengajuan", "disetujui", "ditolak")


# ---------------------------- Utilitas Validasi Input ---------------------------- #
def input_non_kosong(prompt: str) -> str:
    while True:
        s = input(prompt).strip()
        if s:
            return s
        print("Input tidak boleh kosong. Coba lagi.")

def input_pilihan(prompt: str, opsi: List[str]) -> int:
    while True:
        try:
            val = int(input(prompt).strip())
            if 1 <= val <= len(opsi):
                return val
            print(f"Masukkan angka 1..{len(opsi)} sesuai menu.")
        except ValueError:
            print("Masukan harus berupa angka. Coba lagi.")

def valid_tanggal(s: str) -> bool:
    try:
        datetime.strptime(s, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def valid_jam(s: str) -> bool:
    try:
        datetime.strptime(s, "%H:%M")
        return True
    except ValueError:
        return False

def jam_berurutan(mulai: str, selesai: str) -> bool:
    try:
        t1 = datetime.strptime(mulai, "%H:%M")
        t2 = datetime.strptime(selesai, "%H:%M")
        return t2 > t1
    except ValueError:
        return False


# ---------------------------- Fitur Register & Login ---------------------------- #
def register():
    print("\n=== Registrasi Akun Baru ===")
    while True:
        user_id = input_non_kosong("Buat ID (username/NIM): ")
        if user_id in accounts:
            print("ID sudah terdaftar. Gunakan ID lain.")
            continue
        break
    while True:
        pwd = input_non_kosong("Buat Password (min 4 karakter): ")
        if len(pwd) < 4:
            print("Password terlalu pendek (min 4).")
            continue
        break

    accounts[user_id] = pwd
    # Buat profil awal
    nama = input_non_kosong("Nama: ")
    alamat = input_non_kosong("Alamat: ")
    hp = input_non_kosong("No. HP: ")
    profiles[user_id] = {"nama": nama, "alamat": alamat, "hp": hp}

    # Inisialisasi daftar peminjaman user
    peminjaman[user_id] = []

    print(f"Akun '{user_id}' berhasil dibuat!\n")


def login() -> str:
    print("\n=== Login ===")
    user_id = input_non_kosong("ID: ")
    pwd = input_non_kosong("Password: ")
    if user_id in accounts and accounts[user_id] == pwd:
        print(f"Login berhasil. Selamat datang, {profiles[user_id]['nama']}!\n")
        return user_id
    print("ID atau Password salah.\n")
    return ""


# ---------------------------- Fitur Profil ---------------------------- #
def lihat_profil(user_id: str):
    print("\n=== Profil Saya ===")
    p = profiles.get(user_id, {})
    if not p:
        print("Profil tidak ditemukan.")
        return
    print(f"ID     : {user_id}")
    print(f"Nama   : {p.get('nama','-')}")
    print(f"Alamat : {p.get('alamat','-')}")
    print(f"HP     : {p.get('hp','-')}")
    print("")


def ubah_profil(user_id: str):
    print("\n=== Ubah Profil ===")
    p = profiles.get(user_id, {})
    if not p:
        print("Profil tidak ditemukan.")
        return
    nama = input("Nama (kosongkan jika tidak diubah): ").strip()
    alamat = input("Alamat (kosongkan jika tidak diubah): ").strip()
    hp = input("No. HP (kosongkan jika tidak diubah): ").strip()

    if nama:
        p["nama"] = nama
    if alamat:
        p["alamat"] = alamat
    if hp:
        p["hp"] = hp

    profiles[user_id] = p
    print("Profil berhasil diperbarui.\n")


# ---------------------------- Fitur CRUD Peminjaman ---------------------------- #
def tampilkan_peminjaman(user_id: str):
    print("\n=== Daftar Peminjaman Saya ===")
    data = peminjaman.get(user_id, [])
    if not data:
        print("(Belum ada peminjaman)\n")
        return
    for i, d in enumerate(data, start=1):
        print(f"{i}. [{d.get('status','pengajuan').upper():10}] {d.get('kelas','-')} | {d.get('tanggal','-')} {d.get('mulai','-')}-{d.get('selesai','-')}")
        print(f"   Keperluan: {d.get('keperluan','-')}")
    print("")


def pilih_kelas() -> str:
    print("Pilih Kelas:")
    for i, r in enumerate(ROOMS, start=1):
        print(f"{i}. {r}")
    idx = input_pilihan("Masukkan pilihan: ", list(ROOMS))
    return ROOMS[idx - 1]


def input_tanggal() -> str:
    while True:
        tgl = input_non_kosong("Tanggal (YYYY-MM-DD): ")
        if valid_tanggal(tgl):
            return tgl
        print("Format tanggal tidak valid.")


def input_jam_range() -> (str, str):
    while True:
        mulai = input_non_kosong("Jam Mulai (HH:MM): ")
        selesai = input_non_kosong("Jam Selesai (HH:MM): ")
        if not valid_jam(mulai) or not valid_jam(selesai):
            print("Format jam tidak valid.")
            continue
        if not jam_berurutan(mulai, selesai):
            print("Jam selesai harus lebih besar dari jam mulai.")
            continue
        return mulai, selesai


def ajukan_peminjaman(user_id: str):
    print("\n=== Ajukan Peminjaman Kelas ===")
    kls = pilih_kelas()
    tgl = input_tanggal()
    mulai, selesai = input_jam_range()
    kep = input_non_kosong("Keperluan: ")
    entry = {"kelas": kls, "tanggal": tgl, "mulai": mulai, "selesai": selesai, "keperluan": kep, "status": "pengajuan"}
    peminjaman[user_id].append(entry)
    print("Pengajuan peminjaman disimpan.\n")


def ubah_peminjaman(user_id: str):
    print("\n=== Ubah Peminjaman ===")
    data = peminjaman.get(user_id, [])
    if not data:
        print("(Belum ada peminjaman)\n")
        return
    tampilkan_peminjaman(user_id)
    idx = minta_indeks(len(data))
    if idx is None:
        return

    d = data[idx]
    print("Tekan Enter untuk mempertahankan nilai lama.")
    ganti_kelas = input("Ganti kelas? (y/n): ").strip().lower()
    if ganti_kelas == "y":
        d["kelas"] = pilih_kelas()

    s_tgl = input("Tanggal baru (YYYY-MM-DD): ").strip()
    if s_tgl:
        if valid_tanggal(s_tgl):
            d["tanggal"] = s_tgl
        else:
            print("Format tanggal salah. Dibiarkan lama.")

    s_mulai = input("Jam Mulai baru (HH:MM): ").strip()
    s_selesai = input("Jam Selesai baru (HH:MM): ").strip()
    if s_mulai or s_selesai:
        # jika salah satu diisi, keduanya harus valid dan berurutan
        if s_mulai and s_selesai and valid_jam(s_mulai) and valid_jam(s_selesai) and jam_berurutan(s_mulai, s_selesai):
            d["mulai"] = s_mulai
            d["selesai"] = s_selesai
        else:
            print("Jam tidak valid/berurutan. Dibiarkan nilai lama.")

    s_kep = input("Keperluan baru: ").strip()
    if s_kep:
        d["keperluan"] = s_kep

    # (Opsional) admin-only: ubah status. Di sini kita izinkan user mengubah untuk simulasi.
    print("Ubah status (opsional): 1) pengajuan  2) disetujui  3) ditolak  4) (lewati)")
    while True:
        st = input("Pilihan: ").strip()
        if st == "":
            break
        if st in ("1", "2", "3"):
            d["status"] = STATUS_OPSI[int(st) - 1]
            break
        if st == "4":
            break
        print("Masukan tidak valid.")

    data[idx] = d
    peminjaman[user_id] = data
    print("Peminjaman diperbarui.\n")


def batalkan_peminjaman(user_id: str):
    print("\n=== Batalkan (Hapus) Peminjaman ===")
    data = peminjaman.get(user_id, [])
    if not data:
        print("(Belum ada peminjaman)\n")
        return
    tampilkan_peminjaman(user_id)
    idx = minta_indeks(len(data))
    if idx is None:
        return
    hapus = data.pop(idx)
    print(f"Peminjaman {hapus.get('kelas','-')} pada {hapus.get('tanggal','-')} dibatalkan.\n")


def minta_indeks(n: int):
    while True:
        s = input("Pilih nomor data (atau 'b' untuk batal): ").strip().lower()
        if s == "b":
            print("Dibatalkan.\n")
            return None
        try:
            val = int(s)
            if 1 <= val <= n:
                return val - 1
            print(f"Masukkan angka 1..{n}.")
        except ValueError:
            print("Masukan tidak valid.")


def menu_crud(user_id: str):
    while True:
        print("=== Menu Peminjaman Kelas ===")
        for i, item in enumerate(CRUD_MENU, start=1):
            print(f"{i}. {item}")
        choice = input_pilihan("Pilih menu (1-5): ", list(CRUD_MENU))

        if choice == 1:
            ajukan_peminjaman(user_id)
        elif choice == 2:
            tampilkan_peminjaman(user_id)
        elif choice == 3:
            ubah_peminjaman(user_id)
        elif choice == 4:
            batalkan_peminjaman(user_id)
        elif choice == 5:
            print("Kembali ke menu pengguna.\n")
            return


# ---------------------------- Loop Menu Setelah Login ---------------------------- #
def menu_setelah_login(user_id: str):
    while True:
        print("=== Menu Pengguna ===")
        for i, item in enumerate(AUTH_MENU, start=1):
            print(f"{i}. {item}")
        choice = input_pilihan("Pilih menu (1-4): ", list(AUTH_MENU))

        if choice == 1:
            lihat_profil(user_id)
        elif choice == 2:
            ubah_profil(user_id)
        elif choice == 3:
            menu_crud(user_id)
        elif choice == 4:
            print("Logout berhasil.\n")
            return


# ---------------------------- Aplikasi Utama ---------------------------- #
def print_selamat_datang():
    print("="*64)
    print("   SELAMAT DATANG DI SISTEM INFORMASI PEMINJAMAN KELAS (SIPK)")
    print("="*64)
    print("Menu utama disimpan sebagai TUPLE. Contoh slicing MAIN_MENU[:3] =>")
    print("->", MAIN_MENU[:3])  # Demonstrasi slicing mengambil 3 item pertama
    print("-"*64)
    print("Daftar kelas (ROOMS) juga berupa TUPLE (immutable referensi ruang).")
    print("")

def main():
    print_selamat_datang()
    while True:
        print("=== Menu Utama ===")
        menu_awal = MAIN_MENU[:3]  # slicing sesuai ketentuan
        for i, item in enumerate(menu_awal, start=1):
            print(f"{i}. {item}")
        choice = input_pilihan("Pilih menu (1-3): ", list(menu_awal))

        if choice == 1:
            register()
        elif choice == 2:
            user = login()
            if user:
                menu_setelah_login(user)
        elif choice == 3:
            print("Terima kasih telah menggunakan SIPK. Sampai jumpa!")
            break


if __name__ == "__main__":
    main()
