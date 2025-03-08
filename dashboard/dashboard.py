import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
file_path = os.path.abspath("../data/hour.csv")
print("Path absolut:", file_path)
df_hour = pd.read_csv(file_path)
file1_path = os.path.abspath("../data/day.csv")

# Load dataset (pastikan sudah dimuat sebelumnya)
# df_hour = pd.read_csv("../data/hour.csv")  # Sesuaikan dengan lokasi dataset
df_day = pd.read_csv(files1_path)
df_season = df_day[['cnt','season','weekday','workingday','weathersit']]
st.title('Analisis Data - Bike Sharing Dataset') 
# Sidebar untuk memilih tampilan
with st.sidebar:
    st.header("Tentang Dataset")
    st.write("Dataset ini berisi informasi penyewaan sepeda berdasarkan waktu, cuaca, dan hari kerja/akhir pekan.")
    st.write("- **hour.csv**: Data penyewaan sepeda per jam.")
    st.write("- **day.csv**: Data penyewaan sepeda per hari.")


 
hourly_workingday = df_hour[df_hour["workingday"] == 1].groupby("hr")["cnt"].mean()
hourly_weekend = df_hour[df_hour["workingday"] == 0].groupby("hr")["cnt"].mean()

tab1, tab2, tab3 = st.tabs(["Question 1", "Question 2", "Question 3"])

with tab1:
    st.header("Apakah ada pola penggunaan yang menunjukkan jam-jam sibuk dan sepi untuk sistem penyewaan sepeda?")
    with st.container():
    # st.write("### Perbandingan Pola Penyewaan Sepeda: Hari Kerja vs. Akhir Pekan")
    
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(hourly_workingday.index, hourly_workingday.values, marker="o", linestyle="-", color="blue", label="Hari Kerja")
        ax.plot(hourly_weekend.index, hourly_weekend.values, marker="o", linestyle="-", color="red", label="Akhir Pekan")
        
        ax.set_xticks(range(0, 24))
        ax.set_xlabel("Jam")
        ax.set_ylabel("Rata-rata Jumlah Penyewaan Sepeda")
        ax.set_title("Perbandingan Pola Penyewaan Sepeda: Hari Kerja vs. Akhir Pekan")
        ax.legend()
        ax.grid()
        
        st.pyplot(fig)
    # st.image("https://static.streamlit.io/examples/cat.jpg")
    with st.expander("See explanation"):
        st.write(
            """Dari grafik, terlihat pola penggunaan sepeda yang berbeda antara hari kerja (garis biru) dan akhir pekan (garis merah):

1. Jam Sibuk (Peak Hours)
Hari kerja:
- Pagi (07:00 - 09:00) → Lonjakan besar, mencapai puncak sekitar pukul 08:00. Ini menunjukkan bahwa banyak pengguna menggunakan sepeda untuk perjalanan ke tempat kerja atau sekolah.
- Sore (17:00 - 19:00) → Puncak lain terjadi sekitar 18:00, yang mencerminkan perjalanan pulang dari kantor/sekolah.
Akhir pekan:
- Siang hingga sore (10:00 - 17:00) → Aktivitas penyewaan meningkat secara bertahap dan tetap tinggi hingga sore hari. Tidak ada lonjakan tajam seperti di hari kerja, tetapi penggunaannya lebih stabil.
2. Jam Sepi (Off-Peak Hours)
- Dini hari hingga pagi (00:00 - 05:00) → Penggunaan sangat rendah di kedua kategori, karena jam ini biasanya bukan waktu perjalanan utama.
- Hari kerja antara jam 09:00 - 16:00 → Penyewaan cenderung lebih rendah dibandingkan jam sibuk pagi dan sore, menunjukkan bahwa sebagian besar pengguna sudah berada di tempat kerja atau sekolah.

Indikasi : 

Hari kerja menunjukkan pola yang khas untuk komuter, dengan dua lonjakan tajam di pagi dan sore hari.
Akhir pekan memiliki pola penggunaan yang lebih merata sepanjang siang dan sore, menunjukkan penggunaan untuk rekreasi atau perjalanan santai.
Jam-jam sepi terjadi di dini hari dan pagi buta (00:00 - 05:00), serta di antara jam sibuk pada hari kerja."""
        )
