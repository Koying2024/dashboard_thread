import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import time
import os

# ============================
# 🔧 Konfigurasi Halaman
# ============================
st.set_page_config(
    page_title="Dashboard Thread TOP GUN",
    page_icon="📊",
)

# ============================
# ⏰ Tampilkan Jam Sekarang
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
# 📁 Load Data
# ============================
excel_path = r"C:\Users\karimudin\OneDrive - Zi.Care\Documents - Data Team - Zi.Care\General\#005-User Story DevOps\Recap Top Gun 20250227.xlsx"

if not os.path.exists(excel_path):
    st.error("File Excel tidak ditemukan. Pastikan path file benar.")
    st.stop()

df = pd.read_excel(excel_path)

# ============================
# 🔍 Filter Awal
# ============================
if 'Title' not in df.columns:
    st.error("Kolom 'Title' tidak ditemukan dalam file Excel.")
    st.stop()

df_filtered = df[df['Title'].notna() & (df['Title'] != "")]
kolom_non = ["Week", "Month", "Days", "Year", "Title Validation", "Validation", "Keyword", "insight", "insight Standarized"]
df_tampil = df_filtered.drop(columns=kolom_non, errors='ignore')

# ============================
# 🎛️ Filter Interaktif
# ============================
def buat_filter(kolom_nama, label):
    if kolom_nama in df_tampil.columns:
        st.subheader(label)
        pilihan = st.multiselect(f"Pilih {label.split()[-1]}:", df_tampil[kolom_nama].dropna().unique())
        if pilihan:
            return df_tampil[df_tampil[kolom_nama].isin(pilihan)]
    return df_tampil

df_tampil = buat_filter('Site', "🏥 Filter Berdasarkan Site")
df_tampil = buat_filter('Status', "🔍 Filter Berdasarkan Status")
df_tampil = buat_filter('Role', "👥 Filter Berdasarkan Role")
df_tampil = buat_filter('Title', "🏷️ Filter Berdasarkan Title")

# ============================
# 📊 Pie Chart Status
# ============================
st.subheader("📈 Distribusi Status")

if not df_tampil.empty and 'Status' in df_tampil.columns:
    status_count = df_tampil['Status'].value_counts().sort_values(ascending=False)
    total = status_count.sum()
    labels = [f"{status} ({(jumlah/total)*100:.1f}%) ({jumlah})" for status, jumlah in status_count.items()]

    fig_pie, ax_pie = plt.subplots()
    colors = plt.cm.Pastel1.colors
    ax_pie.pie(status_count, labels=labels, startangle=90, colors=colors)
    ax_pie.axis('equal')
    st.pyplot(fig_pie)
else:
    st.info("Tidak ada data untuk visualisasi Status.")

# ============================
# 📊 Bar Chart Site
# ============================
st.subheader("🏢 Distribusi Jumlah per Site")

if not df_tampil.empty and 'Site' in df_tampil.columns:
    site_count = df_tampil['Site'].value_counts().sort_values(ascending=False)
    fig_site, ax_site = plt.subplots()
    bars = ax_site.bar(site_count.index, site_count.values, color='skyblue')
    ax_site.set_xlabel("Site")
    ax_site.set_ylabel("Jumlah")
    ax_site.set_title("Jumlah Data per Site")
    ax_site.set_xticklabels(site_count.index, rotation=45, ha='right')

    for bar in bars:
        yval = bar.get_height()
        ax_site.text(bar.get_x() + bar.get_width()/2, yval + 0.5, int(yval), ha='center', va='bottom')

    st.pyplot(fig_site)
else:
    st.info("Tidak ada data untuk visualisasi Site.")

# ============================
# 📊 Bar Chart Role
# ============================
st.subheader("👥 Distribusi Jumlah per Role")

if not df_tampil.empty and 'Role' in df_tampil.columns:
    role_count = df_tampil['Role'].value_counts().sort_values(ascending=True)
    fig_role, ax_role = plt.subplots(figsize=(8, len(role_count) * 0.4))
    bars = ax_role.barh(role_count.index, role_count.values, color='mediumseagreen')
    ax_role.set_xlabel("Jumlah")
    ax_role.set_ylabel("Role")
    ax_role.set_title("Jumlah Data per Role")

    for bar in bars:
        xval = bar.get_width()
        ax_role.text(xval + 1, bar.get_y() + bar.get_height()/2, int(xval), va='center')

    st.pyplot(fig_role)
else:
    st.info("Tidak ada data untuk visualisasi Role.")

# ============================
# 📋 Data & Ringkasan
# ============================
st.subheader("✅ Data Setelah Difilter")
st.dataframe(df_tampil)

st.subheader("🧾 Jumlah Row Data")
st.write(f"Jumlah data setelah filter: **{len(df_tampil)} baris**")

# ============================
# 📆 Thread per Bulan & Minggu
# ============================
if 'Tanggal Open' in df_tampil.columns:
    df_tampil['Tanggal Open'] = pd.to_datetime(df_tampil['Tanggal Open'], errors='coerce')
    df_tampil = df_tampil.dropna(subset=['Tanggal Open'])

    # Bulan
    st.subheader("📆 Jumlah Thread per Bulan")
    df_tampil['Bulan'] = df_tampil['Tanggal Open'].dt.strftime('%Y-%m')
    bulan_count = df_tampil['Bulan'].value_counts().sort_index()

    fig_bulan, ax_bulan = plt.subplots(figsize=(10, 5))
    bars = ax_bulan.bar(bulan_count.index, bulan_count.values, color='cornflowerblue')
    ax_bulan.set_xlabel("Bulan")
    ax_bulan.set_ylabel("Jumlah Thread")
    ax_bulan.set_title("Jumlah Thread per Bulan")
    ax_bulan.tick_params(axis='x', rotation=45)

    for bar in bars:
        yval = bar.get_height()
        ax_bulan.text(bar.get_x() + bar.get_width()/2, yval + 0.5, int(yval), ha='center', va='bottom')

    st.pyplot(fig_bulan)

    # Minggu
    st.subheader("📈 Jumlah Thread per Minggu")
    df_tampil['Minggu'] = df_tampil['Tanggal Open'].dt.strftime('%Y-W%U')
    minggu_count = df_tampil['Minggu'].value_counts().sort_index()

    fig_minggu, ax_minggu = plt.subplots(figsize=(12, 5))
    ax_minggu.plot(minggu_count.index, minggu_count.values, marker='o', color='seagreen')
    ax_minggu.set_xlabel("Minggu (Tahun-W)")
    ax_minggu.set_ylabel("Jumlah Thread")
    ax_minggu.set_title("Jumlah Thread per Minggu")
    ax_minggu.tick_params(axis='x', rotation=45)

    for i, val in enumerate(minggu_count.values):
        ax_minggu.text(i, val + 0.5, str(val), ha='center', va='bottom', fontsize=8)

    st.pyplot(fig_minggu)
else:
    st.warning("Kolom 'Tanggal Open' tidak ditemukan atau kosong.")
