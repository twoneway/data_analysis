import pandas as pd
import numpy as np
import seaborn as sns
from datetime import datetime
from scipy.stats import norm
import logging
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import plotly.express as px
from plotly.subplots import make_subplots
from sklearn.preprocessing import StandardScaler, MinMaxScaler
import warnings
warnings.simplefilter('ignore')
import plotly.graph_objects as go
import plotly
import streamlit as st

st.set_page_config(
    page_title="Data Table",
    page_icon="📈",
)

st.title('Lagging 데이터 시각화')

data_path = '/mnt/c/Users/wongi/Desktop/알고리즘랩스/프로젝트/롯데케미칼'

df = pd.read_csv(f'{data_path}/23년 4월_lagging_data.csv')
df['날짜'] = pd.to_datetime(df['날짜'])
fe_list = df.columns.tolist()[1:]

select_col = st.sidebar.multiselect(
    '확인하고자 하는 feature를 선택해주세요.',
    fe_list
)

col_name = select_col

temp = df.copy()
scaler = StandardScaler()
scaled_main = scaler.fit_transform(temp[temp.columns[1:]])
temp[temp.columns[1:]] = scaled_main

fig = go.Figure()

for i in range(len(col_name)):
    fig.add_trace(go.Scatter(x=temp['날짜'], y=temp[col_name[i]], name=col_name[i], legendgroup = col_name[i]))
    
fig.update_layout(height=500, width=250, title_text="Timeline")

tab1, tab2 = st.tabs(['Data Table', 'Timeline'])

with tab1 : 
    st.table(df[['날짜'] + col_name])

with tab2 : 
    st.plotly_chart(fig, theme="streamlit", use_container_width=True)