import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="Portal BPS Sidoarjo",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. CSS "SUPER PREMIUM" (SAMA SEPERTI SEBELUMNYA) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    .stApp { background: linear-gradient(135deg, #f0f4f8 0%, #d9e2ec 100%); font-family: 'Poppins', sans-serif; }
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}

    /* Styling Kartu Menu Depan */
    div.stButton > button:first-child {
        background: white; border: none; height: 160px; width: 100%; border-radius: 16px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.05); color: #333; font-family: 'Poppins', sans-serif;
        font-size: 15px; font-weight: 600; transition: all 0.3s; padding: 20px;
    }
    div.stButton > button:first-child:hover {
        transform: translateY(-8px); box-shadow: 0 15px 30px rgba(0, 84, 166, 0.15);
        background: linear-gradient(135deg, #0054A6 0%, #007bff 100%); color: white !important;
    }

    /* Styling File Card */
    .file-card {
        background-color: white; padding: 15px; border-radius: 12px; border-left: 5px solid #0054A6;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05); margin-bottom: 10px; display: flex;
        justify-content: space-between; align-items: center; transition: transform 0.2s;
    }
    .file-card:hover { transform: scale(1.02); box-shadow: 0 5px 15px rgba(0,0,0,0.1); cursor: pointer; }
    .file-title { font-weight: 600; color: #2c3e50; margin: 0; }
    .file-meta { font-size: 12px; color: #7f8c8d; }

    /* Badge Status */
    .status-badge { padding: 5px 12px; border-radius: 20px; font-size: 12px; font-weight: 600; }
    .badge-green {background-color: #e6fffa; color: #047857;}
    .badge-blue {background-color: #ebf8ff; color: #0054A6;}
    .badge-orange {background-color: #fffaf0; color: #dd6b20;}

    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] { gap: 20px; }
    .stTabs [data-baseweb="tab"] {
        height: 50px; background-color: white; border-radius: 10px 10px 0 0;
        box-shadow: 0 -2px 10px rgba(0,0,0,0.02); font-weight: 600;
    }
    .stTabs [aria-selected="true"] { background-color: #fff; color: #0054A6; border-bottom: 3px solid #0054A6; }
</style>
""", unsafe_allow_html=True)

# --- 3. KONEKSI DATA (BAGIAN DINAMIS) ---
# Mengambil data dari Google Sheet
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    # ttl=60 artinya data di-cache selama 60 detik agar tidak lemot loadingnya
    df = conn.read(ttl=60) 
    
    # Pastikan kolom tidak ada yang kosong (fillna) agar tidak error
    df = df.fillna("-")
except Exception as e:
    st.error("Gagal terhubung ke Google Sheet. Cek file secrets.toml atau koneksi internet.")
    st.stop()

# --- 4. NAVIGASI STATE ---
if 'current_level' not in st.session_state: st.session_state.current_level = 'home'
if 'selected_category' not in st.session_state: st.session_state.selected_category = None

def go_home():
    st.session_state.current_level = 'home'
    st.session_state.selected_category = None

# --- 5. FUNGSI RENDER KOMPONEN ---
def render_file_card(title, link):
    # Link sekarang mengambil dari Google Sheet
    st.markdown(f"""
    <a href="{link}" target="_blank" style="text-decoration:none;">
        <div class="file-card">
            <div>
                <div class="file-title">📄 {title}</div>
                <div class="file-meta">Klik untuk membuka dokumen</div>
            </div>
            <div style="background:#eef2ff; padding:8px 15px; border-radius:8px; color:#0054A6; font-weight:bold; font-size:12px;">
                Buka ↗️
            </div>
        </div>
    </a>
    """, unsafe_allow_html=True)

def render_status_header(title, status, progress):
    col1, col2 = st.columns([3, 1])
    with col1: st.markdown(f"### 👉 {title}")
    
    # Tentukan warna badge
    status_lower = str(status).lower()
    if "selesai" in status_lower: color = "badge-green"
    elif "jalan" in status_lower or "ongoing" in status_lower: color = "badge-blue"
    else: color = "badge-orange"
    
    with col2: st.markdown(f'<div style="text-align:right;"><span class="status-badge {color}">{status}</span></div>', unsafe_allow_html=True)
    
    # Progress bar (konversi ke int jika mungkin)
    try:
        prog_val = int(progress)
        st.progress(prog_val)
    except:
        pass

# --- 6. LOGIKA UI UTAMA ---

# HEADER HERO
st.markdown("""
<div style="text-align: center; margin-bottom: 30px; padding: 20px; background: white; border-radius: 20px; box-shadow: 0 10px 20px rgba(0,0,0,0.03);">
    <h1 style="color:#0054A6; margin:0; font-size: 2.2rem;">PORTAL KEGIATAN SOSIAL</h1>
    <p style="color:#F7941D; font-weight:600; margin:0;">BPS KABUPATEN SIDOARJO</p>
    <p style="color:#666; font-size:0.9rem; margin-top:10px;">Dashboard Data Terintegrasi (Real-time)</p>
</div>
""", unsafe_allow_html=True)

# SEARCH BAR
search_query = st.text_input("", placeholder="🔍 Cari Kegiatan atau File...", label_visibility="collapsed")
st.write("")

# --- LOGIKA TAMPILAN ---

if search_query:
    # FITUR PENCARIAN DINAMIS DARI DATAFRAME
    st.info(f"🔍 Hasil Pencarian: '{search_query}'")
    
    # Filter Dataframe (Case insensitive)
    # Mencari di kolom Nama_Kegiatan atau Nama_File
    mask = df['Nama_Kegiatan'].str.contains(search_query, case=False) | df['Nama_File'].str.contains(search_query, case=False)
    results = df[mask]
    
    if not results.empty:
        for index, row in results.iterrows():
            with st.container():
                st.markdown(f"**{row['Kategori']} > {row['Nama_Kegiatan']}**")
                render_file_card(row['Nama_File'], row['Link_File'])
    else:
        st.warning("Tidak ditemukan.")

else:
    # --- HALAMAN DEPAN (KARTU KATEGORI) ---
    if st.session_state.current_level == 'home':
        # Ambil daftar kategori unik dari Sheet
        kategori_unik = df['Kategori'].unique()
        
        # Grid kolom dinamis (maksimal 5 kolom)
        cols = st.columns(5)
        
        for i, kategori in enumerate(kategori_unik):
            # Ambil data baris pertama dari kategori ini untuk Icon & Deskripsi
            data_kat = df[df['Kategori'] == kategori].iloc[0]
            icon = data_kat['Icon']
            desc = data_kat['Deskripsi']
            
            # Gunakan modulo untuk menempatkan kartu di kolom yang benar
            with cols[i % 5]:
                if st.button(f"{icon}\n\n{kategori}\n\n{desc}", key=kategori):
                    st.session_state.selected_category = kategori
                    st.session_state.current_level = 'detail_view'
                    st.rerun()

    # --- HALAMAN DETAIL (ISI KATEGORI) ---
    elif st.session_state.current_level == 'detail_view':
        selected = st.session_state.selected_category
        
        # Tombol Kembali
        if st.button("⬅️ Kembali ke Dashboard"):
            go_home()
            st.rerun()
            
        # Ambil Icon kategori
        icon_cat = df[df['Kategori'] == selected].iloc[0]['Icon']
        st.markdown(f"<h2 style='color:#0054A6;'>{icon_cat} {selected}</h2>", unsafe_allow_html=True)
        
        # Filter data hanya untuk kategori yang dipilih
        df_cat = df[df['Kategori'] == selected]
        
        # Ambil Sub Menu unik (untuk Tabs)
        sub_menus = df_cat['Sub_Menu'].unique()
        
        # Buat Tabs
        tabs = st.tabs([f"📂 {sub}" for sub in sub_menus])
        
        for i, tab_name in enumerate(tabs):
            current_sub = sub_menus[i]
            with tab_name:
                st.write("") # Spacer
                
                # Filter data lagi berdasarkan Sub Menu
                df_sub = df_cat[df_cat['Sub_Menu'] == current_sub]
                
                # Grouping berdasarkan Nama Kegiatan (Agar file terkumpul dalam satu Expander)
                kegiatan_list = df_sub['Nama_Kegiatan'].unique()
                
                for keg in kegiatan_list:
                    # Ambil data kegiatan (baris pertama utk status/progress)
                    data_keg = df_sub[df_sub['Nama_Kegiatan'] == keg]
                    first_row = data_keg.iloc[0]
                    
                    with st.expander(f"{keg}", expanded=True):
                        # Tampilkan Status Header
                        render_status_header(keg, first_row['Status'], first_row['Progress'])
                        
                        st.markdown("#### 📥 Dokumen")
                        
                        # Grid File (2 Kolom)
                        f_cols = st.columns(2)
                        for idx, (index, row) in enumerate(data_keg.iterrows()):
                            with f_cols[idx % 2]:
                                render_file_card(row['Nama_File'], row['Link_File'])

# Footer
st.markdown("---")
st.caption("Data dikelola melalui Google Sheets (Auto-Sync)")
