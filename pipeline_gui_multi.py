import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import date

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
# CSS OVERHAUL (INSTAMON / MODERN SAAS STYLE)
# =============================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;800&display=swap');

/* Base Font & Background */
html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif;
}

.stApp {
    background-color: #F8FAFC;
}

/* Hide Streamlit Garbage */
#MainMenu, header, footer {visibility:hidden;}

/* ===== MODERN LOGIN CARD ===== */
.login-box {
    background: white;
    padding: 3rem;
    border-radius: 30px;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.08);
    max-width: 450px;
    margin: 8vh auto;
    border: 1px solid #F1F5F9;
}

/* ===== HEADER BANNER (PREMIUM) ===== */
.premium-header {
    background: white;
    padding: 2rem;
    border-radius: 24px;
    border: 1px solid #E2E8F0;
    margin-bottom: 2rem;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.02);
}

/* ===== THE "WOW" CARD BUTTONS ===== */
/* Menargetkan tombol di dashboard utama */
div.stButton > button:first-child {
    background: white !important;
    color: #1E293B !important;
    border: 1px solid #E2E8F0 !important;
    border-radius: 24px !important;
    height: 220px !important;
    width: 100% !important;
    padding: 1.5rem !important;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.02) !important;
    white-space: pre-wrap !important; /* Agar line break \n berfungsi */
    display: flex !important;
    flex-direction: column !important;
    align-items: center !important;
    justify-content: center !important;
}

div.stButton > button:first-child:hover {
    border-color: #3B82F6 !important;
    transform: translateY(-12px) !important;
    box-shadow: 0 20px 25px -5px rgba(59, 130, 246, 0.1) !important;
    background: #F0F7FF !important;
    color: #3B82F6 !important;
}

/* Styling teks di dalam tombol kategori */
div.stButton > button p {
    font-size: 14px !important;
    line-height: 1.5 !important;
}

/* ===== FILE CARD (LIST STYLE) ===== */
.file-card-modern {
    background: white;
    padding: 1.25rem 1.5rem;
    border-radius: 18px;
    border: 1px solid #E2E8F0;
    margin-bottom: 0.75rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    transition: 0.3s ease;
}

.file-card-modern:hover {
    background: #F8FAFC;
    border-color: #3B82F6;
    transform: translateX(10px);
}

/* Tab & Expander Styling */
.stTabs [data-baseweb="tab-list"] { gap: 10px; }
.stTabs [data-baseweb="tab"] {
    background: #EDF2F7;
    border-radius: 12px;
    padding: 8px 20px;
}
.stTabs [aria-selected="true"] {
    background: #3B82F6 !important;
    color: white !important;
}

/* Search Bar Pill */
.stTextInput input {
    border-radius: 50px !important;
    padding: 12px 25px !important;
    border: 1px solid #E2E8F0 !important;
}
</style>
""", unsafe_allow_html=True)

# =============================
# LOGIN LOGIC
# =============================
if "is_logged_in" not in st.session_state: st.session_state.is_logged_in = False
if "current_level" not in st.session_state: st.session_state.current_level = "home"

def login_page():
    st.markdown('<div class="login-box">', unsafe_allow_html=True)
    st.markdown('<h2 style="text-align:center; color:#1E293B; font-weight:800;">Portal BPS</h2>', unsafe_allow_html=True)
    st.markdown('<p style="text-align:center; color:#64748B; margin-bottom:2rem;">Statistik Sosial Central Hub</p>', unsafe_allow_html=True)
    
    with st.form("login_form", clear_on_submit=False):
        u = st.text_input("Username")
        p = st.text_input("Password", type="password")
        if st.form_submit_button("Sign In", use_container_width=True):
            if u == "admin" and p == "bps123":
                st.session_state.is_logged_in = True
                st.rerun()
            else: st.error("Wrong credentials")
    st.markdown('</div>', unsafe_allow_html=True)

if not st.session_state.is_logged_in:
    login_page()
    st.stop()

# =============================
# MAIN HEADER
# =============================
st.markdown(f"""
<div class="premium-header">
    <div style="display:flex; justify-content:space-between; align-items:center;">
        <div>
            <h1 style="margin:0; font-weight:800; color:#1E293B; font-size:24px;">Data Statistik Sosial ⚡</h1>
            <p style="margin:0; color:#64748B;">Pusat kendali dokumen dan aset digital BPS Sidoarjo</p>
        </div>
        <div style="background:#F1F5F9; padding:8px 16px; border-radius:12px; color:#1E293B; font-weight:600; font-size:13px;">
            {date.today().strftime('%B %Y')}
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Logout (Floating Right)
c_main, c_out = st.columns([8,1])
with c_out:
    if st.button("🚪 Keluar", use_container_width=True):
        st.session_state.is_logged_in = False
        st.rerun()

