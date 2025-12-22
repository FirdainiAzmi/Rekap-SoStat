import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# =============================
# SESSION STATE
# =============================
if "is_logged_in" not in st.session_state:
    st.session_state.is_logged_in = False
if "current_level" not in st.session_state:
    st.session_state.current_level = "home"
if "selected_category" not in st.session_state:
    st.session_state.selected_category = None

# navigasi dari search
if "nav_menu" not in st.session_state:
    st.session_state.nav_menu = None
if "nav_submenu" not in st.session_state:
    st.session_state.nav_submenu = None
if "nav_sub2" not in st.session_state:
    st.session_state.nav_sub2 = None

# key widget search
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
# CSS (STYLE BARU)
# =============================
st.markdown("""
<style>
/* 1. BACKGROUND */
.stApp {
  background: linear-gradient(180deg, #E3F2FD 0%, #F8FAFC 100%) !important;
  background-attachment: fixed;
}
header[data-testid="stHeader"] { background-color: rgba(0,0,0,0) !important; }

/* 2. HEADER */
.page-wrap { padding: 8px 8px 30px; }
.title-row { display: flex; gap: 14px; align-items: center; margin-bottom: 20px; }
.title-ico { font-size: 42px; }
.title-text h1 { margin: 0; font-size: 40px; font-weight: 800; color: #0B2F5B; }

/* 3. PENGATURAN GAMBAR MENU UTAMA */
div[data-testid="stImage"] img {
    height: 150px !important; 
    width: 100% !important;
    object-fit: cover !important;
    border-radius: 12px 12px 0 0;
}

/* 4. TOMBOL DI BAWAH GAMBAR */
div[data-testid="stButton"] > button {
  background: white !important;
  color: #334155 !important;
  border: 1px solid #e2e8f0 !important;
  border-top: none !important;
  border-radius: 0 0 12px 12px !important;
  padding: 12px 0;
  width: 100% !important;
  font-family: 'Segoe UI', sans-serif;
  font-size: 14px;
  font-weight: 700;
  box-shadow: 0 4px 6px rgba(0,0,0,0.02);
  transition: all 0.2s;
}

div[data-testid="stButton"] > button:hover {
  background: #0054A6 !important;
  color: white !important;
  transform: translateY(-2px);
  box-shadow: 0 8px 15px rgba(0, 84, 166, 0.15);
}

/* Reset tombol navigasi kecil */
div[data-testid="stButton"] > button[aria-label="Logout"],
div[data-testid="stButton"] > button[aria-label="⬅️ Kembali"],
div[data-testid="stButton"] > button[aria-label="Masuk Portal"],
div[data-testid="stButton"] > button[aria-label="Buka ↗"] {
  background: #f1f5f9 !important;
  color: #334155 !important;
  border: 1px solid transparent !important;
  border-radius: 8px !important;
  height: auto !important;
  box-shadow: none !important;
  padding: 8px 16px !important;
}

/* 5. CARD FILE (DETAIL PAGE) */
.file-card {
  background: white;
  border-radius: 14px;
  padding: 18px;
  border-left: 5px solid #0B5BD3;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  border: 1px solid #f1f5f9;
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
  height: 100%;
}
.file-card:hover { transform: translateY(-3px); box-shadow: 0 8px 15px rgba(0,0,0,0.08); }
.file-left { display: flex; gap: 12px; align-items: center; overflow: hidden; }
.file-title { font-weight: 700; margin: 0; font-size: 14px; color: #1e293b; line-height: 1.4; }
.file-meta { font-size: 11px; color: #64748b; margin-top: 2px; }
.dl-btn {
  padding: 6px 12px; background: #EFF6FF; border-radius: 10px;
  font-weight: 700; font-size: 12px; text-decoration: none; color: #1D4ED8;
  border: 1px solid #DBEAFE; white-space: nowrap; transition: all 0.2s;
}
.dl-btn:hover { background: #2563EB; color: white; }

/* 6. FOOTER */
.stApp > div:first-child { display: flex; flex-direction: column; min-height: 100vh; }
.footer { margin-top: auto; padding: 14px 0; text-align: center; font-size: 12px; color: #94a3b8; border-top: 1px solid rgba(15,23,42,.08); }
</style>
""", unsafe_allow_html=True)

