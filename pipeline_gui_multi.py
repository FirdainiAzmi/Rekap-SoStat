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
    page_title="Portal BPS Sidoarjo",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =============================
# CSS (HANYA TAMPILAN)
# =============================
st.markdown("""
<style>
/* 1. BACKGROUND BERKELAS (Opsi 1: Professional Blue) */
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

/* 4. KARTU TOMBOL UTAMA (HOME) - DIBUAT TIMBUL */
div[data-testid="stButton"] > button {
  background: white !important;
  color: #334155 !important;
  border: 1px solid rgba(255,255,255,0.6) !important; /* Border halus */
  border-radius: 16px !important;
  /* Shadow ini kuncinya: bikin kartu melayang */
  box-shadow: 0 10px 20px rgba(0, 50, 100, 0.08), 0 2px 6px rgba(0, 50, 100, 0.05) !important;
  padding: 20px;
  height: 160px !important;
  width: 100% !important;
  font-family: 'Segoe UI', sans-serif;
  font-size: 15px;
  font-weight: 600;
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1) !important;
}

/* Efek Hover (Saat mouse diarahkan) */
div[data-testid="stButton"] > button:hover {
  transform: translateY(-5px);
  /* Warna berubah jadi gradasi biru BPS saat hover */
  background: linear-gradient(135deg, #0054A6 0%, #007bff 100%) !important;
  color: white !important;
  box-shadow: 0 15px 30px rgba(0, 84, 166, 0.3) !important;
  border: 1px solid transparent !important;
}

/* Reset tombol navigasi kecil agar tidak ikut besar */
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
  /* Shadow konsisten */
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  border-top: 1px solid #f1f5f9;
  border-right: 1px solid #f1f5f9;
  border-bottom: 1px solid #f1f5f9;
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
  transition: transform 0.2s;
}
.file-card:hover {
  transform: translateX(4px);
}
.file-left { display: flex; gap: 12px; align-items: center; }
.file-title { font-weight: 700; margin: 0; font-size: 15px; color: #1e293b; }
.file-meta { font-size: 12px; color: #64748b; margin-top: 2px; }

/* Tombol Download */
.dl-btn {
  padding: 8px 16px;
  background: #EFF6FF;
  border-radius: 10px;
  font-weight: 700;
  font-size: 13px;
  text-decoration: none;
  color: #1D4ED8;
  border: 1px solid #DBEAFE;
  transition: all 0.2s;
}
.dl-btn:hover {
  background: #2563EB;
  color: white;
  box-shadow: 0 4px 10px rgba(37, 99, 235, 0.2);
}

/* 6. TABS (MENU NAVIGASI) */
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

/* 7. TEXT INPUT (SEARCH BAR) */
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
</style>
""", unsafe_allow_html=True)

# =============================
# LOGIN PAGE
# =============================
def login_page():
    st.markdown("""
    <div style="margin-top:10vh;text-align:center">
      <div style="background:white;width:340px;padding:24px;margin:auto;
      border-radius:16px;box-shadow:0 8px 25px rgba(0,0,0,.08)">
        <h3>🔐 Login Portal</h3>
    """, unsafe_allow_html=True)

    with st.form("login_form"):
        u = st.text_input("Username")
        p = st.text_input("Password", type="password")
        if st.form_submit_button("Masuk"):
            if u == "admin" and p == "bps123":
                st.session_state.is_logged_in = True
                st.rerun()
            else:
                st.error("Login salah")

    st.markdown("</div></div>", unsafe_allow_html=True)

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
        <p> Portal ini merupakan dashboard penyimpanan terpusat aset digital kegiatan Sosial Statistik.\n 
        Gunakan menu di bawah untuk mengakses folder Google Drive, spreadsheet, notulen, dan dokumentasi kegiatan secara cepat dan terstruktur. </p>
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

# ✅ HAPUS 'Deskripsi' dari daftar wajib
required_cols = ["Kategori","Icon","Menu","Sub_Menu","Sub2_Menu","Nama_File","Link_File"]
if any(c not in df.columns for c in required_cols):
    st.error("Kolom Google Sheet belum lengkap")
    st.stop()

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

                # ✅ jangan clear langsung; tandai dulu
                st.session_state["pending_clear_search"] = True

                st.rerun()
    st.stop()

# =============================
# HOME
# =============================
if st.session_state.current_level == "home":
    jumlah_kategori = df["Kategori"].nunique()
    cols = st.columns(jumlah_kategori)
    for i, kat in enumerate(df["Kategori"].unique()):
        d = df[df["Kategori"] == kat].iloc[0]
        with cols[i % 5]:
            # ✅ HAPUS bagian deskripsi di tombol
            if st.button(
                f"{d['Icon']}\n\n{kat}", 
                key=f"kat_btn_{kat}",
                use_container_width=True
            ):
                st.session_state.selected_category = kat
                st.session_state.current_level = "detail"
                st.rerun()
                
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

# ✅ HAPUS bagian deskripsi di header detail
st.markdown(f"""
<div class="title-row">
  <div class="title-ico">{first['Icon']}</div>
  <div class="title-text">
    <h1>{st.session_state.selected_category}</h1>
  </div>
</div>
""", unsafe_allow_html=True)

# =============================
# FILTER PANEL (AMAN)
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
# RENDER MENU → SUB → SUB2 → FILE
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
                        for _, r in df_s[df_s["Sub2_Menu"]==sub2].iterrows():
                            st.markdown(f"""
                            <div class="file-card">
                              <div class="file-left">
                                <div>📄</div>
                                <div>
                                  <p class="file-title">{r['Nama_File']}</p>
                                  <p class="file-meta">Klik untuk membuka</p>
                                </div>
                              </div>
                              <a class="dl-btn" href="{r['Link_File']}" target="_blank">Unduh ⬇️</a>
                            </div>
                            """, unsafe_allow_html=True)

# reset nav agar tidak nempel
st.session_state.nav_menu = None
st.session_state.nav_submenu = None
st.session_state.nav_sub2 = None

# =============================
# FOOTER
# =============================
st.markdown("""
<div style="margin-top:40px;text-align:center;font-size:12px;color:#94a3b8;">
© 2025 Badan Pusat Statistik Kabupaten Sidoarjo
</div>
""", unsafe_allow_html=True)
