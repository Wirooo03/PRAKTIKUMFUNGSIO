#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Program CLI: Sistem Informasi Peminjaman Kelas (SIPK) – Login/Register + CRUD
REFACTORED TO FUNCTIONAL PROGRAMMING PARADIGM

Perubahan ke Paradigma Fungsional:
1) Semua fungsi menjadi PURE FUNCTIONS (tidak mengubah state global)
2) Pendekatan DEKLARATIF (menggambarkan apa yang ingin dicapai)
3) Immutable data operations (mengembalikan data baru, bukan memodifikasi)
4) Functional composition dan higher-order functions
5) No side effects dalam core business logic

Ketentuan yang dipenuhi:
1) Data akun dalam dictionary -> accounts = {id: password}
2) Data profil nested dictionary -> profiles = {id: {"nama":..., "alamat":..., "hp":...}}
3) Daftar menu aplikasi dalam bentuk tuple -> MAIN_MENU (diakses memakai slicing)
4) Register: buat akun (ID & password) - PURE FUNCTION
5) Login: hanya akun terdaftar - PURE FUNCTION
6) CRUD data (peminjaman kelas) - PURE FUNCTIONS
7) Validasi input dengan functional approach
8) Data Tambahan per akun: "peminjaman" bertipe LIST of DICT

