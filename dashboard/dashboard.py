import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
sns.set(style='dark')

@st.cache_data
def load_data():
    df = pd.read_csv("dashboard/merged.csv")
    df['dteday'] = pd.to_datetime(df['dteday'])

    if 'cnt_x' in df.columns and 'cnt_y' in df.columns:
        df['cnt'] = df[['cnt_x', 'cnt_y']].max(axis=1)
        df.drop(['cnt_x', 'cnt_y'], axis=1, inplace=True)

    season_mapping = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
    df['season_name'] = df['season'].map(season_mapping)

    return df

df = load_data()

st.sidebar.header("Filter")

year_options = df['dteday'].dt.year.unique()
selected_years = st.sidebar.multiselect("Pilih Tahun", year_options, default=year_options, key="year_filter")

season_order = ["Spring", "Summer", "Fall", "Winter"]
season_options = df['season_name'].unique()
selected_seasons = st.sidebar.multiselect("Pilih Musim", season_options, default=season_options, key="season_filter")

peak_hours = [7, 8, 9, 17, 18, 19]

df_filtered = df[
    (df['dteday'].dt.year.isin(selected_years)) & 
    (df['season_name'].isin(selected_seasons)) & 
    (df['hr'].isin(peak_hours))
]

df_filtered["season_name"] = pd.Categorical(df_filtered["season_name"], categories=season_order, ordered=True)

peak_usage_by_season = df_filtered.groupby('season_name')['cnt'].mean().reindex(season_order)

st.header(':bike: Bike Rental Dashboard :bike:')
st.subheader("Penyewaan Sepeda Pada Peak Hours Per Musim")

colors = ['#FF9999', '#66B3FF', '#99FF99', '#FFCC99']
fig, ax = plt.subplots(figsize=(8, 6))
sns.barplot(x=peak_usage_by_season.index, y=peak_usage_by_season.values, palette=colors, ax=ax)

ax.set_xlabel('Musim')
ax.set_ylabel('Rata-rata Sepeda yang Disewa')
ax.set_xticklabels(peak_usage_by_season.index, rotation=0, ha='right')

st.pyplot(fig)


@st.cache_data
def load_data():
    df = pd.read_csv("dashboard/merged.csv")
    df['dteday'] = pd.to_datetime(df['dteday'])
    df = df[(df['dteday'].dt.year >= 2011) & (df['dteday'].dt.year <= 2012)]
    
    weather_mapping = {1: "Clear", 2: "Cloudy", 3: "Light Rain", 4: "Heavy Rain"}
    df['weather_name'] = df['weathersit'].map(weather_mapping)

    df['is_weekend'] = df['workingday'].apply(lambda x: "Weekday" if x == 1 else "Weekend/Holiday")

    if 'cnt_x' in df.columns and 'cnt_y' in df.columns:
        df['cnt'] = df[['cnt_x', 'cnt_y']].max(axis=1)
        df.drop(['cnt_x', 'cnt_y'], axis=1, inplace=True)
    
    return df

df = load_data()

st.sidebar.header("Filter")

weather_options = df['weather_name'].unique()
selected_weather = st.sidebar.multiselect("Pilih Cuaca", weather_options, default=weather_options, key="weather_filter")

df_filtered = df[df['weather_name'].isin(selected_weather)]

weather_order = ["Clear", "Cloudy", "Light Rain", "Heavy Rain"]
df_filtered['weather_name'] = pd.Categorical(df_filtered['weather_name'], categories=weather_order, ordered=True)

result = df_filtered.groupby(['is_weekend', 'weather_name'])['cnt'].mean().reset_index()

st.subheader("Penyewaan sepeda berdasarkan kondisi cuaca")

plt.figure(figsize=(10, 6))
ax = sns.barplot(x="is_weekend", y="cnt", hue="weather_name", data=result, palette="pastel", hue_order=weather_order)

plt.xlabel("Hari")
plt.ylabel("Rata-rata Sepeda yang Disewa")
plt.legend(title="Kondisi Cuaca")
plt.xticks(rotation=0)

st.pyplot(plt)

