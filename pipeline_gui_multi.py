import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import re
from urllib.parse import quote

# =============================
# HELPER: LINK DRIVE -> URL GAMBAR (UNTUK st.image)
# =============================
def extract_drive_file_id(url: str):
    if not url or url == "-":
        return None
    url = str(url).strip()
    m = re.search(r"/file/d/([a-zA-Z0-9_-]+)", url)
    if m:
        return m.group(1)
    m = re.search(r"[?&]id=([a-zA-Z0-9_-]+)", url)
    if m:
        return m.group(1)
    return None

def icon_to_image_url(icon_value: str):
    """
    Return URL gambar yang bisa dibaca st.image().
    - Jika direct image URL (.png/.jpg/.webp) -> pakai langsung
    - Jika link Google Drive -> pakai thumbnail endpoint (lebih stabil)
    """
    if icon_value is None:
        return None
    s = str(icon_value).strip()
    if s == "" or s == "-":
        return None

    # harus http(s)
    if not (s.startswith("http://") or s.startswith("https://")):
        return None

    # direct image url
    if re.search(r"\.(png|jpg|jpeg|webp)(\?.*)?$", s, flags=re.IGNORECASE):
        return s

    # drive share link -> thumbnail url
    file_id = extract_drive_file_id(s)
    if file_id:
        return f"https://drive.google.com/thumbnail?id={file_id}&sz=w600"

    return None


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

# ✅ FLAG: untuk clear search DI RUN BERIKUTNYA (aman)
if "pending_clear_search" not in st.session_state:
    st.session_state["pending_clear_search"] = False