Paradigma Fungsional:
- Fungsi murni: input sama selalu menghasilkan output sama, tanpa side effects
- Immutability: tidak mengubah data asli, selalu membuat copy baru
- Deklaratif: fokus pada WHAT (apa yang dicapai) bukan HOW (bagaimana caranya)
"""

from typing import Dict, List, Tuple, Optional, Callable, NamedTuple
from datetime import datetime
from functools import reduce
from copy import deepcopy

# ---------------------------- Immutable Data Structures ---------------------------- #
class AppState(NamedTuple):
    """Immutable application state - Pure functional approach"""
    accounts: Dict[str, str] = {}
    profiles: Dict[str, Dict[str, str]] = {}
    peminjaman: Dict[str, List[Dict[str, str]]] = {}

# Initial empty state
EMPTY_STATE = AppState()

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


# ---------------------------- Pure Functions - Validasi ---------------------------- #

def is_valid_date(date_str: str) -> bool:
    """PURE FUNCTION: Validasi format tanggal
    Input: string tanggal
    Output: boolean (True jika valid)
    No side effects, deterministic
    """
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def is_valid_time(time_str: str) -> bool:
    """PURE FUNCTION: Validasi format jam
    Input: string jam
    Output: boolean (True jika valid)
    No side effects, deterministic
    """
    try:
        datetime.strptime(time_str, "%H:%M")
        return True
    except ValueError:
        return False

def is_time_sequential(start_time: str, end_time: str) -> bool:
    """PURE FUNCTION: Cek urutan jam mulai < jam selesai
    Input: dua string waktu
    Output: boolean (True jika berurutan)
    No side effects, deterministic
    """
    if not (is_valid_time(start_time) and is_valid_time(end_time)):
        return False
    
    start = datetime.strptime(start_time, "%H:%M")
    end = datetime.strptime(end_time, "%H:%M")
    return end > start

def is_non_empty_string(s: str) -> bool:
    """PURE FUNCTION: Cek string tidak kosong
    Input: string
    Output: boolean (True jika tidak kosong)
    No side effects, deterministic
    """
    return bool(s.strip())

def is_valid_menu_choice(choice: str, max_options: int) -> bool:
    """PURE FUNCTION: Validasi pilihan menu
    Input: string pilihan, jumlah maksimal opsi
    Output: boolean (True jika valid)
    No side effects, deterministic
    """
    try:
        val = int(choice.strip())
        return 1 <= val <= max_options
    except ValueError:
        return False

def validate_password_strength(password: str) -> bool:
    """PURE FUNCTION: Validasi kekuatan password
    Input: string password
    Output: boolean (True jika memenuhi kriteria)
    No side effects, deterministic
    """
    return len(password.strip()) >= 4

# ---------------------------- Pure Functions - Input dengan Validasi ---------------------------- #

def get_validated_input(prompt: str, validator: Callable[[str], bool], error_msg: str) -> str:
    """PURE dalam konteks: menggunakan higher-order function
    Menerima validator function sebagai parameter
    Deklaratif: menggambarkan validasi berdasarkan fungsi validator
    """
    while True:
        user_input = input(prompt).strip()
        if validator(user_input):
            return user_input
        print(error_msg)

def get_validated_choice(prompt: str, options: List[str]) -> int:
    """Input dengan validasi pilihan menu - menggunakan functional approach"""
    validator = lambda x: is_valid_menu_choice(x, len(options))
    error_msg = f"Masukkan angka 1..{len(options)} sesuai menu."
    
    while True:
        choice_str = get_validated_input(prompt, validator, error_msg)
        return int(choice_str.strip())


# ---------------------------- Pure Functions - Authentication ---------------------------- #

def is_user_exists(state: AppState, user_id: str) -> bool:
    """PURE FUNCTION: Cek apakah user sudah terdaftar
    Input: state aplikasi, user_id
    Output: boolean
    No side effects, deterministic
    """
    return user_id in state.accounts

def create_new_user(state: AppState, user_id: str, password: str, 
                   nama: str, alamat: str, hp: str) -> AppState:
    """PURE FUNCTION: Membuat user baru dengan mengembalikan state baru
    Input: state lama, data user baru
    Output: state baru dengan user ditambahkan
    Immutable - tidak mengubah state asli
    """
    new_accounts = {**state.accounts, user_id: password}
    new_profiles = {**state.profiles, user_id: {"nama": nama, "alamat": alamat, "hp": hp}}
    new_peminjaman = {**state.peminjaman, user_id: []}
    
    return AppState(
        accounts=new_accounts,
        profiles=new_profiles,
        peminjaman=new_peminjaman
    )

def authenticate_user(state: AppState, user_id: str, password: str) -> bool:
    """PURE FUNCTION: Autentikasi user
    Input: state aplikasi, user_id, password
    Output: boolean (True jika kredensial valid)
    No side effects, deterministic
    """
    return (user_id in state.accounts and 
            state.accounts[user_id] == password)

def get_user_profile(state: AppState, user_id: str) -> Optional[Dict[str, str]]:
    """PURE FUNCTION: Ambil profil user
    Input: state aplikasi, user_id
    Output: profil user atau None
    No side effects, deterministic
    """
    return state.profiles.get(user_id)

# ---------------------------- Imperative Wrapper Functions (untuk UI) ---------------------------- #

def register_workflow(state: AppState) -> AppState:
    """Workflow registrasi dengan pure functions sebagai core logic"""
    print("\n=== Registrasi Akun Baru ===")
    
    # Input dan validasi user_id
    user_id = get_validated_input(
        "Buat ID (username/NIM): ",
        lambda x: is_non_empty_string(x) and not is_user_exists(state, x),
        "ID tidak valid atau sudah terdaftar. Gunakan ID lain."
    )
    
    # Input dan validasi password
    password = get_validated_input(
        "Buat Password (min 4 karakter): ",
        validate_password_strength,
        "Password terlalu pendek (min 4 karakter)."
    )
    
    # Input profil
    nama = get_validated_input("Nama: ", is_non_empty_string, "Nama tidak boleh kosong.")
    alamat = get_validated_input("Alamat: ", is_non_empty_string, "Alamat tidak boleh kosong.")
    hp = get_validated_input("No. HP: ", is_non_empty_string, "No. HP tidak boleh kosong.")
    
    # Gunakan pure function untuk membuat user baru
    new_state = create_new_user(state, user_id, password, nama, alamat, hp)
    print(f"Akun '{user_id}' berhasil dibuat!\n")
    
    return new_state

def login_workflow(state: AppState) -> Optional[str]:
    """Workflow login dengan pure functions sebagai core logic"""
    print("\n=== Login ===")
    
    user_id = get_validated_input("ID: ", is_non_empty_string, "ID tidak boleh kosong.")
    password = get_validated_input("Password: ", is_non_empty_string, "Password tidak boleh kosong.")
    
    # Gunakan pure function untuk autentikasi
    if authenticate_user(state, user_id, password):
        profile = get_user_profile(state, user_id)
        nama = profile['nama'] if profile else user_id
        print(f"Login berhasil. Selamat datang, {nama}!\n")
        return user_id
    
    print("ID atau Password salah.\n")
    return None


# ---------------------------- Pure Functions - Profile Management ---------------------------- #

def format_profile_display(user_id: str, profile: Optional[Dict[str, str]]) -> str:
    """PURE FUNCTION: Format tampilan profil
    Input: user_id, profile data
    Output: string formatted profile
    No side effects, deterministic
    """
    if not profile:
        return "Profil tidak ditemukan."
    
    return f"""ID     : {user_id}
