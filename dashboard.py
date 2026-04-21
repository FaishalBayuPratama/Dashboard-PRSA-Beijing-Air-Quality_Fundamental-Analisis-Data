import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Load & cache data 

@st.cache_data
def load_data():
    df = pd.read_csv('all_data.csv.gz')
    df["datetime"] = pd.to_datetime(df["datetime"])
    df.sort_values("datetime", inplace=True)
    return df

df = load_data()

# Sidebar filter 

st.sidebar.title("Filter Data")

start_date, end_date = st.sidebar.date_input(
    "Rentang Waktu",
    value=[df["datetime"].min().date(), df["datetime"].max().date()],
)

all_stations = sorted(df["station"].unique())
selected = st.sidebar.multiselect("Pilih Stasiun", all_stations, default=all_stations)

# Filter utama
mask = (
    (df["datetime"].dt.date >= start_date)
    & (df["datetime"].dt.date <= end_date)
    & (df["station"].isin(selected))
)
main = df[mask].copy()

# Header & metrik 

st.title("Dashboard Kualitas Udara Beijing 2013–2017")

col1, col2, col3, col4 = st.columns(4)
col1.metric("PM2.5 (µg/m³)", f"{main['PM2.5'].mean():.1f}")
col2.metric("PM10 (µg/m³)",  f"{main['PM10'].mean():.1f}")
col3.metric("NO2 (µg/m³)",   f"{main['NO2'].mean():.1f}")
col4.metric("O3 (µg/m³)",    f"{main['O3'].mean():.1f}")

st.markdown("---")

# 1. Tren harian PM2.5 

st.subheader("Tren Harian PM2.5")

daily = main.resample("D", on="datetime")["PM2.5"].mean().reset_index()

fig, ax = plt.subplots(figsize=(14, 4))
ax.plot(daily["datetime"], daily["PM2.5"], color="#90CAF9", linewidth=1.2)
ax.fill_between(daily["datetime"], daily["PM2.5"], alpha=0.2, color="#90CAF9")
ax.axhline(75, color="#EF5350", linestyle="--", linewidth=1, label="Batas WHO 75 µg/m³")
ax.set_xlabel("Tanggal")
ax.set_ylabel("PM2.5 (µg/m³)")
ax.legend()
st.pyplot(fig)

st.markdown("""
**Insight:** PM2.5 tinggi di musim dingin (Okt-Feb) dan rendah di musim panas.
Beberapa lonjakan ekstrem terjadi di 2013-2014. Nilai sering melampaui batas WHO.
""")

st.markdown("---")

# 2. PM2.5 per stasiun 

st.subheader("PM2.5 per Stasiun")

station = (
    main.groupby("station")["PM2.5"]
    .mean()
    .sort_values(ascending=False)
    .reset_index()
)

fig, ax = plt.subplots(figsize=(10, 5))
colors = ["#EF5350" if i == 0 else "#66BB6A" if i == len(station) - 1 else "#D3D3D3"
          for i in range(len(station))]
ax.barh(station["station"], station["PM2.5"], color=colors)
ax.invert_yaxis()
ax.set_xlabel("Rata-rata PM2.5 (µg/m³)")
st.pyplot(fig)

worst = station.iloc[0]["station"]
best  = station.iloc[-1]["station"]
st.markdown(f"**Terburuk:** {worst} | **Terbaik:** {best}")

st.markdown("---")

# 3. Pola musiman

st.subheader("Rata-rata PM2.5 per Musim")

season_order = ["Spring", "Summer", "Autumn", "Winter"]
season = main.groupby("season")["PM2.5"].mean().reindex(season_order).reset_index()

fig, ax = plt.subplots(figsize=(7, 4))
ax.bar(season["season"], season["PM2.5"], color=["#90CAF9", "#66BB6A", "#FFA726", "#78909C"])
ax.set_ylabel("PM2.5 (µg/m³)")
st.pyplot(fig)

st.markdown("Winter punya PM2.5 tertinggi karena penggunaan pemanas batu bara.")

st.markdown("---")

# 4. Heatmap korelasi 

st.subheader("Korelasi Antar Variabel")

cols = ["PM2.5", "PM10", "SO2", "NO2", "CO", "O3", "TEMP", "WSPM"]
corr = main[cols].corr()

fig, ax = plt.subplots(figsize=(8, 6))
sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", center=0,
            annot_kws={"size": 8}, ax=ax)
ax.tick_params(axis="x", rotation=45, labelsize=8)
ax.tick_params(axis="y", rotation=0,  labelsize=8)
st.pyplot(fig)

st.markdown("""
- PM2.5 berkorelasi tinggi dengan PM10, NO2, CO → semua dari pembakaran.
- Suhu (TEMP) berkorelasi negatif → udara dingin = polutan menumpuk.
""")

st.markdown("---")

# Kesimpulan

st.subheader("Kesimpulan")
st.markdown(f"""
1. PM2.5 memburuk di musim dingin dan membaik di musim panas.
2. Stasiun **{worst}** paling tercemar, **{best}** paling bersih.
3. Polusi utama berasal dari pembakaran (batu bara & kendaraan).
""")

st.caption("Data: PRSA Dataset 12 Stasiun Beijing 2013-2017")