import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

def create_daily_orders_df(df):
    daily_orders_df = df.groupby('dteday')['cnt'].sum().reset_index()
    daily_orders_df.rename(columns={
        "dteday":"day",
        "cnt": "customer_count"
    }, inplace=True)

    return daily_orders_df
def create_hourly_orders_df(df):
    hourly_orders_df = df.groupby('hr')['cnt'].mean().reset_index()
    hourly_orders_df.rename(columns={
        "cnt": "customer_count",
        "hr":"hour"
    }, inplace=True)

    return hourly_orders_df
def create_byseason_df(df):
    byseason_df = df.groupby(by="season")['cnt'].sum().reset_index()
    byseason_df.rename(columns={
        "cnt": "customer_count",
    }, inplace=True)
    
    return byseason_df
def create_byworkingday_df(df):
    byworkingday_df = df.groupby(by="workingday")['cnt'].sum().reset_index()
    byworkingday_df.rename(columns={
        "cnt": "customer_count"
    }, inplace=True)
    
    return byworkingday_df

def create_byweather_df(df):
    byweather_df = df.groupby(by="weathersit")['cnt'].sum().reset_index()
    byweather_df.rename(columns={
        "cnt": "customer_count",
    }, inplace=True)
    return byweather_df

df = pd.read_csv('./bikeshare-dataset/hour.csv')
df['dteday'] = pd.to_datetime(df['dteday'])

min_date = df["dteday"].min()
max_date = df["dteday"].max()
 
with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = df[(df["dteday"] >= str(start_date)) & 
                (df["dteday"] <= str(end_date))]

daily_orders_df = create_daily_orders_df(main_df)
hourly_orders_df = create_hourly_orders_df(main_df)
byseason_df = create_byseason_df(main_df)
byworkingday_df = create_byworkingday_df(main_df)
byweather_df = create_byweather_df(main_df)

st.header('Dicoding Collection Dashboard :sparkles:')

st.subheader('Daily Orders')

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    daily_orders_df["day"],
    daily_orders_df["customer_count"],
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
 
st.pyplot(fig)

st.subheader('Average Hourly Orders')

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    hourly_orders_df["hour"],
    hourly_orders_df["customer_count"],
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
 
st.pyplot(fig)

st.subheader("By season & working day")
 
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))
 
colors = ["#55DDE0",  "#F6AE2D", "#F26419", "#33658A"]
 
sns.barplot(x="season", y="customer_count", data=byseason_df, palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel("Season", fontsize=30)
ax[0].set_title("Total Sales", loc="center", fontsize=50)
ax[0].tick_params(axis='x', labelsize=35)
ax[0].tick_params(axis='y', labelsize=30)
categories = ['springer', 'summer', 'fall','winter']
ax[0].set_xticklabels(categories, rotation=45, ha='right')

 
sns.barplot(x="workingday", y="customer_count", data=byworkingday_df, palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel("Working Day", fontsize=35)
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Total Sales", loc="center", fontsize=50)
ax[1].tick_params(axis='x', labelsize=35)
ax[1].tick_params(axis='y', labelsize=30)
categories_work = ['workingday','non workingday']
ax[1].set_xticklabels(categories_work, rotation=45, ha='right')

 
st.pyplot(fig)

fig, ax = plt.subplots(figsize=(16, 8))

# Your Seaborn plot code here
colors = ["#55DDE0",  "#F6AE2D", "#F26419", "#33658A"]
sns.barplot(
    x="weathersit", 
    y="customer_count",
    data=byweather_df,
    palette=colors,
    ax=ax
)
ax.set_title("Number of Customer by weather", loc="center", fontsize=30)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)

# Display the plot in Streamlit
st.subheader("By Weather")
st.pyplot(fig)