with tab2:
    st.header("Apakah ada pola penyewaan yang menunjukkan adanya anomali atau kejadian khusus?")
    with st.container():
        fig, ax = plt.subplots(figsize=(6, 4))  # Buat figure dan axis
        df_season.groupby("weathersit")["cnt"].mean().plot(
            kind="bar", 
            color=["lightgreen", "gold", "red", "darkred"], 
            edgecolor="black",
            ax=ax  # Menggunakan axis yang sudah dibuat
        )
        ax.set_xticks([0, 1, 2, 3])
        ax.set_xticklabels(["Cerah", "Berawan", "Hujan Ringan", "Cuaca Ekstrem"], rotation=0)
        ax.set_title("Pengaruh Cuaca terhadap Penyewaan Sepeda")
        ax.set_xlabel("Kondisi Cuaca")
        ax.set_ylabel("Jumlah Sewa Rata-rata")

        st.pyplot(fig)
    with st.expander("See explanation"):
        st.write(
            """Dari grafik, terlihat bahwa jumlah penyewaan sepeda berbanding terbalik dengan kondisi cuaca:

1. Cuaca cerah memiliki jumlah penyewaan tertinggi (~5000 sewa).
2. Cuaca berawan masih cukup tinggi (~4000 sewa), namun mulai menurun.
3. Hujan ringan menyebabkan penurunan drastis (~2000 sewa).
4. Cuaca ekstrem hampir tidak memiliki penyewaan sepeda (jumlahnya mendekati nol).

Indikasi Anomali atau Kejadian Khusus:

1. Penurunan drastis saat hujan ringan & cuaca ekstrem → Hal ini bisa menjadi indikasi bahwa pengguna lebih menghindari penyewaan sepeda ketika kondisi cuaca memburuk.
2. Cuaca ekstrem hampir tidak ada penyewaan → Bisa disebabkan oleh faktor keamanan atau regulasi yang membatasi penggunaan sepeda dalam kondisi cuaca ekstrem.
3. Berbeda dengan pola jam sibuk di hari kerja dan akhir pekan → Jika pola penyewaan normal menunjukkan lonjakan di jam sibuk (pagi & sore), cuaca buruk bisa menghilangkan pola tersebut, menunjukkan anomali dalam data.
4. Potensi kejadian khusus (misalnya badai besar atau kondisi cuaca ekstrem tertentu) → Jika ada periode dengan penyewaan nol meskipun tidak hujan lebat, mungkin ada faktor lain seperti pemeliharaan sistem atau larangan dari pemerintah."""
        )
