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
    page_title="Visualization",
    page_icon="📈",
)

st.title('주기에 따른 데이터 시각화')

col_list = ["23년 4월", "23년 2월", "22년 10월", "22년 8월", "22년 5월", "22년 3월", "22년 1월"]

fe_list = ['물성', 'IZOD', 'MI', 'VST', '이물', 'SHEET', 'YI', 'TS', 'TE', 'BR%',
       'RTVM', 'RPS', 'RPS_YN', 'Gloss(60˚)', 'Gloss(85˚)', 'LAST_YN', '거칠기',
       '흑점', '홍점', 'TDDM FEED', '산방제 FEED', '개시제 FEED', 'RUBBER SOLUTION FEED',
       'PL FEED RATE', 'R-1 중량', 'R-1 압력', 'R-1 온도', 'R-1 REFLUX',
       'R-1 AGITATOR RPM', 'R-1 MELT PUMP AMP', 'R-2 중량', 'R-2 압력', 'R-2 온도', 'R-2 REFLUX',
       'R-2 AGITATOR RPM', 'R-2 MELT PUMP AMP', 'DV-1 온도', 'ZAPPER 온도',
       'DV-1 JACKET 온도', 'DV-1 진공도', 'RECYCLE 후단 압력', 'DV-2 PREHEATER 온도',
       'DV-2 진공도', 'DV-2 JACKET 온도']


st.sidebar.title('생산회차 및 feature 선택')

select_year = st.sidebar.multiselect(
    '확인하고자 하는 생산회차를 선택해주세요. 복수선택가능',
    col_list
)

select_col = st.sidebar.multiselect(
    '확인하고자 하는 feature를 선택해주세요. 복수선택가능(10개 이하 선택을 권장)',
    fe_list
)

data_path = '/mnt/c/Users/wongi/Desktop/알고리즘랩스/프로젝트/롯데케미칼'
  
# plotly scatter plot
col_name = select_col
fig1 = make_subplots(rows=len(select_year), cols=1, subplot_titles=tuple(select_year))
cnt = 1

# cols = plotly.colors.DEFAULT_PLOTLY_COLORS
cols = px.colors.qualitative.Alphabet

for item in select_year: 
    idx = col_list.index(item)
    temp = pd.read_csv(f'{data_path}/{item}_data.csv')
    temp['날짜'] = pd.to_datetime(temp['날짜'])
    scaler = StandardScaler()
    scaled_main = scaler.fit_transform(temp[temp.columns[1:]])
    temp[temp.columns[1:]] = scaled_main

    for i in range(len(col_name)):
        if col_name[i] == 'RPS' : 
            fig1.add_trace(go.Scatter(x=temp['날짜'], y=temp[col_name[i]], name=col_name[i], legendgroup = col_name[i],
                                 marker=dict(color=cols[i]), showlegend=cnt == 1), row=cnt, col=1)
        else : 
            fig1.add_trace(go.Scatter(x=temp['날짜'], y=temp[col_name[i]], name=col_name[i], legendgroup = col_name[i], line=dict(dash='dashdot'), 
                                 marker=dict(color=cols[i]), showlegend=cnt == 1, opacity=0.3), row=cnt, col=1)

    cnt += 1

if len(select_year) == 1 : 
    fig1.update_layout(height=500, width=250, title_text="Timeline")

elif len(select_year) == 2 : 
    fig1.update_layout(height=750, width=500, title_text="Timeline")
else : 
    fig1.update_layout(height=1500, width=1000, title_text="Timeline")
fig1.show()




fig2 = make_subplots(rows=len(select_year), cols=1, subplot_titles=tuple(select_year))
cnt = 1

# cols = plotly.colors.DEFAULT_PLOTLY_COLORS
cols = px.colors.qualitative.Alphabet

for item in select_year: 
    idx = col_list.index(item)
    temp = pd.read_csv(f'{data_path}/{item}_rps_data.csv')
    temp['날짜'] = pd.to_datetime(temp['날짜'])
    scaler = StandardScaler()
    scaled_main = scaler.fit_transform(temp[temp.columns[1:]])
    temp[temp.columns[1:]] = scaled_main

    for i in range(len(col_name)):
        if col_name[i] == 'RPS' : 
            fig2.add_trace(go.Scatter(x=temp['날짜'], y=temp[col_name[i]], name=col_name[i], legendgroup = col_name[i],
                                 marker=dict(color=cols[i]), showlegend=cnt == 1), row=cnt, col=1)
        else : 
            fig2.add_trace(go.Scatter(x=temp['날짜'], y=temp[col_name[i]], name=col_name[i], legendgroup = col_name[i], line=dict(dash='dashdot'), 
                                 marker=dict(color=cols[i]), showlegend=cnt == 1, opacity=0.3), row=cnt, col=1)

    cnt += 1

if len(select_year) == 1 : 
    fig2.update_layout(height=500, width=250, title_text="Timeline")

elif len(select_year) == 2 : 
    fig2.update_layout(height=750, width=500, title_text="Timeline")
else : 
    fig2.update_layout(height=1500, width=1000, title_text="Timeline")
fig2.show()


fig3 = make_subplots(rows=len(select_year), cols=1, subplot_titles=tuple(select_year))
cnt = 1

# cols = plotly.colors.DEFAULT_PLOTLY_COLORS
cols = px.colors.qualitative.Alphabet

for item in select_year: 
    idx = col_list.index(item)
    temp = pd.read_csv(f'{data_path}/{item}_final_data.csv')
    temp['날짜'] = pd.to_datetime(temp['날짜'])
    scaler = StandardScaler()
    scaled_main = scaler.fit_transform(temp[temp.columns[1:]])
    temp[temp.columns[1:]] = scaled_main

    for i in range(len(col_name)):
        if col_name[i] == 'RPS' : 
            fig3.add_trace(go.Scatter(x=temp['날짜'], y=temp[col_name[i]], name=col_name[i], legendgroup = col_name[i],
                                 marker=dict(color=cols[i]), showlegend=cnt == 1), row=cnt, col=1)
        else : 
            fig3.add_trace(go.Scatter(x=temp['날짜'], y=temp[col_name[i]], name=col_name[i], legendgroup = col_name[i], line=dict(dash='dashdot'), 
                                 marker=dict(color=cols[i]), showlegend=cnt == 1, opacity=0.3), row=cnt, col=1)
    cnt += 1


if len(select_year) == 1 : 
    fig3.update_layout(height=500, width=250, title_text="Timeline")

elif len(select_year) == 2 : 
    fig3.update_layout(height=750, width=500, title_text="Timeline")
else : 
    fig3.update_layout(height=1500, width=1000, title_text="Timeline")
fig3.show()


tab1, tab2, tab3 = st.tabs(['2 hours with missing', 'Only RPS not missing', 'Imputation'])

with tab1 : 
    st.plotly_chart(fig1, theme="streamlit", use_container_width=True)

with tab2 : 
    st.plotly_chart(fig2, theme="streamlit", use_container_width=True)
    
with tab3 : 
    st.plotly_chart(fig3, theme="streamlit", use_container_width=True)
    
    
def page1_function() : 
    return tab1   

def page2_function() : 
    return tab2