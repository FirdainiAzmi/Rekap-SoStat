
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
# CSS (CARD BUTTON ONLY)
# =============================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap');

.stApp {
    background: linear-gradient(135deg, #f0f4f8, #d9e2ec);
    font-family: 'Poppins', sans-serif;
}

#MainMenu, header, footer {visibility:hidden;}

/* ===== CARD BUTTON (HANYA DASHBOARD) ===== */
div.stButton > button:first-child {
    background:white;
    border:none;
    height:160px;
    width:100%;
    border-radius:16px;
    box-shadow:0 4px 20px rgba(0,0,0,0.05);
    font-size:15px;
    font-weight:600;
    padding:20px;
    transition:0.3s;
}

div.stButton > button:first-child:hover {
    transform:translateY(-8px);
    background:linear-gradient(135deg,#0054A6,#007bff);
    color:white;
}
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
            <h3 style="color:#0054A6;margin-bottom:6px;">🔐 Login Portal</h3>
            <p style="font-size:12px;color:#777;margin-bottom:16px;">
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
# HEADER + LOGOUT (KECIL)
# =============================
with st.form("logout_form"):
    col1, col2 = st.columns([6,1])
    with col1:
        st.markdown("### 📊 Selamat datang di Portal Data Statistik Sosial⚡\n Portal ini merupakan dashboard penyimpanan terpusat aset digital kegiatan Sosial Statistik. Gunakan menu di bawah untuk mengakses folder Google Drive, spreadsheet, notulen, dan dokumentasi kegiatan secara cepat dan terstruktur. ")
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
search_query = st.text_input(
    "", placeholder="🔍 Cari Kegiatan atau File...", label_visibility="collapsed"
)

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
            <div>
                <b>📄 {title}</b><br>
                <span style="font-size:12px;color:#777;">Klik untuk membuka</span>
            </div>
            <span style="font-size:12px;color:#0054A6;font-weight:600;">Buka ↗</span>
        </div>
    </a>
    """, unsafe_allow_html=True)

# =============================
# UI LOGIC
# =============================
if search_query:
    results = df[
        df["Nama_Kegiatan"].str.contains(search_query, case=False) |
        df["Nama_File"].str.contains(search_query, case=False)
    ]
    for _, row in results.iterrows():
        st.markdown(f"**{row['Kategori']} > {row['Nama_Kegiatan']}**")
        render_file_card(row["Nama_File"], row["Link_File"])

else:
    if st.session_state.current_level == "home":
        kategori_unik = df["Kategori"].unique()
        cols = st.columns(5)

        for i, kat in enumerate(kategori_unik):
            data = df[df["Kategori"] == kat].iloc[0]
            with cols[i % 5]:
                if st.button(f"{data['Icon']}\n\n{kat}\n\n{data['Deskripsi']}", key=kat):
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
        sub_menus = df_cat["Sub_Menu"].unique()
        tabs = st.tabs(sub_menus)

        for i, tab in enumerate(tabs):
            with tab:
                df_sub = df_cat[df_cat["Sub_Menu"] == sub_menus[i]]
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
login portal
