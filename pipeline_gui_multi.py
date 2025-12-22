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
# CSS "WOW" FACTOR (MODERN UI)
# =============================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;800&display=swap');

/* 1. GLOBAL STYLE */
.stApp {
  background-color: #f8fafc !important;
  background-image: radial-gradient(#e2e8f0 1px, transparent 1px);
  background-size: 20px 20px;
  font-family: 'Plus Jakarta Sans', sans-serif !important;
}
header[data-testid="stHeader"] { background-color: transparent !important; }

/* 2. HEADER & HERO SECTION */
.hero-container {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    padding: 40px;
    border-radius: 24px;
    color: white;
    text-align: center;
    margin-bottom: 40px;
    box-shadow: 0 20px 40px rgba(15, 23, 42, 0.2);
    position: relative;
    overflow: hidden;
}
.hero-container::before {
    content: "";
    position: absolute;
    top: -50%; left: -50%; width: 200%; height: 200%;
    background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 60%);
    animation: rotate 20s linear infinite;
}
@keyframes rotate { from {transform: rotate(0deg);} to {transform: rotate(360deg);} }

.hero-title { font-size: 32px; font-weight: 800; margin: 0; z-index: 2; position: relative; letter-spacing: -0.5px; }
.hero-subtitle { font-size: 16px; opacity: 0.8; margin-top: 10px; z-index: 2; position: relative; font-weight: 400; }

/* 3. CARD MENU (GRID) - EFEK 3D */
/* Target kolom container agar terlihat seperti kartu */
div[data-testid="stVerticalBlock"] > div > div[data-testid="stVerticalBlock"] {
    /* Ini menargetkan container pembungkus tombol dan gambar */
}

/* KITA GUNAKAN CSS HACK PINTAR UNTUK MEMBUAT KARTU */
/* Menargetkan kotak gambar + tombol */
div.stButton > button {
    width: 100%;
    border-radius: 0 0 16px 16px !important;
    border: none !important;
    background: white !important;
    color: #1e293b !important;
    font-weight: 700 !important;
    padding: 16px !important;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1) !important;
    transition: all 0.3s ease !important;
    text-transform: uppercase;
    font-size: 12px !important;
    letter-spacing: 0.5px;
}

div.stButton > button:hover {
    background: #0B5BD3 !important;
    color: white !important;
    padding-bottom: 20px !important; /* Efek naik */
}

/* GAMBAR */
div[data-testid="stImage"] {
    background: white;
    border-radius: 16px 16px 0 0;
    padding: 10px;
    box-shadow: 0 -4px 6px -1px rgba(0, 0, 0, 0.05);
    margin-bottom: -5px; /* Nempel sama tombol */
    display: flex; justify-content: center; align-items: center;
}

div[data-testid="stImage"] img {
    height: 140px !important;
    width: 100% !important;
    object-fit: contain !important; /* Logo utuh */
    object-position: center !important;
    transition: transform 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
}

/* Efek Hover pada Gambar saat mouse di area (agak tricky di streamlit, kita buat img nya aja yg zoom) */
div[data-testid="stImage"]:hover img {
    transform: scale(1.1);
}

