import streamlit as st
import pandas as pd
 
 # Tambahkan background menggunakan CSS
 st.markdown("""
     <style>
     .stApp {
         background-image: url("https://images.unsplash.com/photo-1514996937319-344454492b37?ixlib=rb-4.0.3&auto=format&fit=crop&w=1950&q=80");
         background-attachment: fixed;
         background-size: cover;
     }
 
     /* Opsional: buat latar belakang konten semi-transparan agar teks tetap terbaca */
     .main > div {
         background-color: rgba(255, 255, 255, 0.85);
         padding: 2rem;
         border-radius: 10px;
     }
     </style>
 """, unsafe_allow_html=True)
 
 # Konfigurasi halaman
 st.set_page_config(page_title="Kalkulator Vitamin MPASI", layout="wide")
 
 # Fungsi untuk navigasi halaman
 def set_page(page_name):
     st.session_state.page = page_name
 
 # Inisialisasi halaman
 if "page" not in st.session_state:
     st.session_state.page = "beranda"
 
 # ===================== DATA VITAMIN =====================
 vitamin_data_mg = {
     "Wortel": {"Vitamin A (mg)": 0.835, "Vitamin B1 (mg)": 0.07, "Vitamin C (mg)": 5.9, "Vitamin D (mg)": 0, "Vitamin E (mg)": 0.66},
    "Bayam": {"Vitamin A (mg)": 0.469, "Vitamin B1 (mg)": 0.10, "Vitamin C (mg)": 28.1, "Vitamin D (mg)": 0, "Vitamin E (mg)": 2.0},
    "Daging Ayam": {"Vitamin A (mg)": 0.013, "Vitamin B1 (mg)": 0.07, "Vitamin C (mg)": 0, "Vitamin D (mg)": 0.000175, "Vitamin E (mg)": 0.3},
    "Telur": {"Vitamin A (mg)": 0.14, "Vitamin B1 (mg)": 0.04, "Vitamin C (mg)": 0, "Vitamin D (mg)": 0.000925, "Vitamin E (mg)": 0.97},
    "Pisang": {"Vitamin A (mg)": 0.064, "Vitamin B1 (mg)": 0.03, "Vitamin C (mg)": 8.7, "Vitamin D (mg)": 0, "Vitamin E (mg)": 0.1},
    "Brokoli": {"Vitamin A (mg)": 0.567, "Vitamin B1 (mg)": 0.07, "Vitamin C (mg)": 89.2, "Vitamin D (mg)": 0, "Vitamin E (mg)": 1.5},
    "Ikan Salmon": {"Vitamin A (mg)": 0.05, "Vitamin B1 (mg)": 0.23, "Vitamin C (mg)": 0, "Vitamin D (mg)": 0.01315, "Vitamin E (mg)": 2.0},
    "Kentang": {"Vitamin A (mg)": 0.0, "Vitamin B1 (mg)": 0.08, "Vitamin C (mg)": 19.7, "Vitamin D (mg)": 0, "Vitamin E (mg)": 0.01},
    "Hati Ayam": {"Vitamin A (mg)": 9.442, "Vitamin B1 (mg)": 0.23, "Vitamin C (mg)": 27.0, "Vitamin D (mg)": 0.00175, "Vitamin E (mg)": 0.5},
}

# ===================== FUNGSI VITAMIN =====================
def kebutuhan_vitamin_mg(usia_bulan):
    if usia_bulan <= 11:
        return {
            "Vitamin A (mg)": 0.4,
            "Vitamin B1 (mg)": 0.3,
            "Vitamin C (mg)": 50,
            "Vitamin D (mg)": 0.01,
            "Vitamin E (mg)": 4,
        }
    else:
        return {
            "Vitamin A (mg)": 0.4,
            "Vitamin B1 (mg)": 0.5,
            "Vitamin C (mg)": 40,
            "Vitamin D (mg)": 0.015,
            "Vitamin E (mg)": 6,
        }

def estimasi_porsi(usia_bulan):
    if usia_bulan <= 8:
        return 50
    elif usia_bulan <= 12:
        return 100
    elif usia_bulan <= 18:
        return 150
    else:
        return 200

# ===================== BERANDA =====================
if st.session_state.page == "beranda":
    st.title("👶 Selamat Datang di Aplikasi Kalkulator Vitamin MPASI 🍽️")
    st.markdown("""
Aplikasi ini membantu menghitung kadar vitamin dalam MPASI bayi berdasarkan bahan makanan, berat (gram), dan usia bayi.

### Fitur:
- 🥕 Hitung kandungan vitamin dari bahan MPASI
- 👶 Sesuaikan dengan kebutuhan vitamin berdasarkan usia bayi
- 🍗 Rancang menu MPASI yang bergizi dan seimbang

""")
    st.button("➡ Mulai Perhitungan", on_click=set_page, args=("perhitungan",))

# ===================== KALKULATOR =====================
elif st.session_state.page == "perhitungan":
    st.title("🧮 Kalkulator Kadar Vitamin MPASI untuk Bayi")
    st.button("🔙 Kembali ke Beranda", on_click=set_page, args=("beranda",))

    usia = st.slider("Usia bayi (bulan):", min_value=6, max_value=24, value=9)
    kebutuhan = kebutuhan_vitamin_mg(usia)
    default_porsi = estimasi_porsi(usia)

    bahan_dipilih = st.multiselect("Pilih bahan MPASI:", list(vitamin_data_mg.keys()))

    total_vitamin = {k: 0 for k in kebutuhan}

    if bahan_dipilih:
        st.subheader("⚖️ Masukkan jumlah gram untuk setiap bahan:")
        for bahan in bahan_dipilih:
            gram = st.number_input(f"{bahan} (gram):", min_value=0, max_value=500, value=default_porsi, step=10)
            for vitamin in total_vitamin:
                total_vitamin[vitamin] += vitamin_data_mg[bahan][vitamin] * gram / 100

        st.subheader("📊 Total Asupan Vitamin (mg)")
        hasil_df = pd.DataFrame({
            "Asupan MPASI (mg)": total_vitamin,
            "Kebutuhan Harian (mg)": kebutuhan,
            "Persentase Kecukupan (%)": {
                k: round((total_vitamin[k] / kebutuhan[k]) * 100, 1) if kebutuhan[k] > 0 else 0
                for k in kebutuhan
            }
        })

