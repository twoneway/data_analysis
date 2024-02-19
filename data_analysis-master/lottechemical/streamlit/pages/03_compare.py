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
import copy
import streamlit as st

st.set_page_config(
    page_title="Compare",
    page_icon="📈",
)

st.title('동일한 누적 가동시간에 따른 시각화')

col_list = ["23년 4월", "23년 2월", "22년 10월", "22년 8월", "22년 5월", "22년 3월", "22년 1월", "23년 8월"]

fe_list = ['RPS', 'TDDM FEED', '산방제 FEED', '개시제 FEED', 'RUBBER SOLUTION FEED',
       'PL FEED RATE', 'R-1 중량', 'R-1 압력', 'R-1 온도', 'R-1 REFLUX',
       'R-1 AGITATOR RPM', 'R-2 중량', 'R-2 압력', 'R-2 온도', 'R-2 REFLUX',
       'R-2 AGITATOR RPM', 'DV-1 온도', 'ZAPPER 온도',
       'DV-1 JACKET 온도', 'DV-1 진공도', 'RECYCLE 후단 압력', 'DV-2 PREHEATER 온도',
       'DV-2 진공도', 'DV-2 JACKET 온도', 'product_time']

st.sidebar.title('feature 선택')

select_col = st.sidebar.selectbox(
    '확인하고자 하는 feature를 선택해주세요. 복수선택가능(10개 이하 선택을 권장)',
    fe_list
)

multi_col = st.sidebar.multiselect(
    '확인하고자 하는 feature를 선택해주세요. 복수선택가능(10개 이하 선택을 권장)',
    fe_list
)

col_name = select_col

data_path = '/mnt/c/Users/wongi/Desktop/알고리즘랩스/프로젝트/롯데케미칼'
  
# plotly scatter plot
fig1 = make_subplots(rows=1, cols=1)
fig2 = make_subplots(rows=1, cols=1)
cnt = 0

cols = px.colors.sequential.Rainbow
for item in col_list: 
    temp = pd.read_csv(f'{data_path}/{item}_final_data.csv')
    ch_data = copy.deepcopy(temp)
    ch_data.index = ch_data['날짜']
    fig1.add_trace(go.Scatter(x=temp['product_time'], y=temp[col_name], name=col_list[cnt], legendgroup = col_name, marker=dict(color=cols[cnt])), row=1, col=1)
    
    temp[ch_data[fe_list].drop(['RPS', 'product_time'], axis=1).columns] = ch_data[fe_list].drop(['RPS', 'product_time'], axis=1).pct_change().reset_index(drop=True)
    temp.drop([0], axis=0, inplace=True)
    fig2.add_trace(go.Scatter(x=temp['product_time'], y=temp[col_name], name=col_list[cnt], legendgroup = col_name, marker=dict(color=cols[cnt])), row=1, col=1)
    cnt += 1
    
fig1.update_layout(height=500, width=1000, title_text=f"{col_name} Timeline")
fig1.show()

fig2.update_layout(height=500, width=1000, title_text=f"{col_name} pct_change Timeline")
fig2.show()


col_name = multi_col
fig3 = make_subplots(rows=len(col_list), cols=1, subplot_titles=tuple(col_list))
cnt = 1

for item in col_list: 
    temp = pd.read_csv(f'{data_path}/{item}_final_data.csv')
    scaler = StandardScaler()
    scaled_main = scaler.fit_transform(temp.drop(['날짜', 'product_time'], axis=1))
    temp[temp.drop(['날짜', 'product_time'], axis=1).columns] = scaled_main
    
    for i in range(len(col_name)):
        if col_name[i] == 'RPS' : 
            fig3.add_trace(go.Scatter(x=temp['product_time'], y=temp[col_name[i]], name=col_name[i], legendgroup = col_name[i],
                                 marker=dict(color=cols[i]), showlegend=cnt == 1), row=cnt, col=1)
        else : 
            fig3.add_trace(go.Scatter(x=temp['product_time'], y=temp[col_name[i]], name=col_name[i], legendgroup = col_name[i], line=dict(dash='dashdot'), 
                                 marker=dict(color=cols[i]), showlegend=cnt == 1, opacity=0.3), row=cnt, col=1)

    cnt += 1

fig3.update_layout(height=2500, width=3000, title_text="Timeline", font=dict(size=18))
fig3.show()

tab1, tab2 = st.tabs(['product_time by 생산차수', 'product_time by feature'])

with tab1 : 
    st.plotly_chart(fig1, theme="streamlit", use_container_width=True)
    st.plotly_chart(fig2, theme="streamlit", use_container_width=True)
    
with tab2 : 
    st.plotly_chart(fig3, theme="streamlit", use_container_width=True)