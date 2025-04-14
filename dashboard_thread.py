import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import time

# ============================
# 🔧 Konfigurasi Halaman (Ubah Judul Tab, Icon, Layout)
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
# ⏰ Tampilkan Jam + Tanggal di Kanan Atas
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
url_csv = "https://docs.google.com/spreadsheets/d/1TQrJEkRmeEek2GILWxzJrP25py2bxxS8/export?format=csv"
df = pd.read_csv(url_csv)

# ============================
# 🔍 Filter Awal: Hanya Title yang tidak kosong
# ============================
df_filtered = df[df['Title'].notna() & (df['Title'] != "")]

# ============================
# 🚫 Sembunyikan Kolom Tidak Ditampilkan
# ============================
kolom_non = ["Week", "Month", "Days", "Year", "Title Validation", "Validation", "Keyword", "insight", "insight Standarized"]
df_tampil = df_filtered.drop(columns=kolom_non, errors='ignore')

# ============================
# 🏥 Filter Berdasarkan Site
# ============================
st.subheader("🏥 Filter Berdasarkan Site")
site_list = df_tampil['Site'].dropna().unique()
selected_site = st.multiselect("Pilih Site:", site_list)
if selected_site:
    df_tampil = df_tampil[df_tampil['Site'].isin(selected_site)]

# ============================
# 🔍 Filter Berdasarkan Status
# ============================
st.subheader("🔍 Filter Berdasarkan Status")
status_list = df_tampil['Status'].dropna().unique()
selected_status = st.multiselect("Pilih Status:", status_list)
if selected_status:
    df_tampil = df_tampil[df_tampil['Status'].isin(selected_status)]

# ============================
# 👥 Filter Berdasarkan Role
# ============================
st.subheader("👥 Filter Berdasarkan Role")
role_list = df_tampil['Role'].dropna().unique()
selected_role = st.multiselect("Pilih Role:", role_list)
if selected_role:
    df_tampil = df_tampil[df_tampil['Role'].isin(selected_role)]

# ============================
# 🏷️ Filter Berdasarkan Title
# ============================
st.subheader("🏷️ Filter Berdasarkan Title")
title_list = df_tampil['Title'].dropna().unique()
selected_title = st.multiselect("Pilih Title:", title_list)
if selected_title:
    df_tampil = df_tampil[df_tampil['Title'].isin(selected_title)]

# ============================
# 📊 Chart 1: Pie Chart Status
# ============================
st.subheader("📈 Distribusi Status")
if not df_tampil.empty:
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
# 📊 Chart 2: Bar Chart Site
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
# 📊 Chart 3: Horizontal Bar Chart Role
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
# 📋 Tampilkan Data
# ============================
st.subheader("✅ Data Setelah Difilter")
st.dataframe(df_tampil)

# ============================
# 🧮 Ringkasan Data
# ============================
st.subheader("💾 Jumlah Row Data")
st.write(f"Jumlah data setelah filter: **{len(df_tampil)} baris**")

# ============================
# 📊 Jumlah Thread Berdasarkan Bulan
# ============================
st.subheader("📆 Jumlah Thread per Bulan (Berdasarkan Tanggal Open)")
if 'Tanggal Open' in df_tampil.columns:
    df_tampil['Tanggal Open'] = pd.to_datetime(df_tampil['Tanggal Open'], errors='coerce')
    df_tampil = df_tampil.dropna(subset=['Tanggal Open'])
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
        ax_bulan.text(bar.get_x() + bar.get_width()/2, yval + 0.5, int(yval), ha='center', va='bottom', fontsize=9)
    st.pyplot(fig_bulan)

    # ============================
    # 📈 Jumlah Thread Berdasarkan Minggu
    # ============================
    st.subheader("📈 Jumlah Thread per Minggu (Berdasarkan Tanggal Open)")
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
