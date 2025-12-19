import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# =============================
# LOGIN STATE
# =============================
if 'is_logged_in' not in st.session_state:
    st.session_state.is_logged_in = False

# =============================
# KONFIGURASI HALAMAN
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
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

.stApp {
    background: linear-gradient(135deg, #f0f4f8 0%, #d9e2ec 100%);
    font-family: 'Poppins', sans-serif;
}

#MainMenu, footer, header {visibility: hidden;}

div.stButton > button:first-child {
    background: white;
    border: none;
    height: 160px;
    width: 100%;
    border-radius: 16px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.05);
    color: #333;
    font-size: 15px;
    font-weight: 600;
    transition: all 0.3s;
    padding: 20px;
}

div.stButton > button:first-child:hover {
    transform: translateY(-8px);
    box-shadow: 0 15px 30px rgba(0, 84, 166, 0.15);
    background: linear-gradient(135deg, #0054A6 0%, #007bff 100%);
    color: white !important;
}

.file-card {
    background-color: white;
    padding: 15px;
    border-radius: 12px;
    border-left: 5px solid #0054A6;
    box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    margin-bottom: 10px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.file-card:hover {
    transform: scale(1.02);
    box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    cursor: pointer;
}

.file-title { font-weight: 600; }
.file-meta { font-size: 12px; color: #7f8c8d; }

.stTabs [data-baseweb="tab"] {
    height: 50px;
    background-color: white;
    border-radius: 10px 10px 0 0;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)

# =============================
# LOGIN PAGE
# =============================
def login_page():
    st.markdown("""
    <div style="
        display:flex;
        justify-content:center;
        margin-top:8vh;
    ">
        <div style="
            background:white;
            padding:22px;
            width:340px;
            border-radius:16px;
            box-shadow:0 8px 25px rgba(0,0,0,0.08);
            text-align:center;
        ">
            <h2 style="color:#0054A6;margin-bottom:4px;font-size:20px;">
                🔐 Login Portal
            </h2>
            <p style="font-size:12px;color:#777;margin-bottom:16px;">
                Portal Kegiatan Sosial BPS Sidoarjo
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # === INPUT DI CONTAINER (INI KUNCI NYA) ===
    with st.container():
        st.markdown("<div style='max-width:340px;margin:auto;'>", unsafe_allow_html=True)

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Masuk"):
            if username == "admin" and password == "bps123":
                st.session_state.is_logged_in = True
                st.rerun()
            else:
                st.error("Username atau password salah")

        st.markdown("</div>", unsafe_allow_html=True)


if not st.session_state.is_logged_in:
    login_page()
    st.stop()

# =============================
# HEADER + LOGOUT
# =============================
st.markdown("""
<div style="background:white;padding:10px 25px;border-radius:16px;
margin-bottom:20px;box-shadow:0 4px 15px rgba(0,0,0,0.04);
display:flex;justify-content:space-between;align-items:center;">
    <div style="font-weight:600;font-size:14px;color:#0054A6;">
        📊 Portal Kegiatan Sosial BPS Sidoarjo
    </div>
    <form>
        <button name="logout" style="
            background:#f1f5f9;border:none;padding:6px 14px;
            border-radius:8px;font-size:12px;font-weight:600;
            color:#475569;cursor:pointer;">
            Logout
        </button>
    </form>
</div>
""", unsafe_allow_html=True)

if st.query_params.get("logout") is not None:
    st.session_state.is_logged_in = False
    st.query_params.clear()
    st.rerun()

# =============================
# KONEKSI DATA
# =============================
conn = st.connection("gsheets", type=GSheetsConnection)
df = conn.read(ttl=60).fillna("-")

# =============================
# STATE NAVIGASI
# =============================
if 'current_level' not in st.session_state:
    st.session_state.current_level = 'home'
if 'selected_category' not in st.session_state:
    st.session_state.selected_category = None

def go_home():
    st.session_state.current_level = 'home'
    st.session_state.selected_category = None

# =============================
# KOMPONEN
# =============================
def render_file_card(title, link):
    st.markdown(f"""
    <a href="{link}" target="_blank" style="text-decoration:none;">
        <div class="file-card">
            <div>
                <div class="file-title">📄 {title}</div>
                <div class="file-meta">Klik untuk membuka dokumen</div>
            </div>
            <div style="background:#eef2ff;padding:8px 15px;
            border-radius:8px;color:#0054A6;font-size:12px;font-weight:bold;">
                Buka ↗️
            </div>
        </div>
    </a>
    """, unsafe_allow_html=True)

# =============================
# HEADER HERO
# =============================
st.markdown("""
<div style="text-align:center;margin-bottom:30px;padding:20px;
background:white;border-radius:20px;box-shadow:0 10px 20px rgba(0,0,0,0.03);">
    <h1 style="color:#0054A6;margin:0;">PORTAL KEGIATAN SOSIAL</h1>
    <p style="color:#F7941D;font-weight:600;margin:0;">
        BPS KABUPATEN SIDOARJO
    </p>
</div>
""", unsafe_allow_html=True)

# =============================
# SEARCH
# =============================
search_query = st.text_input("", placeholder="🔍 Cari Kegiatan atau File...", label_visibility="collapsed")

# =============================
# UI LOGIC
# =============================
if search_query:
    results = df[
        df['Nama_Kegiatan'].str.contains(search_query, case=False) |
        df['Nama_File'].str.contains(search_query, case=False)
    ]
    for _, row in results.iterrows():
        st.markdown(f"**{row['Kategori']} > {row['Nama_Kegiatan']}**")
        render_file_card(row['Nama_File'], row['Link_File'])

else:
    if st.session_state.current_level == 'home':
        kategori_unik = df['Kategori'].unique()
        cols = st.columns(5)
        for i, kategori in enumerate(kategori_unik):
            data = df[df['Kategori'] == kategori].iloc[0]
            with cols[i % 5]:
                if st.button(f"{data['Icon']}\n\n{kategori}\n\n{data['Deskripsi']}", key=kategori):
                    st.session_state.selected_category = kategori
                    st.session_state.current_level = 'detail_view'
                    st.rerun()

    elif st.session_state.current_level == 'detail_view':
        if st.button("⬅️ Kembali ke Dashboard"):
            go_home()
            st.rerun()

        selected = st.session_state.selected_category
        st.markdown(f"<h2 style='color:#0054A6;'>{selected}</h2>", unsafe_allow_html=True)

        df_cat = df[df['Kategori'] == selected]
        sub_menus = df_cat['Sub_Menu'].unique()
        tabs = st.tabs([f"📂 {sub}" for sub in sub_menus])

        for i, tab in enumerate(tabs):
            with tab:
                df_sub = df_cat[df_cat['Sub_Menu'] == sub_menus[i]]
                kegiatan = df_sub['Nama_Kegiatan'].unique()

                for keg in kegiatan:
                    data_keg = df_sub[df_sub['Nama_Kegiatan'] == keg]
                    with st.expander(keg, expanded=True):
                        st.markdown("#### 📥 Dokumen")
                        cols = st.columns(2)
                        for idx, (_, row) in enumerate(data_keg.iterrows()):
                            with cols[idx % 2]:
                                render_file_card(row['Nama_File'], row['Link_File'])

# =============================
# FOOTER
# =============================
st.markdown("""
<div style="margin-top:40px;text-align:center;font-size:12px;color:#94a3b8;">
    © 2025 Badan Pusat Statistik Kabupaten Sidoarjo<br>
    Data Google Sheets • Auto Sync
</div>
""", unsafe_allow_html=True)
