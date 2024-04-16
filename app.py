import os

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

import pandas as pd
from datetime import datetime, timedelta

import requests
import json

# 봇 토큰 및 앱 초기화
chatbot_token = ''
bot_user_token = ''
slcak_hook_url = ''

def get_baseball_rankings(kbo_data):
    # 오늘 날짜 가져오기
    today = datetime.today().strftime("%Y.%m.%d")
    
    # 원하는 날짜의 데이터를 필터링하기
    desired_date_data = kbo_data[kbo_data['날짜'] == today]

    # 필터링된 데이터가 있으면 반환하기
    if not desired_date_data.empty:
        return desired_date_data
    else:
        print("오늘의 데이터가 없습니다.")
        print("전 날 순위를 보여드릴게요")
        
        # 어제 날짜 가져오기
        yesterday = datetime.today() - timedelta(1)
        yesterday = yesterday.strftime("%Y.%m.%d")
        
        # 어제 날짜의 데이터 필터링하여 반환하기
        desired_date_data = kbo_data[kbo_data['날짜'] == yesterday]
        return desired_date_data

# CSV 파일을 DataFrame으로 읽어오기
kbo_data = pd.read_csv('kbo_data.csv')

# '날짜' 열을 datetime 형식으로 변환하기
kbo_data['날짜'] = pd.to_datetime(kbo_data['날짜'])

# 오늘의 순위 메세지 보내기
baseball_rankings = get_baseball_rankings(kbo_data)
payload = {"text" : "현재 야구 순위는 다음과 같습니다:\n" + baseball_rankings.to_string(index=False)}
header = {"Content-type" : "application/json"}
response = requests.post(
    slcak_hook_url,
    data=json.dumps(payload),
    headers=header
)
print(response)

app = App(token = bot_user_token)

# hello 언급시 챗봇 대답하기
@app.message("hello")
def message_hello(message, say):
    say(f"hey there <@{message['user']}>!")

# 오늘의 야구 순위 알려주기
@app.message("순위")
def message_rank(message, say):
    # 야구 순위 가져오기
    baseball_rankings = get_baseball_rankings(kbo_data)
    if not baseball_rankings.empty:
        # 가져온 순위 정보를 메시지로 보내기
        say("현재 야구 순위는 다음과 같습니다:\n" + baseball_rankings.to_string(index=False))
    else:
        say("죄송합니다. 야구 순위 정보를 가져올 수 없습니다.")
        
SocketModeHandler(app, chatbot_token).start()

