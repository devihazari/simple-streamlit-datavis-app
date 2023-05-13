import streamlit as st
import pandas as pd
import plotly_express as px
import plotly.graph_objects as go
import numpy as np

df = pd.read_csv('vehicles_us.csv')
df['manufacturer'] = df['model'].apply(lambda x: x.split()[0])


# replace null values in the 'is_4wd' column with the value 0
df['is_4wd'].fillna(value=0, inplace=True)
df['is_4wd'] = df['is_4wd'].astype('int')


# compute the median of non-null values in the 'model_year' column for each model group
medians = df.groupby('model')['model_year'].transform(lambda x: x.median())
# replace null values in the 'model_year' column with the median of non-null values for each model group
df['model_year'].fillna(medians, inplace=True)


# compute the median of non-null values in the 'cylinders' column for each model group
medians = df.groupby('model')['cylinders'].transform(lambda x: x.median())
# replace null values in the 'cylinders' column with the median of non-null values for each model group
df['cylinders'].fillna(medians, inplace=True)


# compute the median of non-null values in the 'odometer' column for each model_year group
medians = df.groupby('model_year')['odometer'].transform(lambda x: x.median())
# replace null values in the 'odometer' column with the median of non-null values for each model+year group
df['odometer'].fillna(medians, inplace=True)


# replace null values in the 'paint_color' column with the value 'NA'
df['paint_color'].fillna(value='NA', inplace=True)

df['model_year'] = df['model_year'].astype('int')
df['cylinders'] = df['cylinders'].astype('int')


st.header('Data viewer')
show_manuf_1k_ads = st.checkbox('Include manufacturers with less than 1000 ads')
if not show_manuf_1k_ads:
    df = df.groupby('manufacturer').filter(lambda x: len(x) > 1000)
st.dataframe(df)


st.header('Scatter plot of `model_year` vs `price`')
# Create a scatter plot using plotly_express
st.write(px.scatter(df, x='model_year', y='price'))


st.header('Vehicle types by fuel')
st.write(px.histogram(df, x='manufacturer', color='fuel'))
st.header('Histogram of `transmission` vs `model_year`')

# -------------------------------------------------------
# histograms in plotly:
# fig = go.Figure()
# fig.add_trace(go.Histogram(x=df[df['condition']=='good']['model_year'], name='good'))
# fig.add_trace(go.Histogram(x=df[df['condition']=='excellent']['model_year'], name='excellent'))
# fig.update_layout(barmode='stack')
# st.write(fig)
# works, but too many lines of code
# -------------------------------------------------------

# histograms in plotly_express:
st.write(px.histogram(df, x='model_year', color='transmission'))
# a lot more concise!
# -------------------------------------------------------

st.header('Compare price distribution between manufacturers')
manufac_list = sorted(df['manufacturer'].unique())
manufacturer_1 = st.selectbox('Select manufacturer 1',
                              manufac_list, index=manufac_list.index('chevrolet'))

manufacturer_2 = st.selectbox('Select manufacturer 2',
                              manufac_list, index=manufac_list.index('hyundai'))
mask_filter = (df['manufacturer'] == manufacturer_1) | (df['manufacturer'] == manufacturer_2)
df_filtered = df[mask_filter]
normalize = st.checkbox('Normalize histogram', value=True)
if normalize:
    histnorm = 'percent'
else:
    histnorm = None
st.write(px.histogram(df_filtered,
                      x='price',
                      nbins=30,
                      color='manufacturer',
                      histnorm=histnorm,
                      barmode='overlay'))