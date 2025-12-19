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
# CSS
# =============================
st.markdown("""<style>/* CSS KAMU TIDAK DIUBAH */</style>""", unsafe_allow_html=True)

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
          background: linear-gradient(135deg, #595CFF 0%, #C6F8FF 100%);
          padding: 16px 20px;
          border-radius: 14px;
          margin-bottom: 12px;
        }
        
        /* optional: teks di dalamnya */
        .hero-box h3,
        .hero-box p {
          color: #ffffff;
        }
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

# OPTIONAL: cek kolom wajib biar ketahuan kalau sheet belum sesuai
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
# FILE CARD
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
        # sebelumnya: kategori_unik = df["Kategori"]  (ini bikin dobel)
        kategori_unik = df["Kategori"].unique()  # tetap konsep sama: list kategori, tapi unik
        cols = st.columns(5)

        for i, kat in enumerate(kategori_unik):
            data = df[df["Kategori"] == kat].iloc[0]
            with cols[i % 5]:
                if st.button(f"{data['Icon']}\n\n{kat}\n\n{data['Deskripsi']}", key=f"kat_{kat}"):
                    st.session_state.selected_category = kat
                    st.session_state.current_level = "detail"
                    st.rerun()

    else:
        with st.form("back_form"):
            if st.form_submit_button("⬅️ Kembali ke Dashboard"):
                st.session_state.current_level = "home"
                st.session_state.selected_category = None
                st.rerun()

        selected = st.session_state.selected_category
        st.markdown(f"## {selected}")

        df_cat = df[df["Kategori"] == selected]

        # sebelumnya: sub_menus = df_cat["Sub_Menu"] (ini bikin tab dobel)
        sub_menus = df_cat["Sub_Menu"].unique()
        tabs = st.tabs(sub_menus.tolist())

        for i, tab in enumerate(tabs):
            with tab:
                df_sub = df_cat[df_cat["Sub_Menu"] == sub_menus[i]]

                # sebelumnya: for keg in df_sub["Nama_Kegiatan"] (ini bikin expander dobel)
                for keg in df_sub["Nama_Kegiatan"].unique():
                    with st.expander(keg, expanded=True):
                        for _, row in df_sub[df_sub["Nama_Kegiatan"] == keg].iterrows():
                            render_file_card(row["Nama_File"], row["Link_File"])

# =============================
# FOOTER
# =============================
st.markdown("""
<div style="margin-top:40px;text-align:center;font-size:12px;color:#94a3b8;">
© 2025 Badan Pusat Statistik Kabupaten Sidoarjo<br>
Data Google Sheets • Auto Sync
</div>
""", unsafe_allow_html=True)