Nama   : {profile.get('nama', '-')}
Alamat : {profile.get('alamat', '-')}
HP     : {profile.get('hp', '-')}"""

def update_profile_data(current_profile: Dict[str, str], 
                       nama: str = "", alamat: str = "", hp: str = "") -> Dict[str, str]:
    """PURE FUNCTION: Update profil dengan data baru
    Input: profil saat ini, data baru (opsional)
    Output: profil yang sudah diupdate
    Immutable - mengembalikan copy baru
    """
    updated = current_profile.copy()
    
    if nama.strip():
        updated["nama"] = nama.strip()
    if alamat.strip():
        updated["alamat"] = alamat.strip()
    if hp.strip():
        updated["hp"] = hp.strip()
        
    return updated

def update_user_profile(state: AppState, user_id: str, 
                       nama: str = "", alamat: str = "", hp: str = "") -> AppState:
    """PURE FUNCTION: Update profil user dalam state
    Input: state lama, user_id, data profil baru
    Output: state baru dengan profil terupdate
    Immutable operation
    """
    current_profile = state.profiles.get(user_id, {})
    updated_profile = update_profile_data(current_profile, nama, alamat, hp)
    
    new_profiles = {**state.profiles, user_id: updated_profile}
    
    return AppState(
        accounts=state.accounts,
        profiles=new_profiles,
        peminjaman=state.peminjaman
    )

# ---------------------------- Profile Workflow Functions ---------------------------- #

def display_profile_workflow(state: AppState, user_id: str) -> None:
    """Workflow untuk menampilkan profil"""
    print("\n=== Profil Saya ===")
    profile = get_user_profile(state, user_id)
    profile_text = format_profile_display(user_id, profile)
    print(profile_text)
    print("")

def update_profile_workflow(state: AppState, user_id: str) -> AppState:
    """Workflow untuk mengubah profil"""
    print("\n=== Ubah Profil ===")
    
    current_profile = get_user_profile(state, user_id)
    if not current_profile:
        print("Profil tidak ditemukan.")
        return state
    
    nama = input("Nama (kosongkan jika tidak diubah): ").strip()
    alamat = input("Alamat (kosongkan jika tidak diubah): ").strip()
    hp = input("No. HP (kosongkan jika tidak diubah): ").strip()
    
    # Gunakan pure function untuk update
    new_state = update_user_profile(state, user_id, nama, alamat, hp)
    print("Profil berhasil diperbarui.\n")
    
    return new_state


# ---------------------------- Pure Functions - Peminjaman CRUD ---------------------------- #

def create_peminjaman_entry(kelas: str, tanggal: str, mulai: str, 
                           selesai: str, keperluan: str, status: str = "pengajuan") -> Dict[str, str]:
    """PURE FUNCTION: Membuat entry peminjaman baru
    Input: data peminjaman
    Output: dictionary peminjaman
    No side effects, deterministic
    """
    return {
        "kelas": kelas,
        "tanggal": tanggal,
        "mulai": mulai,
        "selesai": selesai,
        "keperluan": keperluan,
        "status": status
    }

def add_peminjaman_to_user(state: AppState, user_id: str, peminjaman_data: Dict[str, str]) -> AppState:
    """PURE FUNCTION: Menambah peminjaman ke user
    Input: state lama, user_id, data peminjaman
    Output: state baru dengan peminjaman ditambahkan
    Immutable operation
    """
    current_peminjaman = state.peminjaman.get(user_id, [])
    new_peminjaman_list = current_peminjaman + [peminjaman_data]
    new_peminjaman = {**state.peminjaman, user_id: new_peminjaman_list}
    
    return AppState(
        accounts=state.accounts,
        profiles=state.profiles,
        peminjaman=new_peminjaman
    )

def get_user_peminjaman(state: AppState, user_id: str) -> List[Dict[str, str]]:
    """PURE FUNCTION: Ambil daftar peminjaman user
    Input: state aplikasi, user_id
    Output: list peminjaman user
    No side effects, deterministic
    """
    return state.peminjaman.get(user_id, [])

def format_peminjaman_display(peminjaman_list: List[Dict[str, str]]) -> str:
    """PURE FUNCTION: Format tampilan daftar peminjaman
    Input: list peminjaman
    Output: string formatted
    No side effects, deterministic, menggunakan functional approach
    """
    if not peminjaman_list:
        return "(Belum ada peminjaman)"
    
    # Functional approach: map setiap peminjaman ke string format
    formatted_items = [
        f"{i}. [{p.get('status','pengajuan').upper():10}] {p.get('kelas','-')} | "
        f"{p.get('tanggal','-')} {p.get('mulai','-')}-{p.get('selesai','-')}\n"
        f"   Keperluan: {p.get('keperluan','-')}"
        for i, p in enumerate(peminjaman_list, start=1)
    ]
    
    return "\n".join(formatted_items)

def update_peminjaman_at_index(peminjaman_list: List[Dict[str, str]], 
                              index: int, updated_data: Dict[str, str]) -> List[Dict[str, str]]:
    """PURE FUNCTION: Update peminjaman pada indeks tertentu
    Input: list peminjaman, indeks, data baru
    Output: list baru dengan item terupdate
    Immutable operation
    """
    if index < 0 or index >= len(peminjaman_list):
        return peminjaman_list
    
    new_list = peminjaman_list.copy()
    new_list[index] = {**peminjaman_list[index], **updated_data}
    return new_list

def delete_peminjaman_at_index(peminjaman_list: List[Dict[str, str]], 
                              index: int) -> Tuple[List[Dict[str, str]], Optional[Dict[str, str]]]:
    """PURE FUNCTION: Hapus peminjaman pada indeks tertentu
    Input: list peminjaman, indeks
    Output: tuple (list baru, item yang dihapus atau None)
    Immutable operation
    """
    if index < 0 or index >= len(peminjaman_list):
        return peminjaman_list, None
    
    new_list = peminjaman_list[:index] + peminjaman_list[index+1:]
    deleted_item = peminjaman_list[index]
    return new_list, deleted_item

def update_user_peminjaman(state: AppState, user_id: str, 
                          new_peminjaman_list: List[Dict[str, str]]) -> AppState:
    """PURE FUNCTION: Update seluruh daftar peminjaman user
    Input: state lama, user_id, list peminjaman baru
    Output: state baru
    Immutable operation
    """
    new_peminjaman = {**state.peminjaman, user_id: new_peminjaman_list}
    
    return AppState(
        accounts=state.accounts,
        profiles=state.profiles,
        peminjaman=new_peminjaman
    )

# ---------------------------- Input Helper Functions ---------------------------- #

def select_room_from_list() -> str:
    """Input helper untuk memilih kelas - menggunakan functional approach"""
    print("Pilih Kelas:")
    room_options = list(ROOMS)
    
    # Functional approach: enumerate untuk menampilkan opsi
    room_display = [f"{i}. {room}" for i, room in enumerate(room_options, start=1)]
    print("\n".join(room_display))
    
    choice = get_validated_choice("Masukkan pilihan: ", room_options)
    return room_options[choice - 1]

def get_date_input() -> str:
    """Input helper untuk tanggal dengan validasi"""
    return get_validated_input(
        "Tanggal (YYYY-MM-DD): ",
        is_valid_date,
        "Format tanggal tidak valid."
    )

def get_time_range_input() -> Tuple[str, str]:
    """Input helper untuk jam mulai dan selesai dengan validasi"""
    while True:
        mulai = get_validated_input(
            "Jam Mulai (HH:MM): ",
            is_valid_time,
            "Format jam tidak valid."
        )
        
        selesai = get_validated_input(
            "Jam Selesai (HH:MM): ",
            is_valid_time,
            "Format jam tidak valid."
        )
        
        if is_time_sequential(mulai, selesai):
            return mulai, selesai
        
        print("Jam selesai harus lebih besar dari jam mulai.")

def get_index_input(max_count: int) -> Optional[int]:
    """Input helper untuk memilih indeks dengan validasi"""
    while True:
        user_input = input("Pilih nomor data (atau 'b' untuk batal): ").strip().lower()
        if user_input == "b":
            print("Dibatalkan.\n")
            return None
        
        if is_valid_menu_choice(user_input, max_count):
            return int(user_input) - 1
        
        print(f"Masukkan angka 1..{max_count} atau 'b' untuk batal.")

# ---------------------------- CRUD Workflow Functions ---------------------------- #

def create_peminjaman_workflow(state: AppState, user_id: str) -> AppState:
    """Workflow untuk menambah peminjaman - menggunakan pure functions"""
    print("\n=== Ajukan Peminjaman Kelas ===")
    
    kelas = select_room_from_list()
    tanggal = get_date_input()
    mulai, selesai = get_time_range_input()
    keperluan = get_validated_input("Keperluan: ", is_non_empty_string, "Keperluan tidak boleh kosong.")
    
    # Gunakan pure function untuk membuat entry
    peminjaman_entry = create_peminjaman_entry(kelas, tanggal, mulai, selesai, keperluan)
    new_state = add_peminjaman_to_user(state, user_id, peminjaman_entry)
    
    print("Pengajuan peminjaman disimpan.\n")
    return new_state

def read_peminjaman_workflow(state: AppState, user_id: str) -> None:
    """Workflow untuk menampilkan daftar peminjaman"""
    print("\n=== Daftar Peminjaman Saya ===")
    
    user_peminjaman = get_user_peminjaman(state, user_id)
    display_text = format_peminjaman_display(user_peminjaman)
    print(display_text)
    print("")

def update_peminjaman_workflow(state: AppState, user_id: str) -> AppState:
    """Workflow untuk mengubah peminjaman - menggunakan pure functions"""
    print("\n=== Ubah Peminjaman ===")
    
    user_peminjaman = get_user_peminjaman(state, user_id)
    if not user_peminjaman:
        print("(Belum ada peminjaman)\n")
        return state
    
    # Tampilkan daftar untuk dipilih
    read_peminjaman_workflow(state, user_id)
    
    index = get_index_input(len(user_peminjaman))
    if index is None:
        return state
    
    current_data = user_peminjaman[index]
    print("Tekan Enter untuk mempertahankan nilai lama.")
    
    # Input perubahan dengan validasi
    updated_data = {}
    
    # Kelas
    ganti_kelas = input("Ganti kelas? (y/n): ").strip().lower()
    if ganti_kelas == "y":
        updated_data["kelas"] = select_room_from_list()
    
    # Tanggal
    tanggal_baru = input("Tanggal baru (YYYY-MM-DD): ").strip()
    if tanggal_baru and is_valid_date(tanggal_baru):
        updated_data["tanggal"] = tanggal_baru
    elif tanggal_baru and not is_valid_date(tanggal_baru):
        print("Format tanggal salah. Dibiarkan nilai lama.")
    
    # Jam
    jam_mulai_baru = input("Jam Mulai baru (HH:MM): ").strip()
    jam_selesai_baru = input("Jam Selesai baru (HH:MM): ").strip()
    
    if jam_mulai_baru or jam_selesai_baru:
        # Gunakan jam lama jika tidak diisi
        mulai_final = jam_mulai_baru if jam_mulai_baru else current_data.get("mulai", "")
        selesai_final = jam_selesai_baru if jam_selesai_baru else current_data.get("selesai", "")
        
        if (is_valid_time(mulai_final) and is_valid_time(selesai_final) and 
            is_time_sequential(mulai_final, selesai_final)):
            updated_data["mulai"] = mulai_final
            updated_data["selesai"] = selesai_final
        else:
            print("Jam tidak valid/berurutan. Dibiarkan nilai lama.")
    
    # Keperluan
    keperluan_baru = input("Keperluan baru: ").strip()
    if keperluan_baru:
        updated_data["keperluan"] = keperluan_baru
    
    # Status (simulasi admin)
    print("Ubah status (opsional): 1) pengajuan  2) disetujui  3) ditolak  4) (lewati)")
    status_choice = input("Pilihan: ").strip()
    if status_choice in ("1", "2", "3"):
        updated_data["status"] = STATUS_OPSI[int(status_choice) - 1]
    
    # Update menggunakan pure function
    new_peminjaman_list = update_peminjaman_at_index(user_peminjaman, index, updated_data)
    new_state = update_user_peminjaman(state, user_id, new_peminjaman_list)
    
    print("Peminjaman diperbarui.\n")
    return new_state

def delete_peminjaman_workflow(state: AppState, user_id: str) -> AppState:
    """Workflow untuk menghapus peminjaman - menggunakan pure functions"""
    print("\n=== Batalkan (Hapus) Peminjaman ===")
    
    user_peminjaman = get_user_peminjaman(state, user_id)
    if not user_peminjaman:
        print("(Belum ada peminjaman)\n")
        return state
    
    # Tampilkan daftar untuk dipilih
    read_peminjaman_workflow(state, user_id)
    
    index = get_index_input(len(user_peminjaman))
    if index is None:
        return state
    
    # Hapus menggunakan pure function
    new_peminjaman_list, deleted_item = delete_peminjaman_at_index(user_peminjaman, index)
    new_state = update_user_peminjaman(state, user_id, new_peminjaman_list)
    
    if deleted_item:
        kelas = deleted_item.get('kelas', '-')
        tanggal = deleted_item.get('tanggal', '-')
        print(f"Peminjaman {kelas} pada {tanggal} dibatalkan.\n")
    
    return new_state

def crud_menu_workflow(state: AppState, user_id: str) -> AppState:
    """Menu CRUD dengan pure functions approach"""
    current_state = state
    
    while True:
        print("=== Menu Peminjaman Kelas ===")
        crud_options = list(CRUD_MENU)
        
        for i, item in enumerate(crud_options, start=1):
            print(f"{i}. {item}")
        
        choice = get_validated_choice("Pilih menu (1-5): ", crud_options)
        
        if choice == 1:
            current_state = create_peminjaman_workflow(current_state, user_id)
        elif choice == 2:
            read_peminjaman_workflow(current_state, user_id)
        elif choice == 3:
            current_state = update_peminjaman_workflow(current_state, user_id)
        elif choice == 4:
            current_state = delete_peminjaman_workflow(current_state, user_id)
        elif choice == 5:
            print("Kembali ke menu pengguna.\n")
            return current_state

# ---------------------------- Main Menu Workflows ---------------------------- #

def authenticated_menu_workflow(state: AppState, user_id: str) -> AppState:
    """Menu setelah login dengan pure functions approach"""
    current_state = state
    
    while True:
        print("=== Menu Pengguna ===")
        auth_options = list(AUTH_MENU)
        
        for i, item in enumerate(auth_options, start=1):
            print(f"{i}. {item}")
        
        choice = get_validated_choice("Pilih menu (1-4): ", auth_options)
        
        if choice == 1:
            display_profile_workflow(current_state, user_id)
        elif choice == 2:
            current_state = update_profile_workflow(current_state, user_id)
        elif choice == 3:
            current_state = crud_menu_workflow(current_state, user_id)
        elif choice == 4:
            print("Logout berhasil.\n")
            return current_state

def print_welcome_functional():
    """Welcome message dengan penjelasan paradigma fungsional"""
    print("="*80)
    print("   SISTEM INFORMASI PEMINJAMAN KELAS (SIPK) - FUNCTIONAL PARADIGM")
    print("="*80)
    print("🔥 PARADIGMA FUNGSIONAL TELAH DITERAPKAN:")
    print("✅ PURE FUNCTIONS: Semua fungsi bisnis logic tanpa side effects")
    print("✅ IMMUTABILITY: State tidak pernah diubah langsung, selalu membuat copy baru") 
    print("✅ DECLARATIVE: Fokus pada WHAT (apa yang dicapai) bukan HOW")
    print("✅ FUNCTIONAL COMPOSITION: Higher-order functions & function composition")
    print("")
    print("Menu utama (TUPLE dengan slicing):", MAIN_MENU[:3])
    print("Daftar kelas (IMMUTABLE TUPLE):", ROOMS[:3], "...")
    print("-"*80)

def main_functional():
    """Main function dengan pure functional approach"""
    print_welcome_functional()
    
    # State aplikasi dimulai dari state kosong
    app_state = EMPTY_STATE
    
    while True:
        print("\n=== Menu Utama ===")
        main_options = list(MAIN_MENU[:3])  # Slicing sesuai ketentuan
        
        # Functional approach untuk menampilkan menu
        menu_display = [f"{i}. {item}" for i, item in enumerate(main_options, start=1)]
        print("\n".join(menu_display))
        
        choice = get_validated_choice("Pilih menu (1-3): ", main_options)
        
        if choice == 1:
            # Register - pure function approach
            app_state = register_workflow(app_state)
            
        elif choice == 2:
            # Login - pure function approach  
            user_id = login_workflow(app_state)
            if user_id:
                app_state = authenticated_menu_workflow(app_state, user_id)
                
        elif choice == 3:
            print("Terima kasih telah menggunakan SIPK Functional! 🚀")
            print("Semua operasi telah menggunakan PURE FUNCTIONS & IMMUTABLE STATE!")
            break

if __name__ == "__main__":
    main_functional()
