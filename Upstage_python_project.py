from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

import time

import pandas as pd

# KBO DATA CRAWLING
# 매일 kbo 팀별 데이터 수집
# 매일 상위 3개팀 및 수집한 정보 슬랙봇? 카카오톡으로 보내주기

# 추후 13~23년도까지의 데이터 크롤링 후, 진출 가능성 매일 업데이트

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

url = "https://www.koreabaseball.com/Record/TeamRank/TeamRankDaily.aspx"
browser.get(url)

# 오늘의 날짜 출력
today = browser.find_element(By.CLASS_NAME, "date").text
print(today)

# 시즌 개막 페이지 이동
browser.find_element(By.CLASS_NAME, "ui-datepicker-trigger").click() # 데이트피커 클릭
time.sleep(1)
browser.find_element(By.XPATH, "//*[@id=\"ui-datepicker-div\"]/div/a[1]").click() # 이전달 클릭
browser.find_element(By.XPATH, "//*[@id=\"ui-datepicker-div\"]/table/tbody/tr[4]/td[7]/a").click() # 3월23일 클릭
time.sleep(2)

head_list = []
head_list.append("날짜")
    
# 헤더 추출
thead = browser.find_element(By.TAG_NAME, "thead")
for i in range(9):
    th = thead.find_elements(By.TAG_NAME, "th")[i].text
    if i == 7:
        continue
        
    head_list.append(th)   
print(head_list)

def kbo_data_crawling(): 
    body_list = []
    
    # 데이터 추출
    tbody = browser.find_element(By.TAG_NAME, "tbody")
    for row in tbody.find_elements(By.TAG_NAME, "tr"):
        body_list.append(date)
        for i in range(9):
            if i == 7 :
                continue
            
            # 내용 추출
            cell_value = row.find_elements(By.TAG_NAME, "td")[i].text
            body_list.append(cell_value)
    print(body_list)
    
    # 데이터프레임 생성
    df = pd.DataFrame([body_list[i:i+9] for i in range(0, len(body_list), 9)], columns=head_list)
    
    return df

# CSV 파일에 데이터 쓰기 위한 헤더 작성
header_written = False

while(True):
    # 해당 날짜 출력
    date = browser.find_element(By.CLASS_NAME, "date").text

    print("Date:", date)
    print("Today:", today)
    
    kbo_data = kbo_data_crawling()  # 전체 팀 데이터를 추출
    print(kbo_data)
    
    # CSV 파일에 데이터 추가
    if not header_written:
        kbo_data.to_csv("kbo_data.csv", mode='a', encoding='utf-8-sig', index=False)
        header_written = True
    else:
        kbo_data.to_csv("kbo_data.csv", mode='a', header=False, encoding='utf-8-sig', index=False)
    
    # 최신화 완료하면 끝내기
    if date == today:
        print("데이터 수집 완료")
        break
    
    # 다음날 클릭
    browser.find_element(By.XPATH, "//*[@id=\"cphContents_cphContents_cphContents_btnNextDate\"]").click()
    time.sleep(3)