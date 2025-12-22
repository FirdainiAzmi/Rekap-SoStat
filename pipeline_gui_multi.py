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
    page_title="Sostat Dashboard Pro",
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
  height: 100%;
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
  padding: 14px 12px 18px;
  min-height: 56px;
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
  color: white;
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
}
.dl-link:active{ transform: scale(.98); }

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
    c1, c2, c3 = st.columns([1,1,1])
    with c2:
        st.markdown("<br><br><br>", unsafe_allow_html=True)
        st.markdown("""
        <div style="background:white; padding:40px; border-radius:16px;
                    box-shadow:0 18px 40px rgba(0,0,0,0.08);
                    text-align:center; border:1px solid #E5E7EB;">
            <h2 style="color:#4F46E5; margin:0 0 6px 0;">Admin Login</h2>
            <p style="color:#6B7280; margin:0;">Silakan masuk untuk mengelola data</p>
        </div>
        """, unsafe_allow_html=True)

        with st.form("login"):
            u = st.text_input("Username")
            p = st.text_input("Password", type="password")
            if st.form_submit_button("MASUK SISTEM", use_container_width=True, type="primary"):
                if u=="admin" and p=="admin":
                    st.session_state['logged_in']=True
                    st.rerun()
                else:
                    st.error("Login Gagal")


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

            pilihan_mode = "Buat Baru"
            if existing_cats:
                pilihan_mode = st.radio("Pilih Mode Kategori:", ["Gunakan Kategori Lama", "Buat Kategori Baru"], horizontal=True)

            final_kategori = ""
            if pilihan_mode == "Gunakan Kategori Lama":
                final_kategori = st.selectbox("Pilih Kategori:", existing_cats)
            else:
                final_kategori = st.text_input("Ketik Nama Kategori Baru:", placeholder="Contoh: Statistik Sosial")

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("### 📷 Gambar Cover")
            in_img = st.file_uploader("Upload Cover (Opsional)", type=['png','jpg','jpeg'])

        with col_kanan:
            st.markdown("### 2. Detail Dokumen")

            is_old_cat = (pilihan_mode == "Gunakan Kategori Lama") and (final_kategori in existing_cats)

            in_menu = ""
            if is_old_cat:
                df_cat = df[df['Kategori'] == final_kategori]
                list_menu = df_cat['Menu'].unique().tolist()
                list_menu.append("➕ Buat Menu Baru")

                sel_menu = st.selectbox("Menu Utama", list_menu, key="sel_menu")

                if sel_menu == "➕ Buat Menu Baru":
                    in_menu = st.text_input("Ketik Nama Menu Baru", placeholder="Misal: Publikasi", key="txt_menu_new")
                else:
                    in_menu = sel_menu
            else:
                in_menu = st.text_input("Menu Utama", placeholder="Misal: Publikasi", key="txt_menu_default")

            in_sub = ""
            if is_old_cat and in_menu != "➕ Buat Menu Baru" and not df_cat[df_cat['Menu'] == in_menu].empty:
                df_menu = df_cat[df_cat['Menu'] == in_menu]
                list_sub = df_menu['Sub_Menu'].unique().tolist()
                list_sub.append("➕ Buat Sub Baru")

                sel_sub = st.selectbox("Sub Menu (Tahun)", list_sub, key="sel_sub")

                if sel_sub == "➕ Buat Sub Baru":
                    in_sub = st.text_input("Ketik Sub Menu Baru", placeholder="Misal: 2025", key="txt_sub_new")
                else:
                    in_sub = sel_sub
            else:
                in_sub = st.text_input("Sub Menu (Tahun)", placeholder="Misal: 2025", key="txt_sub_default")

            in_sub2 = ""
            valid_sub = False
            if is_old_cat and in_menu != "➕ Buat Menu Baru" and in_sub != "➕ Buat Sub Baru":
                if 'df_menu' in locals() and not df_menu[df_menu['Sub_Menu'] == in_sub].empty:
                    valid_sub = True

            if valid_sub:
                df_sub = df_menu[df_menu['Sub_Menu'] == in_sub]
                list_sub2 = df_sub['Sub2_Menu'].unique().tolist()
                list_sub2 = [x for x in list_sub2 if str(x) != 'nan']
                list_sub2.append("➕ Buat Sub 2 Baru")

                sel_sub2 = st.selectbox("Sub Menu 2 (Judul Kegiatan)", list_sub2, key="sel_sub2")

                if sel_sub2 == "➕ Buat Sub 2 Baru":
                    in_sub2 = st.text_input("Ketik Sub Menu 2 Baru", placeholder="Misal: Semester 1", key="txt_sub2_new")
                else:
                    in_sub2 = sel_sub2
            else:
                in_sub2 = st.text_input("Sub Menu 2 (Judul Kegiatan)", placeholder="Misal: Semester 1", key="txt_sub2_default")

            st.markdown("---")
            in_nama = st.text_input("Judul File (Wajib Diisi)*", key="input_nama_file")
            in_link = st.text_input("Link File (Google Drive/Web)", key="input_link_file")

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("💾 SIMPAN PERMANEN", type="primary", use_container_width=True):
            if final_kategori and in_nama:
                img_str = image_to_base64(in_img)

                if not img_str and final_kategori in existing_cats:
                    try:
                        prev = df[df['Kategori']==final_kategori]['Gambar_Base64'].iloc[0]
                        img_str = prev
                    except:
                        pass

                new_row = {
                    'Kategori': final_kategori, 'Gambar_Base64': img_str,
                    'Menu': in_menu, 'Sub_Menu': in_sub, 'Sub2_Menu': in_sub2,
                    'Nama_File': in_nama, 'Link_File': in_link
                }

                updated_df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                st.session_state['data'] = updated_df
                save_data(updated_df)

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
            st.info("Pilih berjenjang: Kategori → Menu → Sub Menu → Judul Kegiatan (Sub2) → File")

            a1, a2, a3 = st.columns(3)
            b1, b2 = st.columns(2)

            # 1) Kategori
            list_kat = sorted(df['Kategori'].dropna().unique().tolist())
            del_kat = a1.selectbox("Kategori", list_kat, key="del_kat")

            df_kat = df[df['Kategori'] == del_kat].copy()
            if df_kat.empty:
                st.warning("Tidak ada data di kategori ini.")
                st.stop()

            # 2) Menu
            list_menu = sorted(df_kat['Menu'].fillna("-").unique().tolist())
            del_menu = a2.selectbox("Menu", list_menu, key="del_menu")

            df_menu = df_kat[df_kat['Menu'].fillna("-") == del_menu].copy()
            if df_menu.empty:
                st.warning("Tidak ada data di menu ini.")
                st.stop()

            # 3) Sub Menu
            list_sub = sorted(df_menu['Sub_Menu'].fillna("-").unique().tolist())
            del_sub = a3.selectbox("Sub Menu", list_sub, key="del_sub")

            df_sub = df_menu[df_menu['Sub_Menu'].fillna("-") == del_sub].copy()
            if df_sub.empty:
                st.warning("Tidak ada data di sub menu ini.")
                st.stop()

            # 4) Sub2 (Judul Kegiatan)
            list_sub2 = sorted(df_sub['Sub2_Menu'].fillna("-").unique().tolist())
            del_sub2 = b1.selectbox("Judul Kegiatan (Sub2)", list_sub2, key="del_sub2")

            df_sub2 = df_sub[df_sub['Sub2_Menu'].fillna("-") == del_sub2].copy()
            if df_sub2.empty:
                st.warning("Tidak ada data di judul kegiatan ini.")
                st.stop()

            # 5) File
            list_file = df_sub2['Nama_File'].fillna("-").tolist()
            del_file = b2.selectbox("Nama File", list_file, key="del_file")

            # Preview pilihan
            pick = df_sub2[df_sub2['Nama_File'].fillna("-") == del_file]
            if not pick.empty:
                st.caption(f"Link: {pick.iloc[0]['Link_File']}")

            st.markdown("<br>", unsafe_allow_html=True)

            if st.button("🗑️ Hapus Permanen", type="primary", use_container_width=True, key="btn_hapus_permanen"):
                idx = df[
                    (df['Kategori'] == del_kat) &
                    (df['Menu'].fillna("-") == del_menu) &
                    (df['Sub_Menu'].fillna("-") == del_sub) &
                    (df['Sub2_Menu'].fillna("-") == del_sub2) &
                    (df['Nama_File'].fillna("-") == del_file)
                ].index

                if len(idx) == 0:
                    st.warning("Data tidak ditemukan / sudah terhapus.")
                else:
                    new_df = df.drop(idx).reset_index(drop=True)
                    st.session_state['data'] = new_df
                    save_data(new_df)
                    st.success("✅ File berhasil dihapus permanen.")
                    time.sleep(1)
                    st.rerun()



