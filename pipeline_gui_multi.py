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
# CSS "ULTIMATE WOW" (THEME BLUE)
# =============================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');

/* 1. ANIMATED BACKGROUND (Deep Blue Ocean) */
.stApp {
    background: linear-gradient(-45deg, #0f172a, #1e3a8a, #172554, #0f172a);
    background-size: 400% 400%;
    animation: gradientBG 15s ease infinite;
    font-family: 'Poppins', sans-serif !important;
}
@keyframes gradientBG {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

header[data-testid="stHeader"] { background-color: transparent !important; }

/* 2. HERO CARD (GLASSMORPHISM) */
.hero-glass {
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border-radius: 20px;
    border: 1px solid rgba(255, 255, 255, 0.2);
    padding: 40px;
    text-align: center;
    color: white;
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    margin-bottom: 40px;
}
.hero-title {
    font-size: 42px; font-weight: 700; 
    background: -webkit-linear-gradient(#fff, #93c5fd);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 10px;
}

/* 3. MENU CARDS (FLOATING & GLOWING) */
/* Container Button agar menyatu */
div.stButton > button {
    width: 100%;
    border-radius: 0 0 20px 20px !important; /* Rounded bawah */
    border: none !important;
    background: white !important;
    color: #0f172a !important;
    font-weight: 700 !important;
    padding: 15px !important;
    text-transform: uppercase;
    font-size: 13px !important;
    letter-spacing: 1px;
    transition: all 0.3s ease !important;
    box-shadow: 0 10px 20px rgba(0,0,0,0.2) !important;
}

div.stButton > button:hover {
    background: #3b82f6 !important; /* Bright Blue */
    color: white !important;
    letter-spacing: 2px; /* Efek teks melebar */
}

/* Container Gambar (Bagian Atas Kartu) */
div[data-testid="stImage"] {
    background: white;
    border-radius: 20px 20px 0 0; /* Rounded atas */
    padding: 15px;
    display: flex !important;
    justify-content: center !important;
    align-items: center !important;
    height: 180px !important; /* Tinggi fix */
    box-shadow: 0 10px 20px rgba(0,0,0,0.1);
    margin-bottom: -5px; /* Hilangkan celah putih */
    transition: all 0.3s ease;
}

/* Gambar Logo (Tengah & Rapi) */
div[data-testid="stImage"] img {
    height: 150px !important;
    width: 100% !important;
    object-fit: contain !important; /* Logo utuh */
    object-position: center !important;
    filter: drop-shadow(0 5px 5px rgba(0,0,0,0.1));
    transition: transform 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

/* EFEK HOVER CARD SEKALIGUS (Trick CSS) */
/* Saat mouse hover di area container (sulit di streamlit, kita akali via img hover) */
div[data-testid="stImage"]:hover img {
    transform: scale(1.15) translateY(-10px);
}

/* 4. SEARCH BAR MODERN */
div[data-testid="stTextInput"] input {
    background: rgba(255, 255, 255, 0.9) !important;
    border-radius: 50px !important; /* Pill shape */
    border: 2px solid transparent !important;
    padding: 15px 25px !important;
    font-size: 15px;
    color: #0f172a;
    box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    transition: all 0.3s;
}
div[data-testid="stTextInput"] input:focus {
    background: white !important;
    border-color: #3b82f6 !important;
    box-shadow: 0 0 20px rgba(59, 130, 246, 0.5) !important;
    width: 100%;
}

/* 5. LOGIN BOX GLOW */
.login-box {
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 24px;
    padding: 40px;
    box-shadow: 0 20px 50px rgba(0,0,0,0.5);
    text-align: center;
    color: white;
}

/* 6. DETAIL FILE LIST */
.file-card {
    background: white;
    border-radius: 16px;
    padding: 18px;
    border-left: 6px solid #3b82f6;
    margin-bottom: 15px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    box-shadow: 0 5px 15px rgba(0,0,0,0.05);
    transition: transform 0.2s;
}
.file-card:hover {
    transform: translateX(5px);
    box-shadow: 0 8px 25px rgba(59, 130, 246, 0.2);
}

/* TOMBOL DOWNLOAD */
.dl-btn {
    padding: 8px 20px;
    background: #3b82f6;
    color: white !important;
    border-radius: 30px;
    text-decoration: none;
    font-weight: 600;
    font-size: 12px;
    box-shadow: 0 4px 10px rgba(59, 130, 246, 0.4);
    transition: all 0.3s;
}
.dl-btn:hover {
    background: #2563eb;
    box-shadow: 0 6px 15px rgba(37, 99, 235, 0.6);
    transform: translateY(-2px);
}

/* 7. FOOTER & TEXT */
h1, h2, h3, p { color: white; } /* Force text white on dark bg */
.file-card p { color: #0f172a; } /* Kecuali text di dalam kartu putih */
.footer { 
    color: rgba(255,255,255,0.5); 
    text-align: center; 
    margin-top: 50px; 
    font-size: 12px;
    border-top: 1px solid rgba(255,255,255,0.1);
    padding-top: 20px;
}

/* Tombol kecil navigasi */
div[data-testid="stButton"] > button[aria-label="Logout"],
div[data-testid="stButton"] > button[aria-label="⬅️ Kembali"] {
    background: rgba(255,255,255,0.1) !important;
    color: white !important;
    border: 1px solid rgba(255,255,255,0.2) !important;
    border-radius: 10px !important;
}
div[data-testid="stButton"] > button[aria-label="Logout"]:hover,
div[data-testid="stButton"] > button[aria-label="⬅️ Kembali"]:hover {
    background: #3b82f6 !important;
    border-color: #3b82f6 !important;
}

/* EXPANDER (Accordion) */
.streamlit-expanderHeader {
    background-color: white !important;
    color: #0f172a !important;
    border-radius: 10px !important;
}
</style>
""", unsafe_allow_html=True)

# =============================
# LOGIC LOGIN PAGE
# =============================
def login_page():
    col1, col2, col3 = st.columns([1, 1.2, 1]) 
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("""
        <div class="login-box">
            <div style="font-size: 60px; margin-bottom: 10px;">🔐</div>
            <h2 style="font-weight:700; margin-bottom:5px;">Secure Portal</h2>
            <p style="opacity:0.7; font-size:14px; margin-bottom:30px;">Divisi Statistik Sosial</p>
        """, unsafe_allow_html=True)

        with st.form("login_form"):
            u = st.text_input("Username", placeholder="Enter Username")
            p = st.text_input("Password", type="password", placeholder="Enter Password")
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Tombol Login
            if st.form_submit_button("Masuk Dashboard", use_container_width=True):
                try:
                    correct_user = st.secrets["login"]["username"]
                    correct_pass = st.secrets["login"]["password"]
                    if u == correct_user and p == correct_pass:
                        st.session_state.is_logged_in = True
                        st.rerun()
                    else:
                        st.error("Akses Ditolak!")
                except:
                    st.error("Setup secrets.toml dulu!")
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
    st.error(f"Error Database: Kolom {', '.join(missing_cols)} tidak ditemukan.")
    st.stop()

# =============================
# LAYOUT UTAMA (HEADER)
# =============================
# Tombol Logout dipojok kanan atas
with st.container():
    c_logo, c_space, c_logout = st.columns([2, 8, 1])
    with c_logout:
        if st.button("Logout", key="logout_top"):
            st.session_state.is_logged_in = False
            st.rerun()

# =============================
# SEARCH BAR (CENTERED GLOW)
# =============================
c1, c2, c3 = st.columns([1, 6, 1])
with c2:
    search = st.text_input("", placeholder="🔍 Cari dokumen, data, atau kategori...", key="global_search")

if search:
    st.markdown(f"<h3 style='text-align:center'>🔍 Hasil Pencarian: '{search}'</h3>", unsafe_allow_html=True)
    res = df[
        df["Nama_File"].str.contains(search, case=False, na=False) |
        df["Menu"].str.contains(search, case=False, na=False)
    ]
    if res.empty:
        st.warning("Tidak ditemukan dokumen yang cocok.")
    else:
        for i, r in res.iterrows():
            c1, c2 = st.columns([9,1])
            with c1:
                st.markdown(f"""
                <div class="file-card">
                    <div>
                        <div style="font-weight:700; color:#0f172a; font-size:16px;">{r['Nama_File']}</div>
                        <div style="font-size:12px; color:#64748b;">📂 {r['Kategori']} > {r['Menu']}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            with c2:
                if st.button("Go ↗", key=f"nav{i}"):
                    st.session_state.current_level = "detail"
                    st.session_state.selected_category = r["Kategori"]
                    st.session_state.nav_menu = r["Menu"]
                    st.session_state.nav_submenu = r["Sub_Menu"]
                    st.session_state.nav_sub2 = r["Sub2_Menu"]
                    st.session_state["pending_clear_search"] = True
                    st.rerun()
    st.stop()

# =============================
# HOME PAGE "WOW BLUE THEME"
# =============================
if st.session_state.current_level == "home":
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # HERO SECTION (GLASS)
    st.markdown("""
    <div class="hero-glass">
        <h1 class="hero-title">Portal Statistik Sosial</h1>
        <p style="font-size:16px; opacity:0.9;">Pusat Data & Repositori Digital Badan Pusat Statistik</p>
    </div>
    """, unsafe_allow_html=True)
    
    # GRID MENU
    unique_cats = df["Kategori"].unique()
    cols = st.columns(4) 
    
    for i, kat in enumerate(unique_cats):
        d = df[df["Kategori"] == kat].iloc[0]
        
        with cols[i % 4]:
            with st.container():
                # GAMBAR (Centered Logic)
                raw_link = d['Link_Gambar']
                final_img_link = convert_google_drive_link(raw_link)
                st.image(final_img_link, use_container_width=True)
                
                # TOMBOL (Styled via CSS)
                if st.button(kat, key=f"btn_home_{i}", use_container_width=True):
                    st.session_state.selected_category = kat
                    st.session_state.current_level = "detail"
                    st.rerun()
            
            st.markdown("<div style='margin-bottom: 40px;'></div>", unsafe_allow_html=True)

    # FOOTER
    st.markdown("""
    <div class="footer">
      Developed with 💙 by Tim Sosial BPS Sidoarjo © 2025
    </div>
    """, unsafe_allow_html=True)
                
    st.stop()

# =============================
# DETAIL PAGE
# =============================
# Tombol Kembali
if st.button("⬅️ Kembali Menu Utama"):
    st.session_state.current_level = "home"
    st.session_state.selected_category = None
    st.rerun()

st.markdown("<br>", unsafe_allow_html=True)

# HEADER KATEGORI
df_cat = df[df["Kategori"] == st.session_state.selected_category]
st.markdown(f"""
<div style="background:rgba(255,255,255,0.1); padding:20px; border-radius:15px; border:1px solid rgba(255,255,255,0.2); display:flex; align-items:center; gap:15px; margin-bottom:20px;">
    <div style="font-size:32px; background:white; width:60px; height:60px; border-radius:12px; display:flex; justify-content:center; align-items:center; box-shadow:0 4px 10px rgba(0,0,0,0.1);">📂</div>
    <div>
        <h1 style="margin:0; font-size:28px; color:white;">{st.session_state.selected_category}</h1>
        <p style="margin:0; color:rgba(255,255,255,0.7); font-size:14px;">Arsip Dokumen Digital</p>
    </div>
</div>
""", unsafe_allow_html=True)

# FILTER AREA
with st.expander("🔎 Klik disini untuk Filter Data", expanded=False):
    c_f1, c_f2, c_f3 = st.columns(3)
    
    menu_list = ["Semua"] + sorted(df_cat["Menu"].unique().tolist())
    with c_f1: f_menu = st.selectbox("Pilih Menu", menu_list)
    df_f = df_cat if f_menu == "Semua" else df_cat[df_cat["Menu"] == f_menu]

    sub_list = ["Semua"] + sorted(df_f["Sub_Menu"].unique().tolist())
    with c_f2: f_sub = st.selectbox("Pilih Sub Menu", sub_list)
    df_f2 = df_f if f_sub == "Semua" else df_f[df_f["Sub_Menu"] == f_sub]

    sub2_list = ["Semua"] + sorted(df_f2["Sub2_Menu"].unique().tolist())
    with c_f3: f_sub2 = st.selectbox("Pilih Sub2 Menu", sub2_list)
    df_view = df_f2 if f_sub2 == "Semua" else df_f2[df_f2["Sub2_Menu"] == f_sub2]

st.divider()

# CONTENT TABS (Nested)
menus = df_view["Menu"].unique()
if len(menus) > 0:
    # Styling Tabs Text Color (Streamlit default tabs are black on white, let's keep them readable)
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
                        with st.expander(f"{sub2}", expanded=False):
                            files = df_s[df_s["Sub2_Menu"]==sub2]
                            cols_file = st.columns(2)
                            for idx, (_, r) in enumerate(files.iterrows()):
                                with cols_file[idx % 2]:
                                    st.markdown(f"""
                                    <div class="file-card">
                                      <div style="display:flex; gap:12px; align-items:center; overflow:hidden;">
                                        <div style="font-size:24px; padding:10px; background:#eff6ff; border-radius:10px;">📄</div>
                                        <div>
                                          <p style="margin:0; font-weight:700; font-size:14px; color:#0f172a;">{r['Nama_File']}</p>
                                          <p style="margin:0; font-size:11px; color:#64748b;">Klik tombol unduh disamping</p>
                                        </div>
                                      </div>
                                      <a class="dl-btn" href="{r['Link_File']}" target="_blank">Unduh ⬇️</a>
                                    </div>
                                    """, unsafe_allow_html=True)
                    st.markdown("<br>", unsafe_allow_html=True)
else:
    st.info("Tidak ada dokumen yang ditemukan.")

# FOOTER DETAIL
st.markdown("""
<div class="footer">
  Developed with 💙 by Tim Sosial BPS Sidoarjo © 2025
</div>
""", unsafe_allow_html=True)

st.session_state.nav_menu = None
st.session_state.nav_submenu = None
st.session_state.nav_sub2 = None