with tab3:
    st.header("Bagaimana pola penggunaan sepeda antara pengguna kasual dan terdaftar?")
    def categorize_time(hour):
        if 0 <= hour < 6:
            return 'Pagi (00-06)'
        elif 6 <= hour < 12:
            return 'Siang (06-12)'
        elif 12 <= hour < 18:
            return 'Sore (12-18)'
        else:
            return 'Malam (18-24)'

    df_hour['time_category'] = df_hour['hr'].apply(categorize_time)
    df_day['day_type'] = df_day['workingday'].apply(lambda x: 'Hari Kerja' if x == 1 else 'Akhir Pekan')
    agg_data = df_day.groupby(['day_type'])[['casual', 'registered']].sum().reset_index()
    agg_data['casual_pct'] = (agg_data['casual'] / (agg_data['casual'] + agg_data['registered'])) * 100
    agg_data['registered_pct'] = (agg_data['registered'] / (agg_data['casual'] + agg_data['registered'])) * 100
    st.write("### Perbandingan Pengguna Kasual dan Terdaftar pada Hari Kerja vs Akhir Pekan")
    fig, ax = plt.subplots(figsize=(8,5))
    ax.bar(agg_data["day_type"], agg_data["casual_pct"], color='skyblue', label="Casual Users")
    ax.bar(agg_data["day_type"], agg_data["registered_pct"], color='orange', bottom=agg_data["casual_pct"], label="Registered Users")

    ax.set_xlabel("Tipe Hari")
    ax.set_ylabel("Persentase (%)")
    ax.set_title("Perbandingan Pengguna Kasual dan Terdaftar pada Hari Kerja vs Akhir Pekan")
    ax.legend()

    st.pyplot(fig)
    st.write("### Tren Penyewaan Pengguna Kasual vs Terdaftar per Bulan")
    fig, ax = plt.subplots(figsize=(10,5))
    ax.plot(df_day["mnth"], df_day["casual"], marker="o", linestyle="-", color='blue', label="Casual Users")
    ax.plot(df_day["mnth"], df_day["registered"], marker="o", linestyle="-", color='orange', label="Registered Users")

    ax.set_xlabel("Bulan")
    ax.set_ylabel("Jumlah Penyewaan")
    ax.set_title("Tren Penyewaan Pengguna Kasual vs Terdaftar per Bulan")
    ax.legend()
    
    st.pyplot(fig)
    with st.expander("See explanation"):
        st.write("""
        Dari kedua grafik di atas, kita bisa melihat pola penggunaan sepeda antara pengguna kasual dan pengguna terdaftar:

1. Perbandingan Pengguna Kasual vs Terdaftar pada Hari Kerja vs Akhir Pekan (Grafik 1)
- Pada hari kerja, mayoritas penyewaan sepeda dilakukan oleh pengguna terdaftar, sementara pengguna kasual hanya menyumbang bagian kecil.
- Pada akhir pekan, proporsi pengguna kasual meningkat secara signifikan, meskipun pengguna terdaftar masih mendominasi.

Insight:

- Pengguna terdaftar cenderung menggunakan sepeda untuk keperluan rutin, seperti komuter harian.
- Pengguna kasual lebih banyak menggunakan sepeda pada akhir pekan, kemungkinan untuk rekreasi atau aktivitas santai.

2. Tren Penyewaan Pengguna Kasual vs Terdaftar per Bulan (Grafik 2)
- Tren penyewaan pengguna terdaftar menunjukkan pola yang lebih tinggi dan stabil sepanjang tahun, dengan puncak pada bulan pertengahan tahun (Mei - Agustus).
- Pengguna kasual juga mengalami peningkatan di pertengahan tahun, meskipun jumlahnya jauh lebih kecil dibanding pengguna terdaftar.

Insight:

- Puncak peminjaman terjadi pada musim panas (pertengahan tahun), menunjukkan bahwa kondisi cuaca dan liburan mungkin berpengaruh.
- Pengguna kasual mengalami peningkatan yang lebih tajam dibandingkan pengguna terdaftar pada bulan-bulan tertentu, mengindikasikan bahwa kasual lebih terpengaruh oleh faktor musiman.
- Pengguna terdaftar tetap aktif sepanjang tahun, menunjukkan kebiasaan penggunaan reguler.

Kesimpulan :
- Pengguna kasual lebih cenderung menyewa sepeda pada akhir pekan dan bulan-bulan hangat, kemungkinan besar untuk keperluan rekreasi.
- Pengguna terdaftar lebih konsisten dalam penyewaan sepanjang tahun dan lebih aktif di hari kerja, menunjukkan bahwa mereka menggunakan sepeda sebagai bagian dari rutinitas harian, seperti transportasi ke kantor atau sekolah.
- Faktor musim, cuaca, dan hari dalam seminggu memiliki pengaruh signifikan terhadap pola penggunaan sepeda, terutama untuk pengguna kasual.""")