# =============================
# DATA & SEARCH
# =============================
conn = st.connection("gsheets", type=GSheetsConnection)
df = conn.read(ttl=60).fillna("-")

search_q = st.text_input("", placeholder="🔍 Cari apa saja: kegiatan, file, atau kategori...", label_visibility="collapsed")

def render_modern_file(title, link):
    st.markdown(f"""
    <a href="{link}" target="_blank" style="text-decoration:none; color:inherit;">
        <div class="file-card-modern">
            <div>
                <b style="color:#1E293B; display:block; font-size:15px;">{title}</b>
                <span style="font-size:11px; color:#94A3B8; text-transform:uppercase;">Klik untuk akses file ↗</span>
            </div>
            <div style="color:#3B82F6;">
                <svg width="20" height="20" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"></path></svg>
            </div>
        </div>
    </a>
    """, unsafe_allow_html=True)

# =============================
# UI NAVIGATION
# =============================
if search_q:
    res = df[df["Nama_Kegiatan"].str.contains(search_q, case=False) | df["Nama_File"].str.contains(search_q, case=False)]
    for _, row in res.iterrows():
        st.caption(f"{row['Kategori']} > {row['Nama_Kegiatan']}")
        render_modern_file(row["Nama_File"], row["Link_File"])

else:
    if st.session_state.current_level == "home":
        st.markdown("<h4 style='color:#1E293B; margin-bottom:1rem;'>Pilih Kategori</h4>", unsafe_allow_html=True)
        kats = df["Kategori"].unique()
        cols = st.columns(4) # Grid 4 kolom agar tidak terlalu rapat

        for i, kat in enumerate(kats):
            d = df[df["Kategori"] == kat].iloc[0]
            with cols[i % 4]:
                # Tombol Kategori (Card Style)
                # Teks dipecah: Icon (besar), Nama (Bold), Deskripsi (Kecil)
                btn_text = f"{d['Icon']}\n\n{kat}\n\n{d['Deskripsi']}"
                if st.button(btn_text, key=f"btn_{kat}"):
                    st.session_state.selected_category = kat
                    st.session_state.current_level = "detail"
                    st.rerun()

    else:
        # Halaman Detail
        col_back, _ = st.columns([1, 5])
        with col_back:
            if st.button("⬅️ Kembali", use_container_width=True):
                st.session_state.current_level = "home"
                st.rerun()

        sel = st.session_state.selected_category
        st.markdown(f"<h2 style='font-weight:800; color:#1E293B;'>{sel}</h2>", unsafe_allow_html=True)

        df_cat = df[df["Kategori"] == sel]
        subs = df_cat["Sub_Menu"].unique()
        tabs = st.tabs([f"📁 {s}" for s in subs])

        for i, t in enumerate(tabs):
            with t:
                df_sub = df_cat[df_cat["Sub_Menu"] == subs[i]]
                for keg in df_sub["Nama_Kegiatan"].unique():
                    with st.expander(f"📌 {keg}", expanded=True):
                        for _, row in df_sub[df_sub["Nama_Kegiatan"] == keg].iterrows():
                            render_modern_file(row["Nama_File"], row["Link_File"])

# =============================
# FOOTER
# =============================
st.markdown("""
<div style="margin-top:100px; text-align:center; padding-bottom:40px;">
    <p style="color:#94A3B8; font-size:12px;">BPS Kabupaten Sidoarjo © 2025</p>
</div>
""", unsafe_allow_html=True)
