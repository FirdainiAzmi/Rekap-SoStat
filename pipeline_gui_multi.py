import streamlit as st
import pandas as pd
import time
import base64
import os

# ================= KONFIGURASI DATABASE =================
CSV_FILE = 'database_sostat.csv'

def load_data():
    if os.path.exists(CSV_FILE):
        try:
            return pd.read_csv(CSV_FILE)
        except:
            return pd.DataFrame(columns=['Kategori', 'Gambar_Base64', 'Menu', 'Sub_Menu', 'Sub2_Menu', 'Nama_File', 'Link_File'])
    else:
        return pd.DataFrame(columns=['Kategori', 'Gambar_Base64', 'Menu', 'Sub_Menu', 'Sub2_Menu', 'Nama_File', 'Link_File'])

def save_data(df):
    df.to_csv(CSV_FILE, index=False)

# ================= KONFIGURASI HALAMAN =================
st.set_page_config(
    page_title="ARSITAL BPS Sidoarjo",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ================= CSS PROFESSIONAL (FRONTEND ONLY) =================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;700&display=swap');

:root{
  --bg: #F6F8FC;
  --card: #FFFFFF;
  --text: #0F172A;
  --muted: #64748B;
  --line: rgba(15, 23, 42, .08);
  --brand1:#4F46E5;
  --brand2:#6366F1;
  --shadow1: 0 10px 30px rgba(2, 6, 23, .06);
  --shadow2: 0 30px 60px rgba(2, 6, 23, .12);
  --ring: 0 0 0 4px rgba(99,102,241,.18);
}

html, body, [class*="css"]{
  font-family: 'Plus Jakarta Sans', sans-serif;
  background: var(--bg);
  color: var(--text);
}

header[data-testid="stHeader"]{ background: transparent; }
section.main > div { padding-top: 1.1rem; }

.stApp {
  background: linear-gradient(180deg,
    #86BFE4 0%,
    #A9D2EC 40%,
    #CFE7F5 70%,
    #F3F9FD 100%
  );
}

/* ================= HERO ================= */
.hero-container{
  position: relative;
  overflow: hidden;
  background: radial-gradient(1200px 600px at 10% 10%, rgba(255,255,255,.22), transparent 40%),
              linear-gradient(135deg, var(--brand1), var(--brand2));
  padding: 42px 40px;
  border-radius: 22px;
  color: white;
  box-shadow: 0 22px 60px rgba(79,70,229,.28);
  margin-bottom: 26px;
  transform: translateZ(0);
}
.hero-container:before{
  content:"";
  position:absolute;
  inset:-2px;
  background: radial-gradient(600px 400px at 80% 20%, rgba(255,255,255,.18), transparent 60%);
  pointer-events:none;
}
.hero-subtitle{
  font-size: 1rem;
  opacity: .92;
  max-width: 680px;
  line-height: 1.55;
}

/* ================= METRIC ================= */
.stat-card{
  background: rgba(255,255,255,.9);
  border: 1px solid var(--line);
  border-radius: 18px;
  padding: 22px;
  text-align:center;
  box-shadow: var(--shadow1);
  transition: transform .35s cubic-bezier(.2,.8,.2,1),
              box-shadow .35s cubic-bezier(.2,.8,.2,1),
              border-color .35s cubic-bezier(.2,.8,.2,1);
  transform: translateZ(0);
  backdrop-filter: blur(6px);
}
.stat-card:hover{
  transform: translateY(-6px);
  box-shadow: var(--shadow2);
  border-color: rgba(99,102,241,.35);
}
.stat-number{ font-size: 2rem; font-weight: 800; color: var(--brand1); }
.stat-label{ font-size: .75rem; color: var(--muted); text-transform: uppercase; letter-spacing: 1px; margin-top: 2px; }

/* ================= CATEGORY GRID ================= */
.cat-card{
  position: relative;
  background: rgba(255,255,255,.92);
  border-radius: 20px;
  overflow: hidden;
  border: 1px solid var(--line);
  aspect-ratio: 1 / 0.85;
  width: 100%;
  height: auto;
  box-shadow: var(--shadow1);
  transition: transform .42s cubic-bezier(.2,.8,.2,1),
              box-shadow .42s cubic-bezier(.2,.8,.2,1),
              border-color .42s cubic-bezier(.2,.8,.2,1),
              filter .42s cubic-bezier(.2,.8,.2,1);
  transform: translateZ(0);
  backdrop-filter: blur(6px);
}
.cat-card::before{
  content:"";
  position:absolute;
  inset:-2px;
  background: radial-gradient(800px 240px at 50% -20%, rgba(99,102,241,.35), transparent 55%),
              radial-gradient(600px 240px at 0% 100%, rgba(79,70,229,.18), transparent 55%);
  opacity: 0;
  transition: opacity .42s cubic-bezier(.2,.8,.2,1);
  pointer-events:none;
}
.cat-card::after{
  content:"";
  position:absolute;
  top:-40%;
  left:-60%;
  width: 120%;
  height: 180%;
  background: linear-gradient(115deg, transparent 0%, rgba(255,255,255,.22) 35%, transparent 70%);
  transform: rotate(12deg) translateX(-40%);
  opacity: 0;
  transition: transform .7s cubic-bezier(.2,.8,.2,1), opacity .35s ease;
  pointer-events:none;
}
.cat-card:hover{
  transform: translateY(-10px) scale(1.012);
  box-shadow: 0 36px 80px rgba(2,6,23,.16);
  border-color: rgba(99,102,241,.40);
  filter: saturate(1.05);
}
.cat-card:hover::before{ opacity: 1; }
.cat-card:hover::after{
  opacity: 1;
  transform: rotate(12deg) translateX(60%);
}
.cat-card img{
  width: 100%;
  height: 170px;
  object-fit: contain;
  background: linear-gradient(180deg, #F8FAFF, #F6F7FF);
  padding: 14px;
  transition: transform .45s cubic-bezier(.2,.8,.2,1),
              filter .45s cubic-bezier(.2,.8,.2,1);
}
.cat-card:hover img{
  transform: scale(1.03);
  filter: drop-shadow(0 18px 30px rgba(2,6,23,.12));
}
.cat-title{
  font-weight: 800;
  font-size: 1.02rem;
  text-align: center;
  padding: 0 12px;
  height: 56px;
  display:flex;
  align-items:center;
  justify-content:center;
  color: #0F172A;
}

/* ================= BUTTON ================= */
.stButton > button{
  border-radius: 12px !important;
  font-weight: 800 !important;
  padding: 10px 16px !important;
  border: 1px solid var(--line) !important;
  background: rgba(255,255,255,.92) !important;
  box-shadow: 0 8px 18px rgba(2,6,23,.06) !important;
  transition: transform .18s ease,
              box-shadow .18s ease,
              background .18s ease,
              color .18s ease,
              border-color .18s ease !important;
  transform: translateZ(0);
}
.stButton > button:hover{
  transform: translateY(-2px);
  box-shadow: 0 16px 32px rgba(2,6,23,.12) !important;
  border-color: rgba(99,102,241,.35) !important;
}
.stButton > button:active{
  transform: translateY(0px) scale(.98);
}
div[data-testid="stButton"] > button[kind="primary"],
div[data-testid="stButton"] > button[data-testid="baseButton-primary"] {
    color: #000000 !important;
}

/* ================= FILTER PANEL ================= */
.filter-panel{
  background: rgba(255,255,255,.92);
  border: 1px solid var(--line);
  border-radius: 18px;
  padding: 14px 16px;
  box-shadow: var(--shadow1);
  margin-top: 10px;
  margin-bottom: 12px;
}

/* ================= FILE LIST ================= */
.file-row{
  background: rgba(255,255,255,.92);
  border-radius: 16px;
  padding: 16px;
  margin-bottom: 12px;
  display:flex;
  justify-content:space-between;
  align-items:center;
  border: 1px solid var(--line);
  box-shadow: 0 10px 22px rgba(2,6,23,.05);
  transition: transform .35s cubic-bezier(.2,.8,.2,1),
              box-shadow .35s cubic-bezier(.2,.8,.2,1),
              border-color .35s cubic-bezier(.2,.8,.2,1);
  transform: translateZ(0);
}
.file-row:hover{
  transform: translateY(-6px);
  box-shadow: 0 26px 54px rgba(2,6,23,.12);
  border-color: rgba(99,102,241,.25);
}
.file-meta{ font-size: .82rem; color: var(--muted); margin-top: 3px; }

.dl-link{
  background: linear-gradient(135deg, var(--brand1), var(--brand2));
  color: #FFFFFF !important;
  text-decoration: none !important;
  padding: 9px 14px;
  border-radius: 12px;
  text-decoration: none;
  font-size: .84rem;
  font-weight: 800;
  box-shadow: 0 14px 26px rgba(79,70,229,.22);
  transition: transform .18s ease, box-shadow .18s ease, filter .18s ease;
  display:inline-block;
}
.dl-link:hover{
  transform: translateY(-2px);
  box-shadow: 0 20px 40px rgba(79,70,229,.30);
  filter: saturate(1.1);
  color: #FFFFFF !important;
  text-decoration: none !important;
}
.dl-link:visited,
.dl-link:active{ 
  transform: scale(.98);
  color: #FFFFFF !important;
  text-decoration: none !important;
}

/* grouping title (Sub2) */
.kegiatan-title{
  font-weight: 900;
  font-size: 1.02rem;
  color: #111827;
  margin: 16px 0 10px;
  display:flex;
  align-items:center;
  gap: 10px;
}
.kegiatan-pill{
  font-size: .78rem;
  padding: 6px 10px;
  border-radius: 999px;
  border: 1px solid rgba(99,102,241,.22);
  background: rgba(99,102,241,.10);
  color: #3730A3;
  font-weight: 800;
}

/* ================= SIDEBAR ================= */
[data-testid="stSidebar"]{
  background: rgba(255,255,255,.95);
  border-right: 1px solid var(--line);
  backdrop-filter: blur(8px);
}

.footer{
  text-align:center;
  font-size:.78rem;
  color:#94A3B8;
  margin-top: 50px;
}
*{ scroll-behavior:smooth; }
@media (prefers-reduced-motion: reduce){
  *{ transition: none !important; animation: none !important; }
}
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
if 'data' not in st.session_state:
    st.session_state['data'] = load_data()

if st.session_state['data'].empty and os.path.exists(CSV_FILE):
    st.session_state['data'] = load_data()

if 'logged_in' not in st.session_state: st.session_state['logged_in'] = False
if 'current_view' not in st.session_state: st.session_state['current_view'] = 'home'
if 'selected_category' not in st.session_state: st.session_state['selected_category'] = None


# ================= LOGIN =================
def login_page():
    try:
        img_code = get_base64_of_bin_file("logo_arsital.png")
        img_tag = f'<img src="data:image/png;base64,{img_code}" class="hero-logo2">'
    except:
        img_tag = ""

    st.markdown("""
    <style>
        .hero-logo2{ width: 250px; height: auto; margin-bottom: 0px; display: block; }
    </style>
    """, unsafe_allow_html=True)

    st.markdown(f"""
        <div>
            {img_tag}
        </div>
    """, unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1,1,1])
    with c2:
        st.markdown("<br><br><br>", unsafe_allow_html=True)
        st.markdown("""
        <div style="background:white; padding:40px; border-radius:16px;
                    box-shadow:0 18px 40px rgba(0,0,0,0.08);
                    text-align:center; border:1px solid #E5E7EB;">
            <h2 style="color:#4F46E5; margin:0 0 6px 0;">Login Page</h2>
            <p style="color:#6B7280; margin:0;">Silakan masuk</p>
        </div>
        """, unsafe_allow_html=True)

        with st.form("login"):
            ADMIN_USERNAME = st.secrets.get("username")
            ADMIN_PASSWORD = st.secrets.get("password")
            
            u = st.text_input("Username")
            p = st.text_input("Password", type="password")
            if st.form_submit_button("MASUK SISTEM", use_container_width=True, type="primary"):
                if u==ADMIN_USERNAME and p==ADMIN_PASSWORD:
                    st.session_state['logged_in']=True
                    st.rerun()
                else:
                    st.error("Login Gagal")


# ================= ADMIN PAGE (AUTO-SAVE) =================
def admin_page():
    st.markdown("## ⚙️ Panel Admin")

    # KITA BUAT 3 TAB DI SINI
    tab1, tab2, tab3 = st.tabs(["📝 Input Data Baru", "✏️ Edit Data", "🗑️ Hapus Data"])
    df = st.session_state['data']

    # ================= TAB 1: INPUT DATA BARU =================
    with tab1:
        st.info("💡 Tambah data file baru ke database.")
        
        c1, c2 = st.columns(2)
        
        # --- Kolom Kiri: Kategori ---
        with c1:
            st.markdown("### 1. Pengaturan Kategori")
            existing_cats = df['Kategori'].dropna().unique().tolist() if not df.empty else []
            opsi_kategori = existing_cats + ["➕ Buat Kategori Baru"]
            
            # Key unik agar tidak bentrok dengan tab lain
            sel_kategori = st.selectbox("Pilih Kategori:", opsi_kategori, key="in_kat_select")

            final_kategori = ""
            if sel_kategori == "➕ Buat Kategori Baru":
                final_kategori = st.text_input("Ketik Nama Kategori Baru:", placeholder="Contoh: Statistik Sosial", key="in_kat_text")
            else:
                final_kategori = sel_kategori

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("### 📷 Gambar Cover")
            in_img = st.file_uploader("Upload Cover (Opsional)", type=['png','jpg','jpeg'], key="in_img_upload")

        # --- Kolom Kanan: Detail ---
        with c2:
            st.markdown("### 2. Detail Dokumen")
            is_old_cat = (sel_kategori != "➕ Buat Kategori Baru")

            # MENU
            in_menu = ""
            if is_old_cat:
                df_cat = df[df['Kategori'] == final_kategori]
                list_menu = df_cat['Menu'].dropna().unique().tolist()
                list_menu.append("➕ Buat Menu Baru")
                sel_menu = st.selectbox("Menu Utama", list_menu, key="in_menu_sel")
                
                if sel_menu == "➕ Buat Menu Baru":
                    in_menu = st.text_input("Ketik Nama Menu Baru", placeholder="Misal: Sakernas", key="in_menu_txt")
                else:
                    in_menu = sel_menu
            else:
                in_menu = st.text_input("Menu Utama", placeholder="Misal: Sakernas", key="in_menu_txt_def")

            # SUB MENU
            in_sub = ""
            menu_is_existing = False
            if is_old_cat and in_menu != "➕ Buat Menu Baru" and 'df_cat' in locals():
                if not df_cat[df_cat['Menu'] == in_menu].empty:
                    menu_is_existing = True
            
            if menu_is_existing:
                df_menu = df_cat[df_cat['Menu'] == in_menu]
                list_sub = df_menu['Sub_Menu'].dropna().unique().tolist()
                list_sub.append("➕ Buat Sub Baru")
                sel_sub = st.selectbox("Sub Menu (Tahun)", list_sub, key="in_sub_sel")
                
                if sel_sub == "➕ Buat Sub Baru":
                    in_sub = st.text_input("Ketik Sub Menu Baru", placeholder="Misal: Sakernas Agustus 2025", key="in_sub_txt")
                else:
                    in_sub = sel_sub
            else:
                in_sub = st.text_input("Sub Menu (Tahun)", placeholder="Misal: Sakernas Agustus 2025", key="in_sub_txt_def")

            # SUB MENU 2 (KEGIATAN)
            in_sub2 = ""
            valid_sub = False
            if menu_is_existing and in_sub != "➕ Buat Sub Baru" and 'df_menu' in locals():
                if not df_menu[df_menu['Sub_Menu'] == in_sub].empty:
                    valid_sub = True

            if valid_sub:
                df_sub = df_menu[df_menu['Sub_Menu'] == in_sub]
                list_sub2 = df_sub['Sub2_Menu'].dropna().unique().tolist()
                list_sub2 = [x for x in list_sub2 if str(x) != 'nan']
                list_sub2.append("➕ Buat Sub 2 Baru")
                sel_sub2 = st.selectbox("Sub Menu 2 (Judul Kegiatan)", list_sub2, key="in_sub2_sel")
                
                if sel_sub2 == "➕ Buat Sub 2 Baru":
                    in_sub2 = st.text_input("Ketik Sub Menu 2 Baru", placeholder="Misal: Pelatihan Petugas", key="in_sub2_txt")
                else:
                    in_sub2 = sel_sub2
            else:
                in_sub2 = st.text_input("Sub Menu 2 (Judul Kegiatan)", placeholder="Misal: Pelatihan Petugas", key="in_sub2_txt_def")

            st.markdown("---")
            in_nama = st.text_input("Judul File (Wajib Diisi)*", key="in_nama")
            in_link = st.text_input("Link File (Google Drive/Web)", key="in_link")

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("💾 SIMPAN DATA BARU", type="primary", use_container_width=True, key="btn_save_new"):
            if final_kategori and in_nama:
                img_str = image_to_base64(in_img)
                # Ambil gambar lama jika tidak upload baru
                if not img_str and sel_kategori != "➕ Buat Kategori Baru":
                    try:
                        prev = df[df['Kategori']==final_kategori]['Gambar_Base64'].iloc[0]
                        img_str = prev
                    except: pass

                new_row = {
                    'Kategori': final_kategori, 'Gambar_Base64': img_str,
                    'Menu': in_menu, 'Sub_Menu': in_sub, 'Sub2_Menu': in_sub2,
                    'Nama_File': in_nama, 'Link_File': in_link
                }
                updated_df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                st.session_state['data'] = updated_df
                save_data(updated_df)
                st.success("✅ Data berhasil disimpan!")
                time.sleep(1)
                st.rerun()
            else:
                st.warning("Nama Kategori dan Judul File wajib diisi.")

    # ================= TAB 2: EDIT DATA (Baru ditambahkan ke sini) =================
    with tab2:
        if df.empty:
            st.info("Database masih kosong, belum ada yang bisa diedit.")
        else:
            st.info("✏️ Edit metadata file yang sudah ada.")
            
            ec1, ec2 = st.columns([1, 2])

            with ec1:
                st.markdown("#### Pilih File")
                # 1. Pilih Kategori
                ekat_list = sorted(df['Kategori'].dropna().unique().tolist())
                esel_kat = st.selectbox("Pilih Kategori", ekat_list, key="edit_sel_kat")

                # 2. Pilih File di kategori tersebut
                df_ekat = df[df['Kategori'] == esel_kat].copy()
                efile_list = df_ekat['Nama_File'].fillna("").tolist()
                
                if not efile_list:
                    st.warning("Tidak ada file di kategori ini.")
                    esel_file = None
                else:
                    esel_file = st.selectbox("Pilih File", efile_list, key="edit_sel_file")

            with ec2:
                if esel_file:
                    # Ambil index data asli
                    try:
                        row_idx = df_ekat[df_ekat['Nama_File'] == esel_file].index[0]
                        cur = df.loc[row_idx]

                        st.markdown("#### Form Edit")
                        # Prefill data lama
                        e_menu = st.text_input("Menu", value=str(cur.get('Menu', '') if pd.notna(cur.get('Menu', '')) else ''), key="e_menu")
                        e_sub = st.text_input("Sub Menu", value=str(cur.get('Sub_Menu', '') if pd.notna(cur.get('Sub_Menu', '')) else ''), key="e_sub")
                        e_sub2 = st.text_input("Judul Kegiatan (Sub2)", value=str(cur.get('Sub2_Menu', '') if pd.notna(cur.get('Sub2_Menu', '')) else ''), key="e_sub2")
                        e_nama = st.text_input("Nama File", value=str(cur.get('Nama_File', '') if pd.notna(cur.get('Nama_File', '')) else ''), key="e_nama")
                        e_link = st.text_input("Link File", value=str(cur.get('Link_File', '') if pd.notna(cur.get('Link_File', '')) else ''), key="e_link")

                        st.markdown("---")
                        st.markdown("**Ganti Cover Kategori (Opsional)**")
                        e_img = st.file_uploader("Upload cover baru", type=['png','jpg','jpeg'], key="e_img_up")

                        if st.button("💾 SIMPAN PERUBAHAN", type="primary", use_container_width=True, key="btn_save_edit"):
                            df_edit = df.copy()
                            
                            df_edit.at[row_idx, 'Menu'] = e_menu
                            df_edit.at[row_idx, 'Sub_Menu'] = e_sub
                            df_edit.at[row_idx, 'Sub2_Menu'] = e_sub2
                            df_edit.at[row_idx, 'Nama_File'] = e_nama
                            df_edit.at[row_idx, 'Link_File'] = e_link

                            # Logic ganti gambar
                            if e_img is not None:
                                img_str_edit = image_to_base64(e_img)
                                if img_str_edit:
                                    # Update semua baris dengan kategori yang sama agar gambar konsisten
                                    df_edit.loc[df_edit['Kategori'] == esel_kat, 'Gambar_Base64'] = img_str_edit

                            st.session_state['data'] = df_edit
                            save_data(df_edit)
                            st.success("✅ Perubahan disimpan!")
                            time.sleep(1)
                            st.rerun()
                    except IndexError:
                        st.error("Terjadi kesalahan saat mengambil data file.")


    # ================= TAB 3: HAPUS DATA =================
    with tab3:
        if df.empty:
            st.warning("Data kosong.")
        else:
            st.info("🗑️ Hapus data secara permanen.")

            del_c1, del_c2, del_c3 = st.columns(3)
            del_d1, del_d2 = st.columns(2)

            # 1) Kategori
            d_list_kat = sorted(df['Kategori'].dropna().unique().tolist())
            d_sel_kat = del_c1.selectbox("Kategori", d_list_kat, key="del_kat")

            d_df_kat = df[df['Kategori'] == d_sel_kat].copy()
            
            # 2) Menu
            if not d_df_kat.empty:
                d_list_menu = sorted(d_df_kat['Menu'].fillna("-").unique().tolist())
                d_sel_menu = del_c2.selectbox("Menu", d_list_menu, key="del_menu")
                d_df_menu = d_df_kat[d_df_kat['Menu'].fillna("-") == d_sel_menu].copy()
            else:
                d_df_menu = pd.DataFrame()

            # 3) Sub Menu
            if not d_df_menu.empty:
                d_list_sub = sorted(d_df_menu['Sub_Menu'].fillna("-").unique().tolist())
                d_sel_sub = del_c3.selectbox("Sub Menu", d_list_sub, key="del_sub")
                d_df_sub = d_df_menu[d_df_menu['Sub_Menu'].fillna("-") == d_sel_sub].copy()
            else:
                d_df_sub = pd.DataFrame()

            # 4) Sub2
            if not d_df_sub.empty:
                d_list_sub2 = sorted(d_df_sub['Sub2_Menu'].fillna("-").unique().tolist())
                d_sel_sub2 = del_d1.selectbox("Judul Kegiatan (Sub2)", d_list_sub2, key="del_sub2")
                d_df_sub2 = d_df_sub[d_df_sub['Sub2_Menu'].fillna("-") == d_sel_sub2].copy()
            else:
                d_df_sub2 = pd.DataFrame()

            # 5) File
            if not d_df_sub2.empty:
                d_list_file = d_df_sub2['Nama_File'].fillna("-").tolist()
                d_sel_file = del_d2.selectbox("Nama File", d_list_file, key="del_file")
            else:
                d_sel_file = None

            st.markdown("<br>", unsafe_allow_html=True)

            if st.button("🚫 HAPUS FILE INI", type="primary", use_container_width=True, key="btn_delete"):
                if d_sel_file:
                    idx = df[
                        (df['Kategori'] == d_sel_kat) &
                        (df['Menu'].fillna("-") == d_sel_menu) &
                        (df['Sub_Menu'].fillna("-") == d_sel_sub) &
                        (df['Sub2_Menu'].fillna("-") == d_sel_sub2) &
                        (df['Nama_File'].fillna("-") == d_sel_file)
                    ].index

                    if len(idx) > 0:
                        new_df = df.drop(idx).reset_index(drop=True)
                        st.session_state['data'] = new_df
                        save_data(new_df)
                        st.success("✅ File berhasil dihapus.")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("Data tidak ditemukan.")

    st.markdown("""<div class="footer">Developed by Firdaini Azmi & Muhammad Ariq Hibatullah<br>© 2025 Badan Pusat Statistik • Dashboard Sostat</div>""", unsafe_allow_html=True)

def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()


# ================= HOME DASHBOARD =================
def home_page():
    # --- Bagian Logo & Hero ---
    try:
        # 1. Gambar Kiri (Logo Arsital)
        img_code = get_base64_of_bin_file("logo_arsital.png")
        img_tag = f'<img src="data:image/png;base64,{img_code}" class="hero-logo">'
        
        # 2. Gambar Kanan (Logo Orang)
        img_code2 = get_base64_of_bin_file("logo_orang.png")
        img_orang_src = f'<img src="data:image/png;base64,{img_code2}" class="hero-logo-orang">'

    except:
        img_tag = ""
        img_orang_src = ""

    # CSS
    st.markdown("""
    <style>
      .hero-logo{ width: 300px; height: auto; display:block; margin-bottom: 14px; }
      .hero-logo-orang{ width: 300px; height: auto; display:block; }
    
      /* ✅ 2 kolom */
      .hero-grid{
        display: grid;
        grid-template-columns: 1.35fr 0.65fr;  /* kolom 1 lebih besar */
        gap: 24px;
        align-items: center;
      }
    
      .hero-col1{
        display:flex;
        flex-direction: column;   /* logo lalu teks di bawah */
        align-items: flex-start;  /* rata kiri */
      }
    
      .hero-col2{
        display:flex;
        justify-content: flex-end; /* logo orang ke kanan */
        align-items: center;
      }
    
      /* ✅ responsif */
      @media (max-width: 900px){
        .hero-grid{ grid-template-columns: 1fr; }
        .hero-col1{ align-items: center; text-align:center; }
        .hero-col2{ justify-content: center; }
        .hero-logo, .hero-logo-orang{ width: 240px; }
      }
    </style>
    """, unsafe_allow_html=True)
    
    # HTML STRUCTURE
    st.markdown(f"""
    <div class="hero-container">
      <div class="hero-row">
        <div class="hero-left">{img_tag}</div>
        <div class="hero-mid hero-subtitle">
          <div style="font-weight:800; font-size:1.5rem; margin-bottom:6px;">
            Selamat datang di Arsip Digial BPS Kabupaten Sidoarjo⚡
          </div>
          <div style="opacity:.92; font-size:1rem">
            Portal ini merupakan dashboard penyimpanan terpusat aset digital kegiatan Sosial Statistik.
          </div>
        </div>
        <div class="hero-right">{img_orang_src}</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    df = st.session_state['data']

    # --- Metrics (Tetap sama) ---
    if not df.empty:
        m1, m2, m3 = st.columns(3)
        with m1:
            st.markdown(f"""<div class="stat-card"><div class="stat-number">{len(df['Kategori'].unique())}</div><div class="stat-label">Kategori Data</div></div>""", unsafe_allow_html=True)
        with m2:
            st.markdown(f"""<div class="stat-card"><div class="stat-number">{len(df)}</div><div class="stat-label">Total File</div></div>""", unsafe_allow_html=True)
        with m3:
            st.markdown(f"""<div class="stat-card"><div class="stat-number">{len(df['Menu'].unique())}</div><div class="stat-label">Topik Bahasan</div></div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        
    if df.empty:
        st.info("📂 Database masih kosong. Silakan login ke Admin untuk mengisi data.")
        return

    # ================= PERBAIKAN SEARCH GLOBAL DI SINI =================
    st.markdown("### 🔍 Global Search")
    search = st.text_input("Cari File di seluruh database...", placeholder="Ketik nama dokumen...", label_visibility="collapsed")
    
    # 1. INISIALISASI subset dari df utama
    subset = df.copy() 

    # 2. JIKA ADA INPUT PENCARIAN
    if search:
        # Filter data
        subset = subset[subset['Nama_File'].astype(str).str.contains(search, case=False, na=False)]
        
        st.write(f"Menampilkan {len(subset)} hasil pencarian untuk: **'{search}'**")
        
        if subset.empty:
            st.warning("Tidak ditemukan file dengan nama tersebut.")
        else:
            # Tampilkan hasil search menggunakan style file-row
            for _, r in subset.iterrows():
                st.markdown(f"""
                <div class="file-row">
                    <div>
                        <div style="font-size:0.8rem; color:#6366F1; font-weight:bold;">{r['Kategori']} > {r['Menu']}</div>
                        <div style="font-weight:800; color:#111827;">📄 {r['Nama_File']}</div>
                    </div>
                    <a href="{r['Link_File']}" target="_blank" class="dl-link">Buka ⬇</a>
                </div>
                """, unsafe_allow_html=True)
        
        # Return agar tidak menampilkan kategori di bawahnya saat sedang search
        return 
    # ================= AKHIR PERBAIKAN =================

    st.markdown("### 📂 Jelajahi Kategori")
    cols = st.columns(3)
    cats = df['Kategori'].unique()

    for idx, cat in enumerate(cats):
        with cols[idx % 3]:
            # Handle jika gambar kosong/error
            try:
                row = df[df['Kategori'] == cat].iloc[0]
                img = row['Gambar_Base64']
                src = f"data:image/png;base64,{img}" if img else "https://cdn-icons-png.flaticon.com/512/10698/10698776.png"
            except:
                src = "https://cdn-icons-png.flaticon.com/512/10698/10698776.png"

            st.markdown(f"""
            <div class="cat-card">
                <img src="{src}">
                <div class="cat-title">{cat}</div>
            </div>
            """, unsafe_allow_html=True)

            if st.button("Buka Folder", key=f"btn_{idx}", use_container_width=True):
                st.session_state['selected_category'] = cat
                st.session_state['current_view'] = 'detail'
                st.rerun()
            st.write("")

    st.markdown("""<div class="footer">Developed by Firdaini Azmi & Muhammad Ariq Hibatullah<br>© 2025 Badan Pusat Statistik • Dashboard Sostat</div>""", unsafe_allow_html=True)


# ================= DETAIL PAGE =================
def detail_page():
    cat = st.session_state['selected_category']
    df = st.session_state['data']
    
    # Ambil data hanya kategori yang dipilih
    subset_all = df[df['Kategori'] == cat].copy()

    st.button("⬅️ Kembali ke Dashboard", on_click=lambda: st.session_state.update({'current_view': 'home'}))

    st.markdown(f"""
    <div style="background:white; padding:20px; border-radius:18px; border-left:6px solid #6366F1; margin-top:10px; border:1px solid #E5E7EB; box-shadow:0 10px 22px rgba(2,6,23,.05);">
        <h2 style="margin:0; color:#111827;">📂 {cat}</h2>
        <p style="margin:6px 0 0; color:#6B7280;">Arsip dokumen digital</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # SEARCH GLOBAL
    search = st.text_input("🔍 Cari File...", placeholder="Ketik nama dokumen...")

    # === LOGIKA FILTER BERJENJANG (CASCADING) ===
    f1, f2, f3 = st.columns(3)

    # 1. DROPWN MENU (Level 1)
    # Ambil semua menu unik di kategori ini
    menu_opts = ["Semua"] + sorted([x for x in subset_all['Menu'].dropna().unique().tolist() if str(x).strip() != ""])
    
    with f1:
        sel_menu = st.selectbox("Filter Menu", menu_opts, index=0)

    # 2. DROPDOWN SUB MENU (Level 2)
    # Filter dataset sementara berdasarkan Menu yang dipilih di atas
    if sel_menu != "Semua":
        df_level2 = subset_all[subset_all['Menu'] == sel_menu]
    else:
        df_level2 = subset_all # Kalau 'Semua', pakai data full

    # Ambil opsi Sub Menu hanya dari data yang sudah difilter menu-nya
    sub_opts = ["Semua"] + sorted([x for x in df_level2['Sub_Menu'].dropna().unique().tolist() if str(x).strip() != ""])
    
    with f2:
        sel_sub = st.selectbox("Filter Sub Menu", sub_opts, index=0)

    # 3. DROPDOWN SUB MENU 2 / KEGIATAN (Level 3)
    # Filter dataset sementara berdasarkan Sub Menu yang dipilih di atas
    if sel_sub != "Semua":
        df_level3 = df_level2[df_level2['Sub_Menu'] == sel_sub]
    else:
        df_level3 = df_level2

    # Ambil opsi Sub2 hanya dari data yang sudah difilter sub menu-nya
    sub2_opts = ["Semua"] + sorted([x for x in df_level3['Sub2_Menu'].dropna().unique().tolist() if str(x).strip() != ""])
    
    with f3:
        sel_sub2 = st.selectbox("Filter Judul Kegiatan (Sub2)", sub2_opts, index=0)

    st.markdown('</div>', unsafe_allow_html=True)

    # === PENERAPAN FILTER AKHIR ===
    # Kita mulai filter dari data utama (subset_all) menggunakan variabel yang sudah dipilih user
    subset = subset_all.copy()

    if sel_menu != "Semua":
        subset = subset[subset['Menu'] == sel_menu]
    
    if sel_sub != "Semua":
        subset = subset[subset['Sub_Menu'] == sel_sub]
        
    if sel_sub2 != "Semua":
        subset = subset[subset['Sub2_Menu'] == sel_sub2]

    if search:
        subset = subset[subset['Nama_File'].astype(str).str.contains(search, case=False, na=False)]

    # === TAMPILKAN DATA (Sama seperti sebelumnya) ===
    menus = subset['Menu'].dropna().unique()

    if len(menus) == 0:
        st.info("Tidak ada data sesuai filter/pencarian.")
        return

    # Tabs logic tetap sama...
    tabs = st.tabs([str(m) for m in menus if str(m).strip() != ""])
    
    # ... (lanjutkan kode render tabs di bawahnya tetap sama dengan yang lama)
    # Copy paste sisa kode render di bawah ini:
    
    for i, m in enumerate([x for x in menus if str(x).strip() != ""]):
        with tabs[i]:
            sub_df = subset[subset['Menu'] == m]
            # Pastikan ambil sub menu unik yang ada di subset hasil filter
            subs = [x for x in sub_df['Sub_Menu'].dropna().unique()]

            if len(subs) == 0:
                # Cek jika ada file tanpa sub menu
                if not sub_df.empty:
                    # Tampilkan file langsung jika tidak ada sub menu
                    for _, r in sub_df.iterrows():
                         st.markdown(f"""<div class="file-row"><div><b>📄 {r['Nama_File']}</b></div><a href="{r['Link_File']}" target="_blank" class="dl-link">Buka ⬇</a></div>""", unsafe_allow_html=True)
                else:
                    st.caption("Tidak ada sub menu.")
                continue

            for s in subs:
                with st.expander(f"📁 {s if str(s).strip() else 'Umum'}"):
                    s_df = sub_df[sub_df['Sub_Menu'] == s].copy()

                    kegiatan_list = s_df['Sub2_Menu'].fillna("-").unique().tolist()

                    for keg in kegiatan_list:
                        keg_label = keg if str(keg).strip() else "-"
                        
                        # Hanya tampilkan header kegiatan jika Sub2 difilter "Semua" atau sesuai pilihan
                        if sel_sub2 == "Semua" or sel_sub2 == keg:
                            if keg_label != "-":
                                st.markdown(
                                    f'<div class="kegiatan-title">🎯 {keg_label} <span class="kegiatan-pill">Kegiatan</span></div>',
                                    unsafe_allow_html=True
                                )

                        keg_df = s_df[s_df['Sub2_Menu'].fillna("-") == keg_label]

                        if keg_df.empty: continue

                        for _, r in keg_df.iterrows():
                            st.markdown(f"""
                            <div class="file-row">
                                <div>
                                    <div style="font-weight:800; color:#111827;">📄 {r['Nama_File']}</div>
                                </div>
                                <a href="{r['Link_File']}" target="_blank" class="dl-link">Buka ⬇</a>
                            </div>
                            """, unsafe_allow_html=True)

    st.markdown("""<div class="footer">Developed by Firdaini Azmi & Muhammad Ariq Hibatullah<br>© 2025 Badan Pusat Statistik • Dashboard Sostat</div>""", unsafe_allow_html=True)

# ================= MAIN CONTROLLER =================
if st.session_state['logged_in']:
    with st.sidebar:
        st.image("https://cdn-icons-png.flaticon.com/512/906/906343.png", width=50)
        st.markdown("### Admin Panel")

        # Tombol Dashboard
        if st.button("🏠 Dashboard Utama", use_container_width=True):
            st.session_state['current_view'] = 'home'
            st.rerun()

        # Tombol Admin Panel (Input, Edit, Hapus jadi satu di sini)
        if st.button("⚙️ Kelola Data (Admin)", use_container_width=True):
            st.session_state['current_view'] = 'admin'
            st.rerun()

        st.markdown("---")

        if st.button("🚪 Logout", use_container_width=True):
            st.session_state['logged_in'] = False
            st.rerun()

    # Routing Halaman
    if st.session_state['current_view'] == 'home':
        home_page()
    elif st.session_state['current_view'] == 'detail':
        detail_page()
    elif st.session_state['current_view'] == 'admin':
        admin_page()
    # Halaman 'edit' sudah tidak diperlukan karena masuk ke 'admin'
    
else:
    login_page()
