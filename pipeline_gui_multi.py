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

# --- 2. CSS "SUPER PREMIUM" (Login & Dashboard) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    
    .stApp { 
        background: linear-gradient(135deg, #f0f4f8 0%, #d9e2ec 100%); 
        font-family: 'Poppins', sans-serif; 
    }
    
    /* Hilangkan Elemen Bawaan */
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}

    /* --- CSS KHUSUS LOGIN PAGE --- */
    .login-container {
        background: white;
        padding: 40px;
        border-radius: 20px;
        box-shadow: 0 15px 30px rgba(0,0,0,0.1);
        text-align: center;
        max-width: 400px;
        margin: auto;
        border-top: 5px solid #0054A6;
    }
    .login-title {
        color: #0054A6;
        font-weight: 700;
        font-size: 24px;
        margin-bottom: 10px;
    }
    .login-subtitle {
        color: #7f8c8d;
        font-size: 14px;
        margin-bottom: 30px;
    }

    /* --- CSS DASHBOARD --- */
    div.stButton > button:first-child {
        background: white; border: none; height: 160px; width: 100%; border-radius: 16px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.05); color: #333; font-family: 'Poppins', sans-serif;
        font-size: 15px; font-weight: 600; transition: all 0.3s; padding: 20px;
    }
    div.stButton > button:first-child:hover {
        transform: translateY(-8px); box-shadow: 0 15px 30px rgba(0, 84, 166, 0.15);
        background: linear-gradient(135deg, #0054A6 0%, #007bff 100%); color: white !important;
    }

    .file-card {
        background-color: white; padding: 15px; border-radius: 12px; border-left: 5px solid #0054A6;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05); margin-bottom: 10px; display: flex;
        justify-content: space-between; align-items: center; transition: transform 0.2s;
    }
    .file-card:hover { transform: scale(1.02); box-shadow: 0 5px 15px rgba(0,0,0,0.1); cursor: pointer; }
    .file-title { font-weight: 600; color: #2c3e50; margin: 0; }
    .file-meta { font-size: 12px; color: #7f8c8d; }

    .status-badge { padding: 5px 12px; border-radius: 20px; font-size: 12px; font-weight: 600; }
    .badge-green {background-color: #e6fffa; color: #047857;}
    .badge-blue {background-color: #ebf8ff; color: #0054A6;}
    .badge-orange {background-color: #fffaf0; color: #dd6b20;}
    
    .stTabs [data-baseweb="tab-list"] { gap: 20px; }
    .stTabs [data-baseweb="tab"] {
        height: 50px; background-color: white; border-radius: 10px 10px 0 0;
        box-shadow: 0 -2px 10px rgba(0,0,0,0.02); font-weight: 600;
    }
    .stTabs [aria-selected="true"] { background-color: #fff; color: #0054A6; border-bottom: 3px solid #0054A6; }
</style>
""", unsafe_allow_html=True)

# --- 3. LOGIKA SESSION STATE (LOGIN) ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# Fungsi Login
def check_login():
    user = st.session_state.username_input
    pwd = st.session_state.password_input
    
    # Ambil credential dari secrets.toml
    correct_user = st.secrets["auth"]["username"]
    correct_pwd = st.secrets["auth"]["password"]

    if user == correct_user and pwd == correct_pwd:
        st.session_state.logged_in = True
        st.success("Login Berhasil!")
        time.sleep(0.5)
        st.rerun()
    else:
        st.error("Username atau Password salah.")

# Fungsi Logout
def logout():
    st.session_state.logged_in = False
    st.rerun()

# --- 4. TAMPILAN HALAMAN LOGIN ---
if not st.session_state.logged_in:
    # Menggunakan kolom kosong agar form login di tengah
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col2:
        st.markdown("<div style='margin-top: 100px;'></div>", unsafe_allow_html=True)
        # Container Login Visual
        st.markdown("""
        <div class="login-container">
            <img src="https://upload.wikimedia.org/wikipedia/commons/2/28/Lambang_Badan_Pusat_Statistik_%28BPS%29_Indonesia.svg" width="80" style="margin-bottom:15px;">
            <div class="login-title">Portal Sosial</div>
            <div class="login-subtitle">Silakan login untuk mengakses data</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Form Input
        st.text_input("Username", key="username_input")
        st.text_input("Password", type="password", key="password_input")
        st.button("Masuk 🔐", on_click=check_login, use_container_width=True)
        st.markdown("<div style='text-align:center; margin-top:20px; color:#aaa; font-size:12px;'>© 2025 BPS Sidoarjo</div>", unsafe_allow_html=True)

# --- 5. TAMPILAN DASHBOARD UTAMA (JIKA SUDAH LOGIN) ---
else:
    # Tombol Logout di Sidebar
    with st.sidebar:
        st.write(f"Halo, {st.secrets['auth']['username']}!")
        if st.button("Keluar / Logout"):
            logout()

    # --- KONEKSI DATA GOOGLE SHEET ---
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        df = conn.read(ttl=60)
        df = df.fillna("-")
    except Exception as e:
        st.error("Gagal koneksi database. Cek internet/secrets.")
        st.stop()

    # --- NAVIGASI STATE DASHBOARD ---
    if 'current_level' not in st.session_state: st.session_state.current_level = 'home'
    if 'selected_category' not in st.session_state: st.session_state.selected_category = None

    def go_home():
        st.session_state.current_level = 'home'
        st.session_state.selected_category = None

    # --- FUNGSI RENDER (TANPA PROGRESS BAR) ---
    def render_file_card(title, link):
        st.markdown(f"""
        <a href="{link}" target="_blank" style="text-decoration:none;">
            <div class="file-card">
                <div>
                    <div class="file-title">📄 {title}</div>
                    <div class="file-meta">Klik untuk membuka</div>
                </div>
                <div style="background:#eef2ff; padding:8px 15px; border-radius:8px; color:#0054A6; font-weight:bold; font-size:12px;">
                    Buka ↗️
                </div>
            </div>
        </a>
        """, unsafe_allow_html=True)

    def render_status_header(title, status):
        # Header Status Sederhana (Tanpa Progress Bar)
        col1, col2 = st.columns([3, 1])
        with col1: st.markdown(f"### 👉 {title}")
        
        status_lower = str(status).lower()
        if "selesai" in status_lower: color = "badge-green"
        elif "jalan" in status_lower or "ongoing" in status_lower: color = "badge-blue"
        else: color = "badge-orange"
        
        with col2: 
            st.markdown(f'<div style="text-align:right;"><span class="status-badge {color}">{status}</span></div>', unsafe_allow_html=True)

    # --- HERO SECTION ---
    st.markdown("""
    <div style="text-align: center; margin-bottom: 30px; padding: 20px; background: white; border-radius: 20px; box-shadow: 0 10px 20px rgba(0,0,0,0.03);">
        <h1 style="color:#0054A6; margin:0; font-size: 2.2rem;">PORTAL KEGIATAN SOSIAL</h1>
        <p style="color:#F7941D; font-weight:600; margin:0;">BPS KABUPATEN SIDOARJO</p>
    </div>
    """, unsafe_allow_html=True)

    # --- LOGIKA KONTEN ---
    search_query = st.text_input("", placeholder="🔍 Cari Kegiatan atau File...", label_visibility="collapsed")
    st.write("")

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
            st.warning("Data tidak ditemukan.")

    else:
        # HOME PAGE (MENU KATEGORI)
        if st.session_state.current_level == 'home':
            kategori_unik = df['Kategori'].unique()
            cols = st.columns(5)
            
            for i, kategori in enumerate(kategori_unik):
                data_kat = df[df['Kategori'] == kategori].iloc[0]
                with cols[i % 5]:
                    if st.button(f"{data_kat['Icon']}\n\n{kategori}\n\n{data_kat['Deskripsi']}", key=kategori):
                        st.session_state.selected_category = kategori
                        st.session_state.current_level = 'detail_view'
                        st.rerun()

        # DETAIL PAGE (ISI)
        elif st.session_state.current_level == 'detail_view':
            selected = st.session_state.selected_category
            if st.button("⬅️ Kembali ke Dashboard"):
                go_home()
                st.rerun()
            
            # Ambil icon & judul
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
                        data_keg = df_sub[df_sub['Nama_Kegiatan'] == keg]
                        
                        with st.expander(f"{keg}", expanded=True):
                            # Panggil Status tanpa Progress
                            render_status_header(keg, data_keg.iloc[0]['Status'])
                            
                            st.markdown("#### 📥 Dokumen")
                            f_cols = st.columns(2)
                            for idx, (index, row) in enumerate(data_keg.iterrows()):
                                with f_cols[idx % 2]:
                                    render_file_card(row['Nama_File'], row['Link_File'])
    
    # Footer
    st.markdown("---")
    st.caption("🔒 Logged in as Admin • Data Sync: Google Sheets")
