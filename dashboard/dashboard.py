import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

product_df = pd.read_csv('product_count.csv')
review_df = pd.read_csv('product_review_count2.csv')
revenue_df = pd.read_csv('revenue_by_day.csv')

st.set_page_config(layout="wide")

# Ensuring that the 'order_approved_at' column has the 'datetime' data type
revenue_df['order_approved_at'] = pd.to_datetime(revenue_df['order_approved_at'])


# Creating a date range component for use in the sidebar
min_date = revenue_df['order_approved_at'].min()
max_date = revenue_df['order_approved_at'].max()

with st.sidebar:
    # Creating a slider to determine the time range
    start_date, end_date = st.date_input(label=':blue[Rentang Waktu]',
                                         min_value=min_date,
                                         max_value=max_date,
                                         value=[min_date, max_date],
                                         )

main_df = revenue_df[(revenue_df['order_approved_at'] >= str(start_date))
                     & (revenue_df['order_approved_at'] <= str(end_date))]

revenue_df = pd.read_csv('revenue_by_day.csv')

st.header('ANALYSIS DATA PROJECT : E-COMMERCE PUBLIC DATASET', divider='rainbow' )

st.subheader('Penjualan Harian')

col1, col2 = st.columns(2)

with col1:
    total_orders = main_df.total_order.sum()
    st.metric('Total Penjualan', value=total_orders)

with col2:
    total_revenue = format_currency(
        main_df.total_revenue.sum(), "$BRL", locale='ES_CO'
    )
    st.metric('Total Pendapatan', value=total_revenue)


fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    revenue_df['order_approved_at'],
    revenue_df['total_order'],
    marker='s',
    linewidth=3,
    color='#a1c9f4'
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=20)
ax.set_title('Total Pendapatan 2016/07 - 2018/07', fontsize=30)
st.pyplot(fig)


st.subheader('Produk yang Berkinerja Terbaik dan Terburuk dalam kategori')

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(24, 12))
colors = ["#a1c9f4", "#ff9f9b", "#ff9f9b", "#ff9f9b", "#ff9f9b"]

sns.barplot(x='total_order', y='product_category_name_english', data=product_df.groupby(
    'product_category_name_english').total_order.nunique().sort_values(ascending=False).reset_index().head(5), 
            palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel(None)
ax[0].set_title('Produk yang Berkinerja Terbaik (berdasarkan penjualan)', 
                fontsize=25)
ax[0].tick_params(axis='y', labelsize=20)
ax[0].tick_params(axis='x', labelsize=20)

sns.barplot(x='total_order', y='product_category_name_english', data=product_df.groupby(
    'product_category_name_english').total_order.nunique().sort_values(ascending=True).reset_index().head(5), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel(None)
ax[1].invert_xaxis()
ax[1].yaxis.tick_right()
ax[1].yaxis.set_label_position('right')
ax[1].set_title('Produk yang Berkinerja Terburuk (berdasarkan penjualan)', fontsize=25)
ax[1].tick_params(axis='y', labelsize=20)
ax[1].tick_params(axis='x', labelsize=20)

plt.suptitle('Produk yang Berkinerja Terbaik dan Terburuk(berdasarkan penjualan)', fontsize=35)
st.pyplot(fig)

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(24, 12))
colors = ["#a1c9f4", "#ff9f9b", "#ff9f9b", "#ff9f9b", "#ff9f9b"]

sns.barplot(x='mean_review_score', y='product_category_name_english', data=review_df.sort_values(
    by='mean_review_score', ascending=False).head(5), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel(None)
ax[0].set_title('Produk yang Berkinerja Terbaik (berdasarkan penilaian ulasan)', 
                fontsize=22)
ax[0].tick_params(axis='y', labelsize=20)
ax[0].tick_params(axis='x', labelsize=20)

sns.barplot(x='mean_review_score', y='product_category_name_english', data=review_df.sort_values(
    by='mean_review_score', ascending=True).head(5), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel(None)
ax[1].invert_xaxis()
ax[1].yaxis.tick_right()
ax[1].yaxis.set_label_position('right')
ax[1].set_title('Produk yang Berkinerja Terburuk (berdasarkan penilaian ulasan)', 
                fontsize=22)
ax[1].tick_params(axis='y', labelsize=20)
ax[1].tick_params(axis='x', labelsize=20)

plt.suptitle('Produk yang Berkinerja Terbaik dan Terburuk (berdasarkan penilaian ulasan)', fontsize=35)
st.pyplot(fig)


hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 
