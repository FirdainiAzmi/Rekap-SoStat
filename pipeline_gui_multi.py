import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import time

# --- 1. KONFIGURASI HALAMAN (LAPTOP FIRST) ---
st.set_page_config(
    page_title="Portal Data BPS",
    page_icon="💻",
    layout="wide", # Layout Wide untuk Laptop
    initial_sidebar_state="collapsed"
)

# --- 2. CSS CUSTOM (LOGIN PRESISI + KARTU BIRU UTAMA) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    .stApp { background-color: #f8f9fa; font-family: 'Inter', sans-serif; }
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    [data-testid="stSidebar"] {display: none;}

    /* --- 1. CSS LOGIN PAGE (Tengah Presisi) --- */
    [data-testid="stAppViewContainer"] > .main > .block-container {
        padding-top: 2rem; padding-bottom: 2rem;
    }
    
    .login-header {
        background: white; padding: 40px 40px 20px 40px;
        border-radius: 20px 20px 0 0; text-align: center; border: 1px solid #e0e0e0; border-bottom: none;
    }
    .login-body-wrapper {
        background: white; padding: 10px 40px 40px 40px;
        border-radius: 0 0 20px 20px; border: 1px solid #e0e0e0; border-top: none;
        box-shadow: 0 10px 30px rgba(0,0,0,0.05);
    }
    .stTextInput input {
        background-color: #f8fafc !important; border: 1px solid #e2e8f0 !important;
        border-radius: 10px !important; padding: 12px !important;
    }
    div.stButton > button.login-btn {
        background: #0054A6 !important; color: white !important; border-radius: 10px !important;
        height: 50px !important; font-weight: bold !important; border: none !important; width: 100%;
    }

    /* --- 2. CSS KARTU MENU UTAMA (MATERIAL BLUE - SESUAI GAMBAR) --- */
    /* Ini style khusus untuk tombol kategori di halaman depan agar jadi KOTAK BIRU */
    div[data-testid="stVerticalBlock"] > div:has(div.stButton) > div.stButton > button:first-child:not(.login-btn) {
        background: linear-gradient(135deg, #2196F3 0%, #1976D2 100%); /* Biru Google Sites */
        color: white !important;
        border: none;
        height: 200px; /* Tinggi Kotak Presisi Laptop */
        width: 100%;
        border-radius: 12px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        font-family: 'Inter', sans-serif;
        font-size: 18px;
        font-weight: 600;
        transition: transform 0.2s;
        display: flex; flex-direction: column; justify-content: center; align-items: center;
        white-space: pre-wrap; /* Agar teks bisa enter */
    }
    
    /* Hover Effect */
    div[data-testid="stVerticalBlock"] > div:has(div.stButton) > div.stButton > button:first-child:not(.login-btn):hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 20px rgba(33, 150, 243, 0.4);
        background: linear-gradient(135deg, #42A5F5 0%, #1E88E5 100%);
    }

    /* --- 3. CSS FILE LIST (NORMAL) --- */
    .file-card {
        background: white; padding: 15px; border-radius: 8px; border: 1px solid #eee;
        border-left: 5px solid #0054A6; margin-bottom: 10px; display: flex; justify-content: space-between; align-items: center;
        transition: 0.2s;
    }
    .file-card:hover { transform: scale(1.01); box-shadow: 0 5px 15px rgba(0,0,0,0.05); }
    .stTabs [data-baseweb="tab-list"] { border-bottom: 1px solid #eee; }
    .stTabs [aria-selected="true"] { color: #0054A6; border-bottom: 3px solid #0054A6; }

</style>
""", unsafe_allow_html=True)

# --- 3. SESSION STATE & DATA ---
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'current_level' not in st.session_state: st.session_state.current_level = 'home'
if 'selected_category' not in st.session_state: st.session_state.selected_category = None

def load_data():
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        df = conn.read(ttl=60)
        return df.fillna("-")
    except: return None

# =========================================
# 1. HALAMAN LOGIN (LOGIKA PRESISI)
# =========================================
if not st.session_state.logged_in:
    col1, col2, col3 = st.columns([1, 1.5, 1]) # Kolom tengah lebih lebar utk laptop
    
    with col1: st.write("") # Spacer kiri
    with col3: st.write("") # Spacer kanan
    
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True) # Spacer atas
        # Header HTML
        st.markdown("""
        <div class="login-header">
            <img src="https://upload.wikimedia.org/wikipedia/commons/2/28/Lambang_Badan_Pusat_Statistik_%28BPS%29_Indonesia.svg" width="80" style="margin-bottom:15px;">
            <h3 style="color:#0054A6; margin:0; font-weight:700;">PORTAL SOSIAL</h3>
            <p style="color:#888; font-size:14px; margin-top:5px;">Badan Pusat Statistik Sidoarjo</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Body Form (Inputan)
        st.markdown('<div class="login-body-wrapper">', unsafe_allow_html=True)
        user_input = st.text_input("Username", placeholder="ID Pengguna", label_visibility="collapsed")
        st.write("")
        pass_input = st.text_input("Password", type="password", placeholder="Kata Sandi", label_visibility="collapsed")
        st.write("")
        
        # Tombol Login (Pake class login-btn biar warnanya beda)
        if st.button("MASUK SISTEM", key="login_main", type="primary"):
            # Cek secrets
            try:
                c_user = st.secrets["auth"]["username"]
                c_pass = st.secrets["auth"]["password"]
                if user_input == c_user and pass_input == c_pass:
                    st.session_state.logged_in = True
                    st.rerun()
                else:
                    st.error("Username/Password Salah")
            except:
                st.error("Setup secrets.toml dulu!")
        
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("<div style='text-align:center; margin-top:20px; color:#aaa; font-size:12px;'>© 2025 Tim Pengolahan Data</div>", unsafe_allow_html=True)

# =========================================
# 2. HALAMAN UTAMA (DASHBOARD)
# =========================================
else:
    df = load_data()
    if df is None: st.stop()

    # --- NAVBAR SEDERHANA ---
    c_logo, c_text, c_out = st.columns([0.5, 8, 1])
    with c_logo: st.image("https://upload.wikimedia.org/wikipedia/commons/2/28/Lambang_Badan_Pusat_Statistik_%28BPS%29_Indonesia.svg", width=50)
    with c_text: st.markdown("<h3 style='margin:10px 0 0 0; color:#0054A6;'>Data Dashboard</h3>", unsafe_allow_html=True)
    with c_out: 
        st.write("")
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.rerun()
    st.markdown("---")

    # --- LOGIKA TAMPILAN UTAMA (HOME) ---
    if st.session_state.current_level == 'home':
        
        # 1. Search Bar
        search = st.text_input("", placeholder="🔍 Cari nama kegiatan atau file...", label_visibility="collapsed")
        st.write("")

        # 2. Tampilkan Hasil Search / Menu Utama
        if search:
            st.info(f"Hasil pencarian: {search}")
            mask = df['Nama_Kegiatan'].str.contains(search, case=False) | df['Nama_File'].str.contains(search, case=False)
            res = df[mask]
            for i, r in res.iterrows():
                st.markdown(f"**{r['Kategori']} > {r['Nama_Kegiatan']}**")
                st.markdown(f"<a href='{r['Link_File']}' target='_blank' style='text-decoration:none;'><div class='file-card'>📄 {r['Nama_File']}</div></a>", unsafe_allow_html=True)
        
        else:
            # === INI LOGIKA YANG ANDA MAKSUD ===
            # Menggunakan 3 Kolom agar presisi Laptop (seperti gambar Google Sites)
            
            kategori_unik = df['Kategori'].unique()
            
            # Grid 3 Kolom (Kunci Presisi Laptop)
            cols = st.columns(3) 
            
            for i, kat in enumerate(kategori_unik):
                data_kat = df[df['Kategori'] == kat].iloc[0]
                icon = data_kat['Icon']
                desc = data_kat['Deskripsi']
                
                # Tentukan kolom mana (0, 1, atau 2)
                with cols[i % 3]:
                    # Tombol ini sekarang warnanya BIRU (Cek CSS di atas)
                    # Label pake \n\n biar ada jarak
                    label_btn = f"{icon}\n\n{kat}\n\n{desc}"
                    
                    if st.button(label_btn, key=kat):
                        st.session_state.selected_category = kat
                        st.session_state.current_level = 'detail'
                        st.rerun()

    # --- LOGIKA TAMPILAN DETAIL (ISI FILE) ---
    elif st.session_state.current_level == 'detail':
        sel = st.session_state.selected_category
        
        if st.button("⬅️ KEMBALI"):
            st.session_state.current_level = 'home'
            st.rerun()
            
        st.markdown(f"## 📂 {sel}")
        
        # Ambil Data
        df_cat = df[df['Kategori'] == sel]
        subs = df_cat['Sub_Menu'].unique()
        
        # Tabs
        tabs = st.tabs(list(subs))
        
        for i, t in enumerate(tabs):
            sub_now = subs[i]
            with t:
                st.write("")
                # Filter per sub menu
                df_sub = df_cat[df_cat['Sub_Menu'] == sub_now]
                kegiatan = df_sub['Nama_Kegiatan'].unique()
                
                for keg in kegiatan:
                    with st.expander(f"{keg}", expanded=True):
                        # List File Grid 3 Kolom
                        df_files = df_sub[df_sub['Nama_Kegiatan'] == keg]
                        f_cols = st.columns(3)
                        
                        for idx, (ix, row) in enumerate(df_files.iterrows()):
                            with f_cols[idx % 3]:
                                st.markdown(f"""
                                <a href="{row['Link_File']}" target="_blank" style="text-decoration:none;">
                                    <div class="file-card">
                                        <div style="font-weight:600; font-size:14px; color:#333;">
                                            📄 {row['Nama_File']}
                                        </div>
                                        <div style="font-size:12px; color:blue;">Unduh ⬇</div>
                                    </div>
                                </a>
                                """, unsafe_allow_html=True)