/* 4. DETAIL PAGE & LIST FILE */
.file-card {
  background: white;
  border-radius: 16px;
  padding: 20px;
  border: 1px solid #f1f5f9;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05);
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  transition: transform 0.2s;
}
.file-card:hover { transform: translateY(-4px); border-color: #0B5BD3; }
.file-title { font-weight: 700; font-size: 15px; color: #1e293b; margin: 0; }
.file-meta { font-size: 12px; color: #64748b; margin-top: 4px; }
.dl-btn {
  padding: 8px 16px; background: linear-gradient(135deg, #0B5BD3, #0046a1);
  border-radius: 8px; font-weight: 600; font-size: 12px; color: white !important;
  text-decoration: none; box-shadow: 0 4px 6px rgba(11, 91, 211, 0.2);
  transition: all 0.2s;
}
.dl-btn:hover { box-shadow: 0 8px 12px rgba(11, 91, 211, 0.3); transform: translateY(-1px); }

/* 5. SEARCH BAR MODERN */
div[data-testid="stTextInput"] input {
    border-radius: 12px !important;
    padding: 12px 20px !important;
    border: 2px solid #e2e8f0 !important;
    font-size: 14px;
    background-color: white;
    box-shadow: 0 4px 6px rgba(0,0,0,0.02);
}
div[data-testid="stTextInput"] input:focus {
    border-color: #0B5BD3 !important;
    box-shadow: 0 0 0 3px rgba(11, 91, 211, 0.1) !important;
}

/* 6. FOOTER */
.footer { 
    margin-top: 60px; padding: 30px 0; text-align: center; 
    font-size: 13px; color: #94a3b8; font-weight: 500;
    border-top: 1px dashed #cbd5e1;
}

/* Navigasi Kecil */
div[data-testid="stButton"] > button[aria-label="Logout"],
div[data-testid="stButton"] > button[aria-label="⬅️ Kembali"] {
    background: #f1f5f9 !important; border: none !important;
    color: #475569 !important; border-radius: 8px !important;
    box-shadow: none !important;
}
</style>
""", unsafe_allow_html=True)

# =============================
# LOGIC LOGIN PAGE (TETAP SAMA)
# =============================
def login_page():
    col1, col2, col3 = st.columns([1, 1, 1]) 
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("""
        <div style="background:white; padding:40px; border-radius:24px; box-shadow:0 20px 50px rgba(0,0,0,0.1); text-align:center;">
            <div style="font-size: 50px; margin-bottom: 10px;">🔐</div>
            <h2 style="color:#0f172a; margin-bottom:10px; font-weight:800;">Portal Statistik</h2>
            <p style="color:#64748b; font-size:14px; margin-bottom:30px;">Divisi Statistik Sosial - Login Area</p>
        """, unsafe_allow_html=True)

        with st.form("login_form"):
            u = st.text_input("Username", placeholder="Username")
            p = st.text_input("Password", type="password", placeholder="Password")
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Tombol Login khusus
            if st.form_submit_button("Masuk Dashboard", use_container_width=True):
                try:
                    correct_user = st.secrets["login"]["username"]
                    correct_pass = st.secrets["login"]["password"]
                    if u == correct_user and p == correct_pass:
                        st.session_state.is_logged_in = True
                        st.rerun()
                    else:
                        st.error("Akses Ditolak: Username/Password salah")
                except:
                    st.error("Konfigurasi secrets.toml belum diatur")
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
# LAYOUT UTAMA (CONTAINER)
# =============================
# Tombol Logout dipojok kanan atas
with st.container():
    c_logo, c_space, c_logout = st.columns([2, 8, 1])
    with c_logout:
        if st.button("Logout", key="logout_top"):
            st.session_state.is_logged_in = False
            st.rerun()

# =============================
# SEARCH BAR (GLOBAL)
# =============================
st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
search = st.text_input("", placeholder="🔍 Ketik judul dokumen, menu, atau kategori...", key="global_search")

if search:
    # TAMPILAN HASIL PENCARIAN
    st.markdown(f"### 🔍 Hasil: '{search}'")
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
                <div style="background:white; padding:15px; border-radius:12px; border:1px solid #e2e8f0; margin-bottom:10px;">
                    <div style="font-weight:700; color:#0f172a;">{r['Nama_File']}</div>
                    <div style="font-size:12px; color:#64748b;">📂 {r['Kategori']} > {r['Menu']}</div>
                </div>
                """, unsafe_allow_html=True)
            with c2:
                if st.button("Buka", key=f"nav{i}"):
                    st.session_state.current_level = "detail"
                    st.session_state.selected_category = r["Kategori"]
                    st.session_state.nav_menu = r["Menu"]
                    st.session_state.nav_submenu = r["Sub_Menu"]
                    st.session_state.nav_sub2 = r["Sub2_Menu"]
                    st.session_state["pending_clear_search"] = True
                    st.rerun()
    st.stop()

# =============================
# HOME PAGE "WOW"
# =============================
if st.session_state.current_level == "home":
    
    # HERO SECTION (BANNER)
    st.markdown("""
    <div class="hero-container">
        <h1 class="hero-title">Portal Statistik Sosial</h1>
        <p class="hero-subtitle">Pusat Repositori Aset Digital & Publikasi Data Statistik</p>
    </div>
    """, unsafe_allow_html=True)
    
    # GRID MENU
    unique_cats = df["Kategori"].unique()
    cols = st.columns(4) 
    
    for i, kat in enumerate(unique_cats):
        d = df[df["Kategori"] == kat].iloc[0]
        
        with cols[i % 4]:
            # Container Cards
            with st.container():
                # GAMBAR (Logic tetap sama)
                raw_link = d['Link_Gambar']
                final_img_link = convert_google_drive_link(raw_link)
                st.image(final_img_link, use_container_width=True)
                
                # TOMBOL (Tampilannya diubah via CSS diatas)
                if st.button(kat, key=f"btn_home_{i}", use_container_width=True):
                    st.session_state.selected_category = kat
                    st.session_state.current_level = "detail"
                    st.rerun()
            
            # Spacer antar baris
            st.markdown("<div style='margin-bottom: 30px;'></div>", unsafe_allow_html=True)

    # FOOTER
    st.markdown("""
    <div class="footer">
      Developed with ❤️ by Tim Sosial<br>
      © 2025 Badan Pusat Statistik Kabupaten Sidoarjo
    </div>
    """, unsafe_allow_html=True)
                
    st.stop()

# =============================
# DETAIL PAGE
# =============================
# Tombol Kembali
if st.button("⬅️ Kembali ke Menu Utama"):
    st.session_state.current_level = "home"
    st.session_state.selected_category = None
    st.rerun()

st.markdown("<br>", unsafe_allow_html=True)

# HEADER KATEGORI
df_cat = df[df["Kategori"] == st.session_state.selected_category]
st.markdown(f"""
<div style="display:flex; align-items:center; gap:15px; margin-bottom:20px;">
    <div style="font-size:32px; background:white; width:60px; height:60px; border-radius:12px; display:flex; justify-content:center; align-items:center; box-shadow:0 4px 10px rgba(0,0,0,0.05);">📂</div>
    <div>
        <h1 style="margin:0; font-size:28px; color:#0f172a;">{st.session_state.selected_category}</h1>
        <p style="margin:0; color:#64748b; font-size:14px;">Menampilkan seluruh dokumen dalam kategori ini</p>
    </div>
</div>
""", unsafe_allow_html=True)

# FILTER AREA
with st.expander("🔎 Filter & Sortir Data", expanded=False):
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

# CONTENT TABS
menus = df_view["Menu"].unique()
if len(menus) > 0:
    tabs_menu = st.tabs(menus.tolist())
    for i, tab in enumerate(tabs_menu):
        with tab:
            df_m = df_view[df_view["Menu"] == menus[i]]
            sub_menus = df_m["Sub_Menu"].unique()
            if len(sub_menus) > 0:
                # Nested Tabs jika ada sub menu
                # Menggunakan container agar rapi
                for j, sub_m_name in enumerate(sub_menus):
                    st.markdown(f"#### 📌 {sub_m_name}")
                    df_s = df_m[df_m["Sub_Menu"] == sub_m_name]
                    
                    for sub2 in df_s["Sub2_Menu"].unique():
                        with st.expander(f"{sub2} (Klik untuk lihat file)", expanded=False):
                            files = df_s[df_s["Sub2_Menu"]==sub2]
                            cols_file = st.columns(2)
                            for idx, (_, r) in enumerate(files.iterrows()):
                                with cols_file[idx % 2]:
                                    # Card File HTML
                                    st.markdown(f"""
                                    <div class="file-card">
                                      <div style="display:flex; gap:12px; align-items:center; overflow:hidden;">
                                        <div style="font-size:28px; padding:10px; background:#eff6ff; border-radius:10px;">📄</div>
                                        <div>
                                          <p class="file-title">{r['Nama_File']}</p>
                                          <p class="file-meta">Dokumen Digital</p>
                                        </div>
                                      </div>
                                      <a class="dl-btn" href="{r['Link_File']}" target="_blank">Download ⬇️</a>
                                    </div>
                                    """, unsafe_allow_html=True)
                    st.markdown("<br>", unsafe_allow_html=True)
else:
    st.info("Tidak ada dokumen yang ditemukan dengan filter ini.")

# FOOTER DETAIL
st.markdown("""
<div class="footer">
  Developed with ❤️ by Tim Sosial<br>
  © 2025 Badan Pusat Statistik Kabupaten Sidoarjo
</div>
""", unsafe_allow_html=True)

# Clean up nav vars
st.session_state.nav_menu = None
st.session_state.nav_submenu = None
st.session_state.nav_sub2 = None