# ✅ CLEAR search harus dilakukan SEBELUM widget dibuat
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
# CSS (TAMPILAN BARU - WOW EFFECT)
# =============================
st.markdown("""
<style>
/* 1. BACKGROUND BERKELAS (Professional Blue) */
.stApp {
  background: linear-gradient(180deg, #E3F2FD 0%, #F8FAFC 100%) !important;
  background-attachment: fixed;
}

/* 2. HEADER */
header[data-testid="stHeader"] {
  background-color: rgba(0,0,0,0) !important;
}

/* 3. TYPOGRAPHY */
.page-wrap { padding: 8px 8px 30px; }
.title-row { display: flex; gap: 14px; align-items: center; margin-bottom: 20px; }
.title-ico { font-size: 42px; }
.title-text h1 { margin: 0; font-size: 40px; font-weight: 800; color: #0B2F5B; }
.subtitle { margin: 0; color: #475569; font-weight: 500; }

/* 4. KARTU TOMBOL UTAMA (HOME) - TIMBUL (tetap dipakai buat tombol kecil lain) */
div[data-testid="stButton"] > button {
  background: white !important;
  color: #334155 !important;
  border: 1px solid rgba(255,255,255,0.6) !important;
  border-radius: 16px !important;
  box-shadow: 0 10px 20px rgba(0, 50, 100, 0.08), 0 2px 6px rgba(0, 50, 100, 0.05) !important;
  padding: 20px;
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1) !important;
}

div[data-testid="stButton"] > button:hover {
  transform: translateY(-5px);
  background: linear-gradient(135deg, #0054A6 0%, #007bff 100%) !important;
  color: white !important;
  box-shadow: 0 15px 30px rgba(0, 84, 166, 0.3) !important;
  border: 1px solid transparent !important;
}

/* Reset tombol navigasi kecil */
div[data-testid="stButton"] > button[aria-label="Logout"],
div[data-testid="stButton"] > button[aria-label="⬅️ Kembali"],
div[data-testid="stButton"] > button[aria-label="Buka ↗"] {
  background: initial !important;
  color: initial !important;
  border: initial !important;
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
  border-top: 1px solid #f1f5f9;
  border-right: 1px solid #f1f5f9;
  border-bottom: 1px solid #f1f5f9;
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
  height: 100%;
  transition: transform 0.2s;
}
.file-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 15px rgba(0,0,0,0.08);
}
.file-left { display: flex; gap: 12px; align-items: center; overflow: hidden; }
.file-title { font-weight: 700; margin: 0; font-size: 14px; color: #1e293b; white-space: normal; line-height: 1.4; }
.file-meta { font-size: 11px; color: #64748b; margin-top: 2px; }

/* Tombol Download */
.dl-btn {
  padding: 6px 12px;
  background: #EFF6FF;
  border-radius: 10px;
  font-weight: 700;
  font-size: 12px;
  text-decoration: none;
  color: #1D4ED8;
  border: 1px solid #DBEAFE;
  white-space: nowrap;
  transition: all 0.2s;
}
.dl-btn:hover {
  background: #2563EB;
  color: white;
  box-shadow: 0 4px 10px rgba(37, 99, 235, 0.2);
}

/* 6. TABS */
.stTabs [data-baseweb="tab-list"] { gap: 10px; }
.stTabs [data-baseweb="tab"] {
  height: 50px;
  white-space: pre-wrap;
  background-color: rgba(255,255,255,0.7);
  border-radius: 10px 10px 0 0;
  border: none;
  padding: 0 20px;
  font-weight: 600;
  color: #64748b;
}
.stTabs [aria-selected="true"] {
  background-color: #fff;
  color: #0054A6;
  border-bottom: 3px solid #0054A6;
  box-shadow: 0 -4px 10px rgba(0,0,0,0.02);
}

/* 7. SEARCH BAR */
div[data-testid="stTextInput"] > div > div {
  border-radius: 12px;
  border: 1px solid #cbd5e1;
  background: white;
  box-shadow: 0 2px 5px rgba(0,0,0,0.02);
}
div[data-testid="stTextInput"] > div > div:focus-within {
  border-color: #0054A6;
  box-shadow: 0 0 0 3px rgba(0, 84, 166, 0.1);
}

/* 8. FOOTER */
.stApp > div:first-child {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}
.footer {
  margin-top: auto;
  padding: 14px 0;
  text-align: center;
  font-size: 12px;
  color: #94a3b8;
  border-top: 1px solid rgba(15,23,42,.08);
}

/* HOME CARD KLIK (HTML) */
.cat-card{
  height: 160px;
  width: 100%;
  background: white;
  border-radius: 16px;
  box-shadow: 0 10px 20px rgba(0, 50, 100, 0.08), 0 2px 6px rgba(0, 50, 100, 0.05);
  border: 1px solid rgba(255,255,255,0.6);
  overflow: hidden;
  display: flex;
  flex-direction: column;
  text-decoration: none !important;
  transition: all 0.25s ease;
}
.cat-card:hover{
  transform: translateY(-5px);
  box-shadow: 0 15px 30px rgba(0, 84, 166, 0.25);
}
.cat-img{
  flex: 1;
  display:flex;
  align-items:center;
  justify-content:center;
  background: #f8fafc;
}
.cat-img img{
  width: 100%;
  height: 100%;
  object-fit: cover;         /* gambar memenuhi kotak */
}
.cat-title{
  padding: 10px 12px;
  font-weight: 800;
  color: #334155;
  text-align: center;
  line-height: 1.2;
  font-size: 15px;
}
</style>
""", unsafe_allow_html=True)