# ================= EDIT PAGE (MENU BARU) =================
def edit_page():
    st.markdown("## ✏️ Edit Data")
    df = st.session_state['data']

    if df.empty:
        st.info("Database masih kosong.")
        return

    c1, c2 = st.columns([1, 2])

    with c1:
        kat_list = sorted(df['Kategori'].dropna().unique().tolist())
        sel_kat = st.selectbox("Pilih Kategori", kat_list)

        df_kat = df[df['Kategori'] == sel_kat].copy()
        # pilih berdasarkan Nama_File biar gampang
        file_list = df_kat['Nama_File'].fillna("").tolist()
        sel_file = st.selectbox("Pilih File", file_list)

        # ambil index row asli
        row_idx = df_kat[df_kat['Nama_File'] == sel_file].index[0]

    with c2:
        st.markdown("### Form Edit")
        cur = df.loc[row_idx]

        # prefill
        e_menu = st.text_input("Menu", value=str(cur.get('Menu', '') if pd.notna(cur.get('Menu', '')) else ''))
        e_sub = st.text_input("Sub Menu", value=str(cur.get('Sub_Menu', '') if pd.notna(cur.get('Sub_Menu', '')) else ''))
        e_sub2 = st.text_input("Judul Kegiatan (Sub2_Menu)", value=str(cur.get('Sub2_Menu', '') if pd.notna(cur.get('Sub2_Menu', '')) else ''))
        e_nama = st.text_input("Nama File", value=str(cur.get('Nama_File', '') if pd.notna(cur.get('Nama_File', '')) else ''))
        e_link = st.text_input("Link File", value=str(cur.get('Link_File', '') if pd.notna(cur.get('Link_File', '')) else ''))

        st.markdown("#### 📷 Edit Cover Kategori (opsional)")
        e_img = st.file_uploader("Upload cover baru (kosongkan jika tidak ingin ganti)", type=['png','jpg','jpeg'], key="edit_cover")

        if st.button("💾 SIMPAN PERUBAHAN", type="primary", use_container_width=True):
            # update row
            df2 = df.copy()

            df2.at[row_idx, 'Menu'] = e_menu
            df2.at[row_idx, 'Sub_Menu'] = e_sub
            df2.at[row_idx, 'Sub2_Menu'] = e_sub2
            df2.at[row_idx, 'Nama_File'] = e_nama
            df2.at[row_idx, 'Link_File'] = e_link

            # cover kategori: kalau upload baru, update semua row kategori agar cover konsisten
            if e_img is not None:
                img_str = image_to_base64(e_img)
                if img_str:
                    df2.loc[df2['Kategori'] == sel_kat, 'Gambar_Base64'] = img_str

            st.session_state['data'] = df2
            save_data(df2)
            st.success("✅ Berhasil disimpan!")
            time.sleep(1)
            st.rerun()