# =============================
# LOGIC LOGIN PAGE
# =============================
def login_page():
    col1, col2, col3 = st.columns([1, 1.2, 1]) 
    with col2:
        st.markdown("""
        <div style="background:white; padding:30px; border-radius:16px; box-shadow:0 10px 25px rgba(0,0,0,0.05); text-align:center;">
            <h2 style="color:#0B2F5B; margin-bottom:5px;">🔐 Portal Statistik Sosial</h2>
            <p style="color:#64748b; font-size:14px; margin-bottom:20px;">Silakan login untuk mengakses dokumen</p>
        """, unsafe_allow_html=True)

        with st.form("login_form"):
            u = st.text_input("Username", placeholder="Masukkan username")
            p = st.text_input("Password", type="password", placeholder="Masukkan password")
            
            if st.form_submit_button("Masuk Portal", use_container_width=True):
                try:
                    correct_user = st.secrets["login"]["username"]
                    correct_pass = st.secrets["login"]["password"]
                    
                    if u == correct_user and p == correct_pass:
                        st.session_state.is_logged_in = True
                        st.rerun()
                    else:
                        st.error("Username atau Password salah!")
                except:
                    st.error("Cek konfigurasi secrets.toml")

        st.markdown("</div>", unsafe_allow_html=True)

if not st.session_state.is_logged_in:
    login_page()
    st.stop()