# =============================
# LOGIC LOGIN PAGE (UPDATE SECRETS)
# =============================
def login_page():
    col1, col2, col3 = st.columns([1, 1.2, 1]) 
    with col2:
        st.markdown("""
        <div class="login-container">
            <div class="login-header">
                <h2 class="login-title">🔐 Portal Statistik Sosial</h2>
                <p class="login-subtitle">Silakan login untuk mengakses dokumen</p>
            </div>
        """, unsafe_allow_html=True)

        with st.form("login_form"):
            u = st.text_input("Username", placeholder="Masukkan username")
            p = st.text_input("Password", type="password", placeholder="Masukkan password")
            
            if st.form_submit_button("Masuk Portal"):
                try:
                    correct_user = st.secrets["login"]["username"]
                    correct_pass = st.secrets["login"]["password"]
                    
                    if u == correct_user and p == correct_pass:
                        st.session_state.is_logged_in = True
                        st.rerun()
                    else:
                        st.error("Username atau Password salah!")
                except FileNotFoundError:
                    st.error("File secrets.toml belum dibuat!")
                except KeyError:
                    st.error("Konfigurasi secrets [login] belum lengkap!")

        st.markdown("""
            <div style="margin-top:20px; font-size:11px; color:#cbd5e1;">
                &copy; Developed by Firdaini Azmi & Muhammad Ariq Hibatullah
            </div>
        </div>
        """, unsafe_allow_html=True)

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
        padding:16px 20px;border-radius:14px;margin-bottom: 12px;color:white">
        <h3>🗃️Selamat datang di Portal Data Statistik Sosial </h3>
        <p>Portal ini merupakan dashboard penyimpanan terpusat aset digital kegiatan Sosial Statistik.\n
        Gunakan menu di bawah untuk mengakses folder Google Drive, spreadsheet, notulen, dan dokumentasi kegiatan secara cepat dan terstruktur.</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        if st.form_submit_button("Logout"):
            st.session_state.is_logged_in = False
            st.rerun()

# =============================
# DATA
# =============================
conn = st.connection("gsheets", type=GSheetsConnection)
df = conn.read(ttl=60).fillna("-")

required_cols = ["Kategori","Icon","Menu","Sub_Menu","Sub2_Menu","Nama_File","Link_File"]
if any(c not in df.columns for c in required_cols):
    st.error("Kolom Google Sheet belum lengkap")
    st.stop()

# =============================
# NAVIGASI DARI HOME CARD (query param)
# =============================
# jika user klik card, URL jadi ?kat=...
if "kat" in st.query_params:
    kat = st.query_params.get("kat")
    if kat:
        st.session_state.selected_category = kat
        st.session_state.current_level = "detail"
        # bersihin param biar ga nyangkut
        st.query_params.clear()
        st.rerun()

# =============================
# SEARCH BAR (NAVIGASI)
# =============================
search = st.text_input(
    "", placeholder="🔍 Cari & navigasi file...", label_visibility="collapsed", key="global_search"
)

