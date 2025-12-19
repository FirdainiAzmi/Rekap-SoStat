import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import time

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="Portal BPS Sidoarjo",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. CSS GABUNGAN (LOGIN PRESISI + DASHBOARD LAMA) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');

    .stApp { background: linear-gradient(135deg, #f0f4f8 0%, #d9e2ec 100%); font-family: 'Poppins', sans-serif; }
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    [data-testid="stSidebar"] {display: none;}

    /* === CSS KHUSUS LOGIN PAGE (PRESISI LAPTOP) === */
    .login-container {
        background-color: white;
        padding: 40px;
        border-radius: 16px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05);
        border: 1px solid #e1e4e8;
        text-align: center;
    }
    .login-header {
        font-family: 'Inter', sans-serif;
        color: #0054A6;
        font-weight: 700;
        font-size: 24px;
        margin-bottom: 5px;
    }
    .login-sub {
        font-family: 'Inter', sans-serif;
        color: #64748b;
        font-size: 13px;
        margin-bottom: 25px;
    }
    /* Kecilkan input box login agar presisi */
    .stTextInput input {
        padding: 10px 15px !important;
        font-size: 14px !important;
        border-radius: 8px !important;
    }

    /* === CSS DASHBOARD (KODE ASLI ANDA) === */
    /* Styling Kartu Menu Depan */
    div.stButton > button:first-child:not(.login-btn) {
        background: white; border: none; height: 160px; width: 100%; border-radius: 16px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.05); color: #333; font-family: 'Poppins', sans-serif;
        font-size: 15px; font-weight: 600; transition: all 0.3s; padding: 20px;
    }
    div.stButton > button:first-child:not(.login-btn):hover {
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

    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] { gap: 20px; }
    .stTabs [data-baseweb="tab"] {
        height: 50px; background-color: white; border-radius: 10px 10px 0 0;
        box-shadow: 0 -2px 10px rgba(0,0,0,0.02); font-weight: 600;
    }
    .stTabs [aria-selected="true"] { background-color: #fff; color: #0054A6; border-bottom: 3px solid #0054A6; }
</style>
""", unsafe_allow_html=True)

# --- 3. SESSION STATE ---
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'current_level' not in st.session_state: st.session_state.current_level = 'home'
if 'selected_category' not in st.session_state: st.session_state.selected_category = None

# ==========================================
# BAGIAN 1: HALAMAN LOGIN (BARU)
# ==========================================
if not st.session_state.logged_in:
    # Layout 3 Kolom Presisi agar kotak login di tengah & tidak kegedean
    c1, c2, c3 = st.columns([1.3, 1, 1.3])
    
    with c1: st.write("")
    with c3: st.write("")
    
    with c2:
        st.markdown("<br><br><br>", unsafe_allow_html=True) # Spacer vertikal
        
        # Container Putih
        st.markdown("""
        <div class="login-container">
            <img src="https://upload.wikimedia.org/wikipedia/commons/2/28/Lambang_Badan_Pusat_Statistik_%28BPS%29_Indonesia.svg" width="70" style="margin-bottom:15px;">
            <div class="login-header">BPS SIDOARJO</div>
            <div class="login-sub">Silakan login untuk mengakses data</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Form Input (Di luar HTML agar interaktif)
        # Menggunakan session state agar value tidak hilang saat refresh
        user_in = st.text_input("Username", placeholder="ID Pengguna", label_visibility="collapsed")
        st.write("") # Jarak tipis
        pass_in = st.text_input("Password", type="password", placeholder="Kata Sandi", label_visibility="collapsed")
        st.write("")
        
        # Tombol Login
        if st.button("Masuk Aplikasi 🔐", type="primary", key="btn_login", use_container_width=True):
            try:
                # Cek kredensial dari secrets.toml
                if user_in == st.secrets["auth"]["username"] and pass_in == st.secrets["auth"]["password"]:
                    st.session_state.logged_in = True
                    st.rerun()
                else:
                    st.error("Username atau Password salah!")
            except:
                st.error("Setup file .streamlit/secrets.toml dulu!")

# ==========================================
# BAGIAN 2: DASHBOARD UTAMA (LOGIKA ASLI)
# ==========================================
else:
    # --- KONEKSI DATA ---
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        df = conn.read(ttl=60)
        df = df.fillna("-")
    except Exception as e:
        st.error("Gagal terhubung ke Google Sheet. Cek file secrets.toml atau koneksi internet.")
        st.stop()

    def go_home():
        st.session_state.current_level = 'home'
        st.session_state.selected_category = None

    # --- FUNGSI RENDER KOMPONEN ---
    def render_file_card(title, link):
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

    # --- UI UTAMA ---
    
    # Tombol Logout Kecil di Pojok Kanan Atas
    with st.container():
        col_h1, col_h2 = st.columns([8, 1])
        with col_h2:
            if st.button("Logout", key="logout_top"):
                st.session_state.logged_in = False
                st.rerun()

    # HEADER HERO (ASLI)
    st.markdown("""
    <div style="text-align: center; margin-bottom: 30px; padding: 20px; background: white; border-radius: 20px; box-shadow: 0 10px 20px rgba(0,0,0,0.03);">
        <h1 style="color:#0054A6; margin:0; font-size: 2.2rem;">PORTAL KEGIATAN SOSIAL</h1>
        <p style="color:#F7941D; font-weight:600; margin:0;">BPS KABUPATEN SIDOARJO</p>
        <p style="color:#666; font-size:0.9rem; margin-top:10px;">Dashboard Data Terintegrasi (Real-time)</p>
    </div>
    """, unsafe_allow_html=True)

    # SEARCH BAR (ASLI)
    search_query = st.text_input("", placeholder="🔍 Cari Kegiatan atau File...", label_visibility="collapsed")
    st.write("")

    # --- LOGIKA TAMPILAN ---
    if search_query:
        st.info(f"🔍 Hasil Pencarian: '{search_query}'")
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
        # --- HALAMAN DEPAN (KARTU KATEGORI - ASLI) ---
        if st.session_state.current_level == 'home':
            kategori_unik = df['Kategori'].unique()
            cols = st.columns(5) # Tetap 5 kolom sesuai kode asli
            
            for i, kategori in enumerate(kategori_unik):
                data_kat = df[df['Kategori'] == kategori].iloc[0]
                icon = data_kat['Icon']
                desc = data_kat['Deskripsi']
                
                with cols[i % 5]:
                    if st.button(f"{icon}\n\n{kategori}\n\n{desc}", key=kategori):
                        st.session_state.selected_category = kategori
                        st.session_state.current_level = 'detail_view'
                        st.rerun()

        # --- HALAMAN DETAIL (ISI KATEGORI - ASLI TAPI TANPA STATUS) ---
        elif st.session_state.current_level == 'detail_view':
            selected = st.session_state.selected_category
            
            if st.button("⬅️ Kembali ke Dashboard"):
                go_home()
                st.rerun()
                
            icon_cat = df[df['Kategori'] == selected].iloc[0]['Icon']
            st.markdown(f"<h2 style='color:#0054A6;'>{icon_cat} {selected}</h2>", unsafe_allow_html=True)
            
            df_cat = df[df['Kategori'] == selected]
            sub_menus = df_cat['Sub_Menu'].unique()
            
            tabs = st.tabs([f"📂 {sub}" for sub in sub_menus])
            
            for i, tab_name in enumerate(tabs):
                current_sub = sub_menus[i]
                with tab_name:
                    st.write("") 
                    df_sub = df_cat[df_cat['Sub_Menu'] == current_sub]
                    kegiatan_list = df_sub['Nama_Kegiatan'].unique()
                    
                    for keg in kegiatan_list:
                        # Ambil data kegiatan
                        data_keg = df_sub[df_sub['Nama_Kegiatan'] == keg]
                        
                        # LOGIKA STATUS/PROGRESS DIHAPUS DISINI
                        # Hanya menampilkan judul kegiatan saja
                        
                        with st.expander(f"{keg}", expanded=True):
                            # Hapus render_status_header, ganti judul simple
                            st.markdown(f"### 👉 {keg}") 
                            
                            st.markdown("#### 📥 Dokumen")
                            f_cols = st.columns(2) # Tetap 2 kolom file sesuai kode asli
                            for idx, (index, row) in enumerate(data_keg.iterrows()):
                                with f_cols[idx % 2]:
                                    render_file_card(row['Nama_File'], row['Link_File'])

    # Footer
    st.markdown("---")
    st.caption("Data dikelola melalui Google Sheets (Auto-Sync) | Mode Admin")