def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()


# ================= HOME DASHBOARD =================
def home_page():
    try:
        img_code = get_base64_of_bin_file("logo.png")
        img_tag = f'<img src="data:image/png;base64,{img_code}" class="hero-logo">'
    except:
        img_tag = ""

    st.markdown("""
    <style>
        .hero-logo{
            width: 230px;
            height: auto;
            margin-bottom: 15px;
            display: block;
        }
    </style>
    """, unsafe_allow_html=True)

    st.markdown(
        f"""
        <div class="hero-container">
            {img_tag}
            <div class="hero-subtitle">
                Pusat database digital Badan Pusat Statistik. Kelola dan temukan data dengan mudah.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

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

            if st.button("Buka Folder", key=f"btn_{idx}", use_container_width=True):
                st.session_state['selected_category'] = cat
                st.session_state['current_view'] = 'detail'
                st.rerun()
            st.write("")

    st.markdown("""<div class="footer">© 2025 Badan Pusat Statistik • Dashboard Sostat</div>""", unsafe_allow_html=True)


# ================= DETAIL PAGE =================
def detail_page():
    cat = st.session_state['selected_category']
    df = st.session_state['data']
    subset_all = df[df['Kategori'] == cat].copy()

    st.button("⬅️ Kembali ke Dashboard", on_click=lambda: st.session_state.update({'current_view': 'home'}))

    st.markdown(f"""
    <div style="background:white; padding:20px; border-radius:18px; border-left:6px solid #6366F1; margin-top:10px; border:1px solid #E5E7EB; box-shadow:0 10px 22px rgba(2,6,23,.05);">
        <h2 style="margin:0; color:#111827;">📂 {cat}</h2>
        <p style="margin:6px 0 0; color:#6B7280;">Arsip dokumen digital</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # SEARCH
    search = st.text_input("🔍 Cari File...", placeholder="Ketik nama dokumen...")

    # FILTER PANEL (di bawah search bar)
    st.markdown('<div class="filter-panel">', unsafe_allow_html=True)
    f1, f2, f3 = st.columns(3)

    menu_opts = ["Semua"] + sorted([x for x in subset_all['Menu'].dropna().unique().tolist() if str(x).strip() != ""])
    sub_opts = ["Semua"] + sorted([x for x in subset_all['Sub_Menu'].dropna().unique().tolist() if str(x).strip() != ""])
    sub2_opts = ["Semua"] + sorted([x for x in subset_all['Sub2_Menu'].dropna().unique().tolist() if str(x).strip() != ""])

    with f1:
        sel_menu = st.selectbox("Filter Menu", menu_opts, index=0)
    with f2:
        sel_sub = st.selectbox("Filter Sub Menu", sub_opts, index=0)
    with f3:
        sel_sub2 = st.selectbox("Filter Judul Kegiatan (Sub2)", sub2_opts, index=0)

    st.markdown('</div>', unsafe_allow_html=True)

    # apply filter
    subset = subset_all
    if sel_menu != "Semua":
        subset = subset[subset['Menu'] == sel_menu]
    if sel_sub != "Semua":
        subset = subset[subset['Sub_Menu'] == sel_sub]
    if sel_sub2 != "Semua":
        subset = subset[subset['Sub2_Menu'] == sel_sub2]

    if search:
        subset = subset[subset['Nama_File'].astype(str).str.contains(search, case=False, na=False)]

    menus = subset['Menu'].dropna().unique()

    if len(menus) == 0:
        st.info("Tidak ada data sesuai filter/pencarian.")
        return

    tabs = st.tabs([str(m) for m in menus if str(m).strip() != ""])

    for i, m in enumerate([x for x in menus if str(x).strip() != ""]):
        with tabs[i]:
            sub_df = subset[subset['Menu'] == m]
            subs = [x for x in sub_df['Sub_Menu'].dropna().unique()]

            if len(subs) == 0:
                st.caption("Tidak ada sub menu.")
                continue

            for s in subs:
                with st.expander(f"📁 {s if str(s).strip() else 'Umum'}", expanded=True):
                    s_df = sub_df[sub_df['Sub_Menu'] == s].copy()

                    # ========= PERUBAHAN UTAMA =========
                    # Sub2_Menu jadi "Judul Kegiatan" (grouping), bukan meta di bawah Nama_File
                    kegiatan_list = s_df['Sub2_Menu'].fillna("-").unique().tolist()

                    for keg in kegiatan_list:
                        keg_label = keg if str(keg).strip() else "-"
                        st.markdown(
                            f'<div class="kegiatan-title">🎯 {keg_label} <span class="kegiatan-pill">Kegiatan</span></div>',
                            unsafe_allow_html=True
                        )

                        keg_df = s_df[s_df['Sub2_Menu'].fillna("-") == keg_label]

                        if keg_df.empty:
                            st.caption("Tidak ada file.")
                            continue

                        for _, r in keg_df.iterrows():
                            st.markdown(f"""
                            <div class="file-row">
                                <div>
                                    <div style="font-weight:800; color:#111827;">📄 {r['Nama_File']}</div>
                                </div>
                                <a href="{r['Link_File']}" target="_blank" class="dl-link">Buka ⬇</a>
                            </div>
                            """, unsafe_allow_html=True)


# ================= MAIN CONTROLLER =================
if st.session_state['logged_in']:
    with st.sidebar:
        st.image("https://cdn-icons-png.flaticon.com/512/906/906343.png", width=50)
        st.markdown("### Admin Panel")

        if st.button("🏠 Dashboard", use_container_width=True):
            st.session_state['current_view'] = 'home'
            st.rerun()

        if st.button("⚙️ Input Data", use_container_width=True):
            st.session_state['current_view'] = 'admin'
            st.rerun()

        # ✅ MENU BARU
        if st.button("✏️ Edit Data", use_container_width=True):
            st.session_state['current_view'] = 'edit'
            st.rerun()

        st.markdown("---")

        if st.button("🚪 Logout", use_container_width=True):
            st.session_state['logged_in'] = False
            st.rerun()

    if st.session_state['current_view'] == 'home':
        home_page()
    elif st.session_state['current_view'] == 'detail':
        detail_page()
    elif st.session_state['current_view'] == 'admin':
        admin_page()
    elif st.session_state['current_view'] == 'edit':
        edit_page()
else:
    login_page()
