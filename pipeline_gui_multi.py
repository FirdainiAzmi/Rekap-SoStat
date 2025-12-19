import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import time

# --- 1. KONFIGURASI HALAMAN (MODUS WIDE KHUSUS LAPTOP) ---
st.set_page_config(
    page_title="Portal Data BPS",
    page_icon="💻",
    layout="wide", # Wajib Wide agar full screen laptop
    initial_sidebar_state="collapsed"
)

# --- 2. CSS "DESKTOP PREMIUM" ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    /* GLOBAL SETTINGS */
    .stApp { 
        background-color: #f8f9fa;
        font-family: 'Inter', sans-serif;
    }
    
    /* HILANGKAN ELEMENT PENGGANGGU */
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    [data-testid="stSidebar"] {display: none;} /* Sembunyikan Sidebar default */

    /* --- LOGIN PAGE STYLING (CENTERED ON LAPTOP) --- */
    .login-wrapper {
        display: flex; justify-content: center; align-items: center; 
        height: 80vh; /* Tengah layar laptop */
    }
    .login-box {
        background: white; padding: 50px; width: 450px;
        border-radius: 24px; box-shadow: 0 20px 60px rgba(0,0,0,0.08);
        text-align: center; border: 1px solid #eee;
    }

    /* --- DASHBOARD CARDS (UKURAN LAPTOP) --- */
    div.stButton > button:first-child {
        background: white; 
        border: 1px solid #eef2f6; 
        height: 220px; /* Lebih tinggi agar proporsional di laptop */
        width: 100%; 
        border-radius: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.03); 
        color: #444; 
        font-family: 'Inter', sans-serif;
        transition: all 0.3s ease;
        padding: 30px 20px;
        display: flex; flex-direction: column; justify-content: center; align-items: center;
    }
    
    /* Hover Effect Mewah */
    div.stButton > button:first-child:hover {
        transform: translateY(-8px); 
        box-shadow: 0 20px 40px rgba(0, 84, 166, 0.12);
        border-color: #0054A6;
    }
    
    /* Typography di dalam tombol */
    div.stButton > button:first-child p {
        font-size: 16px;
    }

    /* --- FILE CARDS (GRID 3 KOLOM) --- */
    .file-card {
        background-color: white; 
        padding: 20px; 
        border-radius: 12px; 
        border: 1px solid #eee;
        border-left: 6px solid #0054A6; /* Aksen BPS */
        box-shadow: 0 2px 8px rgba(0,0,0,0.02); 
        margin-bottom: 15px; 
        display: flex; justify-content: space-between; align-items: center; 
        transition: transform 0.2s, box-shadow 0.2s;
        height: 90px; /* Tinggi fix agar rapi berjejer */
    }
    .file-card:hover { 
        transform: translateY(-3px); 
        box-shadow: 0 10px 20px rgba(0,0,0,0.08); 
        cursor: pointer; 
        border-color: #0054A6;
    }
    .file-title { font-weight: 600; font-size: 15px; color: #1e293b; margin-bottom: 4px; }
    .file-sub { font-size: 12px; color: #94a3b8; }
    
    /* --- HEADER HERO --- */
    .hero-box {
        background: white; padding: 40px; border-radius: 24px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.02); margin-bottom: 40px;
        display: flex; align-items: center; justify-content: space-between;
    }

    /* --- TABS --- */
    .stTabs [data-baseweb="tab-list"] { gap: 30px; border-bottom: 2px solid #f1f5f9; }
    .stTabs [data-baseweb="tab"] {
        height: 60px; font-size: 16px; font-weight: 600; border: none; background: transparent;
    }
    .stTabs [aria-selected="true"] { color: #0054A6; border-bottom: 3px solid #0054A6; }

</style>
""", unsafe_allow_html=True)

# --- 3. SESSION STATE ---
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'current_level' not in st.session_state: st.session_state.current_level = 'home'
if 'selected_category' not in st.session_state: st.session_state.selected_category = None

# --- 4. DATA CONNECTION ---
def load_data():
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        df = conn.read(ttl=60) # Cache 60 detik
        return df.fillna("-")
    except:
        return None

# --- 5. HALAMAN LOGIN (Layout Laptop) ---
if not st.session_state.logged_in:
    # Grid: Kiri Kosong, Tengah Form, Kanan Kosong
    c1, c2, c3 = st.columns([1, 1, 1])
    
    with c2:
        st.markdown("<br><br><br>", unsafe_allow_html=True) # Spacer vertical
        st.markdown("""
        <div class="login-box" style="margin: auto;">
            <img src="https://upload.wikimedia.org/wikipedia/commons/2/28/Lambang_Badan_Pusat_Statistik_%28BPS%29_Indonesia.svg" width="90" style="margin-bottom:20px;">
            <h2 style="color:#0054A6; font-weight:700;">BPS SIDOARJO</h2>
            <p style="color:#888; margin-bottom:30px;">Internal Data Portal</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Input Form di luar HTML agar fungsional
        user = st.text_input("Username", placeholder="Masukkan User ID", label_visibility="collapsed")
        st.write("")
        pwd = st.text_input("Password", type="password", placeholder="Masukkan Password", label_visibility="collapsed")
        st.write("")
        
        if st.button("LOGIN SYSTEM", use_container_width=True):
            # Cek Password dari secrets.toml
            if user == st.secrets["auth"]["username"] and pwd == st.secrets["auth"]["password"]:
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Akses Ditolak. Cek Username/Password.")

# --- 6. HALAMAN DASHBOARD (Layout Laptop) ---
else:
    df = load_data()
    if df is None:
        st.error("Gagal terhubung ke Database.")
        st.stop()

    # --- HEADER SECTION (NAVIGASI ATAS) ---
    col_logo, col_title, col_user = st.columns([1, 6, 2])
    with col_logo:
        st.image("https://upload.wikimedia.org/wikipedia/commons/2/28/Lambang_Badan_Pusat_Statistik_%28BPS%29_Indonesia.svg", width=60)
    with col_title:
        st.markdown("<h2 style='margin:0; padding-top:10px; color:#0054A6;'>Portal Kegiatan Sosial</h2>", unsafe_allow_html=True)
    with col_user:
        st.markdown(f"<div style='text-align:right; padding-top:15px;'><b>Admin User</b> | <a href='#' target='_self' style='text-decoration:none; color:red;'>Logout</a></div>", unsafe_allow_html=True)
        if st.button("Logout Logic", key="logout_btn", help="Klik untuk keluar"):
            st.session_state.logged_in = False
            st.rerun()

    st.markdown("---")

    # --- LOGIC HOME ---
    if st.session_state.current_level == 'home':
        
        # Search Bar Besar
        s_col1, s_col2 = st.columns([4, 1])
        with s_col1:
            search = st.text_input("", placeholder="🔍 Ketik nama dokumen atau kegiatan...", label_visibility="collapsed")
        
        st.write("") # Spacer

        # JIKA SEARCHING
        if search:
            st.markdown(f"### Hasil Pencarian: {search}")
            mask = df['Nama_Kegiatan'].str.contains(search, case=False) | df['Nama_File'].str.contains(search, case=False)
            res = df[mask]
            
            if not res.empty:
                # Grid 3 Kolom untuk hasil search
                res_cols = st.columns(3)
                for i, (idx, row) in enumerate(res.iterrows()):
                    with res_cols[i % 3]:
                        st.markdown(f"""
                        <a href="{row['Link_File']}" target="_blank" style="text-decoration:none;">
                            <div class="file-card">
                                <div>
                                    <div class="file-title">📄 {row['Nama_File']}</div>
                                    <div class="file-sub">{row['Nama_Kegiatan']}</div>
                                </div>
                                <div>↘️</div>
                            </div>
                        </a>
                        """, unsafe_allow_html=True)
            else:
                st.warning("Tidak ditemukan.")

        # JIKA TIDAK SEARCHING (MENU UTAMA)
        else:
            kategori_unik = df['Kategori'].unique()
            
            # GRID 4 KOLOM (LAYOUT LAPTOP)
            # Menggunakan 4 kolom agar kartu lebar dan nyaman dilihat
            cols = st.columns(4)
            
            for i, kat in enumerate(kategori_unik):
                data_kat = df[df['Kategori'] == kat].iloc[0]
                with cols[i % 4]:
                    # Tombol Kartu Besar
                    # Trik CSS: Gunakan banyak \n agar teks terdorong dan rapi
                    label = f"{data_kat['Icon']}\n\n\n**{kat}**\n\n{data_kat['Deskripsi']}"
                    
                    if st.button(label, key=kat):
                        st.session_state.selected_category = kat
                        st.session_state.current_level = 'detail'
                        st.rerun()

    # --- LOGIC DETAIL (SUB MENU) ---
    elif st.session_state.current_level == 'detail':
        sel = st.session_state.selected_category
        
        # Tombol Back
        if st.button("⬅️ KEMBALI KE DASHBOARD"):
            st.session_state.current_level = 'home'
            st.rerun()
            
        st.markdown(f"## 📂 {sel}")
        
        # Ambil Data Kategori Ini
        df_cat = df[df['Kategori'] == sel]
        subs = df_cat['Sub_Menu'].unique()
        
        # Tabs Navigasi
        tabs = st.tabs([f"{s}" for s in subs])
        
        for i, t in enumerate(tabs):
            sub_now = subs[i]
            with t:
                st.write("")
                df_sub = df_cat[df_cat['Sub_Menu'] == sub_now]
                kegiatan_list = df_sub['Nama_Kegiatan'].unique()
                
                for keg in kegiatan_list:
                    # Expander untuk setiap Kegiatan
                    with st.expander(f"{keg}", expanded=True):
                        # Filter file khusus kegiatan ini
                        df_files = df_sub[df_sub['Nama_Kegiatan'] == keg]
                        
                        # GRID 3 KOLOM UNTUK FILE (Agar padat di layar laptop)
                        file_cols = st.columns(3)
                        
                        for idx, (index, row) in enumerate(df_files.iterrows()):
                            with file_cols[idx % 3]:
                                st.markdown(f"""
                                <a href="{row['Link_File']}" target="_blank" style="text-decoration:none;">
                                    <div class="file-card">
                                        <div style="width:85%;">
                                            <div class="file-title">📄 {row['Nama_File']}</div>
                                            <div class="file-sub">Klik untuk unduh</div>
                                        </div>
                                        <div style="color:#0054A6; font-weight:bold;">⬇</div>
                                    </div>
                                </a>
                                """, unsafe_allow_html=True)
                    st.write("") # Jarak antar expander