if search:
    res = df[
        df["Nama_File"].str.contains(search, case=False, na=False) |
        df["Menu"].str.contains(search, case=False, na=False) |
        df["Sub_Menu"].str.contains(search, case=False, na=False) |
        df["Sub2_Menu"].str.contains(search, case=False, na=False)
    ]

    st.markdown("### Hasil Pencarian")
    for i, r in res.iterrows():
        c1, c2 = st.columns([8,2])
        with c1:
            st.markdown(f"""
            **{r['Nama_File']}** <span style="font-size:12px;color:#64748b">
            {r['Kategori']} → {r['Menu']} → {r['Sub_Menu']} → {r['Sub2_Menu']}
            </span>
            """, unsafe_allow_html=True)
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
# HOME (GAMBAR SEGEDE KOTAK, JUDUL DI BAWAH, CLICKABLE)
# =============================
if st.session_state.current_level == "home":
    jumlah_kategori = df["Kategori"].nunique()
    cols = st.columns(jumlah_kategori)

    for i, kat in enumerate(df["Kategori"].unique()):
        d = df[df["Kategori"] == kat].iloc[0]
        with cols[i % 5]:
            img_url = icon_to_image_url(d["Icon"])

            # card clickable pakai query param
            kat_q = quote(str(kat))

            if img_url:
                st.markdown(f"""
                <a class="cat-card" href="?kat={kat_q}">
                  <div class="cat-img"><img src="{img_url}" alt="icon"/></div>
                  <div class="cat-title">{kat}</div>
                </a>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <a class="cat-card" href="?kat={kat_q}">
                  <div class="cat-img" style="font-size:64px;">📊</div>
                  <div class="cat-title">{kat}</div>
                </a>
                """, unsafe_allow_html=True)

    st.markdown("""
    <div class="footer">
      Developed by Firdaini Azmi & Muhammad Ariq Hibatullah\n
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
first = df_cat.iloc[0]

st.markdown(f"""
<div class="title-row">
  <div class="title-ico">{first['Icon']}</div>
  <div class="title-text">
    <h1>{st.session_state.selected_category}</h1>
  </div>
</div>
""", unsafe_allow_html=True)

# =============================
# FILTER PANEL
# =============================
with st.expander("🔎 Filter", expanded=False):
    menu_list = ["Semua"] + sorted(df_cat["Menu"].unique().tolist())
    default_menu = st.session_state.nav_menu
    menu_idx = menu_list.index(default_menu) if default_menu in menu_list else 0
    f_menu = st.selectbox("Menu", menu_list, index=menu_idx)
    df_f = df_cat if f_menu == "Semua" else df_cat[df_cat["Menu"] == f_menu]

    sub_list = ["Semua"] + sorted(df_f["Sub_Menu"].unique().tolist())
    default_sub = st.session_state.nav_submenu
    sub_idx = sub_list.index(default_sub) if default_sub in sub_list else 0
    f_sub = st.selectbox("Sub Menu", sub_list, index=sub_idx)
    df_f2 = df_f if f_sub == "Semua" else df_f[df_f["Sub_Menu"] == f_sub]

    sub2_list = ["Semua"] + sorted(df_f2["Sub2_Menu"].unique().tolist())
    default_sub2 = st.session_state.nav_sub2
    sub2_idx = sub2_list.index(default_sub2) if default_sub2 in sub2_list else 0
    f_sub2 = st.selectbox("Sub2 Menu", sub2_list, index=sub2_idx)
    df_view = df_f2 if f_sub2 == "Semua" else df_f2[df_f2["Sub2_Menu"] == f_sub2]

# =============================
# RENDER MENU → SUB → SUB2 → FILE (MODIFIKASI 2 KOLOM)
# =============================
menus = df_view["Menu"].unique()
tabs_menu = st.tabs(menus.tolist())

for i, tab in enumerate(tabs_menu):
    with tab:
        df_m = df_view[df_view["Menu"] == menus[i]]
        sub_tabs = st.tabs(df_m["Sub_Menu"].unique().tolist())

        for j, st_tab in enumerate(sub_tabs):
            with st_tab:
                df_s = df_m[df_m["Sub_Menu"] == df_m["Sub_Menu"].unique()[j]]

                for sub2 in df_s["Sub2_Menu"].unique():
                    with st.expander(sub2, expanded=False):
                        files = df_s[df_s["Sub2_Menu"]==sub2]
                        cols = st.columns(2)

                        for idx, (_, r) in enumerate(files.iterrows()):
                            with cols[idx % 2]:
                                st.markdown(f"""
                                <div class="file-card">
                                  <div class="file-left">
                                    <div style="font-size:24px">📄</div>
                                    <div>
                                      <p class="file-title">{r['Nama_File']}</p>
                                      <p class="file-meta">Klik tombol disamping untuk membuka file</p>
                                    </div>
                                  </div>
                                  <a class="dl-btn" href="{r['Link_File']}" target="_blank">Buka ⬇️</a>
                                </div>
                                """, unsafe_allow_html=True)

st.markdown("""
<div class="footer">
  Developed by Firdaini Azmi & Muhammad Ariq Hibatullah\n
  © 2025 Badan Pusat Statistik Kabupaten Sidoarjo
</div>
""", unsafe_allow_html=True)

# reset nav
st.session_state.nav_menu = None
st.session_state.nav_submenu = None
st.session_state.nav_sub2 = None
