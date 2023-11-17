import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import datetime 
import numpy as np


# Judul aplikasi
st.title("Cuaca di China")

# Membaca data cuaca dari file CSV
@st.cache_data  # Menggunakan caching untuk mempercepat pembacaan data
def load_data(): 
    data = pd.read_excel('dashboard/cuaca_fix.xlsx')
    return data

data = load_data()


st.title('Daftar 3 Suhu Terdingin dan Terpanas di China')

# Membuat kolom dengan dua div
col1, col2 = st.columns(2)


# Tampilkan kota-kota terdingin di kolom pertama
with col1:
    city_temperatures = data.groupby('station')['TEMP'].min().reset_index()
    coldest_cities = city_temperatures.sort_values(by='TEMP', ascending=True).head(3)
    st.header('Suhu Terdingin')
    coldest_cities['TEMP'] = coldest_cities['TEMP'].round(1).astype(str) + ' °C'
    st.table(coldest_cities[['station', 'TEMP']].reset_index(drop=True))

# Tampilkan kota-kota terpanas di kolom kedua
with col2:
    city_temperatures = data.groupby('station')['TEMP'].max().reset_index()
    top_cities = city_temperatures.sort_values(by='TEMP', ascending=False).head(3)
    st.header('Suhu Terpanas')
    top_cities['TEMP'] = top_cities['TEMP'].round(1).astype(str) + ' °C'
    st.table(top_cities[['station', 'TEMP']].reset_index(drop=True))







st.sidebar.title('Menu')


# Sidebar memilih kolom "station"
selected_station = st.sidebar.selectbox('Pilih Kota', data['station'].unique())

# Filter data berdasarkan kolom "station" yang dipilih
filtered_data = data[data['station'] == selected_station]
st.sidebar.title('') 
# Pilihan Tahun
selected_year = st.sidebar.selectbox('Pilih Tahun', data['year'].unique())

# Pilihan Bulan
selected_month = st.sidebar.selectbox('Pilih Bulan', data['month'].unique())

# Pilihan Tanggal
selected_day = st.sidebar.selectbox('Pilih Tanggal', data['day'].unique())

# Filter data berdasarkan Tahun, Bulan, dan Tanggal yang dipilih
filtered_dat = data[(data['year'] == selected_year) & (data['month'] == selected_month) & (data['day'] == selected_day) & (data['station'] == selected_station)]

# Hitung rata-rata CO2 per tahun untuk data terpilih
df = filtered_data[['TEMP', 'year']].groupby(["year"]).mean().reset_index().sort_values(by='year', ascending=False).round(1)


st.title('Rata-rata Suhu per Tahun')

st.bar_chart(df.set_index('year'), color=['#2E4374'])


  
st.title(f'Perkiraan Cuaca Tanggal {selected_day} / {selected_month} / {selected_year} di {selected_station}')
st.write(filtered_dat[['jam', 'TEMP', 'weather_condition', 'RAIN', 'wd']])


# Hitung jumlah data untuk setiap stasiun
station_counts = data['station'].value_counts()

# Tampilkan judul
st.title("Kontribusi Daerah dalam Data Cuaca")

# Warna gradien
colors = plt.cm.Blues(np.linspace(0, 1, len(station_counts)))

fig, ax = plt.subplots()
pie_wedge_collection = ax.pie(station_counts, labels=station_counts.index, autopct='%1.1f%%', startangle=90, colors=colors)
ax.axis('equal')  # Agar diagram lingkaran menjadi lingkaran sempurna


# Mengatur gradien warna untuk setiap irisan
for i, pie_wedge in enumerate(pie_wedge_collection[0]):
    pie_wedge.set_facecolor(colors[i])


st.pyplot(fig)



# Anda dapat mengelompokkan data berdasarkan kolom 'hour' dan menghitung rata-rata
grouped_data = filtered_dat.groupby('hour')[['TEMP', 'SO2', 'O3', 'PM10']].mean()


st.title(f'Grafik di Tanggal {selected_day} / {selected_month} / {selected_year}')
# Visualisasi data suhu, SO2, O3, dan PM10 dalam satu grafik line chart
st.line_chart(data=grouped_data)

