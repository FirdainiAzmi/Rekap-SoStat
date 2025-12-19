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
# CSS (WOW VERSION – SAFE)
# =============================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');

/* =============================
   ROOT & BACKGROUND
============================= */
.stApp {
    background:
        radial-gradient(1200px at 10% 0%, #ffffff 0%, transparent 60%),
        radial-gradient(900px at 90% 10%, #eef4ff 0%, transparent 55%),
        linear-gradient(180deg, #eef3f9 0%, #d9e2ec 100%);
    font-family: 'Poppins', sans-serif;
}

#MainMenu, header, footer {visibility:hidden;}

h1, h2, h3 { letter-spacing: -0.4px; }
p { line-height: 1.65; }

/* =========================
   HERO HEADER (BIRU FIX)
========================= */
section[data-testid="stVerticalBlock"]:nth-of-type(2) {
    background: linear-gradient(135deg, #0054A6, #1e88e5);
    border-radius: 22px;
    padding: 28px 32px;
    margin-bottom: 28px;
    box-shadow: 0 30px 60px rgba(0, 84, 166, 0.35);
}

section[data-testid="stVerticalBlock"]:nth-of-type(2) h3 {
    color: white !important;
    font-size: 1.4rem;
    font-weight: 700;
}

section[data-testid="stVerticalBlock"]:nth-of-type(2) p {
    color: rgba(255,255,255,0.9);
    font-size: 14px;
}

section[data-testid="stVerticalBlock"]:nth-of-type(2) button {
    background: rgba(255,255,255,0.18) !important;
    color: white !important;
    border-radius: 10px !important;
    font-size: 12px !important;
    padding: 6px 14px !important;
    border: none !important;
}

section[data-testid="stVerticalBlock"]:nth-of-type(2) button:hover {
    background: rgba(255,255,255,0.3) !important;
}
/* =========================
   HERO "SELAMAT DATANG" – GRADIENT ONLY
========================= */
section[data-testid="stVerticalBlock"]:nth-of-type(2) {
    background: linear-gradient(
        135deg,
        #0054A6 0%,
        #1e88e5 50%,
        #42a5f5 100%
    );
    border-radius: 22px;
    padding: 30px 34px;
    margin-bottom: 28px;

    box-shadow:
        0 25px 60px rgba(0, 84, 166, 0.45),
        inset 0 1px 0 rgba(255,255,255,0.25);
}

/* Judul tetap */
section[data-testid="stVerticalBlock"]:nth-of-type(2) h3 {
    color: #ffffff !important;
    font-weight: 700;
}

/* Deskripsi tetap */
section[data-testid="stVerticalBlock"]:nth-of-type(2) p {
    color: rgba(255,255,255,0.92);
}

/* Tombol logout */
section[data-testid="stVerticalBlock"]:nth-of-type(2) button {
    background: rgba(255,255,255,0.2) !important;
    color: white !important;
    border-radius: 12px !important;
    border: none !important;
}

section[data-testid="stVerticalBlock"]:nth-of-type(2) button:hover {
    background: rgba(255,255,255,0.35) !important;
}

/* =============================
   GLASS CARD (NON-HERO ONLY)
============================= */
section[data-testid="stVerticalBlock"]:not(:nth-of-type(2)) > div:has(h3) {
    background: rgba(255,255,255,0.75);
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);
    border-radius: 22px;
    padding: 18px 24px;
    box-shadow:
        0 30px 60px rgba(0,0,0,0.08),
        inset 0 1px 0 rgba(255,255,255,0.6);
}

/* =============================
   DASHBOARD CARD (WOW)
============================= */
div.stButton > button:first-child {
    position: relative;
    overflow: hidden;
    background: linear-gradient(145deg, rgba(255,255,255,0.9), rgba(245,248,255,0.9));
    border: 1px solid rgba(255,255,255,0.7);
    height: 170px;
    width: 100%;
    border-radius: 22px;
    box-shadow: 0 18px 40px rgba(0,0,0,0.08);
    font-size: 15px;
    font-weight: 600;
    padding: 22px;
    color: #1e293b;
    transition: all 0.45s cubic-bezier(.2,.8,.2,1);
}

div.stButton > button:first-child:hover {
    transform: translateY(-14px) scale(1.04);
    background: linear-gradient(135deg, #0054A6, #007bff);
    color: white;
    box-shadow: 0 35px 70px rgba(0,84,166,0.35);
}

/* =============================
   SEARCH BAR
============================= */
input {
    background: rgba(255,255,255,0.9) !important;
    border-radius: 16px !important;
    padding: 14px 18px !important;
    box-shadow: 0 10px 25px rgba(0,0,0,0.06);
}

/* =============================
   FILE CARD
============================= */
a > div {
    transition: transform .3s ease, box-shadow .3s ease;
}
a > div:hover {
    transform: translateX(8px);
    box-shadow: 0 18px 35px rgba(0,0,0,0.12);
}

/* =============================
   FOOTER
============================= */
div[style*="© 2025"] { opacity: .85; }
</style>
""", unsafe_allow_html=True)

# =============================
# LOGIN PAGE
# =============================
def login_page():
    st.markdown("""
    <div style="margin-top:8vh;text-align:center;">
        <div style="
            background:white;
            width:340px;
            padding:22px;
            margin:auto;
            border-radius:16px;
            box-shadow:0 8px 25px rgba(0,0,0,0.08);
        ">
            <h3 style="color:#0054A6;">🔐 Login Portal</h3>
            <p style="font-size:12px;color:#777;">Portal Kegiatan Sosial BPS Sidoarjo</p>
    """, unsafe_allow_html=True)

    with st.form("login_form"):
        u = st.text_input("Username")
        p = st.text_input("Password", type="password")
        if st.form_submit_button("Masuk"):
            if u == "admin" and p == "bps123":
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
    col1, col2 = st.columns([6,1])
    with col1:
        st.markdown(
            "### 📊 Selamat datang di Portal Data Statistik Sosial ⚡\n"
            "Portal ini merupakan dashboard penyimpanan terpusat aset digital kegiatan Sosial Statistik."
        )
    with col2:
        if st.form_submit_button("Logout"):
            st.session_state.is_logged_in = False
            st.rerun()

# =============================
# DATA
# =============================
conn = st.connection("gsheets", type=GSheetsConnection)
df = conn.read(ttl=60).fillna("-")

# =============================
# SEARCH
# =============================
search_query = st.text_input("", placeholder="🔍 Cari Kegiatan atau File...", label_visibility="collapsed")

# =============================
# FILE CARD
# =============================
def render_file_card(title, link):
    st.markdown(f"""
    <a href="{link}" target="_blank" style="text-decoration:none;">
        <div style="
            background:white;
            padding:14px;
            border-radius:12px;
            margin-bottom:10px;
            border-left:5px solid #0054A6;
            display:flex;
            justify-content:space-between;
            align-items:center;
        ">
            <div><b>📄 {title}</b><br>
            <span style="font-size:12px;color:#777;">Klik untuk membuka</span></div>
            <span style="font-size:12px;font-weight:600;color:#0054A6;">Buka ↗</span>
        </div>
    </a>
    """, unsafe_allow_html=True)

# =============================
# UI LOGIC
# =============================
if search_query:
    for _, r in df[
        df["Nama_Kegiatan"].str.contains(search_query, case=False) |
        df["Nama_File"].str.contains(search_query, case=False)
    ].iterrows():
        st.markdown(f"**{r['Kategori']} > {r['Nama_Kegiatan']}**")
        render_file_card(r["Nama_File"], r["Link_File"])
else:
    if st.session_state.current_level == "home":
        cols = st.columns(5)
        for i, k in enumerate(df["Kategori"].unique()):
            d = df[df["Kategori"] == k].iloc[0]
            with cols[i % 5]:
                if st.button(f"{d['Icon']}\n\n{k}\n\n{d['Deskripsi']}"):
                    st.session_state.selected_category = k
                    st.session_state.current_level = "detail"
                    st.rerun()
    else:
        if st.button("⬅️ Kembali ke Dashboard"):
            st.session_state.current_level = "home"
            st.rerun()

        st.markdown(f"## {st.session_state.selected_category}")
        df_cat = df[df["Kategori"] == st.session_state.selected_category]
        tabs = st.tabs(df_cat["Sub_Menu"].unique())

        for i, tab in enumerate(tabs):
            with tab:
                for keg in df_cat["Nama_Kegiatan"].unique():
                    with st.expander(keg, expanded=True):
                        for _, r in df_cat[df_cat["Nama_Kegiatan"] == keg].iterrows():
                            render_file_card(r["Nama_File"], r["Link_File"])

# =============================
# FOOTER
# =============================
st.markdown("""
<div style="margin-top:40px;text-align:center;font-size:12px;color:#94a3b8;">
© 2025 Badan Pusat Statistik Kabupaten Sidoarjo<br>
Data Google Sheets • Auto Sync
</div>
""", unsafe_allow_html=True)
