import streamlit as st
import pandas as pd
import seaborn as sns
import os
import numpy as np
from matplotlib import pyplot as plt


parse_dates = ['Order Date', 'Ship Date']
df = pd.read_csv(
    r"C:\Users\king2\Documents\Sam Docs\Python\Data Apps\Sales Data Analysis\superstore.csv",
    parse_dates=parse_dates)
df = df.drop(columns=["Row ID"])

# Sidebar
st.sidebar.header('Selection Control')

min_date = df['Order Date'].min()
max_date = df['Order Date'].max()
a_date = st.sidebar.date_input("Choose Your Date Range", (min_date, max_date))

df = df[(df['Order Date'] > a_date[0]) & (df['Order Date'] < a_date[1])]
df['year'] = df['Order Date'].dt.year.astype(str)
df['month'] = df['Order Date'].dt.month.astype(str)
df['year_month'] = df['year'] + "_" + df['month']

level = st.sidebar.selectbox('Choose Level of Analysis', ['Category', 'Sub-Category'])

var_1 = st.sidebar.selectbox("Primary Variable", ("Profit", "Sales", "Quantity", "Discount"))
st.write(var_1)

var_2 = st.sidebar.selectbox("Secondary Variable", ("Profit", "Sales", "Quantity", "Discount"))
st.write(var_2)

# Begin Main Page
st.header('Sales Data Analysis')

if level == 'Category':
    # Category DataFrame
    profit_by_cat = df.groupby(['Category'], as_index=False).sum()
    profit_by_cat = profit_by_cat.drop(columns=['Postal Code']).sort_values(by=var_1, ascending=False)
    st.write(profit_by_cat)
    # assign colors
    cats = profit_by_cat['Category'].tolist()
    palette = dict(zip(cats, sns.color_palette(n_colors=len(cats))))
    # Bar Chart
    fig = plt.figure(figsize=(10, 4))
    ax = fig.add_axes([1, 1, 1, 1])
    plt.xticks(rotation=45)
    sns.barplot(profit_by_cat['Category'], y=profit_by_cat[var_1], palette=palette)
    st.write(fig)
    # Line Chart
    year_month_cat = df.groupby(['year_month', 'Category'], as_index=False).sum()
    fig = plt.figure(figsize=(10, 4))
    plt.xticks(rotation=90)
    sns.lineplot(data=year_month_cat, x="year_month", y=var_1, hue="Category", palette=palette)
    plt.legend().remove()
    fig.legend(bbox_to_anchor=[1.10, 1], loc='upper_left', ncol=1)
    fig.tight_layout()
    st.write(fig)
    # Scatterplot
    fig = plt.figure(figsize=(10, 4))
    sns.scatterplot(data= profit_by_cat, x = var_1, y = var_2, hue="Category", palette=palette)
    plt.legend().remove()
    fig.legend(bbox_to_anchor=[1.10, 1], loc='upper_left', ncol=1)
    fig.tight_layout()
    st.write(fig)
elif level == 'Sub-Category':
    # Sub-Category DataFrame
    profit_by_sub_cat = df.groupby(['Sub-Category'], as_index=False).sum()
    profit_by_sub_cat = profit_by_sub_cat.drop(columns=['Postal Code']).sort_values(by=var_1, ascending=False)
    # assign colors
    sub_cats = profit_by_sub_cat['Sub-Category'].tolist()
    palette = dict(zip(sub_cats, sns.color_palette(n_colors=len(sub_cats))))
    # Bar Chart
    fig = plt.figure(figsize=(10, 4))
    plt.xticks(rotation=45)
    sns.barplot(profit_by_sub_cat['Sub-Category'], y=profit_by_sub_cat[var_1], palette=palette)
    st.write(fig)
    # Line Chart
    year_month_subcat = df.groupby(['year_month', 'Sub-Category'], as_index=False).sum()
    fig = plt.figure(figsize=(10, 4))
    sns.lineplot(data=year_month_subcat, x="year_month", y=var_1, hue="Sub-Category", palette=palette)
    plt.xticks(rotation=90)
    plt.legend().remove()
    fig.legend(bbox_to_anchor=[1, 1], loc='upper left', ncol=2)
    plt.tight_layout()
    st.write(fig)
    # Scatterplot
    fig = plt.figure(figsize=(10, 4))
    sns.scatterplot(data= profit_by_sub_cat, x = var_1, y = var_2, hue="Sub-Category", palette=palette)
    plt.legend().remove()
    fig.legend(bbox_to_anchor=[1.3, 1], loc='upper_left', ncol=2)
    fig.tight_layout()
    st.write(fig)
