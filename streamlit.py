import streamlit as st
import pandas as pd 
from datetime import datetime, timedelta
import plotly.graph_objects as go

def get_baseball_rankings(kbo_data):
    today = datetime.today().strftime("%Y.%m.%d")
    desired_date_data = kbo_data[kbo_data['날짜'] == today]
    if not desired_date_data.empty:
        return desired_date_data
    else:
        print("오늘의 데이터가 없습니다.")
        print("전 날 순위를 보여드릴게요")
        yesterday = datetime.today() - timedelta(1)
        yesterday = yesterday.strftime("%Y.%m.%d")
        desired_date_data = kbo_data[kbo_data['날짜'] == yesterday]
        return desired_date_data    

st.title('KBO 야구 순위 및 팀 데이터 시각화')
kbo_data = pd.read_csv('kbo_data.csv')
baseball_rankings = get_baseball_rankings(kbo_data)

date = datetime.today().strftime("%Y.%m.%d")
st.subheader(f'오늘의 야구 순위입니다.({date})')
st.dataframe(baseball_rankings, hide_index=True)

team = ['두산', '한화', '키움', '롯데', '삼성', 'KT', 'KIA', 'LG', 'NC', 'SSG']
my_choice = st.sidebar.selectbox('구단을 선택하세요', team)
st.sidebar.write(f'**{my_choice}을 선택하셨습니다.**')

if my_choice:
    st.subheader('팀별 데이터 시각화')
    
    # Filter data for the selected team
    selected_team_data = kbo_data[kbo_data['팀명'] == my_choice]

    # Create a line chart
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=selected_team_data['날짜'], y=selected_team_data['승률'],
                             mode='lines+markers',
                             name='승률',
                             line=dict(color='blue')))
    fig.update_layout(title=f"{my_choice} 성적 추이",
                      xaxis_title='날짜',
                      legend_title='지표',
                      hovermode='x unified')
    st.plotly_chart(fig)