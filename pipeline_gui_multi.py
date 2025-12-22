import streamlit as st
import pandas as pd
import time
import base64
import os

# ================= KONFIGURASI DATABASE =================
CSV_FILE = 'database_sostat.csv'

# Fungsi Load Data (Baca dari CSV saat web dibuka)
def load_data():
    if os.path.exists(CSV_FILE):
        try:
            return pd.read_csv(CSV_FILE)
        except:
            # Jika file rusak/kosong, buat dataframe baru
            return pd.DataFrame(columns=['Kategori', 'Gambar_Base64', 'Menu', 'Sub_Menu', 'Sub2_Menu', 'Nama_File', 'Link_File'])
    else:
        return pd.DataFrame(columns=['Kategori', 'Gambar_Base64', 'Menu', 'Sub_Menu', 'Sub2_Menu', 'Nama_File', 'Link_File'])

# Fungsi Save Data (Simpan ke CSV setiap ada perubahan)
def save_data(df):
    df.to_csv(CSV_FILE, index=False)

# ================= KONFIGURASI HALAMAN =================
st.set_page_config(
    page_title="Sostat Dashboard Pro",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ================= CSS PROFESSIONAL =================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
        background-color: #F8F9FE;
        color: #172B4D;
    }

    /* HERO SECTION */
    .hero-container {
        background: linear-gradient(135deg, #5e72e4 0%, #825ee4 100%);
        padding: 40px 30px;
        border-radius: 20px;
        color: white;
        margin-bottom: 30px;
        box-shadow: 0 7px 14px rgba(50, 50, 93, 0.1), 0 3px 6px rgba(0, 0, 0, 0.08);
    }
    .hero-title { font-size: 2.2rem; font-weight: 700; margin: 0; }
    .hero-subtitle { font-size: 1rem; opacity: 0.9; font-weight: 300; margin-top: 5px; }

    /* STATS CARD */
    .stat-card {
        background: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.02);
        border-left: 5px solid #5e72e4;
        text-align: center;
    }
    .stat-number { font-size: 1.8rem; font-weight: 700; color: #5e72e4; }
    .stat-label { color: #8898aa; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 1px; }

    /* CARD KATEGORI */
    .cat-card {
        background: white;
        border-radius: 16px;
        padding: 25px;
        text-align: center;
        transition: all 0.3s ease;
        border: 1px solid #e9ecef;
        height: 100%;
    }
    .cat-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 15px 35px rgba(50, 50, 93, 0.1);
        border-color: #5e72e4;
    }
    .cat-card img {
        width: 100%;
        height: 120px;
        object-fit: contain;
        margin-bottom: 20px;
    }
    .cat-title {
        font-weight: 700; color: #32325d; font-size: 1.1rem; margin-bottom: 15px;
        min-height: 50px; display: flex; align-items: center; justify-content: center;
    }
    
    /* Tombol & Input */
    .stButton > button { border-radius: 8px; font-weight: 600; border: none; transition: 0.2s; }
    [data-testid="stSidebar"] { background-color: white; border-right: 1px solid #e9ecef; }
</style>
""", unsafe_allow_html=True)

# ================= FUNGSI BANTUAN =================
def image_to_base64(uploaded_file):
    if uploaded_file is not None:
        try:
            return base64.b64encode(uploaded_file.getvalue()).decode()
        except:
            return None
    return None

# ================= STATE MANAGEMENT (DENGAN LOAD DATA) =================
# Init data dari CSV saat pertama kali load
if 'data' not in st.session_state:
    st.session_state['data'] = load_data()

# Refresh data jika state kosong tapi file ada
if st.session_state['data'].empty and os.path.exists(CSV_FILE):
    st.session_state['data'] = load_data()

if 'logged_in' not in st.session_state: st.session_state['logged_in'] = False
if 'current_view' not in st.session_state: st.session_state['current_view'] = 'home'
if 'selected_category' not in st.session_state: st.session_state['selected_category'] = None

# ================= LOGIN =================
def login_page():
    c1, c2, c3 = st.columns([1,1,1])
    with c2:
        st.markdown("<br><br><br>", unsafe_allow_html=True)
        st.markdown("""
        <div style="background:white; padding:40px; border-radius:15px; box-shadow:0 10px 25px rgba(0,0,0,0.05); text-align:center;">
            <h2 style="color:#5e72e4;">🔐 Admin Login</h2>
            <p style="color:#8898aa;">Silakan masuk untuk mengelola data</p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("login"):
            u = st.text_input("Username")
            p = st.text_input("Password", type="password")
            if st.form_submit_button("MASUK SISTEM", use_container_width=True, type="primary"):
                if u=="admin" and p=="admin":
                    st.session_state['logged_in']=True
                    st.rerun()
                else: st.error("Login Gagal")

# ================= ADMIN PAGE (AUTO-SAVE) =================
def admin_page():
    st.markdown("## ⚙️ Panel Admin")
    
    tab1, tab2 = st.tabs(["📝 Input Data Baru", "🗑️ Hapus Data"])
    df = st.session_state['data']

    # --- TAB INPUT ---
    with tab1:
        st.info("💡 Data yang disimpan akan otomatis tertulis ke database (CSV).")
        
        col_kiri, col_kanan = st.columns(2)
        
        with col_kiri:
            st.markdown("### 1. Pengaturan Kategori")
            
            existing_cats = df['Kategori'].unique().tolist() if not df.empty else []
            
            # Logic Mode Input
            pilihan_mode = "Buat Baru" 
            if existing_cats:
                pilihan_mode = st.radio("Pilih Mode Kategori:", ["Gunakan Kategori Lama", "Buat Kategori Baru"], horizontal=True)
            
            final_kategori = ""
            
            # INPUT LOGIC
            if pilihan_mode == "Gunakan Kategori Lama":
                final_kategori = st.selectbox("Pilih Kategori:", existing_cats)
            else:
                final_kategori = st.text_input("Ketik Nama Kategori Baru:", placeholder="Contoh: Statistik Sosial")
            
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("### 📷 Gambar Cover")
            in_img = st.file_uploader("Upload Cover (Opsional)", type=['png','jpg','jpeg'])

        with col_kanan:
            st.markdown("### 2. Detail Dokumen")
            in_menu = st.text_input("Menu Utama", placeholder="Misal: Publikasi")
            in_sub = st.text_input("Sub Menu (Tahun)", placeholder="Misal: 2025")
            in_sub2 = st.text_input("Sub Menu 2 (Bulan/Periode)", placeholder="Misal: Semester 1")
            st.markdown("---")
            in_nama = st.text_input("Judul File (Wajib Diisi)*")
            in_link = st.text_input("Link File (Google Drive/Web)")

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("💾 SIMPAN PERMANEN", type="primary", use_container_width=True):
            if final_kategori and in_nama:
                img_str = image_to_base64(in_img)
                
                if not img_str and final_kategori in existing_cats:
                    try:
                        prev = df[df['Kategori']==final_kategori]['Gambar_Base64'].iloc[0]
                        img_str = prev
                    except: pass
                
                new_row = {
                    'Kategori': final_kategori, 'Gambar_Base64': img_str,
                    'Menu': in_menu, 'Sub_Menu': in_sub, 'Sub2_Menu': in_sub2,
                    'Nama_File': in_nama, 'Link_File': in_link
                }
                
                # Update DataFrame & SAVE TO CSV
                updated_df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                st.session_state['data'] = updated_df
                save_data(updated_df) # <--- SIMPAN KE FILE
                
                st.success("✅ Data tersimpan aman di Database!")
                time.sleep(1)
                st.rerun()
            else:
                st.warning("Mohon isi Nama Kategori dan Judul File.")

    # --- TAB HAPUS ---
    with tab2:
        if df.empty:
            st.warning("Data kosong.")
        else:
            c1, c2, c3 = st.columns(3)
            list_kat = df['Kategori'].unique()
            del_kat = c1.selectbox("Filter Kategori", list_kat)
            
            df_1 = df[df['Kategori']==del_kat]
            if not df_1.empty:
                del_file = c2.selectbox("Pilih File Hapus", df_1['Nama_File'].unique())
                
                c3.markdown("<br>", unsafe_allow_html=True)
                if c3.button("🗑️ Hapus Permanen", type="primary"):
                    idx = df[(df['Kategori']==del_kat) & (df['Nama_File']==del_file)].index
                    
                    # Drop & SAVE TO CSV
                    new_df = df.drop(idx).reset_index(drop=True)
                    st.session_state['data'] = new_df
                    save_data(new_df) # <--- SIMPAN PERMANEN
                    
                    st.success("File dihapus dari sistem.")
                    time.sleep(1)
                    st.rerun()

# ================= HOME DASHBOARD =================
def home_page():
    st.markdown("""
    <div class="hero-container">
        <div class="hero-title">Portal Data Statistik 📊</div>
        <div class="hero-subtitle">Pusat database digital Badan Pusat Statistik. Kelola dan temukan data dengan mudah.</div>
    </div>
    """, unsafe_allow_html=True)
    
    df = st.session_state['data']
    
    # METRICS
    if not df.empty:
        m1, m2, m3 = st.columns(3)
        with m1:
            st.markdown(f"""<div class="stat-card"><div class="stat-number">{len(df['Kategori'].unique())}</div><div class="stat-label">Kategori Data</div></div>""", unsafe_allow_html=True)
        with m2:
            st.markdown(f"""<div class="stat-card"><div class="stat-number">{len(df)}</div><div class="stat-label">Total File</div></div>""", unsafe_allow_html=True)
        with m3:
            st.markdown(f"""<div class="stat-card"><div class="stat-number">{len(df['Menu'].unique())}</div><div class="stat-label">Topik Bahasan</div></div>""", unsafe_allow_html=True)
        
        st.markdown("<br><br>", unsafe_allow_html=True)

    # GRID KATEGORI
    if df.empty:
        st.info("📂 Database masih kosong. Silakan login ke Admin untuk mengisi data.")
        return

    st.markdown("### 📂 Jelajahi Kategori")
    cols = st.columns(3)
    cats = df['Kategori'].unique()
    
    for idx, cat in enumerate(cats):
        with cols[idx % 3]:
            row = df[df['Kategori'] == cat].iloc[0]
            img = row['Gambar_Base64']
            src = f"data:image/png;base64,{img}" if img else "https://cdn-icons-png.flaticon.com/512/10698/10698776.png"
            
            st.markdown(f"""
            <div class="cat-card">
                <img src="{src}">
                <div class="cat-title">{cat}</div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"Buka Folder", key=f"btn_{idx}", use_container_width=True):
                st.session_state['selected_category'] = cat
                st.session_state['current_view'] = 'detail'
                st.rerun()
            st.write("") 

# ================= DETAIL PAGE =================
def detail_page():
    cat = st.session_state['selected_category']
    df = st.session_state['data']
    subset = df[df['Kategori'] == cat]

    st.button("⬅️ Kembali ke Dashboard", on_click=lambda: st.session_state.update({'current_view': 'home'}))
    
    st.markdown(f"""
    <div style="background:white; padding:20px; border-radius:15px; border-left:6px solid #5e72e4; margin-top:10px;">
        <h2 style="margin:0; color:#32325d;">📂 {cat}</h2>
        <p style="margin:0; color:#8898aa;">Arsip dokumen digital</p>
    </div>
    <br>
    """, unsafe_allow_html=True)

    search = st.text_input("🔍 Cari File...", placeholder="Ketik nama dokumen...")
    
    menus = subset['Menu'].unique()
    if len(menus) > 0:
        tabs = st.tabs([str(m) for m in menus if m]) 
        
        for i, m in enumerate(menus):
            with tabs[i]:
                sub_df = subset[subset['Menu'] == m]
                subs = sub_df['Sub_Menu'].unique()
                
                for s in subs:
                    with st.expander(f"📁 {s if s else 'Umum'}", expanded=True):
                        s2_df = sub_df[sub_df['Sub_Menu'] == s]
                        
                        if search:
                            s2_df = s2_df[s2_df['Nama_File'].str.contains(search, case=False)]
                        
                        if s2_df.empty:
                            st.caption("Tidak ada file.")
                        
                        for _, r in s2_df.iterrows():
                            st.markdown(f"""
                            <div style="
                                display:flex; justify-content:space-between; align-items:center;
                                background:white; padding:15px; border-radius:10px; margin-bottom:10px;
                                border:1px solid #e9ecef; box-shadow:0 2px 4px rgba(0,0,0,0.02);">
                                <div>
                                    <div style="font-weight:600; color:#32325d;">📄 {r['Nama_File']}</div>
                                    <div style="font-size:0.8rem; color:#8898aa;">{r['Sub2_Menu'] if r['Sub2_Menu'] else '-'}</div>
                                </div>
                                <a href="{r['Link_File']}" target="_blank" style="
                                    background-color:#5e72e4; color:white; padding:8px 15px; 
                                    border-radius:6px; text-decoration:none; font-size:0.85rem; font-weight:600;">
                                    Download ⬇
                                </a>
                            </div>
                            """, unsafe_allow_html=True)

# ================= MAIN CONTROLLER =================
if st.session_state['logged_in']:
    with st.sidebar:
        st.image("https://cdn-icons-png.flaticon.com/512/906/906343.png", width=50)
        st.markdown("### Admin Panel")
        if st.button("🏠 Dashboard", use_container_width=True): 
            st.session_state['current_view']='home'
            st.rerun()
        if st.button("⚙️ Input Data", use_container_width=True): 
            st.session_state['current_view']='admin'
            st.rerun()
        st.markdown("---")
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state['logged_in']=False
            st.rerun()

    if st.session_state['current_view'] == 'home': home_page()
    elif st.session_state['current_view'] == 'detail': detail_page()
    elif st.session_state['current_view'] == 'admin': admin_page()
else:
    login_page()
