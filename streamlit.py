import streamlit as st
import pandas as pd 
import plotly.graph_objects as go

from datetime import datetime, timedelta

def get_baseball_rankings(kbo_data):
    today = datetime.today().strftime("%Y.%m.%d")
    day = datetime.today().isoweekday()
    desired_date_data = kbo_data[kbo_data['날짜'] == today]
    if not desired_date_data.empty:
        return desired_date_data
    else:
        print("오늘의 데이터가 없습니다. 최신 기록 보여주기")
        if day == 2: # '2' = 화요일 / 월요일은 항상 경기가 없음
            yesterday = datetime.today() - timedelta(2)
            yesterday = yesterday.strftime("%Y.%m.%d")
        else:
            yesterday = datetime.today() - timedelta(1)
            yesterday = yesterday.strftime("%Y.%m.%d")
        desired_date_data = kbo_data[kbo_data['날짜'] == yesterday]
        return desired_date_data    

def visualize_team_performance(selected_team_data, my_choice, my_year):
    # '날짜' 컬럼의 형식 변환
    selected_team_data['날짜'] = pd.to_datetime(selected_team_data['날짜'], format='%Y.%m.%d')
    selected_team_data_year = selected_team_data['날짜'].dt.year
    
    # 2010~2024년 각각 정규시즌 마지막날 데이터 추출
    last_day_year = selected_team_data.sort_values('날짜').groupby(selected_team_data_year).tail(1)
    
    # 연도별 시각화
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=last_day_year['날짜'], y=last_day_year['승률']*100, 
                             mode='lines+markers',
                             name='승률',
                             line=dict(color='blue')))
    fig.update_layout(title=f"연도별 {my_choice} 성적 추이", 
                      xaxis_title='날짜', 
                      yaxis_title='승률(%)', 
                      legend_title='지표', 
                      hovermode='x unified')
    
    # 선택한 연도에 해당하는 데이터 필터링
    selected_year_data = selected_team_data[selected_team_data['날짜'].dt.year == my_year]
    
    # 월별로 데이터를 그룹화하고 각 그룹에서 마지막 날의 승률을 선택
    last_day_monthly_win_rate = selected_year_data.groupby(selected_team_data['날짜'].dt.month)['승률'].last() * 100
    
    # Plotly 그래프 객체 생성
    fig_month = go.Figure()
    fig_month.add_trace(go.Scatter(x=last_day_monthly_win_rate.index, y=last_day_monthly_win_rate.values, 
                             mode='lines+markers',
                             name='승률',
                             line=dict(color='blue')))
    fig_month.update_layout(title=f"{my_year}년 {my_choice} 팀의 월별 마지막 날 승률", 
                      xaxis_title='월', 
                      yaxis_title='마지막 날 승률(%)', 
                      hovermode='x unified')
    
    return fig, fig_month

st.title('KBO 야구 순위 및 팀 데이터 시각화')
kbo_data = pd.read_csv('kbo_data.csv')
kbo_data['팀명'].replace({'넥센' : '키움', 'SK' : 'SSG'}, inplace=True)
baseball_rankings = get_baseball_rankings(kbo_data)

date = datetime.today().strftime("%Y.%m.%d")
st.subheader(f'오늘의 야구 순위입니다.({date})')
st.dataframe(baseball_rankings, hide_index=True)

team = list(kbo_data['팀명'].unique())
my_choice = st.sidebar.selectbox('구단을 선택하세요', team)

type_year = pd.to_datetime(kbo_data['날짜'], format='%Y.%m.%d')
year = list(type_year.dt.year.unique())
my_year = st.sidebar.selectbox('연도를 선택하세요', year)

if my_choice:
    st.subheader('팀별 데이터 시각화')
    
    # 구단 선택
    selected_team_data = kbo_data[kbo_data['팀명'] == my_choice]
    
    # 시각화
    fig, fig_month = visualize_team_performance(selected_team_data, my_choice, my_year)
    st.plotly_chart(fig)
    st.plotly_chart(fig_month)
    