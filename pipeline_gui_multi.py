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
# CSS (LOGIKA TIDAK DIUBAH)
# =============================
st.markdown("""
<style>
/* ====== CSS KAMU (TIDAK DIUBAH) ====== */
/* taruh CSS kamu yang asli di sini kalau ada */

/* ====== TAMBAHAN CSS UNTUK TAMPILAN DETAIL (MIRIP SCREENSHOT) ====== */
.page-wrap{padding:6px 6px 30px 6px;}
.title-row{display:flex;gap:14px;align-items:center;margin:8px 0 6px;}
.title-ico{font-size:40px;line-height:1;}
.title-text h1{margin:0;font-size:42px;font-weight:800;color:#0B2F5B;}
.subtitle{margin:0;color:#6B7B8C;font-size:15px;}

.section-card{
  background: rgba(255,255,255,0.65);
  border:1px solid rgba(15,23,42,0.08);
  border-radius:14px;
  padding:14px;
  box-shadow: 0 6px 18px rgba(15,23,42,0.06);
}

/* ====== FILE CARD (baru) ====== */
.file-card{
  background:white;
  border-radius:14px;
  border:1px solid rgba(15,23,42,0.08);
  padding:14px;
  display:flex;
  align-items:center;
  justify-content:space-between;
  gap:12px;
  box-shadow:0 10px 22px rgba(15,23,42,0.06);
  margin:8px 0;
  border-left:5px solid #0B5BD3;
}
.file-left{display:flex;gap:10px;align-items:center;}
.file-ico{font-size:22px}
.file-title{font-weight:800;color:#0f172a;margin:0}
.file-meta{font-size:12px;color:#6b7280;margin:2px 0 0 0}

.dl-btn{
  display:inline-flex;
  align-items:center;
  gap:6px;
  padding:10px 14px;
  border-radius:12px;
  background:#EEF5FF;
  color:#0B5BD3;
  font-weight:800;
  text-decoration:none;
  border:1px solid rgba(11,91,211,0.12);
}
.dl-btn:hover{background:#E4F0FF}

.hr{height:1px;background:rgba(15,23,42,0.08);margin:12px 0}

/* expander lebih “card” */
[data-testid="stExpander"]{
  border-radius:14px !important;
  border:1px solid rgba(15,23,42,0.10) !important;
  background: rgba(255,255,255,0.55) !important;
}
</style>
""", unsafe_allow_html=True)

# =============================
# LOGIN PAGE
# =============================
def login_page():
    st.markdown("""
    <div style="margin-top:8vh;text-align:center;">
        <div style="background:white;width:340px;padding:22px;margin:auto;
        border-radius:16px;box-shadow:0 8px 25px rgba(0,0,0,0.08);">
            <h3 style="color:#0054A6;">🔐 Login Portal</h3>
            <p style="font-size:12px;color:#777;">
                Portal Kegiatan Sosial BPS Sidoarjo
            </p>
    """, unsafe_allow_html=True)

    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Masuk")

        if submit:
            if username == "admin" and password == "bps123":
                st.session_state.is_logged_in = True
                st.rerun()
            else:
                st.error("Username atau password salah")

    st.markdown("</div></div>", unsafe_allow_html=True)


if not st.session_state.is_logged_in:
    login_page()
    st.stop()

# =============================
# HEADER + LOGOUT
# =============================
with st.form("logout_form"):
    col1, col2 = st.columns([6, 1])
    with col1:
        st.markdown("""
        <div class="hero-box">
          <h3>📊 Selamat datang di Portal Data Statistik Sosial ⚡</h3>
          <p>
            Portal ini merupakan dashboard penyimpanan terpusat aset digital
            kegiatan Sosial Statistik.
          </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <style>
        .hero-box {
          background: linear-gradient(135deg, #0974F1 0%, #9FCCFA 100%);
          padding: 16px 20px;
          border-radius: 14px;
          margin-bottom: 12px;
        }
        .hero-box h3,
        .hero-box p { color:#ffffff; }
        </style>
        """, unsafe_allow_html=True)
    with col2:
        if st.form_submit_button("Logout"):
            st.session_state.is_logged_in = False
            st.rerun()

# =============================
# DATA (1 SHEET)
# =============================
conn = st.connection("gsheets", type=GSheetsConnection)
df = conn.read(ttl=60).fillna("-")

required_cols = ["Kategori", "Icon", "Deskripsi", "Sub_Menu", "Nama_Kegiatan", "Nama_File", "Link_File"]
missing = [c for c in required_cols if c not in df.columns]
if missing:
    st.error(f"Kolom ini belum ada di Google Sheets: {missing}")
    st.stop()

