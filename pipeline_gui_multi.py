import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import date

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
# CSS WOW EDITION (MODERN BLUE)
# =============================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');

/* Main Style */
.stApp {
    background: radial-gradient(circle at top right, #eef2ff, #e0e7ff, #f8fafc);
    font-family: 'Inter', sans-serif;
}

/* Hide Streamlit Elements */
#MainMenu, header, footer {visibility:hidden;}

/* ===== LOGIN CARD GLASSMORPHISM ===== */
.login-container {
    background: rgba(255, 255, 255, 0.7);
    backdrop-filter: blur(15px);
    border: 1px solid rgba(255, 255, 255, 0.5);
    padding: 40px;
    border-radius: 24px;
    box-shadow: 0 20px 40px rgba(0,0,0,0.1);
    max-width: 400px;
    margin: 10vh auto;
    text-align: center;
}

/* ===== HEADER BANNER ===== */
.header-banner {
    background: linear-gradient(135deg, #003366 0%, #0054A6 100%);
    padding: 30px;
    border-radius: 20px;
    color: white;
    margin-bottom: 30px;
    box-shadow: 0 10px 25px rgba(0, 84, 166, 0.2);
}

/* ===== DASHBOARD CARD BUTTONS ===== */
div.stButton > button:first-child {
    background: white;
    border: 1px solid #e2e8f0;
    height: 180px;
    width: 100%;
    border-radius: 20px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.02);
    font-size: 16px;
    font-weight: 600;
    color: #1e293b;
    padding: 20px;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    line-height: 1.4;
}

div.stButton > button:first-child:hover {
    transform: translateY(-10px);
    background: white;
    border: 1px solid #0054A6;
    box-shadow: 0 20px 30px rgba(0, 84, 166, 0.15);
    color: #0054A6;
}

/* Icon size inside button */
div.stButton > button p {
    font-size: 40px !important;
    margin-bottom: 10px;
}

/* ===== FILE CARDS ===== */
.file-card {
    background: white;
    padding: 16px 20px;
    border-radius: 14px;
    margin-bottom: 12px;
    border: 1px solid #f1f5f9;
    display: flex;
    justify-content: space-between;
    align-items: center;
    transition: 0.2s;
    text-decoration: none !important;
}

.file-card:hover {
    background: #f8fafc;
    border-color: #0054A6;
    transform: scale(1.01);
}

/* Search Input Styling */
.stTextInput input {
    border-radius: 12px !important;
    padding: 12px 20px !important;
    border: 1px solid #e2e8f0 !important;
    box-shadow: 0 2px 10px rgba(0,0,0,0.02) !important;
}

/* Tab Styling */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
}

.stTabs [data-baseweb="tab"] {
    background-color: transparent;
    border-radius: 8px;
    padding: 10px 20px;
    color: #64748b;
}

.stTabs [aria-selected="true"] {
    background-color: #0054A6 !important;
    color: white !important;
}

</style>
""", unsafe_allow_html=True)

# =============================
# LOGIN PAGE
# =============================
def login_page():
    st.markdown("""
    <div class="login-container">
        <h2 style="color:#0054A6; font-weight:800; margin-bottom:0;">BPS SIDOARJO</h2>
        <p style="color:#64748b; font-size:14px; margin-bottom:30px;">Social Statistics Central Assets</p>
    """, unsafe_allow_html=True)

    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Sign In →", use_container_width=True)

        if submit:
            if username == "admin" and password == "bps123":
                st.session_state.is_logged_in = True
                st.rerun()
            else:
                st.error("Invalid credentials")

    st.markdown("</div>", unsafe_allow_html=True)


if not st.session_state.is_logged_in:
    login_page()
    st.stop()

# =============================
# HEADER SECTION
# =============================
st.markdown(f"""
<div class="header-banner">
    <div style="display:flex; justify-content:space-between; align-items:center;">
        <div>
            <h1 style="margin:0; font-weight:800; font-size:28px;">Portal Data Statistik Sosial ⚡</h1>
            <p style="margin:0; opacity:0.8; font-size:15px;">Dashboard terpusat aset digital Statistik Sosial BPS Kabupaten Sidoarjo</p>
        </div>
        <div style="text-align:right;">
            <p style="margin:0; font-size:12px; opacity:0.7;">{date.today().strftime('%A, %d %B %Y')}</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Logout Button separate from Header to maintain clean look
