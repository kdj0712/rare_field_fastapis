## dbmongo의 collection 연결
from pymongo import MongoClient
mongoClient = MongoClient("mongodb://trainings.iptime.org:45003")
# database 연결
database = mongoClient["data_analysis"]
# collection 작업
collection = database['KMSS']
# insert 작업 진행
# 크롤링 동작
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

import time


# Chrome 드라이버 설치 디렉터리 설정
# webdriver_manager_directory = ChromeDriverManager().install()

# Chrome 브라우저 옵션 설정
chrome_options = Options()
chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36")

# WebDriver 생성
browser = webdriver.Chrome()

# DB초기화
# collection.delete_many({})

# 웹 페이지 열기  
# 크롤링할 웹 페이지 URL
for i in range(1, 61):
    url = f"http://www.kmss.or.kr/bbs/bbsList.php?cid=1212&pn={i}"
    html_source = browser.get(url)

    for j in range(1, 16):
        
        click = browser.find_element(by=By.CSS_SELECTOR,value=f"tr:nth-child({j}) > td.td_subject > a")
        click.click()
        time.sleep(2)
        
        try : 
            title = browser.find_element(by=By.CSS_SELECTOR,value="#bo_v_title").text
            view = browser.find_element(by=By.CSS_SELECTOR,value="#bo_v_info > strong:nth-child(7)").text
            date = browser.find_element(by=By.CSS_SELECTOR,value="#bo_v_info > strong.if_date").text
            contents = browser.find_element(by=By.CSS_SELECTOR,value="#bo_v_con").text
            reply = browser.find_element(by=By.CSS_SELECTOR,value="#bo_vc").text
            time.sleep(2) 
                   
            print(title)
            print(view)
            print(date)
            print(contents)
            print(reply)
            print("-----------------")
            collection.insert_one({
                "title": title
                , "view":view
                , "date":date
                , "contents": contents
                , "reply": reply
                }) 
        except : 
            pass
        
        back_button = browser.find_element(by=By.CSS_SELECTOR, value="#bo_v_top > ul > li > a")
        back_button.click()
        time.sleep(2)

pass