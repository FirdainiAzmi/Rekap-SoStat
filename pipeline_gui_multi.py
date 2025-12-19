import streamlit as st
import time

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="Portal BPS Sidoarjo",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. CSS "SUPER PREMIUM" (LUAR & DALAM) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

    /* BASE STYLING */
    .stApp {
        background: linear-gradient(135deg, #f0f4f8 0%, #d9e2ec 100%);
        font-family: 'Poppins', sans-serif;
    }
    
    /* HIDE DEFAULT ELEMENTS */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* --- STYLING HALAMAN DEPAN (KARTU MENU) --- */
    div.stButton > button:first-child {
        background: white;
        border: none;
        height: 160px;
        width: 100%;
        border-radius: 16px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.05);
        color: #333;
        font-family: 'Poppins', sans-serif;
        font-size: 15px;
        font-weight: 600;
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
        padding: 20px;
    }
    div.stButton > button:first-child:hover {
        transform: translateY(-8px);
        box-shadow: 0 15px 30px rgba(0, 84, 166, 0.15);
        background: linear-gradient(135deg, #0054A6 0%, #007bff 100%);
        color: white !important;
    }

    /* --- STYLING HALAMAN DALAM (ISI WOW) --- */
    
    /* 1. File Card (Pengganti Link Biasa) */
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
        transition: transform 0.2s;
    }
    .file-card:hover {
        transform: scale(1.02);
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        cursor: pointer;
    }
    .file-title {
        font-weight: 600;
        color: #2c3e50;
        margin: 0;
    }
    .file-meta {
        font-size: 12px;
        color: #7f8c8d;
    }
    
    /* 2. Status Badge */
    .status-badge {
        padding: 5px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
    }
    .badge-green {background-color: #e6fffa; color: #047857;}
    .badge-blue {background-color: #ebf8ff; color: #0054A6;}
    .badge-orange {background-color: #fffaf0; color: #dd6b20;}

    /* 3. Section Title Inside */
    .inner-header {
        color: #0054A6;
        font-weight: 700;
        margin-top: 20px;
        margin-bottom: 10px;
        border-bottom: 2px solid #e2e8f0;
        padding-bottom: 10px;
    }
    
    /* 4. Tab Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 20px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: white;
        border-radius: 10px 10px 0 0;
        box-shadow: 0 -2px 10px rgba(0,0,0,0.02);
        padding-left: 20px;
        padding-right: 20px;
        font-weight: 600;
    }
    .stTabs [aria-selected="true"] {
        background-color: #fff;
        color: #0054A6;
        border-bottom: 3px solid #0054A6;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. DATABASE STRUKTUR DATA (DIPERBUAT LEBIH KAYA) ---
# Struktur data ini disesuaikan dengan permintaan user (Logic Dropdown/Drilldown)
data_structure = {
    "Statistik Kependudukan": {
        "icon": "👥", 
        "desc": "Sakernas & Survei Penduduk",
        "subs": {
            "Sakernas Triwulan": {
                "type": "menu",
                "items": {
                    "Sakernas Agustus 2025": {
                        "status": "Sedang Berjalan", 
                        "progress": 70,
                        "files": ["📄 Materi Pelatihan Petugas", "📝 Instrumen Pendataan", "📊 Target Sampel Blok Sensus", "📂 Arsip Surat Tugas"]
                    },
                    "Sakernas November 2025": {
                        "status": "Persiapan", 
                        "progress": 10,
                        "files": ["📄 Draft Pedoman", "📂 Rencana Anggaran (RAB)"]
                    }
                }
            }
        }
    },
    "Statistik Ketahanan": {
        "icon": "🛡️", 
        "desc": "Podes, SNLIK, Polkam",
        "subs": {
            "Potensi Desa (Podes)": {"type": "page", "status": "Selesai", "files": ["📊 Publikasi Podes 2024", "📂 Raw Data Mikro", "📝 Kuesioner Desa"]},
            "SNLIK": {"type": "page", "status": "Analisis", "files": ["📂 Tabulasi SNLIK", "📄 Laporan Eksekutif"]},
            "Polkam": {"type": "page", "status": "Pengolahan", "files": ["📝 Entri Data Polkam", "📂 Dokumen Validasi"]}
        }
    },
    "Statistik Kesejahteraan": {
        "icon": "🏠", 
        "desc": "Susenas & Seruti",
        "subs": {
            "Susenas": {
                "type": "menu",
                "items": {
                    "Susenas Maret 2025": {"status": "Selesai", "progress": 100, "files": ["📂 Master File Susenas", "📄 Pelatihan Inda", "📊 Publikasi Awal"]},
                    "Susenas September 2025": {"status": "Akan Datang", "progress": 0, "files": ["📄 Kerangka Sampel"]}
                }
            },
            "Seruti": {
                "type": "menu",
                "items": {
                    "Triwulan 2 2025": {"status": "Arsip", "progress": 100, "files": ["📂 Data T2 Full"]},
                    "Triwulan 3 2025": {"status": "On Going", "progress": 45, "files": ["📝 Monitoring Lapangan", "📂 Upload Data"]},
                    "Triwulan 4 2025": {"status": "Waiting", "progress": 0, "files": []}
                }
            }
        }
    },
    "Publikasi Statistik": {
        "icon": "📚", "desc": "Buku Dalam Angka, DDA", "direct_link": True,
        "content": "Koleksi Publikasi Digital",
        "files": ["📚 Kab. Sidoarjo Dalam Angka 2024", "📚 Statistik Kesejahteraan Rakyat 2024", "📚 Analisis Profil Kemiskinan"]
    },
    "Desa Cantik": {
        "icon": "🌸", "desc": "Desa Cinta Statistik", "direct_link": True,
        "content": "Program Pembinaan Statistik",
        "files": ["📂 SK Agen Statistik", "📝 Modul Pembinaan Desa", "📷 Galeri Kegiatan"]
    }
}

# --- 4. NAVIGASI STATE ---
if 'current_level' not in st.session_state: st.session_state.current_level = 'home'
if 'selected_category' not in st.session_state: st.session_state.selected_category = None
if 'selected_sub_item' not in st.session_state: st.session_state.selected_sub_item = None

def go_home():
    st.session_state.current_level = 'home'
    st.session_state.selected_category = None
    st.session_state.selected_sub_item = None

# --- 5. FUNGSI RENDER KOMPONEN WOW ---

def render_file_card(title, tag="PDF"):
    # HTML Component untuk File Card yang Cantik
    st.markdown(f"""
    <div class="file-card">
        <div>
            <div class="file-title">📄 {title}</div>
            <div class="file-meta">Diupdate: Baru saja • Tipe: {tag}</div>
        </div>
        <div style="background:#eef2ff; padding:8px 15px; border-radius:8px; color:#0054A6; font-weight:bold; font-size:12px;">
            Unduh ⬇️
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_status_header(title, status, progress=None):
    # Header dinamis dengan Progress bar
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f"### 👉 {title}")
    with col2:
        # Warna badge berdasarkan status
        color_class = "badge-green" if status == "Selesai" else ("badge-blue" if status == "Sedang Berjalan" or status == "On Going" else "badge-orange")
        st.markdown(f'<div style="text-align:right;"><span class="status-badge {color_class}">{status}</span></div>', unsafe_allow_html=True)
    
    if progress is not None:
        st.progress(progress)

# --- 6. LOGIKA UI UTAMA ---

# HEADER GLOBAL (HERO)
st.markdown("""
<div style="text-align: center; margin-bottom: 30px; padding: 20px; background: white; border-radius: 20px; box-shadow: 0 10px 20px rgba(0,0,0,0.03);">
    <h1 style="color:#0054A6; margin:0; font-size: 2.2rem;">PORTAL KEGIATAN SOSIAL</h1>
    <p style="color:#F7941D; font-weight:600; margin:0;">BPS KABUPATEN SIDOARJO</p>
    <p style="color:#666; font-size:0.9rem; margin-top:10px;">Pusat Integrasi Data & Dokumen Digital</p>
</div>
""", unsafe_allow_html=True)

# SEARCH BAR
search_cols = st.columns([1, 6, 1])
with search_cols[1]:
    search_query = st.text_input("", placeholder="🔍 Cari 'Sakernas', 'Susenas', atau dokumen...", label_visibility="collapsed")
    st.markdown("<div style='margin-bottom: 30px;'></div>", unsafe_allow_html=True)

# --- KONTEN UTAMA ---

# A. JIKA ADA PENCARIAN
if search_query:
    st.info(f"🔍 Hasil Pencarian untuk: **{search_query}**")
    # (Logika pencarian sederhana - disingkat untuk fokus visual)
    st.write("Fitur pencarian aktif...") 

# B. JIKA TIDAK ADA PENCARIAN (NORMAL FLOW)
else:
    # --- HALAMAN DEPAN (HOME) ---
    if st.session_state.current_level == 'home':
        cols = st.columns(5)
        categories = list(data_structure.keys())
        for i, col in enumerate(cols):
            cat_name = categories[i]
            data = data_structure[cat_name]
            with col:
                # Kartu Menu Utama
                if st.button(f"{data['icon']}\n\n{cat_name}\n\n{data['desc']}", key=cat_name):
                    st.session_state.selected_category = cat_name
                    st.session_state.current_level = 'direct_page' if data.get("direct_link") else 'category_view'
                    st.rerun()

    # --- HALAMAN DALAM (ISI KATEGORI) ---
    elif st.session_state.current_level == 'category_view':
        selected_cat = st.session_state.selected_category
        cat_data = data_structure[selected_cat]
        
        # Tombol Navigasi Atas
        if st.button("⬅️ Dashboard Utama"):
            go_home()
            st.rerun()
            
        # Judul Halaman Dalam
        st.markdown(f"<h2 style='color:#0054A6;'>{cat_data['icon']} {selected_cat}</h2>", unsafe_allow_html=True)
        st.write("Pilih kegiatan di bawah untuk melihat detail dokumen.")
        
        # LOGIKA TABS OTOMATIS BERDASARKAN SUB-MENU
        subs = cat_data["subs"]
        sub_names = list(subs.keys())
        
        # Membuat Tab untuk Sub-Kategori (Misal: Sakernas Triwulan)
        tabs = st.tabs([f"📂 {name}" for name in sub_names])
        
        for i, tab in enumerate(tabs):
            sub_name = sub_names[i]
            sub_info = subs[sub_name]
            
            with tab:
                st.markdown("<div style='margin-top:20px;'></div>", unsafe_allow_html=True)
                
                # JIKA TIPE NYA ADALAH "PAGE" (Langsung isi file)
                if sub_info["type"] == "page":
                    render_status_header(sub_name, sub_info.get("status", "Aktif"))
                    
                    st.markdown("#### 📥 Dokumen Tersedia")
                    f_cols = st.columns(2) # Grid 2 Kolom untuk File Card
                    for idx, f in enumerate(sub_info["files"]):
                        with f_cols[idx % 2]:
                            render_file_card(f)
                            
                # JIKA TIPE NYA ADALAH "MENU" (Ada sub-item lagi seperti Agt/Nov)
                elif sub_info["type"] == "menu":
                    items = sub_info["items"]
                    
                    # Kita gunakan Expander yang dimodifikasi atau Container
                    for item_name, item_data in items.items():
                        with st.expander(f"{item_name}", expanded=True):
                            # Tampilkan Progress Bar & Status
                            render_status_header(item_name, item_data["status"], item_data.get("progress"))
                            
                            st.markdown("#### 📥 Arsip Dokumen")
                            if not item_data["files"]:
                                st.info("Belum ada dokumen yang diunggah.")
                            else:
                                f_cols = st.columns(2)
                                for idx, f in enumerate(item_data["files"]):
                                    with f_cols[idx % 2]:
                                        render_file_card(f)

    # --- HALAMAN DIRECT LINK (PUBLIKASI / DESA CANTIK) ---
    elif st.session_state.current_level == 'direct_page':
        selected_cat = st.session_state.selected_category
        cat_data = data_structure[selected_cat]
        
        if st.button("⬅️ Dashboard Utama"):
            go_home()
            st.rerun()
            
        st.markdown(f"<h2 style='color:#F7941D;'>{cat_data['icon']} {selected_cat}</h2>", unsafe_allow_html=True)
        
        # Layout Dashboard Ringkas
        c1, c2, c3 = st.columns(3)
        c1.metric("Total Dokumen", len(cat_data["files"]))
        c2.metric("Viewer Bulan Ini", "125 User", "12%")
        c3.metric("Status Update", "Minggu Lalu")
        
        st.divider()
        
        st.markdown("### 📚 Daftar Pustaka")
        for f in cat_data["files"]:
            render_file_card(f, tag="Publikasi")

# Footer Kosong agar rapi
st.write("")
st.write("")
