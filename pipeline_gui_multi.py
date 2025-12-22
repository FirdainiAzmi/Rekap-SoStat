import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# =============================
# FUNGSI BANTUAN
# =============================
def convert_google_drive_link(url):
    if not isinstance(url, str):
        return "https://via.placeholder.com/300x200.png?text=No+Link"
    if url.strip() == "-" or url.strip() == "":
        return "https://via.placeholder.com/300x200.png?text=No+Image"
    if "drive.google.com" in url and "/d/" in url:
        try:
            file_id = url.split('/d/')[1].split('/')[0]
            return f"https://drive.google.com/thumbnail?id={file_id}&sz=w800"
        except:
            return url
    return url

# =============================
# SESSION STATE
# =============================
if "is_logged_in" not in st.session_state:
    st.session_state.is_logged_in = False
if "current_level" not in st.session_state:
    st.session_state.current_level = "home"
if "selected_category" not in st.session_state:
    st.session_state.selected_category = None

# navigasi & search state
if "nav_menu" not in st.session_state:
    st.session_state.nav_menu = None
if "nav_submenu" not in st.session_state:
    st.session_state.nav_submenu = None
if "nav_sub2" not in st.session_state:
    st.session_state.nav_sub2 = None
if "global_search" not in st.session_state:
    st.session_state["global_search"] = ""
if "pending_clear_search" not in st.session_state:
    st.session_state["pending_clear_search"] = False
if st.session_state["pending_clear_search"]:
    st.session_state["global_search"] = ""
    st.session_state["pending_clear_search"] = False

