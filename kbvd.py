import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
file_path = "https://raw.githubusercontent.com/andrianbaros/googlemobility2022dataset/refs/heads/main/2022_ID_Region_Mobility_Report.csv"
data = pd.read_csv(file_path)

# Konversi kolom tanggal ke format datetime
data['date'] = pd.to_datetime(data['date'])

# Kategori Mobilitas
kategori_mobilitas = {
    "retail_and_recreation_percent_change_from_baseline": "Retail & Rekreasi",
    "grocery_and_pharmacy_percent_change_from_baseline": "Toko & Apotek",
    "parks_percent_change_from_baseline": "Taman",
    "transit_stations_percent_change_from_baseline": "Transportasi Publik",
    "workplaces_percent_change_from_baseline": "Tempat Kerja",
    "residential_percent_change_from_baseline": "Area Pemukiman"
}

# Perbandingan Perubahan Mobilitas Berdasarkan Kategori
tren_mobilitas_kategori = data.groupby("date")[list(kategori_mobilitas.keys())].mean().reset_index()
tren_mobilitas_kategori.rename(columns=kategori_mobilitas, inplace=True)

# Perbandingan Mobilitas di Bali Sebelum dan Sesudah Nyepi
bali_data = data[(data["sub_region_1"] == "Bali") & 
                 (data["date"] >= "2022-03-01") & 
                 (data["date"] <= "2022-03-07")]

bali_tren = bali_data.groupby("date")[list(kategori_mobilitas.keys())].mean().reset_index()
bali_tren.rename(columns=kategori_mobilitas, inplace=True)

bali_melted = bali_tren.melt(id_vars=["date"], 
                             value_vars=list(kategori_mobilitas.values()), 
                             var_name="Kategori Mobilitas", 
                             value_name="Perubahan (%)")

# Tren Mobilitas Retail dan Rekreasi di Pulau Jawa (Ramadan & Lebaran)
wilayah_jawa = ["Jawa Barat", "Banten", "Jakarta", "Jawa Tengah", "Jawa Timur", "Daerah Istimewa Yogyakarta"]
jawa_data = data[data["sub_region_1"].isin(wilayah_jawa)]

tanggal_awal = "2022-04-02"
tanggal_akhir = "2022-05-08"
jawa_filtered = jawa_data[(jawa_data["date"] >= tanggal_awal) & (jawa_data["date"] <= tanggal_akhir)]

heatmap_data = jawa_filtered.pivot_table(
    index="sub_region_1", 
    columns="date", 
    values="retail_and_recreation_percent_change_from_baseline")

# Streamlit UI
st.title("📊 Dashboard Analisis Mobilitas Publik di Indonesia")
st.write("Dashboard ini menampilkan analisis mobilitas publik berdasarkan data dari Google Mobility Report tahun 2022.")

# 1️⃣ Perbandingan Perubahan Mobilitas Berdasarkan Kategori
st.subheader("📈 Perbandingan Perubahan Mobilitas Berdasarkan Kategori")
fig1 = px.line(
    tren_mobilitas_kategori, 
    x="date", y=list(kategori_mobilitas.values()), 
    title="Perbandingan Perubahan Mobilitas Berdasarkan Kategori",
    labels={"value": "Rata-Rata Perubahan (%)", "date": "Tanggal", "variable": "Kategori Mobilitas"},
    template="plotly_white")
st.plotly_chart(fig1)

# 2️⃣ Perbandingan Mobilitas di Bali Sebelum dan Sesudah Nyepi
st.subheader("📉 Dampak Nyepi Terhadap Mobilitas di Bali")
fig2 = px.bar(
    bali_melted, x="date", y="Perubahan (%)", color="Kategori Mobilitas", 
    title="Perbandingan Mobilitas di Bali Sebelum dan Sesudah Nyepi (2022)",
    labels={"date": "Tanggal"},
    barmode="relative",
    template="plotly_white")
st.plotly_chart(fig2)

# 3️⃣ Tren Mobilitas Retail dan Rekreasi di Pulau Jawa (Ramadan & Lebaran)
st.subheader("🛍️ Mobilitas Retail & Rekreasi di Pulau Jawa Selama Ramadan & Lebaran")
fig3 = px.imshow(
    heatmap_data, 
    labels={"x": "Tanggal", "y": "Wilayah", "color": "Perubahan (%)"},
    title="Tren Mobilitas Retail dan Rekreasi di Pulau Jawa Ramadan & Lebaran (2022)",
    color_continuous_scale="Reds",
    template="plotly_white")
st.plotly_chart(fig3)