col_empty, col_logout = st.columns([6, 1])
with col_logout:
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.is_logged_in = False
        st.rerun()

# =============================
# DATA CONNECTION
# =============================
conn = st.connection("gsheets", type=GSheetsConnection)
df = conn.read(ttl=60).fillna("-")

# =============================
# SEARCH BAR (STYLIZED)
# =============================
search_query = st.text_input(
    "", placeholder="🔍 Ketik nama kegiatan, file, atau kategori untuk mencari...", label_visibility="collapsed"
)

# =============================
# FILE CARD FUNCTION
# =============================
def render_file_card(title, link):
    st.markdown(f"""
    <a href="{link}" target="_blank" class="file-card">
        <div>
            <span style="color:#1e293b; font-weight:600;">📄 {title}</span><br>
            <span style="font-size:11px; color:#94a3b8; text-transform:uppercase; letter-spacing:0.5px;">Click to open file</span>
        </div>
        <div style="background:#eff6ff; color:#0054A6; padding:6px 12px; border-radius:8px; font-size:12px; font-weight:600;">
            OPEN ↗
        </div>
    </a>
    """, unsafe_allow_html=True)

# =============================
# MAIN UI LOGIC
# =============================
if search_query:
    results = df[
        df["Nama_Kegiatan"].str.contains(search_query, case=False) |
        df["Nama_File"].str.contains(search_query, case=False) |
        df["Kategori"].str.contains(search_query, case=False)
    ]
    if results.empty:
        st.info("Data tidak ditemukan. Coba kata kunci lain.")
    else:
        for _, row in results.iterrows():
            st.markdown(f"<span style='font-size:12px; color:#64748b;'>{row['Kategori']} > {row['Nama_Kegiatan']}</span>", unsafe_allow_html=True)
            render_file_card(row["Nama_File"], row["Link_File"])

else:
    if st.session_state.current_level == "home":
        kategori_unik = df["Kategori"].unique()
        # Responsive grid
        cols = st.columns(len(kategori_unik) if len(kategori_unik) <= 5 else 5)

        for i, kat in enumerate(kategori_unik):
            data = df[df["Kategori"] == kat].iloc[0]
            with cols[i % 5]:
                # Custom button with icon and text
                if st.button(f"{data['Icon']}\n\n{kat}\n\n{data['Deskripsi']}", key=kat):
                    st.session_state.selected_category = kat
                    st.session_state.current_level = "detail"
                    st.rerun()

    else:
        # Detail Page Header
        col_back, col_title = st.columns([1, 4])
        with col_back:
            if st.button("⬅️ Kembali", use_container_width=True):
                st.session_state.current_level = "home"
                st.session_state.selected_category = None
                st.rerun()
        
        selected = st.session_state.selected_category
        st.markdown(f"<h2 style='color:#003366; font-weight:800; margin-top:10px;'>{selected}</h2>", unsafe_allow_html=True)

        df_cat = df[df["Kategori"] == selected]
        sub_menus = df_cat["Sub_Menu"].unique()
        tabs = st.tabs([f"📂 {sm}" for sm in sub_menus])

        for i, tab in enumerate(tabs):
            with tab:
                df_sub = df_cat[df_cat["Sub_Menu"] == sub_menus[i]]
                for keg in df_sub["Nama_Kegiatan"].unique():
                    with st.expander(f"📌 {keg}", expanded=True):
                        for _, row in df_sub[df_sub["Nama_Kegiatan"] == keg].iterrows():
                            render_file_card(row["Nama_File"], row["Link_File"])

# =============================
# FOOTER
# =============================
st.markdown("""
<div style="margin-top:80px; padding:20px; text-align:center; font-size:12px; color:#94a3b8; border-top:1px solid #e2e8f0;">
    <b>Badan Pusat Statistik Kabupaten Sidoarjo</b><br>
    Jl. Pahlawan No. 140 Sidoarjo • © 2025 All Rights Reserved
</div>
""", unsafe_allow_html=True)
