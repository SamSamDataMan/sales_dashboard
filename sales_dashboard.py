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

df1 = df.groupby([level], as_index=False).sum()
# assign colors
cats = df1[level].tolist()
palette = dict(zip(cats, sns.color_palette(n_colors=len(cats))))

# Bar Chart
fig = plt.figure(figsize=(10, 4))
ax = fig.add_axes([1, 1, 1, 1])
plt.xticks(rotation=45)
sns.barplot(df1[level], y=df1[var_1], palette=palette)
st.write(fig)
# Line Chart
year_month_cat = df.groupby(['year_month', level], as_index=False).sum()
fig = plt.figure(figsize=(10, 4))
plt.xticks(rotation=90)
sns.lineplot(data=year_month_cat, x="year_month", y=var_1, hue=level, palette=palette)
plt.legend().remove()
fig.legend(bbox_to_anchor=[1.10, 1], loc='upper_left', ncol=1)
fig.tight_layout()
st.write(fig)
# Scatterplot
fig = plt.figure(figsize=(10, 4))
sns.scatterplot(data= df1, x = var_1, y = var_2, hue=level, palette=palette)
plt.legend().remove()
fig.legend(bbox_to_anchor=[1.10, 1], loc='upper_left', ncol=1)
fig.tight_layout()
st.write(fig)