# =============================
# SEARCH
# =============================
search_query = st.text_input(
    "", placeholder="🔍 Cari Kegiatan atau File...", label_visibility="collapsed"
)

# =============================
# FILE CARD (versi baru untuk detail)
# =============================
def render_file_card_detail(title, link):
    st.markdown(f"""
    <div class="file-card">
      <div class="file-left">
        <div class="file-ico">📄</div>
        <div>
          <p class="file-title">{title}</p>
          <p class="file-meta">Klik untuk membuka</p>
        </div>
      </div>
      <a class="dl-btn" href="{link}" target="_blank">Unduh ⬇️</a>
    </div>
    """, unsafe_allow_html=True)

# =============================
# FILE CARD (versi lama untuk search) - BISA TETAP DIPAKAI
# =============================
def render_file_card(title, link):
    st.markdown(f"""
    <a href="{link}" target="_blank" style="text-decoration:none;">
        <div style="background:white;padding:14px;border-radius:12px;
        margin-bottom:10px;border-left:5px solid #0054A6;
        display:flex;justify-content:space-between;align-items:center;">
            <div>
                <b>📄 {title}</b><br>
                <span style="font-size:12px;color:#777;">Klik untuk membuka</span>
            </div>
            <span style="font-size:12px;color:#0054A6;font-weight:600;">Buka ↗</span>
        </div>
    </a>
    """, unsafe_allow_html=True)

# =============================
# UI LOGIC (LOGIKA UTAMA TETAP)
# =============================
if search_query:
    results = df[
        df["Nama_Kegiatan"].str.contains(search_query, case=False, na=False) |
        df["Nama_File"].str.contains(search_query, case=False, na=False)
    ]
    for _, row in results.iterrows():
        st.markdown(f"**{row['Kategori']} > {row['Nama_Kegiatan']}**")
        render_file_card(row["Nama_File"], row["Link_File"])

else:
    if st.session_state.current_level == "home":
        st.markdown('<div class="kat-grid">', unsafe_allow_html=True)

        kategori_unik = df["Kategori"].unique()
        cols = st.columns(5)

        for i, kat in enumerate(kategori_unik):
            data = df[df["Kategori"] == kat].iloc[0]
            with cols[i % 5]:
                if st.button(f"{data['Icon']}\n\n{kat}\n\n{data['Deskripsi']}", key=f"kat_{kat}"):
                    st.session_state.selected_category = kat
                    st.session_state.current_level = "detail"
                    st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

    else:
        # BACK
        with st.form("back_form"):
            if st.form_submit_button("⬅️ Kembali ke Dashboard"):
                st.session_state.current_level = "home"
                st.session_state.selected_category = None
                st.rerun()

        selected = st.session_state.selected_category
        df_cat = df[df["Kategori"] == selected]

        # ambil icon & deskripsi kategori
        first = df_cat.iloc[0]
        kat_icon = first["Icon"]
        kat_desc = first["Deskripsi"]

        # HEADER mirip screenshot
        st.markdown('<div class="page-wrap">', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="title-row">
          <div class="title-ico">{kat_icon}</div>
          <div class="title-text">
            <h1>{selected}</h1>
            <p class="subtitle">{kat_desc}</p>
          </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="section-card">', unsafe_allow_html=True)

        # TAB SUB MENU (unik)
        sub_menus = df_cat["Sub_Menu"].unique()
        tabs = st.tabs(sub_menus.tolist())

        for i, tab in enumerate(tabs):
            with tab:
                df_sub = df_cat[df_cat["Sub_Menu"] == sub_menus[i]]

                # KEGIATAN (unik)
                for keg in df_sub["Nama_Kegiatan"].unique():
                    with st.expander(keg, expanded=True):
                        st.markdown(f"### 👉 {keg}")
                        st.markdown('<div class="hr"></div>', unsafe_allow_html=True)
                        st.markdown("### 📥 Arsip Dokumen")

                        # GRID KARTU FILE (2 kolom)
                        left, right = st.columns(2)
                        rows = df_sub[df_sub["Nama_Kegiatan"] == keg].reset_index(drop=True)

                        for idx, row in rows.iterrows():
                            if idx % 2 == 0:
                                with left:
                                    render_file_card_detail(row["Nama_File"], row["Link_File"])
                            else:
                                with right:
                                    render_file_card_detail(row["Nama_File"], row["Link_File"])

        st.markdown("</div></div>", unsafe_allow_html=True)

# =============================
# FOOTER
# =============================
st.markdown("""
<div style="margin-top:40px;text-align:center;font-size:12px;color:#94a3b8;">
© 2025 Badan Pusat Statistik Kabupaten Sidoarjo<br>
Data Google Sheets • Auto Sync
</div>
""", unsafe_allow_html=True)
