import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import time

# ============================
# 🔧 Konfigurasi Halaman
# ============================
st.set_page_config(
    page_title="Dashboard Thread TOP GUN",
    page_icon="📊",
)

# ============================
# ⏰ Auto-refresh tiap 60 detik
# ============================
st.query_params["t"] = int(time.time() // 60)

# ============================
# ⏰ Tampilkan Jam + Tanggal
# ============================
now = datetime.now().strftime("%A, %d %B %Y %I:%M:%S %p")
st.markdown(
    f"""
    <div style='text-align: right; font-weight: bold; font-size:16px; color:#FFF; background-color:#262730; padding:10px; border-radius:10px'>
        {now}
    </div>
    """,
    unsafe_allow_html=True
)

# ============================
# 📌 Judul Dashboard
# ============================
st.title("📊 Dashboard Thread")
st.write("Dashboard ini menyajikan informasi visual Thread berdasarkan Chanel 911 - TOP GUN !!!")

# ============================
# 📁 Load Data dari Google Sheets
# ============================
st.subheader("📂 Mengambil data dari Google Sheets...")

sheet_id = "1TQrJEkRmeEek2GILWxzJrP25py2bxxS8"  # Ganti dengan ID dokumenmu
sheet_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"

try:
    df = pd.read_csv(sheet_url)
    st.success("✅ Data berhasil dimuat dari Google Sheets.")
except Exception as e:
    st.error(f"❌ Gagal membaca file dari Google Sheets. Pesan error:\n{e}")
    st.stop()

# ============================
# 🔍 Filter Awal
# ============================
df_filtered = df[df['Title'].notna() & (df['Title'] != "")]
kolom_non = ["Week", "Month", "Days", "Year", "Title Validation", "Validation", "Keyword", "insight", "insight Standarized"]
df_tampil = df_filtered.drop(columns=kolom_non, errors='ignore')

# ============================
# 🎯 Filter
# ============================
def buat_filter(nama_kolom, judul, emoji):
    st.subheader(f"{emoji} Filter Berdasarkan {judul}")
    if nama_kolom in df_tampil.columns:
        options = df_tampil[nama_kolom].dropna().unique()
        selected = st.multiselect(f"Pilih {judul}:", options)
        if selected:
            return df_tampil[df_tampil[nama_kolom].isin(selected)]
    return df_tampil

df_tampil = buat_filter("Site", "Site", "🏥")
df_tampil = buat_filter("Status", "Status", "🔍")
df_tampil = buat_filter("Role", "Role", "👥")
df_tampil = buat_filter("Title", "Title", "🏷️")

# ============================
# 📈 Pie Chart: Status
# ============================
st.subheader("📈 Distribusi Status")
if not df_tampil.empty and "Status" in df_tampil.columns:
    status_count = df_tampil["Status"].value_counts()
    total = status_count.sum()
    labels = [f"{s} ({(c/total)*100:.1f}%) ({c})" for s, c in status_count.items()]

    fig1, ax1 = plt.subplots()
    ax1.pie(status_count, labels=labels, startangle=90, colors=plt.cm.Pastel1.colors)
    ax1.axis("equal")
    st.pyplot(fig1)
else:
    st.info("Tidak ada data untuk visualisasi Status.")

# ============================
# 📊 Bar Chart: Site
# ============================
st.subheader("🏢 Distribusi Jumlah per Site")
if not df_tampil.empty and "Site" in df_tampil.columns:
    site_count = df_tampil["Site"].value_counts()
    fig2, ax2 = plt.subplots()
    bars = ax2.bar(site_count.index, site_count.values, color="skyblue")
    ax2.set_xlabel("Site")
    ax2.set_ylabel("Jumlah")
    ax2.set_title("Jumlah Data per Site")
    ax2.set_xticklabels(site_count.index, rotation=45, ha="right")
    for bar in bars:
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5, int(bar.get_height()), ha='center')
    st.pyplot(fig2)
else:
    st.info("Tidak ada data untuk visualisasi Site.")

# ============================
# 📊 Bar Chart Horizontal: Role
# ============================
st.subheader("👥 Distribusi Jumlah per Role")
if not df_tampil.empty and "Role" in df_tampil.columns:
    role_count = df_tampil["Role"].value_counts().sort_values()
    fig3, ax3 = plt.subplots(figsize=(8, len(role_count) * 0.4))
    bars = ax3.barh(role_count.index, role_count.values, color="mediumseagreen")
    ax3.set_xlabel("Jumlah")
    ax3.set_ylabel("Role")
    ax3.set_title("Jumlah Data per Role")
    for bar in bars:
        ax3.text(bar.get_width() + 1, bar.get_y() + bar.get_height()/2, int(bar.get_width()), va='center')
    st.pyplot(fig3)
else:
    st.info("Tidak ada data untuk visualisasi Role.")

# ============================
# 📋 Tabel Data
# ============================
st.subheader("✅ Data Setelah Difilter")
st.dataframe(df_tampil)

# ============================
# 🧾 Ringkasan
# ============================
st.subheader("📌 Ringkasan")
st.write(f"Jumlah data setelah filter: **{len(df_tampil)} baris**")

# ============================
# 📅 Thread per Bulan dan Minggu
# ============================
st.subheader("📆 Jumlah Thread per Bulan & Minggu")
if "Tanggal Open" in df_tampil.columns:
    df_tampil["Tanggal Open"] = pd.to_datetime(df_tampil["Tanggal Open"], errors="coerce")
    df_tampil = df_tampil.dropna(subset=["Tanggal Open"])
    df_tampil["Bulan"] = df_tampil["Tanggal Open"].dt.strftime('%Y-%m')
    df_tampil["Minggu"] = df_tampil["Tanggal Open"].dt.strftime('%Y-W%U')

    # Bulan
    bulan_count = df_tampil["Bulan"].value_counts().sort_index()
    fig4, ax4 = plt.subplots(figsize=(10, 5))
    bars = ax4.bar(bulan_count.index, bulan_count.values, color='cornflowerblue')
    ax4.set_xlabel("Bulan")
    ax4.set_ylabel("Jumlah Thread")
    ax4.set_title("Jumlah Thread per Bulan")
    ax4.tick_params(axis='x', rotation=45)
    for bar in bars:
        ax4.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5, int(bar.get_height()), ha='center')
    st.pyplot(fig4)

    # Minggu
    minggu_count = df_tampil["Minggu"].value_counts().sort_index()
    fig5, ax5 = plt.subplots(figsize=(12, 5))
    ax5.plot(minggu_count.index, minggu_count.values, marker='o', color='seagreen')
    ax5.set_xlabel("Minggu")
    ax5.set_ylabel("Jumlah Thread")
    ax5.set_title("Jumlah Thread per Minggu")
    ax5.tick_params(axis='x', rotation=45)
    for i, val in enumerate(minggu_count.values):
        ax5.text(i, val + 0.5, str(val), ha='center')
    st.pyplot(fig5)

else:
    st.warning("Kolom 'Tanggal Open' tidak ditemukan atau kosong.")