# =============================
# PAGE CONFIG
# =============================
st.set_page_config(
    page_title="Portal Divisi Sosial Statistik",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =============================
# CSS PREMIUM DARK MODE (THE REAL WOW)
# =============================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');

/* --- 1. CORE THEME (Premium Dark Slate) --- */
.stApp {
    background-color: #0f172a !important; /* Deep dark blue slate */
    font-family: 'Inter', sans-serif !important;
    color: #e2e8f0 !important; /* Light grey text for readability */
}

header[data-testid="stHeader"] { background-color: transparent !important; }

h1, h2, h3, h4, h5, h6 {
    color: #ffffff !important;
    font-weight: 800 !important;
    letter-spacing: -0.5px;
}

/* Warna aksen (Electric Blue) */
:root {
    --primary-blue: #3b82f6;
    --glow-blue: rgba(59, 130, 246, 0.5);
    --dark-card: #1e293b;
    --dark-border: #334155;
}

/* --- 2. LOGIN PAGE --- */
.login-container {
    background: var(--dark-card);
    border: 1px solid var(--dark-border);
    border-radius: 24px;
    padding: 40px;
    text-align: center;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
    position: relative;
    overflow: hidden;
}
/* Efek cahaya di atas box login */
.login-container::before {
    content: ''; position: absolute; top: 0; left: 0; right: 0; height: 5px;
    background: linear-gradient(90deg, var(--primary-blue), #60a5fa);
}

/* --- 3. HERO SECTION (Home Page) --- */
.hero-banner {
    text-align: center;
    padding: 60px 20px;
    background: radial-gradient(circle at center, #1e293b 0%, #0f172a 100%);
    border-bottom: 1px solid var(--dark-border);
    margin-bottom: 40px;
}
.hero-title-text {
    font-size: 48px;
    background: linear-gradient(to right, #ffffff, #60a5fa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* --- 4. MODERN MENU CARDS (Dark & Glowing) --- */
/* Bagian Gambar */
div[data-testid="stImage"] {
    background: var(--dark-card);
    border: 1px solid var(--dark-border);
    border-bottom: none;
    border-radius: 16px 16px 0 0;
    padding: 20px;
    display: flex !important; justify-content: center !important; align-items: center !important;
    height: 180px !important;
    margin-bottom: 0px; /* Rapat dengan tombol */
    transition: all 0.3s ease;
}
div[data-testid="stImage"] img {
    height: 140px !important; width: 100% !important;
    object-fit: contain !important; object-position: center !important;
    filter: drop-shadow(0 4px 6px rgba(0,0,0,0.3)); /* Shadow pada logo agar timbul */
}

/* Bagian Tombol (Judul Menu) */
div.stButton > button {
    width: 100%;
    background: var(--dark-card) !important;
    color: #ffffff !important;
    border: 1px solid var(--dark-border) !important;
    border-top: none !important;
    border-radius: 0 0 16px 16px !important;
    padding: 18px !important;
    font-weight: 600 !important;
    text-transform: uppercase;
    letter-spacing: 1px;
    font-size: 13px !important;
    transition: all 0.3s ease !important;
}

/* EFEK HOVER YANG "WOW" */
/* Saat tombol di-hover, ubah warnanya jadi biru terang dan kasih efek glow */
div.stButton > button:hover {
    background: var(--primary-blue) !important;
    border-color: var(--primary-blue) !important;
    color: white !important;
    box-shadow: 0 0 20px var(--glow-blue); /* Efek neon glow */
    transform: translateY(-2px);
}

/* --- 5. INPUT FIELDS (Searchbar & Login) --- */
/* Ubah input jadi gelap agar menyatu dengan tema */
div[data-testid="stTextInput"] input {
    background-color: #1e293b !important; /* Dark input bg */
    color: white !important;
    border: 2px solid var(--dark-border) !important;
    border-radius: 12px !important;
    padding: 12px 20px !important;
}
div[data-testid="stTextInput"] input:focus {
    border-color: var(--primary-blue) !important;
    box-shadow: 0 0 0 3px var(--glow-blue) !important;
}

/* --- 6. DETAIL PAGE ELEMENTS --- */
/* Kartu Header Kategori */
.category-header {
    background: var(--dark-card);
    border: 1px solid var(--dark-border);
    padding: 25px;
    border-radius: 16px;
    display: flex; align-items: center; gap: 20px;
    margin-bottom: 30px;
    box-shadow: 0 10px 30px -10px rgba(0,0,0,0.5);
}
.category-icon-box {
    font-size: 32px; width: 70px; height: 70px;
    background: linear-gradient(135deg, var(--primary-blue), #1e3a8a);
    border-radius: 12px; display: flex; justify-content: center; align-items: center;
    color: white; box-shadow: 0 4px 10px rgba(59, 130, 246, 0.3);
}

/* File List Cards (Sleek Dark Ribbons) */
.file-card-dark {
    background: var(--dark-card);
    border: 1px solid var(--dark-border);
    border-radius: 12px;
    padding: 15px 20px;
    margin-bottom: 12px;
    display: flex; justify-content: space-between; align-items: center;
    transition: all 0.2s;
}
.file-card-dark:hover {
    border-color: var(--primary-blue);
    box-shadow: 0 4px 15px var(--glow-blue);
    transform: translateX(5px);
}
.dl-btn-glow {
    padding: 8px 24px; background: var(--primary-blue);
    color: white !important; border-radius: 6px; text-decoration: none;
    font-weight: 700; font-size: 12px;
    box-shadow: 0 4px 10px rgba(59, 130, 246, 0.4); transition: all 0.3s;
}
.dl-btn-glow:hover {
    background: #60a5fa; box-shadow: 0 0 20px var(--glow-blue);
}

/* Streamlit Elements Overrides (Tabs, Expanders) */
.stTabs [data-baseweb="tab-list"] { gap: 8px; background-color: transparent; }
.stTabs [data-baseweb="tab"] {
    background-color: var(--dark-card); color: #94a3b8; border-radius: 8px; border: 1px solid var(--dark-border);
}
.stTabs [aria-selected="true"] {
    background-color: var(--primary-blue) !important; color: white !important; border: none;
}
.streamlit-expanderHeader {
    background-color: var(--dark-card) !important; color: white !important;
    border: 1px solid var(--dark-border); border-radius: 8px !important;
}

/* --- 7. FOOTER & NAV BUTTONS --- */
.footer {
    text-align: center; padding: 40px 0; margin-top: 60px;
    border-top: 1px solid var(--dark-border); color: #64748b; font-size: 12px;
}
/* Tombol kecil (Logout/Kembali) jadi dark */
div[data-testid="stButton"] > button[aria-label="Logout"],
div[data-testid="stButton"] > button[aria-label="⬅️ Kembali"] {
    background: var(--dark-card) !important; color: #94a3b8 !important;
    border: 1px solid var(--dark-border) !important;
}
div[data-testid="stButton"] > button[aria-label="Logout"]:hover,
div[data-testid="stButton"] > button[aria-label="⬅️ Kembali"]:hover {
    border-color: var(--primary-blue) !important; color: white !important;
}
</style>
""", unsafe_allow_html=True)

# =============================
# LOGIC LOGIN PAGE (HARDCODED - TETAP SAMA)
# =============================
def login_page():
    col1, col2, col3 = st.columns([1, 1.2, 1]) 
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        # Menggunakan class CSS baru
        st.markdown("""
        <div class="login-container">
            <div style="font-size: 50px; margin-bottom: 20px;">🛡️</div>
            <h2 style="margin-bottom:10px;">PORTAL STATISTIK</h2>
            <p style="color:#94a3b8; font-size:14px; margin-bottom:30px;">Divisi Statistik Sosial - Secure Access</p>
        """, unsafe_allow_html=True)

        with st.form("login_form"):
            # Input field akan otomatis kena style gelap dari CSS
            u = st.text_input("Username", placeholder="Username (admin)")
            p = st.text_input("Password", type="password", placeholder="Password (12345)")
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Tombol Login
            if st.form_submit_button("🔒 MASUK DASHBOARD", use_container_width=True):
                # --- LOGIKA HARDCODED ---
                correct_user = "admin"    # GANTI USERNAME DISINI
                correct_pass = "12345"    # GANTI PASSWORD DISINI
                
                if u == correct_user and p == correct_pass:
                    st.session_state.is_logged_in = True
                    st.rerun()
                else:
                    st.error("Akses Ditolak: Username atau Password salah.")
        st.markdown("</div>", unsafe_allow_html=True)

if not st.session_state.is_logged_in:
    login_page()
    st.stop()

# =============================
# DATA FETCHING
# =============================
conn = st.connection("gsheets", type=GSheetsConnection)
df = conn.read(ttl=60).fillna("-")

# Cek kolom wajib
required_cols = ["Kategori","Link_Gambar","Menu","Sub_Menu","Sub2_Menu","Nama_File","Link_File"]
missing_cols = [c for c in required_cols if c not in df.columns]
if missing_cols:
    st.error(f"Error Database: Kolom {', '.join(missing_cols)} tidak ditemukan di Google Sheet.")
    st.stop()

# =============================
# HEADER AREA (LOGOUT)
# =============================
with st.container():
    c_spacer, c_logout = st.columns([9, 1])
    with c_logout:
        if st.button("Logout", key="logout_top"):
            st.session_state.is_logged_in = False
            st.rerun()

# =============================
# SEARCH BAR (DARK THEME)
# =============================
c_s1, c_s2, c_s3 = st.columns([1, 6, 1])
with c_s2:
    # Input field ini juga akan kena style gelap
    search = st.text_input("", placeholder="🔍 Cari dokumen, kategori, atau menu...", key="global_search")

if search:
    st.markdown(f"<h3 style='text-align:center; margin-top:30px;'>🔍 Hasil Pencarian: '{search}'</h3>", unsafe_allow_html=True)
    st.divider()
    res = df[
        df["Nama_File"].str.contains(search, case=False, na=False) |
        df["Menu"].str.contains(search, case=False, na=False)
    ]
    if res.empty:
        st.warning("Tidak ditemukan dokumen yang cocok.")
    else:
        # Tampilan Hasil Search menggunakan Card Gelap Baru
        for i, r in res.iterrows():
            c1, c2 = st.columns([8.5,1.5])
            with c1:
                st.markdown(f"""
                <div class="file-card-dark" style="margin-bottom:0;">
                    <div>
                        <div style="font-weight:700; font-size:16px; color:white;">📄 {r['Nama_File']}</div>
                        <div style="font-size:12px; color:#94a3b8; margin-top:5px;">📂 {r['Kategori']} > {r['Menu']}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            with c2:
                # Tombol Buka (Navigasi)
                if st.button("Buka ↗", key=f"nav{i}", use_container_width=True):
                    st.session_state.current_level = "detail"
                    st.session_state.selected_category = r["Kategori"]
                    st.session_state.nav_menu = r["Menu"]
                    st.session_state.nav_submenu = r["Sub_Menu"]
                    st.session_state.nav_sub2 = r["Sub2_Menu"]
                    st.session_state["pending_clear_search"] = True
                    st.rerun()
            st.markdown("<br>", unsafe_allow_html=True)
    st.stop()

# =============================
# HOME PAGE "PREMIUM DARK"
# =============================
if st.session_state.current_level == "home":
    
    # HERO BANNER BARU
    st.markdown("""
    <div class="hero-banner">
        <h1 class="hero-title-text">PORTAL DATA STATISTIK</h1>
        <p style="color:#94a3b8; font-size:18px; margin-top:10px;">Pusat Repositori Digital & Arsip Divisi Sosial</p>
    </div>
    """, unsafe_allow_html=True)
    
    # GRID MENU (Tampilan Dark Card)
    unique_cats = df["Kategori"].unique()
    cols = st.columns(4) 
    
    for i, kat in enumerate(unique_cats):
        d = df[df["Kategori"] == kat].iloc[0]
        
        with cols[i % 4]:
            with st.container():
                # GAMBAR (Centered & Shadowed Logo)
                raw_link = d['Link_Gambar']
                final_img_link = convert_google_drive_link(raw_link)
                st.image(final_img_link, use_container_width=True)
                
                # TOMBOL (Dark Button with Neon Hover)
                if st.button(kat, key=f"btn_home_{i}", use_container_width=True):
                    st.session_state.selected_category = kat
                    st.session_state.current_level = "detail"
                    st.rerun()
            
            st.markdown("<div style='margin-bottom: 40px;'></div>", unsafe_allow_html=True)

    # FOOTER
    st.markdown("""
    <div class="footer">
      © 2025 BPS KABUPATEN SIDOARJO<br>Developed by Tim Sosial
    </div>
    """, unsafe_allow_html=True)
                
    st.stop()

# =============================
# DETAIL PAGE "PREMIUM DARK"
# =============================
# Tombol Kembali (Dark Style)
if st.button("⬅️ KEMBALI KE MENU UTAMA"):
    st.session_state.current_level = "home"
    st.session_state.selected_category = None
    st.rerun()

st.markdown("<br>", unsafe_allow_html=True)

# HEADER KATEGORI (Dark Card with Icon)
st.markdown(f"""
<div class="category-header">
    <div class="category-icon-box">📂</div>
    <div>
        <h1 style="margin:0; font-size:32px;">{st.session_state.selected_category}</h1>
        <p style="margin:5px 0 0 0; color:#94a3b8;">Kumpulan dokumen dan arsip digital</p>
    </div>
</div>
""", unsafe_allow_html=True)

# FILTER AREA (Menggunakan Expander Dark)
with st.expander("🔎 KLIK UNTUK FILTER & SORTIR DATA", expanded=False):
    st.markdown("<div style='padding:10px;'>", unsafe_allow_html=True)
    c_f1, c_f2, c_f3 = st.columns(3)
    
    menu_list = ["Semua"] + sorted(df_cat["Menu"].unique().tolist())
    with c_f1: f_menu = st.selectbox("FILTER MENU", menu_list)
    df_f = df_cat if f_menu == "Semua" else df_cat[df_cat["Menu"] == f_menu]

    sub_list = ["Semua"] + sorted(df_f["Sub_Menu"].unique().tolist())
    with c_f2: f_sub = st.selectbox("FILTER SUB MENU", sub_list)
    df_f2 = df_f if f_sub == "Semua" else df_f[df_f["Sub_Menu"] == f_sub]

    sub2_list = ["Semua"] + sorted(df_f2["Sub2_Menu"].unique().tolist())
    with c_f3: f_sub2 = st.selectbox("FILTER SUB2 MENU", sub2_list)
    df_view = df_f2 if f_sub2 == "Semua" else df_f2[df_f2["Sub2_Menu"] == f_sub2]
    st.markdown("</div>", unsafe_allow_html=True)

st.divider()

# CONTENT TABS & FILE LIST
menus = df_view["Menu"].unique()
if len(menus) > 0:
    # Tabs sekarang memiliki style gelap
    tabs_menu = st.tabs(menus.tolist())
    for i, tab in enumerate(tabs_menu):
        with tab:
            st.markdown("<br>", unsafe_allow_html=True)
            df_m = df_view[df_view["Menu"] == menus[i]]
            sub_menus = df_m["Sub_Menu"].unique()
            if len(sub_menus) > 0:
                for j, sub_m_name in enumerate(sub_menus):
                    st.markdown(f"#### 📌 {sub_m_name}")
                    df_s = df_m[df_m["Sub_Menu"] == sub_m_name]
                    
                    for sub2 in df_s["Sub2_Menu"].unique():
                        # Expander Sub2 juga gelap
                        with st.expander(f"{sub2}", expanded=False):
                            files = df_s[df_s["Sub2_Menu"]==sub2]
                            cols_file = st.columns(2)
                            for idx, (_, r) in enumerate(files.iterrows()):
                                with cols_file[idx % 2]:
                                    # Menggunakan File Card Dark yang baru
                                    st.markdown(f"""
                                    <div class="file-card-dark">
                                      <div style="display:flex; gap:15px; align-items:center; overflow:hidden;">
                                        <div style="font-size:24px; padding:12px; background:var(--dark-border); border-radius:10px;">📄</div>
                                        <div>
                                          <p style="margin:0; font-weight:700; font-size:14px; color:white;">{r['Nama_File']}</p>
                                          <p style="margin:5px 0 0 0; font-size:11px; color:#94a3b8;">Siap diunduh</p>
                                        </div>
                                      </div>
                                      <a class="dl-btn-glow" href="{r['Link_File']}" target="_blank">UNDUH ⬇️</a>
                                    </div>
                                    """, unsafe_allow_html=True)
                    st.markdown("<br>", unsafe_allow_html=True)
else:
    st.info("Tidak ada dokumen yang ditemukan dalam filter ini.")

# FOOTER DETAIL
st.markdown("""
<div class="footer">
  © 2025 BPS KABUPATEN SIDOARJO - Tim Sosial
</div>
""", unsafe_allow_html=True)

st.session_state.nav_menu = None
st.session_state.nav_submenu = None
st.session_state.nav_sub2 = None