# =============================
# HEADER + LOGOUT
# =============================
with st.form("logout_form"):
    col1, col2 = st.columns([6,1])
    with col1:
        st.markdown("""
        <div style="background:linear-gradient(135deg,#0974F1,#9FCCFA);
        padding:20px 24px;border-radius:14px;margin-bottom: 12px;color:white; box-shadow:0 4px 15px rgba(9, 116, 241, 0.2);">
        <h3 style="margin:0 0 5px 0;">🗃️ Portal Data Statistik Sosial</h3>
        <p style="margin:0; opacity:0.9; font-size:14px;">Dashboard penyimpanan terpusat aset digital kegiatan Sosial Statistik.</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("<div style='height:15px'></div>", unsafe_allow_html=True)
        if st.form_submit_button("Logout"):
            st.session_state.is_logged_in = False
            st.rerun()

# =============================
# DATA
# =============================
conn = st.connection("gsheets", type=GSheetsConnection)
df = conn.read(ttl=60).fillna("-")

# ✅ PERBAIKAN DI SINI: Menghapus "Icon" dari daftar wajib
required_cols = ["Kategori","Link_Gambar","Menu","Sub_Menu","Sub2_Menu","Nama_File","Link_File"]
missing_cols = [c for c in required_cols if c not in df.columns]
if missing_cols:
    st.error(f"Kolom Google Sheet belum lengkap. Kurang: {', '.join(missing_cols)}")
    st.stop()

# =============================
# SEARCH BAR
# =============================
search = st.text_input(
    "", placeholder="🔍 Cari & navigasi file...", label_visibility="collapsed", key="global_search"
)

if search:
    res = df[
        df["Nama_File"].str.contains(search, case=False, na=False) |
        df["Menu"].str.contains(search, case=False, na=False)
    ]
    st.markdown("### Hasil Pencarian")
    for i, r in res.iterrows():
        c1, c2 = st.columns([8,2])
        with c1:
            st.markdown(f"**{r['Nama_File']}** <br><span style='font-size:12px;color:#64748b'>{r['Kategori']} → {r['Menu']}</span>", unsafe_allow_html=True)
        with c2:
            if st.button("Buka ↗", key=f"nav{i}"):
                st.session_state.current_level = "detail"
                st.session_state.selected_category = r["Kategori"]
                st.session_state.nav_menu = r["Menu"]
                st.session_state.nav_submenu = r["Sub_Menu"]
                st.session_state.nav_sub2 = r["Sub2_Menu"]
                st.session_state["pending_clear_search"] = True
                st.rerun()
    st.stop()

# =============================
# HOME PAGE
# =============================
if st.session_state.current_level == "home":
    
    unique_cats = df["Kategori"].unique()
    cols = st.columns(4) 
    
    for i, kat in enumerate(unique_cats):
        # Ambil baris pertama kategori ini
        d = df[df["Kategori"] == kat].iloc[0]
        
        with cols[i % 4]:
            with st.container():
                # Tampilkan Gambar
                img_url = d['Link_Gambar']
                if img_url == "-" or pd.isna(img_url):
                    img_url = "https://via.placeholder.com/300x200.png?text=No+Image"
                
                st.image(img_url, use_container_width=True)
                
                # Tombol Judul
                if st.button(kat, key=f"btn_home_{i}", use_container_width=True):
                    st.session_state.selected_category = kat
                    st.session_state.current_level = "detail"
                    st.rerun()
            
            st.markdown("<div style='margin-bottom: 25px;'></div>", unsafe_allow_html=True)

    st.markdown("""
    <div class="footer">
      Developed by Firdaini Azmi & Muhammad Ariq Hibatullah<br>
      © 2025 Badan Pusat Statistik Kabupaten Sidoarjo
    </div>
    """, unsafe_allow_html=True)
                
    st.stop()

# =============================
# DETAIL PAGE
# =============================
with st.form("back"):
    if st.form_submit_button("⬅️ Kembali"):
        st.session_state.current_level = "home"
        st.session_state.selected_category = None
        st.rerun()

df_cat = df[df["Kategori"] == st.session_state.selected_category]

# ✅ PERBAIKAN DI SINI: Header tidak lagi mengambil data Icon dari sheet
# Kita ganti pakai emoji statis "📂"
st.markdown(f"""
<div class="title-row">
  <div class="title-ico">📂</div> 
  <div class="title-text">
    <h1>{st.session_state.selected_category}</h1>
  </div>
</div>
""", unsafe_allow_html=True)

# FILTER
with st.expander("🔎 Filter Data", expanded=False):
    menu_list = ["Semua"] + sorted(df_cat["Menu"].unique().tolist())
    f_menu = st.selectbox("Menu", menu_list)
    df_f = df_cat if f_menu == "Semua" else df_cat[df_cat["Menu"] == f_menu]

    sub_list = ["Semua"] + sorted(df_f["Sub_Menu"].unique().tolist())
    f_sub = st.selectbox("Sub Menu", sub_list)
    df_f2 = df_f if f_sub == "Semua" else df_f[df_f["Sub_Menu"] == f_sub]

    sub2_list = ["Semua"] + sorted(df_f2["Sub2_Menu"].unique().tolist())
    f_sub2 = st.selectbox("Sub2 Menu", sub2_list)
    df_view = df_f2 if f_sub2 == "Semua" else df_f2[df_f2["Sub2_Menu"] == f_sub2]

# TABS & FILE LIST
menus = df_view["Menu"].unique()
if len(menus) > 0:
    tabs_menu = st.tabs(menus.tolist())
    for i, tab in enumerate(tabs_menu):
        with tab:
            df_m = df_view[df_view["Menu"] == menus[i]]
            sub_menus = df_m["Sub_Menu"].unique()
            if len(sub_menus) > 0:
                sub_tabs = st.tabs(sub_menus.tolist())
                for j, st_tab in enumerate(sub_tabs):
                    with st_tab:
                        df_s = df_m[df_m["Sub_Menu"] == sub_menus[j]]
                        for sub2 in df_s["Sub2_Menu"].unique():
                            with st.expander(sub2, expanded=False):
                                files = df_s[df_s["Sub2_Menu"]==sub2]
                                cols_file = st.columns(2)
                                for idx, (_, r) in enumerate(files.iterrows()):
                                    with cols_file[idx % 2]:
                                        st.markdown(f"""
                                        <div class="file-card">
                                          <div class="file-left">
                                            <div style="font-size:24px">📄</div>
                                            <div>
                                              <p class="file-title">{r['Nama_File']}</p>
                                              <p class="file-meta">Klik tombol disamping</p>
                                            </div>
                                          </div>
                                          <a class="dl-btn" href="{r['Link_File']}" target="_blank">Buka ⬇️</a>
                                        </div>
                                        """, unsafe_allow_html=True)
else:
    st.info("Data belum tersedia.")

st.markdown("""
<div class="footer">
  Developed by Firdaini Azmi & Muhammad Ariq Hibatullah<br>
  © 2025 Badan Pusat Statistik Kabupaten Sidoarjo
</div>
""", unsafe_allow_html=True)

# reset nav
st.session_state.nav_menu = None
st.session_state.nav_submenu = None
st.session_state.nav_sub2 = None
